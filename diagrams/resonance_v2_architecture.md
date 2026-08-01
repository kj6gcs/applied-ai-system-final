# Resonance v2.0 System Architecture

[README](../README.md) •
[Model Card](../model_card.md) •
[AI Interactions](../ai_interactions.md) •
[Changelog](../changelog.md) •
[License](../LICENSE)

---

This diagram shows the primary components of Resonance v2.0, the flow of listener feedback through the adaptive agent, and the reliability/testing layers used to validate the system.

```mermaid
flowchart TD

    U["Listener"]
    UI["Streamlit App<br/>app.py"]
    CLI["CLI Demo<br/>src/main.py"]

    U -->|"Build profile"| UI
    U -->|"Like / Skip / Replay"| UI

    SS["Streamlit Session State<br/>active profile, agent, active song,<br/>recent songs, cycle counters"]
    UI <--> SS

    subgraph AGENT["Adaptive AI Layer"]
        RA["ResonanceAgent<br/>src/agent.py"]
        AC["AgentConfig<br/>drift thresholds + max step sizes"]
        FB["Feedback Buffer<br/>validated pending events"]
        PH["Recommendation Cycle History<br/>profile before/after, feedback,<br/>recommendations, warnings, explanations"]

        AC --> RA
        RA --> FB
        FB --> RA
        RA --> PH
    end

    SS <--> RA

    subgraph ENGINE["Deterministic Recommendation Layer"]
        REC["Recommender<br/>src/recommender.py"]
        SCORE["Scoring Logic<br/>genre, mood, tempo, valence,<br/>danceability, acousticness,<br/>decade, mood tag, popularity"]
        DIV["Greedy Artist Diversity Penalty"]
        EX1["Layer 1 Explanation<br/>Why this song?"]

        REC --> SCORE
        SCORE --> DIV
        REC --> EX1
    end

    RA -->|"Updated UserProfile"| REC
    CLI -->|"Predefined profiles"| REC

    CAT[("Local Song Catalog<br/>data/songs.csv")]
    LOAD["Catalog Loader<br/>load_songs()"]
    SEL["Session Song Selection<br/>src/song_selection.py"]
    RECENT["Recent Song IDs<br/>repeat avoidance"]

    CAT --> LOAD
    LOAD --> REC
    LOAD --> SS

    REC -->|"Ranked top candidates"| SEL
    RECENT --> SEL
    SS --> RECENT

    SEL -->|"Weighted random pick<br/>from strong candidates"| SS
    SS -->|"Active recommendation"| UI

    UI -->|"Feedback event"| RA
    RA -->|"Observe + validate"| FB
    RA -->|"Reason about evidence"| RA
    RA -->|"Bounded preference drift"| SS
    RA -->|"Run next recommendation cycle"| REC

    EX2["Layer 2 Explanation<br/>Why did recommendations change?"]
    QA["Quality Checks<br/>empty list, repeated artists,<br/>single-genre dominance"]

    RA --> EX2
    RA --> QA
    EX2 --> UI
    QA -->|"Advanced AI Details"| UI
    PH -->|"History / transparency"| UI

    subgraph TESTING["Reliability & Evaluation"]
        TREC["tests/test_recommender.py<br/>scoring, ranking, regression"]
        TAGENT["tests/test_agent.py<br/>feedback, drift, config, history"]
        TSEL["tests/test_song_selection.py<br/>weighted selection, repeat avoidance"]
        TAPP["tests/test_app.py<br/>Streamlit AppTest"]
        LOG["Structured Logging<br/>src/logging_config.py"]
    end

    TREC -. "verifies" .-> REC
    TAGENT -. "verifies" .-> RA
    TSEL -. "verifies" .-> SEL
    TAPP -. "verifies" .-> UI
    LOG -. "diagnostics" .-> REC
    LOG -. "diagnostics" .-> RA

    CYCLE["Recommendation Cycle<br/>Observe → Reason → Adapt → Recommend → Explain → Remember"]
    RA -. "implements" .-> CYCLE
```

## Architecture Overview

Resonance v2.0 separates the listener-facing experience from the adaptive agent and the deterministic recommendation engine.

The **Streamlit interface** manages the interactive session. It allows a listener to create an initial profile, receive one recommendation at a time, and respond with **Like**, **Skip**, or **Replay** feedback.

The **ResonanceAgent** is the stateful AI layer. It validates feedback, accumulates evidence, evaluates whether preference drift is justified, applies bounded profile changes, requests new recommendations, performs lightweight quality checks, explains adaptation, and stores recommendation-cycle history.

The **recommendation engine** remains deterministic. It scores and ranks songs using explicit features such as genre, mood, tempo, valence, danceability, acousticness, decade, mood tags, and popularity preference. Existing artist-diversity behavior remains part of the ranking logic.

The **song-selection layer** introduces controlled variety after ranking. It selects from strong candidates using weighted randomness while avoiding recently shown tracks when possible. It does not calculate recommendation scores or replace the recommendation engine.

The **reliability layer** includes automated tests for scoring/ranking, agent behavior, candidate selection, and Streamlit interaction, plus structured logging for diagnostics.

---

## Recommendation Cycle

The adaptive workflow follows six conceptual stages:

```text
Observe
   ↓
Reason
   ↓
Adapt
   ↓
Recommend
   ↓
Explain
   ↓
Remember
```

### Observe

The listener provides feedback on the active recommendation.

### Reason

The agent evaluates whether enough consistent evidence has accumulated to justify a profile change.

### Adapt

If the evidence threshold is met, the agent applies bounded preference drift using `AgentConfig`.

### Recommend

The updated profile is passed to the deterministic recommendation engine.

### Explain

Resonance provides two explanation layers:

1. **Why this song?** — generated by the recommendation engine.
2. **Why did my recommendations change?** — generated by the `ResonanceAgent`.

### Remember

The completed recommendation cycle is recorded in history so the system remains transparent and inspectable.

---

## Key Design Principle

> **The recommendation engine determines which songs fit the current profile. The ResonanceAgent determines how that profile evolves over time.**

That separation allows the system to become adaptive without replacing the transparent and reproducible scoring logic validated in Resonance v1.0.

---

← [Back to Resonance](../README.md)
