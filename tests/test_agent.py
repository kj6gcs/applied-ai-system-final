"""Tests for ResonanceAgent: feedback observation, bounded preference drift,
delegation to the (unchanged) recommendation engine, and quality evaluation."""
import pytest

from src.agent import AgentConfig, ResonanceAgent
from src.recommender import Recommender, Song, UserProfile


def make_song(**overrides) -> Song:
    fields = {
        "id": 1,
        "title": "Test Song",
        "artist": "Artist A",
        "genre": "pop",
        "mood": "happy",
        "tempo_bpm": 120.0,
        "valence": 0.8,
        "danceability": 0.8,
        "acousticness": 0.1,
        "release_decade": 2020,
        "mood_tag_primary": "joy",
        "mood_tag_secondary": "energy",
        "billboard_peak_at_release": 5,
        "billboard_peak_overall": 5,
    }
    fields.update(overrides)
    return Song(**fields)


def make_catalog():
    return [
        make_song(id=1, title="Fast One", artist="Artist A", tempo_bpm=160.0),
        make_song(id=2, title="Fast Two", artist="Artist B", tempo_bpm=158.0),
        make_song(id=3, title="Fast Three", artist="Artist C", tempo_bpm=162.0),
        make_song(
            id=4, title="Chill One", artist="Artist D", genre="jazz", mood="relaxed",
            tempo_bpm=90.0, valence=0.5, danceability=0.4, acousticness=0.8,
            release_decade=2010, mood_tag_primary="calm", mood_tag_secondary="nostalgia",
            billboard_peak_at_release=None, billboard_peak_overall=None,
        ),
        make_song(
            id=5, title="Chill Two", artist="Artist E", genre="jazz", mood="relaxed",
            tempo_bpm=88.0, valence=0.52, danceability=0.42, acousticness=0.82,
            release_decade=2010, mood_tag_primary="calm", mood_tag_secondary="nostalgia",
            billboard_peak_at_release=None, billboard_peak_overall=None,
        ),
        make_song(
            id=6, title="Chill Three", artist="Artist F", genre="jazz", mood="relaxed",
            tempo_bpm=92.0, valence=0.48, danceability=0.38, acousticness=0.79,
            release_decade=2010, mood_tag_primary="calm", mood_tag_secondary="nostalgia",
            billboard_peak_at_release=None, billboard_peak_overall=None,
        ),
    ]


def make_profile(**overrides) -> UserProfile:
    fields = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_tempo": 120.0,
        "target_valence": 0.6,
        "target_danceability": 0.6,
        "likes_acoustic": False,
        "target_decade": 2020,
        "target_mood_tag": "joy",
        "prefers_mainstream_hits": True,
    }
    fields.update(overrides)
    return UserProfile(**fields)


def make_agent(songs=None, profile=None, config=None) -> ResonanceAgent:
    return ResonanceAgent(
        Recommender(songs if songs is not None else make_catalog()),
        profile or make_profile(),
        config=config,
    )


# ---------------------------------------------------------------------------
# observe_feedback
# ---------------------------------------------------------------------------

def test_observe_feedback_rejects_unknown_event_type():
    agent = make_agent()
    with pytest.raises(ValueError):
        agent.observe_feedback(song_id=1, event_type="love")


def test_observe_feedback_rejects_unknown_song_id():
    agent = make_agent()
    with pytest.raises(ValueError):
        agent.observe_feedback(song_id=9999, event_type="like")


# ---------------------------------------------------------------------------
# run_cycle: bounded drift
# ---------------------------------------------------------------------------

def test_single_feedback_event_does_not_change_profile():
    agent = make_agent()
    agent.observe_feedback(1, "skip")

    cycle = agent.run_cycle(k=3)

    assert cycle.profile_before == cycle.profile_after
    assert "No changes" in cycle.change_explanation


def test_below_threshold_feedback_does_not_change_profile():
    agent = make_agent()
    agent.observe_feedback(1, "skip")
    agent.observe_feedback(2, "skip")  # only 2, threshold is 3

    cycle = agent.run_cycle(k=3)

    assert cycle.profile_before == cycle.profile_after


