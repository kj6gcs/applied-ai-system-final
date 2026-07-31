"""Tests for the session-level song_selection helper (not scoring or ranking)."""
import random

import pytest

from src.recommender import Song
from src.song_selection import choose_next_song


def make_song(**overrides) -> Song:
    fields = {
        "id": 1,
        "title": "Song",
        "artist": "Artist",
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


def make_ranked_songs(count: int):
    return [make_song(id=i, title=f"Song {i}") for i in range(count)]


def test_choose_next_song_raises_on_empty_candidate_list():
    with pytest.raises(ValueError):
        choose_next_song([], rng=random.Random(1))


def test_choose_next_song_returns_one_of_the_ranked_songs():
    ranked = make_ranked_songs(5)
    chosen = choose_next_song(ranked, rng=random.Random(1))
    assert chosen in ranked


def test_choose_next_song_excludes_recent_songs_when_alternatives_exist():
    ranked = make_ranked_songs(3)
    recent_ids = {0, 1}  # only song id=2 has not been shown recently

    for seed in range(20):
        chosen = choose_next_song(ranked, recent_song_ids=recent_ids, rng=random.Random(seed))
        assert chosen.id == 2


def test_choose_next_song_falls_back_to_repeats_when_all_songs_are_recent():
    ranked = make_ranked_songs(3)
    recent_ids = {0, 1, 2}  # every song has been shown recently

    chosen = choose_next_song(ranked, recent_song_ids=recent_ids, rng=random.Random(1))
    assert chosen in ranked


def test_choose_next_song_favors_higher_ranked_songs_over_many_draws():
    ranked = make_ranked_songs(5)
    rng = random.Random(42)

    counts = {song.id: 0 for song in ranked}
    for _ in range(1000):
        chosen = choose_next_song(ranked, rng=rng)
        counts[chosen.id] += 1

    assert counts[0] > counts[4]  # rank 0 (best match) chosen more often than rank 4 (worst in pool)


def test_choose_next_song_is_deterministic_given_a_seeded_rng():
    ranked = make_ranked_songs(5)

    first = choose_next_song(ranked, rng=random.Random(7))
    second = choose_next_song(ranked, rng=random.Random(7))

    assert first.id == second.id


def test_choose_next_song_only_considers_top_pool_size_candidates():
    ranked = make_ranked_songs(10)

    for seed in range(50):
        chosen = choose_next_song(ranked, pool_size=3, rng=random.Random(seed))
        assert chosen.id in (0, 1, 2)
