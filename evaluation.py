"""
Resonance v2.0 -- system-level evaluation harness.

A lightweight acceptance script (separate from pytest) that exercises the
real recommendation engine and agent through their public APIs against a
handful of predefined scenarios, then prints a pass/fail summary.

This script does not reimplement scoring, drift, or quality-check logic --
it only calls into src/recommender.py and src/agent.py and asserts on their
results.
"""

import sys

from src.agent import AgentConfig, ResonanceAgent
from src.recommender import Recommender, Song, UserProfile, load_songs


CATALOG_PATH = "data/songs.csv"


def load_catalog() -> list[Song]:
    """Load the real 210-song catalog as Song objects via the project loader."""
    return [Song(**row) for row in load_songs(CATALOG_PATH)]


def make_profile(**overrides) -> UserProfile:
    """Build a full UserProfile, defaulting unspecified fields to known values."""
    fields = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_tempo": 115,
        "target_valence": 0.55,
        "target_danceability": 0.55,
        "likes_acoustic": False,
        "target_decade": 2020,
        "target_mood_tag": "defiance",
        "prefers_mainstream_hits": True,
    }

    fields.update(overrides)
    return UserProfile(**fields)


class EvalResult:
    """Outcome of a single evaluation scenario."""

    def __init__(self, name: str, passed: bool, detail: str):
        self.name = name
        self.passed = passed
        self.detail = detail

    def print_line(self) -> None:
        """Print this evaluation result in a human-readable format."""
        status = "PASS" if self.passed else "FAIL"
        print(f"[{status}] {self.name}")
        print(f"       {self.detail}")


def eval_static_rock_profile(catalog: list[Song]) -> EvalResult:
    """
    A. Verify the documented rock profile returns five recommendations
    topped by Back In Black.
    """
    recommender = Recommender(catalog)

    profile = make_profile(
        favorite_genre="rock",
        favorite_mood="intense",
        target_tempo=115,
        target_valence=0.55,
        target_danceability=0.55,
        likes_acoustic=False,
    )

    results = recommender.recommend(profile, k=5)

    top = results[0] if results else None

    passed = (
        len(results) == 5
        and top is not None
        and top.title == "Back In Black"
        and top.artist == "AC/DC"
    )

    detail = (
        f"Top result: {top.title} — {top.artist}"
        if top
        else "No recommendations returned"
    )

    return EvalResult(
        "Static rock profile",
        passed,
        detail,
    )


def eval_conflicting_preference_fallback(
    catalog: list[Song],
) -> EvalResult:
    """
    B. Verify a deliberately conflicting profile still returns
    five ranked recommendations.
    """
    recommender = Recommender(catalog)

    profile = make_profile(
        favorite_genre="metal",
        favorite_mood="peaceful",
        target_tempo=170,
        target_valence=0.85,
        target_danceability=0.85,
        likes_acoustic=True,
    )

    results = recommender.recommend(profile, k=5)

    passed = len(results) == 5
    detail = f"Returned {len(results)} recommendations"

    return EvalResult(
        "Conflicting preference fallback",
        passed,
        detail,
    )


def eval_bounded_preference_drift(
    catalog: list[Song],
) -> EvalResult:
    """
    C. Verify sufficient positive feedback on high-tempo songs
    raises target_tempo without exceeding the configured max step.
    """
    recommender = Recommender(catalog)

    profile = make_profile(
        target_tempo=100,
    )

    agent = ResonanceAgent(
        recommender,
        profile,
    )

    high_tempo_songs = sorted(
        catalog,
        key=lambda song: song.tempo_bpm,
        reverse=True,
    )[:3]

    for song in high_tempo_songs:
        agent.observe_feedback(
            song.id,
            "like",
        )

    cycle = agent.run_cycle(k=5)

    before = cycle.profile_before.target_tempo
    after = cycle.profile_after.target_tempo
    max_step = AgentConfig().max_tempo_step

    passed = before < after <= before + max_step

    detail = (
        f"target_tempo drifted {before} -> {after} "
        f"(max step {max_step})"
    )

    return EvalResult(
        "Bounded preference drift",
        passed,
        detail,
    )


def eval_invalid_feedback_rejection(
    catalog: list[Song],
) -> EvalResult:
    """
    D. Verify an unknown feedback event type is rejected
    by the agent's existing validation logic.
    """
    recommender = Recommender(catalog)

    agent = ResonanceAgent(
        recommender,
        make_profile(),
    )

    any_song_id = catalog[0].id

    try:
        agent.observe_feedback(
            song_id=any_song_id,
            event_type="love",
        )

        passed = False
        detail = (
            "Agent accepted an invalid event_type "
            "instead of rejecting it"
        )

    except ValueError as exc:
        passed = True
        detail = f"Rejected as expected: {exc}"

    return EvalResult(
        "Invalid feedback rejection",
        passed,
        detail,
    )


def eval_quality_warning(
    catalog: list[Song],
) -> EvalResult:
    """
    E. Verify a recommendation set dominated by one artist
    triggers the agent's existing quality-warning behavior.
    """
    single_artist_songs = [
        song
        for song in catalog
        if song.artist == "AC/DC"
    ]

    recommender = Recommender(single_artist_songs)

    agent = ResonanceAgent(
        recommender,
        make_profile(),
    )

    cycle = agent.run_cycle(
        k=len(single_artist_songs),
    )

    expected_warnings = (
        "Duplicate artists",
        "same genre",
    )

    matched = [
        warning
        for warning in cycle.quality_warnings
        if any(
            expected in warning
            for expected in expected_warnings
        )
    ]

    passed = bool(matched)

    detail = (
        matched[0]
        if matched
        else f"No expected warning in {cycle.quality_warnings}"
    )

    return EvalResult(
        "Recommendation quality warning",
        passed,
        detail,
    )


def main() -> int:
    """Run all predefined evaluation scenarios and print a summary."""
    catalog = load_catalog()

    scenarios = [
        eval_static_rock_profile,
        eval_conflicting_preference_fallback,
        eval_bounded_preference_drift,
        eval_invalid_feedback_rejection,
        eval_quality_warning,
    ]

    results = [
        scenario(catalog)
        for scenario in scenarios
    ]

    for result in results:
        result.print_line()

    passed_count = sum(
        1
        for result in results
        if result.passed
    )

    failed_count = len(results) - passed_count

    print()
    print("Resonance Evaluation Summary")
    print("============================")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")
    print(f"Total:  {len(results)}")
    print()

    overall_result = (
        "PASS"
        if failed_count == 0
        else "FAIL"
    )

    print(f"Overall result: {overall_result}")

    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())