def test_enough_skips_of_fast_songs_lowers_target_tempo_by_a_bounded_step():
    agent = make_agent()
    agent.observe_feedback(1, "skip")  # 160 bpm
    agent.observe_feedback(2, "skip")  # 158 bpm
    agent.observe_feedback(3, "skip")  # 162 bpm

    cycle = agent.run_cycle(k=3)

    # current=120, skipped mean=160 -> raw delta -40, clamped to max_step=5.0
    assert cycle.profile_after.target_tempo == 115.0
    assert cycle.profile_after.target_tempo < cycle.profile_before.target_tempo
    assert "target_tempo" in cycle.change_explanation


def test_enough_likes_of_a_non_favorite_genre_shifts_favorite_genre():
    agent = make_agent()
    agent.observe_feedback(4, "like")  # jazz
    agent.observe_feedback(5, "like")  # jazz
    agent.observe_feedback(6, "replay")  # jazz

    cycle = agent.run_cycle(k=3)

    assert cycle.profile_after.favorite_genre == "jazz"
    assert cycle.profile_before.favorite_genre == "pop"
    assert "favorite_genre" in cycle.change_explanation


def test_run_cycle_clears_pending_feedback_so_it_is_not_reapplied():
    agent = make_agent()
    agent.observe_feedback(1, "skip")
    agent.observe_feedback(2, "skip")
    agent.observe_feedback(3, "skip")
    first_cycle = agent.run_cycle(k=3)

    second_cycle = agent.run_cycle(k=3)

    assert first_cycle.profile_after.target_tempo != first_cycle.profile_before.target_tempo
    assert second_cycle.profile_before == second_cycle.profile_after
    assert second_cycle.feedback_applied == []


# ---------------------------------------------------------------------------
# run_cycle: delegates to the engine, does not reimplement it
# ---------------------------------------------------------------------------

def test_run_cycle_returns_recommendations_with_explanations():
    agent = make_agent()

    cycle = agent.run_cycle(k=3)

    assert len(cycle.recommendations) == 3
    for recommended in cycle.recommendations:
        assert isinstance(recommended.explanation, str)
        assert recommended.explanation.strip() != ""


def test_run_cycle_is_deterministic_given_the_same_feedback():
    agent1 = make_agent()
    agent2 = make_agent()
    for agent in (agent1, agent2):
        agent.observe_feedback(1, "skip")
        agent.observe_feedback(2, "skip")
        agent.observe_feedback(3, "skip")

    cycle1 = agent1.run_cycle(k=3)
    cycle2 = agent2.run_cycle(k=3)

    assert cycle1.profile_after.target_tempo == cycle2.profile_after.target_tempo
    assert [r.song.id for r in cycle1.recommendations] == [r.song.id for r in cycle2.recommendations]


# ---------------------------------------------------------------------------
# quality evaluation
# ---------------------------------------------------------------------------

def test_evaluate_quality_flags_empty_recommendation_list():
    agent = make_agent(songs=[])

    cycle = agent.run_cycle(k=5)

    assert cycle.recommendations == []
    assert any("No recommendations" in warning for warning in cycle.quality_warnings)


def test_evaluate_quality_flags_duplicate_artists():
    songs = [
        make_song(id=1, title="A1", artist="Same Artist", tempo_bpm=120.0),
        make_song(id=2, title="A2", artist="Same Artist", tempo_bpm=118.0),
    ]
    agent = make_agent(songs=songs)

    cycle = agent.run_cycle(k=2)

    assert any("Duplicate artists" in warning for warning in cycle.quality_warnings)


def test_evaluate_quality_flags_single_genre_dominance():
    songs = [
        make_song(id=1, title="J1", artist="Artist A", genre="jazz", tempo_bpm=90.0),
        make_song(id=2, title="J2", artist="Artist B", genre="jazz", tempo_bpm=92.0),
    ]
    agent = make_agent(songs=songs)

    cycle = agent.run_cycle(k=2)

    assert any("same genre" in warning for warning in cycle.quality_warnings)


