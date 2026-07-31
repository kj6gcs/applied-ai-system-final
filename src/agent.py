"""
ResonanceAgent: the adaptive AI layer that sits on top of the (unchanged,
validated) recommendation engine. It observes listener feedback, detects
gradual preference drift, updates the listener profile, delegates
recommendation generation to Recommender, and explains why recommendations
changed between cycles.

The engine (Recommender / score_song / recommend_songs) is a tool this
agent calls -- it is never modified or reasoned about here.
"""
import logging
from dataclasses import dataclass, replace
from typing import Any, Callable, List

from src.recommender import Recommender, Song, UserProfile, song_popularity

logger = logging.getLogger(__name__)

FEEDBACK_EVENT_TYPES = ("like", "skip", "replay")
POSITIVE_EVENT_TYPES = ("like", "replay")


@dataclass
class AgentConfig:
    """Tuning knobs for preference-drift reasoning. Defaults match Resonance v2.0's
    original hard-coded behavior -- constructing ResonanceAgent without a config
    is equivalent to passing AgentConfig()."""
    min_feedback_for_drift: int = 3
    categorical_shift_threshold: int = 3
    max_tempo_step: float = 5.0
    max_valence_step: float = 0.05
    max_danceability_step: float = 0.05
    max_decade_step: int = 5


@dataclass
class FeedbackEvent:
    song_id: int
    event_type: str
    cycle_index: int


@dataclass
class FieldChange:
    field: str
    old_value: Any
    new_value: Any
    evidence_count: int
    rationale: str


@dataclass
class ProfileUpdate:
    changes: List[FieldChange]
    evidence: List[FeedbackEvent]

    @property
    def has_changes(self) -> bool:
        return bool(self.changes)


@dataclass
class RecommendedSong:
    song: Song
    explanation: str


@dataclass
class RecommendationCycle:
    cycle_index: int
    profile_before: UserProfile
    profile_after: UserProfile
    feedback_applied: List[FeedbackEvent]
    recommendations: List[RecommendedSong]
    quality_warnings: List[str]
    change_explanation: str


# (profile field, matching Song attribute, AgentConfig field naming the max step, value type)
NUMERIC_DRIFT_FIELDS = [
    ("target_tempo", "tempo_bpm", "max_tempo_step", float),
    ("target_valence", "valence", "max_valence_step", float),
    ("target_danceability", "danceability", "max_danceability_step", float),
    ("target_decade", "release_decade", "max_decade_step", int),
]

# (profile field, function deriving that field's "value" from a Song)
CATEGORICAL_DRIFT_FIELDS = [
    ("favorite_genre", lambda song: song.genre),
    ("favorite_mood", lambda song: song.mood),
    ("target_mood_tag", lambda song: song.mood_tag_primary),
    ("likes_acoustic", lambda song: song.acousticness > 0.5),
    ("prefers_mainstream_hits", lambda song: song_popularity(song.billboard_peak_overall) > 0.5),
]


