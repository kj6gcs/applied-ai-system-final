"""
Streamlit entry point for Resonance v2.0.

Reuses the existing, unmodified Recommender/ResonanceAgent public API --
this file adds no scoring, ranking, or drift-reasoning logic of its own.
It only adapts load_songs()'s dicts into Song dataclasses and renders
whatever ResonanceAgent already computed.
"""
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from src.agent import ResonanceAgent
from src.logging_config import configure_logging
from src.recommender import Recommender, Song, UserProfile, load_songs

CATALOG_PATH = "data/songs.csv"

DEFAULT_PROFILE = UserProfile(
    favorite_genre="rock",
    favorite_mood="intense",
    target_tempo=115.0,
    target_valence=0.55,
    target_danceability=0.55,
    likes_acoustic=False,
    target_decade=2020,
    target_mood_tag="defiance",
    prefers_mainstream_hits=True,
)


def _load_catalog(csv_path: str):
    """Adapts load_songs()'s dicts into the Song dataclass Recommender expects."""
    return [Song(**row) for row in load_songs(csv_path)]


def _init_state() -> None:
    if "agent" not in st.session_state:
        configure_logging()
        recommender = Recommender(_load_catalog(CATALOG_PATH))
        agent = ResonanceAgent(recommender, DEFAULT_PROFILE)
        agent.run_cycle(k=5)  # seed the first recommendation cycle

        st.session_state.recommender = recommender
        st.session_state.agent = agent
        st.session_state.pending_feedback_display = []


def _drifted_fields(before: UserProfile, after: UserProfile):
    before_values, after_values = asdict(before), asdict(after)
    return [
        (field, before_values[field], after_values[field])
        for field in before_values
        if before_values[field] != after_values[field]
    ]


def render_profile(profile: UserProfile) -> None:
    st.subheader("Current User Profile")
    st.json(asdict(profile))


def render_recommendations(recommender: Recommender, cycle) -> None:
    st.subheader("Recommendations")
    agent = st.session_state.agent

    for recommended in cycle.recommendations:
        song = recommended.song
        score = recommender.score(cycle.profile_after, song)

        st.markdown(f"**{song.title}** by {song.artist} -- Score: {score:.2f}")
        st.caption(recommended.explanation)

        like_col, skip_col, replay_col = st.columns(3)
        if like_col.button("👍 Like", key=f"like-{cycle.cycle_index}-{song.id}"):
            agent.observe_feedback(song.id, "like")
            st.session_state.pending_feedback_display.append((song.title, "like"))
            st.rerun()
        if skip_col.button("👎 Skip", key=f"skip-{cycle.cycle_index}-{song.id}"):
            agent.observe_feedback(song.id, "skip")
            st.session_state.pending_feedback_display.append((song.title, "skip"))
            st.rerun()
        if replay_col.button("🔁 Replay", key=f"replay-{cycle.cycle_index}-{song.id}"):
            agent.observe_feedback(song.id, "replay")
            st.session_state.pending_feedback_display.append((song.title, "replay"))
            st.rerun()
        st.divider()


def render_cycle_summary(cycle) -> None:
    st.subheader("Recommendation Cycle")
    st.write(f"**Cycle #{cycle.cycle_index}**")

    st.write("**Feedback applied this cycle:**")
    if cycle.feedback_applied:
        for event in cycle.feedback_applied:
            st.write(f"- {event.event_type} on song id {event.song_id}")
    else:
        st.write("None yet -- drift needs at least a few feedback events before the agent acts on it.")

    drifted = _drifted_fields(cycle.profile_before, cycle.profile_after)
    st.write("**Preference drift detected:**")
    if drifted:
        for field, old_value, new_value in drifted:
            st.write(f"- {field}: {old_value} -> {new_value}")
    else:
        st.write("None this cycle.")

    st.info(cycle.change_explanation)

    for warning in cycle.quality_warnings:
        st.warning(warning)


def render_history_sidebar(history) -> None:
    st.sidebar.subheader("History")
    for cycle in reversed(history):
        with st.sidebar.expander(f"Cycle #{cycle.cycle_index}"):
            st.write(cycle.change_explanation)
            for recommended in cycle.recommendations:
                st.write(f"- {recommended.song.title} by {recommended.song.artist}")


def main() -> None:
    st.set_page_config(page_title="Resonance v2.0", page_icon="🎧")
    st.title("🎧 Resonance v2.0")
    st.caption("One ResonanceAgent recommendation cycle at a time.")

    _init_state()
    agent = st.session_state.agent
    recommender = st.session_state.recommender

    if st.session_state.pending_feedback_display:
        st.write("**Feedback given since the last cycle:**")
        for title, event_type in st.session_state.pending_feedback_display:
            st.write(f"- {event_type} on \"{title}\"")

    if st.button("▶️ Run Next Cycle"):
        agent.run_cycle(k=5)
        st.session_state.pending_feedback_display = []
        st.rerun()

    history = agent.get_history()
    current_cycle = history[-1]

    render_history_sidebar(history)
    render_profile(agent.get_profile())
    render_recommendations(recommender, current_cycle)
    render_cycle_summary(current_cycle)


if __name__ == "__main__":
    main()
