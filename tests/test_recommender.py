"""
Tests for the recommendation engine.

Song/UserProfile/Recommender are a dataclass-friendly wrapper around the
same score_song/recommend_songs logic that src/main.py calls directly
through dicts -- there is one recommendation engine, not two.
"""
from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    load_songs,
    score_song,
    recommend_songs,
)


def make_song(**overrides) -> dict:
    song = {
        "id": 1,
        "title": "Test Song",
        "artist": "Test Artist",
        "genre": "pop",
        "mood": "happy",
        "tempo_bpm": 120.0,
        "valence": 0.8,
        "danceability": 0.8,
        "acousticness": 0.2,
        "release_decade": 2020,
        "mood_tag_primary": "joy",
        "mood_tag_secondary": "optimism",
        "billboard_peak_at_release": 5,
        "billboard_peak_overall": 5,
    }
    song.update(overrides)
    return song


def make_user_prefs(**overrides) -> dict:
    prefs = {
        "genre": "pop",
        "mood": "happy",
        "tempo_bpm": 120,
        "valence": 0.8,
        "danceability": 0.8,
        "likes_acoustic": False,
        "release_decade": 2020,
        "mood_tag": "joy",
        "prefers_mainstream_hits": True,
    }
    prefs.update(overrides)
    return prefs


# ---------------------------------------------------------------------------
# score_song: individual scoring components
# ---------------------------------------------------------------------------

def test_score_song_genre_match_awards_two_points():
    match_score, match_reasons = score_song(make_user_prefs(), make_song(genre="pop"))
    mismatch_score, mismatch_reasons = score_song(make_user_prefs(), make_song(genre="rock"))

    assert "genre match (+2.0)" in match_reasons
    assert "genre match (+2.0)" not in mismatch_reasons
    assert match_score > mismatch_score


def test_score_song_mood_match_awards_one_point():
    _, match_reasons = score_song(make_user_prefs(mood="happy"), make_song(mood="happy"))
    _, mismatch_reasons = score_song(make_user_prefs(mood="happy"), make_song(mood="sad"))

    assert "mood match (+1.0)" in match_reasons
    assert "mood match (+1.0)" not in mismatch_reasons


def test_score_song_tempo_closeness_rewards_near_misses_over_extremes():
    close_score, _ = score_song(make_user_prefs(tempo_bpm=120), make_song(tempo_bpm=118))
    far_score, _ = score_song(make_user_prefs(tempo_bpm=120), make_song(tempo_bpm=40))

    assert close_score > far_score


def test_score_song_acoustic_alignment_is_a_flat_bonus():
    _, match_reasons = score_song(make_user_prefs(likes_acoustic=True), make_song(acousticness=0.9))
    _, mismatch_reasons = score_song(make_user_prefs(likes_acoustic=True), make_song(acousticness=0.1))

    assert "acoustic alignment (+0.5)" in match_reasons
    assert "acoustic alignment (+0.5)" not in mismatch_reasons


def test_score_song_mood_tag_matches_either_primary_or_secondary():
    song = make_song(mood_tag_primary="joy", mood_tag_secondary="freedom")

    _, reasons_primary = score_song(make_user_prefs(mood_tag="joy"), song)
    _, reasons_secondary = score_song(make_user_prefs(mood_tag="freedom"), song)
    _, reasons_none = score_song(make_user_prefs(mood_tag="rage"), song)

    assert "mood tag match (+0.5)" in reasons_primary
    assert "mood tag match (+0.5)" in reasons_secondary
    assert "mood tag match (+0.5)" not in reasons_none


def test_score_song_popularity_alignment_uses_billboard_peak():
    mainstream_song = make_song(billboard_peak_overall=1)
    obscure_song = make_song(billboard_peak_overall=99)

    _, reasons_mainstream = score_song(make_user_prefs(prefers_mainstream_hits=True), mainstream_song)
    _, reasons_obscure = score_song(make_user_prefs(prefers_mainstream_hits=True), obscure_song)

    assert "popularity alignment (+0.5)" in reasons_mainstream
    assert "popularity alignment (+0.5)" not in reasons_obscure


def test_score_song_missing_optional_preference_is_skipped_not_errored():
    prefs = make_user_prefs()
    del prefs["mood_tag"]

    _score, reasons = score_song(prefs, make_song())

    assert not any("mood tag" in reason for reason in reasons)


def test_score_song_with_no_preferences_returns_zero_and_no_reasons():
    score, reasons = score_song({}, make_song())

    assert score == 0.0
    assert reasons == []


# ---------------------------------------------------------------------------
# recommend_songs: ordering, k, diversity penalty, edge cases
# ---------------------------------------------------------------------------

def test_recommend_songs_orders_by_score_descending():
    songs = [
        make_song(id=1, title="Best Match", genre="pop", mood="happy"),
        make_song(id=2, title="Partial Match", genre="pop", mood="sad"),
        make_song(id=3, title="No Match", genre="rock", mood="sad", tempo_bpm=40),
    ]

    results = recommend_songs(make_user_prefs(), songs, k=3)
    titles = [song["title"] for song, _score, _explanation in results]

    assert titles == ["Best Match", "Partial Match", "No Match"]