class ResonanceAgent:
    """Observes feedback, detects preference drift, and orchestrates the engine."""

    def __init__(self, recommender: Recommender, profile: UserProfile, config: AgentConfig = None):
        self._recommender = recommender
        self._current_profile = profile
        self._config = config if config is not None else AgentConfig()
        self._pending_feedback: List[FeedbackEvent] = []
        self._feedback_log: List[FeedbackEvent] = []
        self._history: List[RecommendationCycle] = []
        self._cycle_count = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def observe_feedback(self, song_id: int, event_type: str) -> None:
        """Records a like/skip/replay against a song from a past recommendation cycle."""
        if event_type not in FEEDBACK_EVENT_TYPES:
            raise ValueError(f"Unknown feedback event_type: {event_type!r}")
        self._resolve_song(song_id)

        event = FeedbackEvent(
            song_id=song_id,
            event_type=event_type,
            cycle_index=self._cycle_count - 1,
        )
        self._pending_feedback.append(event)
        self._feedback_log.append(event)
        logger.debug("Observed %s feedback for song_id=%s", event_type, song_id)

    def run_cycle(self, k: int = 5) -> RecommendationCycle:
        """Reasons over pending feedback, updates the profile, and requests new recommendations."""
        profile_before = replace(self._current_profile)

        update = self._detect_drift()
        self._apply_update(update)
        self._pending_feedback = []

        profile_after = replace(self._current_profile)

        recommended_songs = self._recommender.recommend(self._current_profile, k=k)
        recommendations = [
            RecommendedSong(
                song=song,
                explanation=self._recommender.explain_recommendation(self._current_profile, song),
            )
            for song in recommended_songs
        ]
        quality_warnings = self._evaluate_quality(recommended_songs)
        change_explanation = self._explain_change(update)

        cycle = RecommendationCycle(
            cycle_index=self._cycle_count,
            profile_before=profile_before,
            profile_after=profile_after,
            feedback_applied=update.evidence,
            recommendations=recommendations,
            quality_warnings=quality_warnings,
            change_explanation=change_explanation,
        )
        self._history.append(cycle)
        self._cycle_count += 1

        logger.info(
            "Cycle %d complete: %d recommendations, %d profile change(s), %d quality warning(s)",
            cycle.cycle_index, len(recommendations), len(update.changes), len(quality_warnings),
        )
        return cycle

    def get_profile(self) -> UserProfile:
        """Returns a snapshot of the current listener profile."""
        return replace(self._current_profile)

    def get_history(self) -> List[RecommendationCycle]:
        """Returns the recorded history of every completed recommendation cycle."""
        return list(self._history)

    # ------------------------------------------------------------------
    # Internal: feedback -> drift reasoning
    # ------------------------------------------------------------------

    def _resolve_song(self, song_id: int) -> Song:
        for song in self._recommender.songs:
            if song.id == song_id:
                return song
        raise ValueError(f"No song with id={song_id} in the catalog")

    def _detect_drift(self) -> ProfileUpdate:
        evidence = list(self._pending_feedback)
        if len(self._pending_feedback) < self._config.min_feedback_for_drift:
            return ProfileUpdate(changes=[], evidence=evidence)

        positive_events = [e for e in self._pending_feedback if e.event_type in POSITIVE_EVENT_TYPES]
        negative_events = [e for e in self._pending_feedback if e.event_type == "skip"]

        changes: List[FieldChange] = []

        for field_name, song_attr, max_step_attr, cast_type in NUMERIC_DRIFT_FIELDS:
            max_step = getattr(self._config, max_step_attr)
            change = self._drift_numeric_field(
                field_name, song_attr, max_step, cast_type, positive_events, negative_events
            )
            if change is not None:
                changes.append(change)

        for field_name, value_fn in CATEGORICAL_DRIFT_FIELDS:
            change = self._drift_categorical_field(field_name, value_fn, positive_events)
            if change is not None:
                changes.append(change)

        return ProfileUpdate(changes=changes, evidence=evidence)

    def _drift_numeric_field(
        self, field_name, song_attr, max_step, cast_type, positive_events, negative_events
    ):
        current_value = getattr(self._current_profile, field_name)

        if positive_events:
            source_events, direction_label, toward = positive_events, "liked/replayed", True
        elif negative_events:
            source_events, direction_label, toward = negative_events, "skipped", False
        else:
            return None

        evidence_values = [getattr(self._resolve_song(e.song_id), song_attr) for e in source_events]
        evidence_mean = sum(evidence_values) / len(evidence_values)

        raw_delta = (evidence_mean - current_value) if toward else (current_value - evidence_mean)
        applied_delta = max(-max_step, min(max_step, raw_delta))
        if abs(applied_delta) < 1e-6:
            return None

        new_value = current_value + applied_delta
        new_value = int(round(new_value)) if cast_type is int else round(new_value, 2)
        if new_value == current_value:
            return None

        verb = "Increased" if new_value > current_value else "Decreased"
        return FieldChange(
            field=field_name,
            old_value=current_value,
            new_value=new_value,
            evidence_count=len(source_events),
            rationale=(
                f"{verb} {field_name} from {current_value} to {new_value} based on "
                f"{len(source_events)} {direction_label} song(s) averaging "
                f"{round(evidence_mean, 2)} {song_attr}"
            ),
        )

    def _drift_categorical_field(self, field_name: str, value_fn: Callable[[Song], Any], positive_events):
        if not positive_events:
            return None

        current_value = getattr(self._current_profile, field_name)
        counts = {}
        for event in positive_events:
            value = value_fn(self._resolve_song(event.song_id))
            counts[value] = counts.get(value, 0) + 1

        candidates = {value: count for value, count in counts.items() if value != current_value}
        if not candidates:
            return None

        best_value, best_count = max(candidates.items(), key=lambda pair: pair[1])
        if best_count < self._config.categorical_shift_threshold:
            return None

        return FieldChange(
            field=field_name,
            old_value=current_value,
            new_value=best_value,
            evidence_count=best_count,
            rationale=(
                f"Shifted {field_name} from {current_value!r} to {best_value!r} after "
                f"{best_count} liked/replayed song(s) matching {best_value!r}"
            ),
        )

    def _apply_update(self, update: ProfileUpdate) -> None:
        for change in update.changes:
            setattr(self._current_profile, change.field, change.new_value)

    # ------------------------------------------------------------------
    # Internal: explanation and quality evaluation
    # ------------------------------------------------------------------

    def _explain_change(self, update: ProfileUpdate) -> str:
        if not update.has_changes:
            return "No changes to your profile this cycle -- not enough new feedback yet."
        return "Your recommendations changed because: " + "; ".join(
            change.rationale for change in update.changes
        )

    def _evaluate_quality(self, songs: List[Song]) -> List[str]:
        warnings: List[str] = []
        if not songs:
            warnings.append("No recommendations were returned this cycle.")
            return warnings

        artists = [song.artist for song in songs]
        if len(set(artists)) < len(artists):
            warnings.append("Duplicate artists appear in the recommendation list.")

        genres = {song.genre for song in songs}
        if len(genres) == 1 and len(songs) > 1:
            warnings.append("All recommended songs share the same genre.")

        return warnings
