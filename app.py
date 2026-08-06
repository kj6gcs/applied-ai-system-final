"""
Streamlit entry point for Resonance v2.0.

Reuses the existing, unmodified Recommender/ResonanceAgent public API -- this
file adds no scoring, ranking, or drift-reasoning logic of its own. It only:
  - adapts load_songs()'s dicts into Song dataclasses,
  - picks which already-ranked song to show next (src/song_selection.py),
  - relabels the engine's technical explanations/field names in plain English.
"""
import sys
from collections import deque
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from src.agent import ResonanceAgent
from src.logging_config import configure_logging
from src.recommender import Recommender, Song, UserProfile, load_songs
from src.song_selection import choose_next_song

CATALOG_PATH = "data/songs.csv"
CANDIDATE_POOL_SIZE = 10
RECENT_SONGS_REMEMBERED = 10
LOGO_PATH ="assets/resonance_v2_cropped.svg"

# Mirrors AgentConfig's own default (min_feedback_for_drift=3). This only
# decides *when the UI calls* run_cycle() -- whether drift actually applies
# is still entirely up to the agent's own _detect_drift() gating.
FEEDBACK_BATCH_SIZE = 3

FIELD_LABELS = {
    "favorite_genre": "favorite genre",
    "favorite_mood": "favorite mood",
    "target_tempo": "preferred tempo",
    "target_valence": "preferred emotional tone",
    "target_danceability": "preferred danceability",
    "likes_acoustic": "acoustic preference",
    "target_decade": "preferred decade",
    "target_mood_tag": "preferred mood tag",
    "prefers_mainstream_hits": "taste for mainstream hits",
}

REASON_LABELS = {
    "genre match": "matches your favorite genre",
    "mood match": "matches your favorite mood",
    "tempo closeness": "has a tempo close to what you like",
    "valence closeness": "has a similar emotional tone to what you like",
    "danceability closeness": "has similar danceability to what you like",
    "acoustic alignment": "matches your acoustic preference",
    "decade closeness": "is from an era close to what you like",
    "mood tag match": "matches a mood you're into",
    "popularity alignment": "matches your taste for mainstream or lesser-known tracks",
}

PRESETS = {
    "\U0001F3B8 Rock Fan": UserProfile(
        favorite_genre="rock", favorite_mood="intense", target_tempo=115.0,
        target_valence=0.55, target_danceability=0.55, likes_acoustic=False,
        target_decade=2020, target_mood_tag="defiance", prefers_mainstream_hits=True,
    ),
    "\U0001F3A7 Lofi Chill": UserProfile(
        favorite_genre="lofi", favorite_mood="chill", target_tempo=75.0,
        target_valence=0.58, target_danceability=0.60, likes_acoustic=True,
        target_decade=2020, target_mood_tag="calm", prefers_mainstream_hits=False,
    ),
    "\U0001F389 Pop Party": UserProfile(
        favorite_genre="pop", favorite_mood="happy", target_tempo=120.0,
        target_valence=0.80, target_danceability=0.80, likes_acoustic=False,
        target_decade=2020, target_mood_tag="joy", prefers_mainstream_hits=True,
    ),
}


def _load_catalog(csv_path: str):
    """Adapts load_songs()'s dicts into the Song dataclass Recommender expects."""
    return [Song(**row) for row in load_songs(csv_path)]


def _friendly_explanation(technical_explanation: str) -> str:
    """Relabels the engine's known reason categories in plain English -- no
    scores, weights, or thresholds are recomputed here."""
    reasons = [reason.split(" (+")[0].strip() for reason in technical_explanation.split(", ")]
    friendly = [REASON_LABELS[reason] for reason in reasons if reason in REASON_LABELS]

    if not friendly:
        return "This one's a bit of a wildcard pick based on your profile."
    if len(friendly) == 1:
        return f"Recommended because it {friendly[0]}."
    return "Recommended because it " + ", ".join(friendly[:-1]) + f", and {friendly[-1]}."


def _friendly_drift_message(before: UserProfile, after: UserProfile) -> str:
    before_values, after_values = asdict(before), asdict(after)
    changed_fields = [field for field in before_values if before_values[field] != after_values[field]]

    if not changed_fields:
        return ""

    updates = [f"your {FIELD_LABELS[field]} (now {after_values[field]})" for field in changed_fields]
    return "Based on your recent feedback, we've updated " + ", ".join(updates) + "."


def _init_catalog() -> None:
    if "catalog" not in st.session_state:
        configure_logging()
        st.session_state.catalog = _load_catalog(CATALOG_PATH)


def _advance_song() -> None:
    recommender = st.session_state.recommender
    agent = st.session_state.agent

    candidates = recommender.recommend(agent.get_profile(), k=CANDIDATE_POOL_SIZE)
    next_song = choose_next_song(candidates, recent_song_ids=st.session_state.recent_song_ids)

    st.session_state.active_song = next_song
    st.session_state.recent_song_ids.append(next_song.id)


def _start_session(profile: UserProfile) -> None:
    recommender = Recommender(st.session_state.catalog)
    agent = ResonanceAgent(recommender, profile)
    agent.run_cycle(k=CANDIDATE_POOL_SIZE)

    st.session_state.recommender = recommender
    st.session_state.agent = agent
    st.session_state.stage = "listening"
    st.session_state.recent_song_ids = deque(maxlen=RECENT_SONGS_REMEMBERED)
    st.session_state.feedback_events_this_cycle = 0
    st.session_state.last_drift_message = ""

    _advance_song()