def test_recommend_songs_respects_k():
    songs = [make_song(id=i, title=f"Song {i}") for i in range(5)]

    results = recommend_songs(make_user_prefs(), songs, k=2)

    assert len(results) == 2


def test_recommend_songs_applies_diversity_penalty_to_repeated_artist():
    songs = [
        make_song(id=1, title="A1", artist="Same Artist"),
        make_song(id=2, title="A2", artist="Same Artist"),
        make_song(id=3, title="B1", artist="Other Artist", mood="sad"),
    ]

    results = recommend_songs(make_user_prefs(), songs, k=3)
    second_pick_explanation = results[1][2]

    assert "diversity penalty" in second_pick_explanation


def test_recommend_songs_handles_empty_catalog():
    assert recommend_songs(make_user_prefs(), [], k=5) == []


def test_recommend_songs_handles_k_larger_than_catalog():
    songs = [make_song(id=1), make_song(id=2)]

    results = recommend_songs(make_user_prefs(), songs, k=10)

    assert len(results) == 2


# ---------------------------------------------------------------------------
# load_songs: real catalog file
# ---------------------------------------------------------------------------

def test_load_songs_reads_full_catalog():
    songs = load_songs("data/songs.csv")

    assert len(songs) == 60
    assert songs[0]["title"] == "Sunrise City"
    assert isinstance(songs[0]["tempo_bpm"], float)


# ---------------------------------------------------------------------------
# Regression tests: documented sample outputs (README.md) must not silently
# drift when the engine is refactored.
# ---------------------------------------------------------------------------

ROBBYS_PROFILE = {
    "genre": "rock",
    "mood": "intense",
    "tempo_bpm": 115,
    "valence": 0.55,
    "danceability": 0.55,
    "likes_acoustic": False,
}

CHILL_LOFI_PROFILE = {
    "genre": "lofi",
    "mood": "chill",
    "tempo_bpm": 75,
    "valence": 0.58,
    "danceability": 0.60,
    "likes_acoustic": True,
}


def test_regression_robbys_profile_matches_documented_top5():
    songs = load_songs("data/songs.csv")

    results = recommend_songs(ROBBYS_PROFILE, songs, k=5)
    titles = [song["title"] for song, _score, _explanation in results]

    assert titles == [
        "Back In Black",
        "Storm Runner",
        "Dreams",
        "Thunderstruck",
        "Bohemian Rhapsody",
    ]
    assert round(results[0][1], 2) == 5.38


def test_regression_chill_lofi_profile_matches_documented_top5():
    songs = load_songs("data/songs.csv")

    results = recommend_songs(CHILL_LOFI_PROFILE, songs, k=5)
    titles = [song["title"] for song, _score, _explanation in results]

    assert titles == [
        "Midnight Coding",
        "Library Rain",
        "Aruarian Dance",
        "Focus Flow",
        "Spacewalk Thoughts",
    ]
    assert round(results[0][1], 2) == 5.46


# ---------------------------------------------------------------------------
# Recommender / Song / UserProfile: dataclass wrapper delegates to the same
# engine exercised above -- it is not a second implementation.
# ---------------------------------------------------------------------------

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
            release_decade=2020,
            mood_tag_primary="calm",
            mood_tag_secondary="focus",
            billboard_peak_at_release=None,
            billboard_peak_overall=None,
        ),
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
            release_decade=2020,
            mood_tag_primary="joy",
            mood_tag_secondary="optimism",
            billboard_peak_at_release=5,
            billboard_peak_overall=5,
        ),
    ]
    # Lofi song listed first on purpose: if Recommender.recommend() ever
    # regressed back to returning self.songs[:k] unsorted, this ordering
    # would catch it, since the pop song only wins by actually scoring higher.
    return Recommender(songs)


def test_recommend_delegates_to_the_real_scoring_engine():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_tempo=120,
        target_valence=0.9,
        target_danceability=0.8,
        likes_acoustic=False,
        target_decade=2020,
        target_mood_tag="joy",
        prefers_mainstream_hits=True,
    )
    rec = make_small_recommender()

    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].title == "Test Pop Track"
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_reflects_actual_score_breakdown():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_tempo=120,
        target_valence=0.9,
        target_danceability=0.8,
        likes_acoustic=False,
        target_decade=2020,
        target_mood_tag="joy",
        prefers_mainstream_hits=True,
    )
    rec = make_small_recommender()
    pop_song = next(song for song in rec.songs if song.title == "Test Pop Track")

    explanation = rec.explain_recommendation(user, pop_song)

    assert isinstance(explanation, str)
    assert "genre match" in explanation
    assert "mood match" in explanation


def test_explain_recommendation_handles_no_matching_attributes():
    user = UserProfile(
        favorite_genre="classical",
        favorite_mood="euphoric",
        target_tempo=200,
        target_valence=0.95,
        target_danceability=0.95,
        likes_acoustic=False,
        target_decade=1700,
        target_mood_tag="nonexistent",
        prefers_mainstream_hits=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)

    assert isinstance(explanation, str)
    assert explanation.strip() != ""
    assert "genre match" not in explanation
    assert "mood match" not in explanation