# ---------------------------------------------------------------------------
# get_profile / get_history: defensive copies, accumulated state
# ---------------------------------------------------------------------------

def test_get_profile_returns_a_copy_not_the_live_object():
    agent = make_agent()

    snapshot = agent.get_profile()
    snapshot.target_tempo = 999.0

    assert agent.get_profile().target_tempo != 999.0


def test_get_history_accumulates_every_completed_cycle():
    agent = make_agent()

    agent.run_cycle(k=2)
    agent.run_cycle(k=2)

    history = agent.get_history()
    assert len(history) == 2
    assert [cycle.cycle_index for cycle in history] == [0, 1]


def test_get_history_returns_a_copy_of_the_internal_list():
    agent = make_agent()
    agent.run_cycle(k=2)

    history = agent.get_history()
    history.append("not a real cycle")

    assert len(agent.get_history()) == 1


# ---------------------------------------------------------------------------
# AgentConfig: tuning knobs are configurable, defaults preserve prior behavior
# ---------------------------------------------------------------------------

def test_default_config_preserves_existing_behavior():
    implicit_agent = make_agent()
    explicit_agent = make_agent(config=AgentConfig())

    for agent in (implicit_agent, explicit_agent):
        agent.observe_feedback(1, "skip")
        agent.observe_feedback(2, "skip")
        agent.observe_feedback(3, "skip")

    implicit_cycle = implicit_agent.run_cycle(k=3)
    explicit_cycle = explicit_agent.run_cycle(k=3)

    assert implicit_cycle.profile_after.target_tempo == explicit_cycle.profile_after.target_tempo == 115.0


def test_custom_min_feedback_for_drift_changes_when_drift_begins():
    default_agent = make_agent()
    custom_agent = make_agent(config=AgentConfig(min_feedback_for_drift=1))

    default_agent.observe_feedback(1, "skip")
    custom_agent.observe_feedback(1, "skip")

    default_cycle = default_agent.run_cycle(k=3)
    custom_cycle = custom_agent.run_cycle(k=3)

    assert default_cycle.profile_after == default_cycle.profile_before  # 1 event < default threshold of 3
    assert custom_cycle.profile_after.target_tempo != custom_cycle.profile_before.target_tempo  # 1 event >= custom threshold of 1


def test_custom_max_tempo_step_changes_bounded_update_amount():
    default_agent = make_agent()
    custom_agent = make_agent(config=AgentConfig(max_tempo_step=10.0))

    for agent in (default_agent, custom_agent):
        agent.observe_feedback(1, "skip")
        agent.observe_feedback(2, "skip")
        agent.observe_feedback(3, "skip")

    default_cycle = default_agent.run_cycle(k=3)
    custom_cycle = custom_agent.run_cycle(k=3)

    assert default_cycle.profile_after.target_tempo == 115.0  # clamped to default max_tempo_step=5.0
    assert custom_cycle.profile_after.target_tempo == 110.0  # clamped to custom max_tempo_step=10.0


def test_custom_categorical_shift_threshold_changes_when_preference_shifts():
    default_agent = make_agent()
    custom_agent = make_agent(config=AgentConfig(categorical_shift_threshold=2))

    for agent in (default_agent, custom_agent):
        agent.observe_feedback(4, "like")  # jazz
        agent.observe_feedback(5, "like")  # jazz
        agent.observe_feedback(1, "skip")  # pop, fast -- pads feedback count, adds no jazz evidence

    default_cycle = default_agent.run_cycle(k=3)
    custom_cycle = custom_agent.run_cycle(k=3)

    assert default_cycle.profile_after.favorite_genre == "pop"  # 2 jazz likes < default threshold of 3
    assert custom_cycle.profile_after.favorite_genre == "jazz"  # 2 jazz likes >= custom threshold of 2