def _record_feedback(event_type: str) -> None:
    agent = st.session_state.agent
    song = st.session_state.active_song

    agent.observe_feedback(song.id, event_type)
    st.session_state.feedback_events_this_cycle += 1

    if st.session_state.feedback_events_this_cycle >= FEEDBACK_BATCH_SIZE:
        cycle = agent.run_cycle(k=CANDIDATE_POOL_SIZE)
        st.session_state.last_drift_message = _friendly_drift_message(cycle.profile_before, cycle.profile_after)
        st.session_state.feedback_events_this_cycle = 0

    _advance_song()

def render_resonance_header() -> None:
    """Displays the Resonance v2.0 branding at the top of the app."""
    left, center, right = st.columns([1, 4, 1])

    with center:
        st.image(LOGO_PATH, use_container_width=True)

def render_setup() -> None:
    render_resonance_header()
    st.subheader("Let's set up your listener profile")

    st.write("Quick start:")
    preset_cols = st.columns(len(PRESETS))
    for col, (label, profile) in zip(preset_cols, PRESETS.items()):
        if col.button(label, key=f"preset-{label}"):
            _start_session(profile)
            st.rerun()

    st.divider()
    st.write("Or build your own profile:")

    catalog = st.session_state.catalog
    genres = sorted({song.genre for song in catalog})
    moods = sorted({song.mood for song in catalog})
    mood_tags = sorted({song.mood_tag_primary for song in catalog} | {song.mood_tag_secondary for song in catalog})
    decades = sorted({song.release_decade for song in catalog})

    with st.form("profile_setup"):
        favorite_genre = st.selectbox(
            "Favorite genre", genres, index=genres.index("rock") if "rock" in genres else 0
        )
        favorite_mood = st.selectbox(
            "Favorite mood", moods, index=moods.index("intense") if "intense" in moods else 0
        )
        target_tempo = st.slider("Preferred tempo (BPM)", 40, 200, 115)
        target_valence = st.slider("Preferred emotional tone (0 = somber, 1 = euphoric)", 0.0, 1.0, 0.55)
        target_danceability = st.slider("Preferred danceability", 0.0, 1.0, 0.55)
        likes_acoustic = st.checkbox("I like acoustic-leaning songs", value=False)
        target_decade = st.selectbox(
            "Preferred decade", decades, index=decades.index(2020) if 2020 in decades else 0
        )
        target_mood_tag = st.selectbox("Preferred mood tag", mood_tags, index=0)
        prefers_mainstream_hits = st.checkbox("I prefer mainstream hits", value=True)

        submitted = st.form_submit_button("Start Listening")

    if submitted:
        profile = UserProfile(
            favorite_genre=favorite_genre,
            favorite_mood=favorite_mood,
            target_tempo=float(target_tempo),
            target_valence=float(target_valence),
            target_danceability=float(target_danceability),
            likes_acoustic=likes_acoustic,
            target_decade=int(target_decade),
            target_mood_tag=target_mood_tag,
            prefers_mainstream_hits=prefers_mainstream_hits,
        )
        _start_session(profile)
        st.rerun()


def render_listening_session() -> None:
    agent = st.session_state.agent
    recommender = st.session_state.recommender
    song = st.session_state.active_song
    profile = agent.get_profile()
    cycle_number = agent.get_history()[-1].cycle_index

    render_resonance_header()

    score = recommender.score(profile, song)
    technical_explanation = recommender.explain_recommendation(profile, song)

    st.header(song.title)
    st.subheader(song.artist)
    st.write(f"Match score: {score:.2f}")
    st.write(_friendly_explanation(technical_explanation))

    with st.expander("Why this song? (technical details)"):
        st.write(technical_explanation)

    like_col, skip_col, replay_col = st.columns(3)
    if like_col.button("\U0001F44D Like"):
        _record_feedback("like")
        st.rerun()
    if skip_col.button("\U0001F44E Skip"):
        _record_feedback("skip")
        st.rerun()
    if replay_col.button("\U0001F501 Replay"):
        _record_feedback("replay")
        st.rerun()
    st.caption("Replay signals a strong positive preference -- there's no audio playback yet.")

    st.divider()
    st.write(
        f"Cycle #{cycle_number} -- "
        f"{st.session_state.feedback_events_this_cycle} of {FEEDBACK_BATCH_SIZE} "
        "feedback events collected toward the next adaptation."
    )
    if st.session_state.last_drift_message:
        st.info(st.session_state.last_drift_message)

    render_advanced_details()


def render_advanced_details() -> None:
    agent = st.session_state.agent

    with st.sidebar.expander("\U0001F52C Advanced AI Details"):
        st.write("**Current profile:**")
        st.json(asdict(agent.get_profile()))

        st.write("**Cycle history:**")
        for cycle in reversed(agent.get_history()):
            st.write(f"Cycle #{cycle.cycle_index}")
            st.write(cycle.change_explanation)
            for warning in cycle.quality_warnings:
                st.warning(warning)
            st.write("---")


def main() -> None:
    st.set_page_config(page_title="Resonance", page_icon="\U0001F3A7")
    _init_catalog()

    if st.session_state.get("stage") != "listening":
        render_setup()
    else:
        render_listening_session()


if __name__ == "__main__":
    main()
