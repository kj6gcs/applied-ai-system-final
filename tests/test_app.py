"""
AppTest-based behavioral tests for app.py: profile creation (preset and
custom-form paths), feedback buttons, song advancement, batched cycle
execution, and preference drift surfacing a listener-friendly message.
"""
from collections import deque

from streamlit.testing.v1 import AppTest

from src.agent import AgentConfig, ResonanceAgent
from src.recommender import Recommender, Song, UserProfile


def make_song(**overrides) -> Song:
    fields = {
        "id": 1,
        "title": "Song",
        "artist": "Artist",
        "genre": "rock",
        "mood": "intense",
        "tempo_bpm": 180.0,
        "valence": 0.8,
        "danceability": 0.8,
        "acousticness": 0.1,
        "release_decade": 2020,
        "mood_tag_primary": "adrenaline",
        "mood_tag_secondary": "power",
        "billboard_peak_at_release": 1,
        "billboard_peak_overall": 1,
    }
    fields.update(overrides)
    return Song(**fields)


def get_app() -> AppTest:
    at = AppTest.from_file("app.py")
    at.run(timeout=30)
    assert not at.exception
    return at


def test_initial_load_shows_setup_stage():
    at = get_app()

    subheaders = [el.value for el in at.subheader]
    assert "Let's set up your listener profile" in subheaders
    assert len(at.selectbox) == 4  # genre, mood, decade, mood tag
    assert len(at.slider) == 3  # tempo, valence, danceability
    assert len(at.checkbox) == 2  # acoustic, mainstream
    assert any(b.label == "Start Listening" for b in at.button)


def test_preset_button_starts_listening_session():
    at = get_app()

    preset_button = [b for b in at.button if "Rock Fan" in b.label][0]
    at = preset_button.click().run(timeout=30)

    assert not at.exception
    assert at.session_state["stage"] == "listening"
    assert at.session_state["agent"].get_profile().favorite_genre == "rock"
    button_labels = [b.label for b in at.button]
    assert "\U0001F44D Like" in button_labels
    assert "\U0001F44E Skip" in button_labels
    assert "\U0001F501 Replay" in button_labels


def test_custom_form_submission_creates_matching_profile():
    at = get_app()

    at.selectbox[0].select("lofi")  # favorite_genre
    at.selectbox[1].select("chill")  # favorite_mood
    at.slider[0].set_value(80)  # target_tempo
    at.checkbox[0].check()  # likes_acoustic

    submit = [b for b in at.button if b.label == "Start Listening"][0]
    at = submit.click().run(timeout=30)

    assert not at.exception
    profile = at.session_state["agent"].get_profile()
    assert profile.favorite_genre == "lofi"
    assert profile.favorite_mood == "chill"
    assert profile.target_tempo == 80.0
    assert profile.likes_acoustic is True


def test_feedback_button_advances_to_a_new_song():
    at = get_app()
    preset_button = [b for b in at.button if "Rock Fan" in b.label][0]
    at = preset_button.click().run(timeout=30)

    first_song_id = at.session_state["active_song"].id
    like_button = [b for b in at.button if b.label == "\U0001F44D Like"][0]
    at = like_button.click().run(timeout=30)

    assert not at.exception
    assert at.session_state["active_song"].id != first_song_id
    assert at.session_state["feedback_events_this_cycle"] == 1


def _inject_controlled_session(at: AppTest, songs, profile, config) -> None:
    """Replaces the normally-started session with a small, fully controlled
    Recommender/ResonanceAgent so drift can be triggered deterministically."""
    recommender = Recommender(songs)
    agent = ResonanceAgent(recommender, profile, config=config)
    agent.run_cycle(k=len(songs))

    at.session_state["recommender"] = recommender
    at.session_state["agent"] = agent
    at.session_state["stage"] = "listening"
    at.session_state["recent_song_ids"] = deque(maxlen=10)
    at.session_state["feedback_events_this_cycle"] = 0
    at.session_state["last_drift_message"] = ""
    at.session_state["active_song"] = songs[0]


def test_feedback_batch_triggers_the_next_cycle():
    at = get_app()
    fast_songs = [make_song(id=901, title="Fast A"), make_song(id=902, title="Fast B")]
    profile = UserProfile(
        favorite_genre="rock", favorite_mood="intense", target_tempo=115.0,
        target_valence=0.55, target_danceability=0.55, likes_acoustic=False,
        target_decade=2020, target_mood_tag="defiance", prefers_mainstream_hits=True,
    )
    _inject_controlled_session(at, fast_songs, profile, config=AgentConfig())
    at.run(timeout=30)

    for _ in range(3):  # matches app.py's FEEDBACK_BATCH_SIZE
        skip_button = [b for b in at.button if b.label == "\U0001F44E Skip"][0]
        at = skip_button.click().run(timeout=30)
        assert not at.exception

    assert at.session_state["feedback_events_this_cycle"] == 0
    assert at.session_state["agent"].get_history()[-1].cycle_index == 1


def test_preference_drift_message_appears_when_drift_occurs():
    at = get_app()
    fast_songs = [make_song(id=901, title="Fast A"), make_song(id=902, title="Fast B")]
    profile = UserProfile(
        favorite_genre="rock", favorite_mood="intense", target_tempo=115.0,
        target_valence=0.55, target_danceability=0.55, likes_acoustic=False,
        target_decade=2020, target_mood_tag="defiance", prefers_mainstream_hits=True,
    )
    # A low drift threshold isn't enough by itself -- app.py's FEEDBACK_BATCH_SIZE
    # still gates when run_cycle() gets called, so 3 skips are needed regardless.
    _inject_controlled_session(at, fast_songs, profile, config=AgentConfig(max_tempo_step=20.0))
    at.run(timeout=30)

    for _ in range(3):
        skip_button = [b for b in at.button if b.label == "\U0001F44E Skip"][0]
        at = skip_button.click().run(timeout=30)
        assert not at.exception

    assert at.session_state["agent"].get_profile().target_tempo == 95.0  # 115 - max_tempo_step(20)
    assert at.session_state["last_drift_message"] != ""
    info_messages = [el.value for el in at.info]
    assert any("preferred tempo" in message for message in info_messages)


def test_advanced_ai_details_available_in_sidebar():
    at = get_app()
    preset_button = [b for b in at.button if "Rock Fan" in b.label][0]
    at = preset_button.click().run(timeout=30)

    sidebar_expanders = [el.label for el in at.sidebar.expander]
    assert any("Advanced AI Details" in label for label in sidebar_expanders)
