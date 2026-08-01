# Resonance

> **An Adaptive, Explainable Music Recommendation Agent**

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pytest](https://img.shields.io/badge/Tested%20with-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## Part 1: Overview

**Resonance** is an adaptive, explainable AI music recommendation system that continuously learns from listener feedback through transparent recommendation cycles.

Unlike traditional recommendation systems that simply rank songs from a static user profile, Resonance maintains an evolving listener profile that gradually adapts as the user interacts with recommendations. Every **Like**, **Skip**, and **Replay** contributes evidence that helps the system refine future recommendations while remaining deterministic, testable, and fully explainable.

At the heart of Resonance is the **ResonanceAgent**, a stateful AI component responsible for observing listener behavior, detecting preference drift, updating the listener profile, orchestrating recommendation cycles, and explaining how recommendations evolve over time.

---

## Why "Resonance"?

Music is deeply personal. Our preferences aren't static—they evolve with our experiences, moods, and listening habits.

Resonance is named after the way music **resonates** with listeners. Rather than treating preferences as fixed values, Resonance models them as something that gradually changes over time.

Every interaction becomes part of an ongoing conversation between the listener and the AI.

Each recommendation cycle follows the same philosophy:

> **Observe → Reason → Adapt → Recommend → Explain → Remember**

The result is a recommendation system that doesn't simply predict what you might enjoy—it continually adapts alongside you through transparent, explainable learning.

---

## Project Evolution

This project began as **Resonance v1.0**, originally developed for **CodePath AI-110 Module 3**.

The original version focused on:

- deterministic recommendation scoring
- weighted recommendation ranking
- explainable score breakdowns
- command-line interaction

For the AI-110 final project, Resonance was redesigned into a complete adaptive AI system featuring:

- Stateful AI agent
- Recommendation cycles
- Listener feedback
- Preference drift
- Explainable AI
- Streamlit interface
- Reliability testing
- Continuous profile adaptation

The original recommendation engine remains fully intact and validated while serving as one of the tools used by the ResonanceAgent.

---

# Features

## Adaptive Recommendation Agent

The **ResonanceAgent** continually learns from listener feedback while preserving deterministic recommendation behavior.

Features include:

- Like / Skip / Replay feedback
- Stateful listener profiles
- Bounded preference drift
- Recommendation history
- Recommendation-cycle explanations
- Transparent adaptation
- Deterministic behavior
- Fully testable architecture

---

## Explainable AI

Resonance provides **two independent explanation layers**.

### Layer 1 — Recommendation Engine

Answers:

> **Why was this song recommended?**

Example:

- Genre match
- Similar tempo
- Mood alignment
- Danceability similarity
- Acoustic preference

---

### Layer 2 — ResonanceAgent

Answers:

> **Why did my recommendations change?**

Example:

> "Your preferred tempo increased after consistently skipping slower songs. Future recommendations now emphasize higher-energy tracks while preserving your preferred genre."

---

## Interactive Streamlit Interface

Resonance includes a fully interactive Streamlit application allowing users to:

- Create a listener profile
- Choose from preset profiles
- Receive continuous recommendations
- Like songs
- Skip songs
- Replay songs
- Watch the listener profile evolve
- Review recommendation history
- Explore advanced AI details

---

## Reliability

Resonance emphasizes reliability through deterministic behavior and automated testing.

Current safeguards include:

- Recommendation regression testing
- Deterministic scoring
- Input validation
- Feedback validation
- Recommendation quality checks
- Repeat-artist detection
- Controlled preference drift
- Streamlit UI testing

---

# Architecture Overview

Resonance separates recommendation logic from AI reasoning.

```text
                    Streamlit UI
                         │
                         ▼
                 ResonanceAgent
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 Feedback      Listener Profile    History
 Analysis          Manager         Timeline
      │              │              │
      └──────────────┼──────────────┘
                     ▼
         Recommendation Engine
                     │
                     ▼
              Song Recommendations
                     │
                     ▼
      Recommendation Explanations
```

The recommendation engine remains deterministic.

The **ResonanceAgent** provides the adaptive intelligence.

---

# Technology Stack

| Component             | Technology                   |
| --------------------- | ---------------------------- |
| Language              | Python 3.13                  |
| Interface             | Streamlit                    |
| Testing               | Pytest                       |
| Recommendation Engine | Custom deterministic scoring |
| Agent Architecture    | Stateful orchestration       |
| Data Source           | Local CSV catalog            |
| Version Control       | Git / GitHub                 |

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/kj6gcs/applied-ai-system-final.git
cd applied-ai-system-final
```

---

## Create a Virtual Environment

Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Git Bash

```bash
source .venv/Scripts/activate
```

macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

Continue to **Part 2** for running the CLI, launching the Streamlit interface, recommendation cycles, example interactions, and project structure.

# Part 2: Running Resonance

Resonance provides two ways to interact with the recommendation engine:

- **Command-Line Interface (CLI)** — ideal for testing and development
- **Streamlit Application** — a fully interactive recommendation experience

---

# Command-Line Interface

Run the original CLI application:

```bash
python -m src.main
```

The CLI demonstrates the original recommendation engine using predefined listener profiles and displays:

- Ranked song recommendations
- Recommendation scores
- Recommendation explanations
- Deterministic recommendation output

This interface remains intentionally unchanged from Resonance v1.0 to preserve regression testing and ensure recommendation consistency.

---

# Streamlit Application

Launch the interactive interface:

```bash
streamlit run app.py
```

Your browser should automatically open.

If it does not, navigate to:

```
http://localhost:8501
```

The Streamlit application demonstrates the complete adaptive AI workflow and is the recommended way to experience Resonance.

---

# User Experience

The Streamlit application guides listeners through two stages.

---

## Stage 1 — Build a Listener Profile

Choose one of the built-in presets or create a completely custom listener profile.

Current profile attributes include:

- Favorite Genre
- Preferred Mood
- Target Tempo
- Target Valence (Emotional Tone)
- Danceability
- Acoustic Preference
- Preferred Decade
- Mood Tag
- Mainstream vs. Discovery Preference

These values provide the ResonanceAgent with an initial understanding of the listener before adaptation begins.

---

## Stage 2 — Continuous Recommendation Session

After creating a profile, Resonance begins recommending one song at a time.

For every recommendation the user can choose:

- 👍 Like
- 👎 Skip
- 🔁 Replay

Each interaction becomes evidence used by the ResonanceAgent.

Recommendations continue indefinitely while the listener profile gradually evolves.

---

# Recommendation Cycle

Every recommendation follows the same six-stage workflow.

```text
Observe
    │
    ▼
Reason
    │
    ▼
Adapt
    │
    ▼
Recommend
    │
    ▼
Explain
    │
    ▼
Remember
```

---

## 1. Observe

The ResonanceAgent records listener feedback.

Possible feedback events include:

- Like
- Skip
- Replay

These events are temporarily collected until sufficient evidence exists for adaptation.

---

## 2. Reason

Rather than reacting immediately to a single interaction, Resonance waits until enough evidence has accumulated.

This prevents abrupt profile changes and reduces noise from isolated interactions.

---

## 3. Adapt

When sufficient evidence exists, the ResonanceAgent applies **bounded preference drift**.

Examples include:

- Increasing preferred tempo
- Decreasing preferred danceability
- Updating preferred genre
- Adjusting emotional tone

Each adjustment is intentionally small and fully explainable.

---

## 4. Recommend

The updated listener profile is passed to the deterministic recommendation engine.

The recommendation engine:

- Scores every song
- Applies diversity penalties
- Produces a ranked candidate pool

A weighted candidate-selection algorithm then introduces controlled variety while preserving recommendation quality.

---

## 5. Explain

Resonance provides two independent explanation layers.

### Recommendation Explanation

Explains why the current song was recommended.

Example:

```
Genre Match
Mood Alignment
Tempo Similarity
Acoustic Preference
```

---

### Adaptation Explanation

Explains why future recommendations changed.

Example:

> Your preferred tempo increased after consistently skipping slower songs. Future recommendations now emphasize higher-energy tracks while preserving your preferred genre.

---

## 6. Remember

Every completed recommendation cycle is recorded.

History includes:

- Listener profile snapshot
- Feedback received
- Recommendation generated
- Preference changes
- Explanation of adaptation

This historical record allows the recommendation process to remain transparent and reproducible.

---

# Example Recommendation Session

## Initial Profile

```text
Favorite Genre: Rock
Preferred Tempo: 110 BPM
Preferred Mood: Energetic
```

---

## Recommendation #1

```
Back In Black — AC/DC

Reason

✓ Genre Match
✓ Tempo Match
✓ High Popularity Alignment
```

User selects:

```
👍 Like
```

---

## Recommendation #2

```
Thunderstruck — AC/DC
```

User selects:

```
🔁 Replay
```

---

## Recommendation #3

```
Dreams — Fleetwood Mac
```

User selects:

```
👎 Skip
```

---

## Adaptation

After sufficient feedback:

```
Recommendation Cycle Complete

Preference Drift Detected

Tempo
110 BPM
↓

115 BPM

Reason

Repeated preference for higher-energy songs
```

Future recommendations now favor faster songs while preserving the listener's overall musical preferences.

---

# Project Structure

```
applied-ai-system-final/

│
├── app.py
├── README.md
├── model_card.md
├── changelog.md
├── ai_interactions.md
├── requirements.txt
│
├── assets/
│
├── data/
│   └── songs.csv
│
├── diagrams/
│   ├── resonance_v1_architecture.md
│   └── resonance_v2_architecture.mmd
│
├── docs/
│   └── README_v1.md
│
├── src/
│   ├── agent.py
│   ├── logging_config.py
│   ├── main.py
│   ├── recommender.py
│   └── song_selection.py
│
└── tests/
    ├── test_agent.py
    ├── test_app.py
    ├── test_recommender.py
    └── test_song_selection.py
```

---

# Screenshots

> **TODO:** Replace the placeholders below with screenshots from the completed application.

## Listener Profile Setup

_(Insert screenshot here)_

---

## Interactive Recommendation Session

_(Insert screenshot here)_

---

## Recommendation History & AI Details

_(Insert screenshot here)_

---

Continue to **Part 3** for reliability testing, explainable AI, responsible AI, model evaluation, and technical design decisions.

# Testing & Reliability

A recommendation system should do more than produce plausible results—it should behave predictably, handle unexpected inputs safely, and provide evidence that its core functionality works as intended.

Reliability was therefore treated as a core design requirement throughout the development of Resonance v2.0.

At the current development milestone, the automated test suite contains **54 passing tests** covering the recommendation engine, adaptive agent, song-selection logic, and Streamlit interface.

Run the complete test suite with:

```bash
python -m pytest tests/ -v
```

Example result:

```text
============================= test session starts =============================
...
============================= 54 passed ==============================
```

---

## Test Coverage

The test suite is divided across four primary components:

| Test Module | Purpose |
|-------------|---------|
| `tests/test_recommender.py` | Validates scoring, ranking, explanations, catalog loading, diversity behavior, and regression outputs |
| `tests/test_agent.py` | Validates feedback handling, preference drift, recommendation cycles, configuration, history, and agent behavior |
| `tests/test_song_selection.py` | Validates controlled random selection, candidate weighting, repeat avoidance, and fallback behavior |
| `tests/test_app.py` | Validates the Streamlit user flow, profile creation, feedback controls, cycle advancement, and visible preference drift |

This layered approach allows failures to be isolated to the recommendation engine, agent, selection layer, or user interface rather than treating the application as a single black box.

---

# Reliability Strategy

Resonance combines several reliability techniques rather than relying on a single test or metric.

## Deterministic Recommendation Engine

The underlying recommendation engine remains deterministic.

Given the same:

- song catalog
- listener profile
- scoring configuration

the engine produces the same ranked recommendations.

This makes recommendation behavior reproducible and allows previously validated outputs to be used as regression tests.

---

## Regression Testing

Resonance v1.0 established known recommendation outputs for several listener profiles.

Those behaviors were preserved while Resonance v2.0 introduced the adaptive agent and Streamlit interface.

Regression tests verify that the original recommendation engine continues to produce expected results after architectural changes.

This separation is intentional:

> **The recommendation engine determines which songs fit the profile. The ResonanceAgent determines how that profile evolves.**

Keeping these responsibilities separate allows the adaptive layer to grow without silently changing the validated scoring system beneath it.

---

## Bounded Preference Drift

Resonance does not dramatically alter a listener profile after a single interaction.

Instead, the agent waits for multiple feedback events before applying preference drift.

Default adaptation settings include:

| Setting | Default |
|---------|---------|
| Minimum feedback before drift | 3 events |
| Categorical shift threshold | 3 supporting events |
| Maximum tempo adjustment | 5 BPM |
| Maximum valence adjustment | 0.05 |
| Maximum danceability adjustment | 0.05 |
| Maximum decade adjustment | 5 years |

These limits are represented through the agent's configuration rather than being embedded throughout the recommendation logic.

The result is intentionally conservative adaptation: listener preferences **drift** rather than jump.

---

## Configurable Agent Behavior

The `ResonanceAgent` supports configurable adaptation thresholds through `AgentConfig`.

Default values preserve the validated system behavior, while custom configuration allows controlled experimentation.

Automated tests verify that:

- default configuration preserves existing behavior
- changing the minimum feedback threshold changes when adaptation begins
- changing numeric step limits changes the maximum profile adjustment
- changing categorical thresholds changes when categorical preferences shift

This makes preference adaptation both testable and tunable without modifying the recommendation engine.

---

# Guardrails & Error Handling

Resonance includes guardrails at multiple levels of the system.

## Feedback Validation

The agent accepts only recognized feedback events:

```text
like
skip
replay
```

Invalid event types are rejected rather than silently influencing the listener profile.

Feedback referencing an unknown song is also rejected.

---

## Controlled Adaptation

Profile changes are bounded to prevent individual recommendation cycles from producing extreme changes.

This protects the system from:

- accidental clicks
- isolated outlier behavior
- sudden profile instability
- overreaction to limited evidence

---

## Recommendation Quality Checks

The agent performs lightweight health checks on recommendation results.

These checks can identify conditions such as:

- empty recommendation lists
- repeated artists
- excessive single-genre dominance

These warnings do not silently rewrite recommendation results. Instead, they provide diagnostic information that can be reviewed through the application's advanced AI details.

This distinction is intentional: **quality monitoring observes the recommendation system without replacing its decision-making process.**

---

## Recent-Song Protection

The interactive application maintains a rolling history of recently displayed songs.

When selecting the next recommendation, Resonance attempts to exclude recently shown tracks from the candidate pool.

If every available candidate has already appeared recently, the system safely falls back to allowing a repeat rather than failing to produce a recommendation.

---

# Controlled Randomness

A real listening experience should not repeatedly present the exact same highest-ranked song.

However, completely random selection would undermine personalization.

Resonance therefore uses **controlled randomness**.

The process is:

```text
Listener Profile
      │
      ▼
Recommendation Engine
      │
      ▼
Ranked Recommendations
      │
      ▼
Top Candidate Pool
      │
      ▼
Remove Recent Songs
      │
      ▼
Weighted Random Selection
      │
      ▼
Next Recommendation
```

The recommendation engine first generates a ranked candidate pool.

The session-selection layer then selects from the strongest candidates using rank-based weighting, giving higher-ranked songs a greater probability of appearing while still introducing variety.

Importantly, the selection layer does **not** calculate recommendation scores or modify rankings. It only chooses among candidates already evaluated by the recommendation engine.

Automated tests verify that the selection process:

- returns a valid recommendation
- avoids recently shown songs when possible
- safely handles exhausted candidate pools
- statistically favors higher-ranked candidates
- behaves deterministically when provided a seeded random-number generator
- rejects an empty candidate list
- respects configured candidate-pool size

---

# Interface Reliability

Streamlit applications rerun the Python script as users interact with widgets.

Without careful state management, this behavior can cause an application to lose track of which song a listener actually rated.

Resonance uses `st.session_state` to preserve session-specific state, including:

- active listener profile
- ResonanceAgent instance
- recommendation engine
- active song
- recently displayed songs
- feedback collected during the current cycle
- most recent preference-drift explanation
- current application stage

The active song changes only when the application explicitly advances the listening session.

This ensures that a Like, Skip, or Replay action applies to the song the listener actually saw.

---

# End-to-End UI Testing

The Streamlit interface is tested programmatically using Streamlit's application-testing tools.

Automated interface tests verify that:

- the listener setup screen renders
- preset profiles can begin a listening session
- custom profiles create the expected `UserProfile`
- feedback controls advance to another song
- three feedback events trigger the next recommendation cycle
- preference drift is displayed when adaptation occurs
- advanced AI details remain accessible

The application has also been verified to start successfully through a standard Streamlit server execution.

---

# Explainable AI

Explainability is a central design goal of Resonance.

Rather than asking the user to trust a recommendation simply because "the AI chose it," the system exposes the reasoning behind both recommendation selection and profile adaptation.

Resonance separates explainability into two layers.

---

## Layer 1 — Why This Song?

The deterministic recommendation engine explains why a song received its score.

Possible factors include:

- genre match
- mood alignment
- tempo closeness
- valence similarity
- danceability similarity
- acoustic preference
- decade preference
- mood-tag alignment
- popularity preference

The technical scoring breakdown remains available through the Streamlit interface for users who want additional detail.

---

## Layer 2 — Why Did My Recommendations Change?

The ResonanceAgent explains changes to the listener profile between recommendation cycles.

For example:

```text
Previous preferred tempo: 110 BPM
Updated preferred tempo: 115 BPM

Reason:
Recent feedback provided sufficient evidence for the agent to shift
the listener's preferred tempo upward.
```

This distinction is important.

The recommendation engine explains a **decision**.

The ResonanceAgent explains **adaptation over time**.

Together, these layers allow the user to inspect both what the system recommended and how listener behavior influenced future recommendations.

---

# Design Decisions & Trade-Offs

Several design decisions were made intentionally during the transition from Resonance v1.0 to v2.0.

## Deterministic Engine + Stateful Agent

One option was to replace the original scoring system with a generative model.

Instead, Resonance preserves the deterministic recommendation engine and places a stateful agent above it.

This provides:

- reproducible recommendations
- transparent scoring
- easier automated testing
- clear separation of responsibilities
- adaptive behavior without sacrificing explainability

The trade-off is that Resonance cannot discover complex latent preference relationships in the same way a large production recommendation model could.

For this project, transparency and reliability were prioritized over model complexity.

---

## Gradual Adaptation Instead of Immediate Learning

A single Like or Skip may not represent a meaningful preference.

Resonance therefore requires multiple feedback events before adapting the listener profile.

The trade-off is that the system reacts more slowly.

The benefit is greater stability and a lower chance of one accidental or unusual interaction significantly altering future recommendations.

---

## Weighted Selection Instead of Pure Randomness

Pure randomness creates variety but can produce poor recommendations.

Always selecting the top-ranked song maximizes score but quickly becomes repetitive.

Resonance uses a middle ground:

> **Rank first, then introduce controlled randomness among strong candidates.**

This preserves personalization while creating a more natural listening experience.

---

## Local Catalog Instead of a Live Music API

Resonance currently uses a local CSV song catalog.

A live music API could provide:

- a much larger catalog
- continuously updated music
- richer metadata
- possible preview or playback capabilities

However, an external API would also introduce:

- network dependency
- authentication requirements
- rate limits
- changing external schemas
- reduced reproducibility

For the AI-110 final project, the local catalog was retained so the complete system can be installed, tested, and evaluated without external services.

A catalog-provider abstraction and external music API remain potential future enhancements.

---

## Session State Instead of Persistent User Accounts

Listener profiles currently persist for the active Streamlit session.

A production application would likely use persistent storage such as a relational database or hosted service to retain profiles and recommendation history between sessions.

Session-based storage was chosen for the current version because it:

- keeps setup reproducible
- avoids requiring external credentials
- eliminates database dependencies
- keeps the project focused on the adaptive AI workflow

Persistent user profiles remain a future enhancement.

---

# Testing Summary

At the current development milestone:

```text
54 automated tests passing
```

Testing has demonstrated that:

- the original recommendation engine remains stable after the v2.0 redesign
- recommendation scoring remains deterministic
- the ResonanceAgent applies bounded preference drift
- configuration changes affect adaptation predictably
- invalid feedback is rejected
- recommendation history is preserved
- controlled randomness favors stronger candidates
- recently shown songs are avoided when possible
- the Streamlit interface correctly maintains session state
- listener feedback advances recommendations
- recommendation cycles execute automatically after sufficient feedback
- profile adaptation can be surfaced to the listener through explainable messages

The most important reliability lesson from development was that adding adaptive behavior did not require replacing the deterministic recommendation system.

Instead, separating **recommendation** from **adaptation** made both components easier to reason about and test.

---

# Known Limitations

Resonance remains a course-scale prototype rather than a production music platform.

Current limitations include:

- A relatively small, hand-curated local song catalog
- No direct music playback or streaming integration
- No persistent user accounts or database-backed profiles
- Preference adaptation is rule-based rather than learned from a large behavioral dataset
- Recommendation quality depends heavily on the metadata available in the catalog
- Some genres, eras, languages, artists, and listening styles are underrepresented
- Listener feedback is limited to Like, Skip, and Replay
- Session history is not retained after the active application session ends
- Controlled randomness means two unseeded listening sessions may not present songs in the same order even when the underlying ranking is identical

These limitations are intentional and documented rather than hidden.

They also identify clear opportunities for future development without compromising the reproducibility of the current system.

---

# What I Learned

Building Resonance v2.0 reinforced that an effective AI system is more than the model or algorithm responsible for producing an output.

The larger engineering challenge was designing the system around that intelligence:

- determining what information should be remembered
- deciding when evidence is strong enough to justify adaptation
- preventing unstable profile changes
- separating recommendation logic from agent reasoning
- making decisions explainable to users
- testing stateful behavior
- managing randomness without losing reproducibility
- presenting technical AI behavior through a usable interface

The transition from Resonance v1.0 to v2.0 demonstrated how a deterministic prototype can evolve into a stateful applied AI system without discarding the reliable components that already work.

The most important architectural lesson was simple:

> **The recommendation engine does not need to be the agent. It can be a tool the agent uses.**

That separation became the foundation for Resonance's adaptive, explainable design.

---

Continue to **Part 4** for the project roadmap, future enhancements, portfolio reflection, acknowledgements, and final project information.

# Future Roadmap

Resonance v2.0 establishes the foundation for an adaptive, explainable music recommendation system, but the current architecture was intentionally designed so that additional capabilities can be added without replacing the validated recommendation engine or ResonanceAgent.

Future development could expand Resonance in several directions.

---

## External Music Catalog

The current version uses a local CSV catalog to ensure deterministic, reproducible execution.

A future version could introduce a catalog-provider abstraction:

```text
                  Catalog Provider
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        Local CSV             Music API
```

This would allow Resonance to retain its local catalog for testing while optionally retrieving songs from a larger external music service.

Potential benefits include:

- significantly larger music catalogs
- international and foreign-language music
- broader genre representation
- richer song metadata
- continuously updated releases
- album artwork
- preview or playback links where supported

The recommendation engine would remain independent of the catalog source.

---

## Persistent Listener Profiles

Resonance currently maintains listener state within the active Streamlit session.

A future version could introduce persistent profile storage using a database platform such as PostgreSQL or Supabase.

Persistent storage could retain:

- listener accounts
- profile preferences
- feedback history
- recommendation cycles
- preference-drift history
- previously recommended songs

This would allow Resonance to continue learning from a listener across multiple sessions and devices.

---

## Authentication

Persistent profiles could eventually be paired with user authentication.

A listener could:

```text
Sign In
   │
   ▼
Load Existing Profile
   │
   ▼
Resume Listening
   │
   ▼
Continue Preference Adaptation
```

Authentication is intentionally outside the scope of the current project because it does not directly improve the core adaptive recommendation workflow.

---

## Expanded Feedback Signals

The current agent learns from three explicit behaviors:

```text
Like
Skip
Replay
```

A future system could incorporate additional signals such as:

- listening duration
- early skips
- repeated plays
- playlist additions
- favorites
- search behavior
- manual ratings
- artist follows
- genre exploration
- time-of-day listening patterns

These signals could provide a richer picture of listener preferences without requiring users to manually configure every profile attribute.

---

## Improved Diversity

Resonance already includes artist-diversity behavior and session-level repeat avoidance.

Future versions could extend diversity controls across:

- genre
- decade
- artist
- language
- popularity
- geographic origin

This could help reduce filter-bubble effects while still respecting listener preferences.

---

## Richer Preference Modeling

The current preference model uses explicit, human-readable attributes such as:

- genre
- mood
- tempo
- valence
- danceability
- acoustic preference
- decade
- popularity

This makes the system highly explainable.

A future version could experiment with embeddings, collaborative filtering, or learned preference representations while retaining the current deterministic system as an explainable baseline.

Such experimentation would allow comparison between:

```text
Transparent Rule-Based Recommendation

vs.

Learned Recommendation Models
```

rather than assuming that greater model complexity automatically produces a better system.

---

## Natural-Language Explanations

The current system generates explanations directly from deterministic recommendation and adaptation logic.

A future enhancement could optionally use a language model to translate structured explanation data into more conversational language.

For example:

```text
Structured Agent Output

tempo: +5 BPM
valence: -0.05
danceability: -0.05
```

could become:

> Your recent feedback suggests that you're leaning toward faster, slightly darker, and less dance-oriented music. Resonance has adjusted your profile gradually while preserving your broader listening preferences.

The language model would explain the decision rather than make the recommendation itself.

This separation would preserve deterministic decision-making while improving communication with the listener.

---

# Development Status

Resonance v2.0 is currently feature-complete for the CodePath AI-110 final project.

The project is under a feature freeze while final documentation, evaluation evidence, and presentation materials are completed.

### Completed

- [x] Deterministic recommendation engine
- [x] Explainable recommendation scoring
- [x] Artist diversity behavior
- [x] ResonanceAgent
- [x] Listener feedback collection
- [x] Bounded preference drift
- [x] Configurable agent behavior
- [x] Recommendation-cycle history
- [x] Two-layer explainability
- [x] Structured logging
- [x] Controlled candidate selection
- [x] Recent-song avoidance
- [x] Listener profile builder
- [x] Interactive Streamlit application
- [x] Automated recommendation tests
- [x] Automated agent tests
- [x] Automated song-selection tests
- [x] Automated Streamlit interface tests
- [x] 54-test automated test suite

### Finalization

- [ ] Final architecture diagram
- [ ] Final `model_card.md`
- [ ] Final `ai_interactions.md`
- [ ] Final rubric audit
- [ ] Reproducible execution evidence
- [ ] Application screenshots
- [ ] Presentation
- [ ] Optional Loom walkthrough

---

# Portfolio Reflection

Resonance demonstrates my progression from building individual AI-related components to designing a complete applied AI system.

The original Resonance project focused primarily on recommendation scoring: given a predefined listener profile and song catalog, the system calculated which songs best matched that profile.

Resonance v2.0 required a different question:

> **What happens after the recommendation?**

Answering that question led to the development of the ResonanceAgent and the recommendation-cycle architecture.

Instead of treating listener preferences as static input, the system now observes behavior, reasons about accumulated feedback, applies controlled preference drift, generates new recommendations, explains its decisions, and remembers previous cycles.

Developing Resonance reinforced the importance of separating concerns within AI systems. The deterministic recommendation engine remains responsible for scoring songs, while the agent is responsible for state, adaptation, orchestration, and history.

That separation allowed the original validated system to remain intact while new capabilities were added around it.

For me, Resonance represents an important shift from thinking primarily about **what an AI component can produce** to thinking about **how an AI system should behave over time**.

---

# Original Project

Resonance v2.0 evolved from my original **CodePath AI-110 Module 3 music recommendation project, Resonance v1.0**.

The original project remains available in its separate repository:

**Original Repository:**  
https://github.com/kj6gcs/ai110-module3show-musicrecommendersimulation-starter

The original README has also been preserved in this repository:

```text
docs/README_v1.md
```

This provides a direct comparison between the original deterministic prototype and the final adaptive system.

---

# AI-110 Final Project

Resonance v2.0 was developed as the final **Show What You Know: Applied AI System** project for CodePath's AI-110: Foundations of AI Engineering course.

The project extends concepts explored throughout the course, including:

- debugging and system design
- structured reasoning
- AI-assisted development
- agentic workflows
- reliability testing
- explainability
- responsible AI
- evaluation
- technical communication

The final project challenged students to evolve an earlier prototype into a cohesive, reliable, and professionally documented applied AI system.

---

# AI-Assisted Development

Generative AI tools were used throughout the development of Resonance as engineering collaborators.

AI assistance supported activities including:

- architectural brainstorming
- codebase review
- implementation planning
- code generation
- automated test design
- debugging
- design critique
- documentation planning
- technical review

AI-generated suggestions were reviewed rather than treated as automatically correct.

Several proposed approaches were modified, postponed, or rejected when they introduced unnecessary complexity, conflicted with the intended architecture, or expanded the project beyond its core requirements.

A detailed discussion of AI collaboration—including helpful and flawed AI suggestions—is documented in:

```text
model_card.md
```

Development interactions are additionally documented in:

```text
ai_interactions.md
```

---

# Responsible AI

Resonance was designed around several responsible-AI principles:

### Transparency

Recommendation and adaptation decisions are exposed rather than hidden behind an opaque model.

### Stability

Listener profiles change gradually through bounded preference drift rather than reacting dramatically to isolated interactions.

### Human Control

The listener remains the source of behavioral feedback and can inspect how that feedback affects the active profile.

### Reproducibility

The local catalog and deterministic recommendation engine allow core recommendation behavior to be reproduced without relying on external AI services.

### Bias Awareness

The system explicitly acknowledges limitations caused by catalog size, metadata selection, genre representation, and manually designed scoring rules.

A more complete discussion of limitations, bias, misuse, testing observations, and responsible AI is available in [`model_card.md`](model_card.md).

---

# Repository Documentation

Additional project documentation is available throughout the repository.

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `model_card.md` | Responsible AI, limitations, testing observations, and AI-collaboration reflection |
| `ai_interactions.md` | Record of AI-assisted development interactions |
| `changelog.md` | Development history and major project changes |
| `diagrams/resonance_v2_architecture.mmd` | Mermaid source for the final system architecture |
| `docs/README_v1.md` | Archived documentation from Resonance v1.0 |

---

# Contributing

Resonance is currently an educational and portfolio project rather than an actively maintained community project.

However, suggestions, bug reports, and constructive feedback are welcome through GitHub Issues.

If extending the project, please preserve the separation between:

```text
Agent Reasoning
Recommendation Logic
Catalog Access
User Interface
```

Keeping these responsibilities independent is a core design principle of Resonance.

---

# License

This project is released under the terms of the license included in this repository.

See [`LICENSE`](LICENSE) for details.

> **Note:** If no `LICENSE` file is currently present in the repository, add an appropriate license before publishing or remove this section.

---

# Acknowledgements

Resonance was developed as part of **CodePath AI-110: Foundations of AI Engineering**.

Special thanks to:

- **CodePath** for the AI-110 curriculum, project framework, and development resources.
- The open-source Python, Streamlit, and pytest communities for the tools used to build and test the application.
- Generative AI tools used as development collaborators throughout the project's design, implementation, review, and documentation process.

---

# About the Author

**Robby Wideman**

Cybersecurity student and developer with interests in defensive security, AI engineering, automation, networking, and open-source software.

Resonance reflects my interest in building systems that are not only functional, but also transparent, testable, explainable, and understandable to the people who use them.

GitHub: [@kj6gcs](https://github.com/kj6gcs)

---

# Final Thought

Music taste is not static.

Neither should the system trying to understand it be.

Resonance begins with a listener profile, but it does not assume that profile tells the entire story. Every Like, Skip, and Replay provides new evidence. Through repeated recommendation cycles, the system observes, reasons, adapts, recommends, explains, and remembers.

The goal is not simply to predict what song should come next.

It is to create an ongoing, transparent interaction in which the recommendation system continually **resonates with the listener**.

---

**Resonance v2.0**  
*An Adaptive, Explainable Music Recommendation Agent*