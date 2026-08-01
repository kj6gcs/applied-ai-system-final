# Model Card: Resonance v2.0

> **Adaptive, Explainable Music Recommendation Agent**

[README](README.md) •
[Model Card](model_card.md) •
[AI Interactions](ai_interactions.md) •
[Changelog](changelog.md) •
[Architecture](diagrams/resonance_v2_architecture.mmd) •
[License](LICENSE)

---

## 1. System Overview

**System Name:** Resonance  
**Version:** 2.0  
**Project Type:** Applied AI / Agentic Music Recommendation System  
**Primary AI Feature:** Agentic Workflow  
**Interface:** Streamlit and command-line interface (CLI)  
**Recommendation Data Source:** Local song catalog (`data/songs.csv`)

Resonance v2.0 is an adaptive music recommendation system that maintains an evolving listener profile and uses explicit listener feedback to influence future recommendations.

The project evolved from **Resonance v1.0**, a deterministic music recommender originally developed for CodePath AI-110 Module 3. The original system ranked songs from a fixed catalog by comparing song metadata with a manually defined listener profile. It could explain why individual songs scored well, but the profile itself remained static.

Resonance v2.0 adds a stateful **ResonanceAgent** above the validated recommendation engine. The agent observes Likes, Skips, and Replays; accumulates evidence; detects preference drift; applies bounded profile changes; requests new recommendations; evaluates recommendation quality; explains why recommendations changed; and stores recommendation-cycle history.

The design can be summarized as:

```text
Observe → Reason → Adapt → Recommend → Explain → Remember
```

The recommendation engine remains deterministic. The adaptive behavior comes from the agent that orchestrates it.

---

## 2. Intended Use

Resonance is an educational applied-AI system designed to demonstrate how a static recommendation prototype can evolve into a stateful, testable, and explainable agentic workflow.

The intended user can:

- create an initial listening profile;
- receive one recommendation at a time;
- respond with Like, Skip, or Replay;
- allow feedback to accumulate across a recommendation cycle;
- observe gradual changes to the active listener profile;
- inspect why a song was recommended;
- inspect why recommendations changed over time; and
- review technical cycle history through the application's advanced details.

Resonance is **not** intended to represent a production-scale music platform. It does not stream music, maintain persistent accounts, use collaborative filtering, or infer preferences from millions of listeners.

The project is primarily intended to demonstrate:

- agentic orchestration;
- state management;
- behavioral feedback;
- bounded adaptation;
- explainability;
- guardrails;
- automated reliability testing; and
- responsible system design.

---

## 3. How Resonance Works

Resonance separates the system into two primary layers.

### Recommendation Engine

The recommendation engine scores songs using explicit, human-readable listener preferences and song metadata.

Examples of features include:

- genre;
- mood;
- tempo;
- valence;
- danceability;
- acoustic preference;
- release decade;
- mood tags; and
- mainstream/popularity preference.

The engine produces ranked recommendations and an explanation of the factors contributing to each recommendation.

### ResonanceAgent

The `ResonanceAgent` is responsible for behavior over time.

It:

1. observes listener feedback;
2. validates the feedback event;
3. accumulates evidence during the current cycle;
4. determines whether enough evidence exists to justify adaptation;
5. applies bounded preference drift when appropriate;
6. asks the existing recommendation engine for new recommendations;
7. evaluates recommendation quality;
8. explains profile changes; and
9. records the completed recommendation cycle in history.

The agent does **not** independently calculate recommendation scores or replace the recommendation engine.

This separation was intentional: the recommendation engine answers **"Which songs fit this profile?"**, while the agent answers **"How should this profile evolve based on the listener's behavior?"**

---

## 4. Feedback and Adaptation

The current system recognizes three listener feedback signals:

| Feedback | Interpretation                                                                                 |
| -------- | ---------------------------------------------------------------------------------------------- |
| `like`   | Positive evidence that the listener enjoyed the recommendation                                 |
| `skip`   | Negative or ambiguous evidence that the recommendation did not fit the listener at that moment |
| `replay` | Strong positive evidence that the recommendation matched the listener's taste                  |

Resonance does not immediately rewrite a profile after every click.

By default, multiple feedback events must accumulate before preference drift is considered. Numeric changes are bounded so that a single recommendation cycle cannot dramatically alter the listener profile.

Default adaptation limits include:

| Configuration                 |             Default |
| ----------------------------- | ------------------: |
| Minimum feedback before drift |            3 events |
| Categorical shift threshold   | 3 supporting events |
| Maximum tempo change          |               5 BPM |
| Maximum valence change        |                0.05 |
| Maximum danceability change   |                0.05 |
| Maximum decade change         |             5 years |

These values are configurable through `AgentConfig`, allowing the adaptation policy to be tested without changing the recommendation algorithm itself.

---

## 5. Explainability

Resonance provides two distinct explanation layers.

### Layer 1: Why Was This Song Recommended?

The recommendation engine exposes the scoring factors that contributed to an individual recommendation.

Examples can include:

- genre match;
- mood match;
- tempo closeness;
- acoustic alignment;
- mood-tag match; and
- popularity alignment.

This makes the recommendation itself inspectable rather than presenting a song as an unexplained AI decision.

### Layer 2: Why Did My Recommendations Change?

The ResonanceAgent compares the listener profile before and after adaptation and records the evidence that caused any change.

This allows the system to explain changes such as:

```text
Preferred tempo:
110 BPM → 115 BPM

Reason:
Recent feedback provided enough evidence for the agent to shift
the listener's preferred tempo upward.
```

The first explanation layer describes a recommendation decision. The second describes adaptation over time.

---

## 6. Reliability and Evaluation

Reliability is treated as a core part of the system rather than an optional final check.

At the current project milestone, Resonance has:

```text
54 automated tests passing
```

The tests cover four major areas:

| Test Module                    | Focus                                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------- |
| `tests/test_recommender.py`    | Scoring, ranking, explanations, diversity behavior, catalog loading, regression outputs           |
| `tests/test_agent.py`          | Feedback validation, bounded drift, configuration, recommendation cycles, history, quality checks |
| `tests/test_song_selection.py` | Candidate selection, repeat avoidance, weighted randomness, fallback behavior                     |
| `tests/test_app.py`            | Streamlit setup, profile creation, feedback controls, cycle advancement, visible preference drift |

Important reliability mechanisms include:

- deterministic recommendation scoring;
- regression tests against known recommendation outputs;
- feedback-event validation;
- rejection of unknown song IDs;
- bounded profile adaptation;
- defensive copies of agent state/history;
- recommendation quality warnings;
- recent-song avoidance;
- seeded-random testing of the selection layer;
- structured logging; and
- end-to-end Streamlit application tests.

The recommendation engine was deliberately preserved while the agentic system was built around it. This made it possible to verify that new adaptive behavior did not silently change the original scoring weights, ranking behavior, or CLI results.

---

# 7. Required Reflection: Limitations and Biases

## What are the limitations or biases in the system?

Resonance has several important limitations, and some of them were already visible in v1.0.

### Catalog Bias

The current catalog is small and hand-curated. This means the recommendation space reflects the music that was selected for the dataset rather than the diversity of music that actually exists.

Genres, languages, countries, eras, artists, and musical traditions are not represented equally. A user whose taste falls outside the strongest areas of the catalog may receive weaker recommendations regardless of how accurately the profile represents them.

The original Resonance project exposed a particularly important version of this problem: **genre imbalance can interact with a heavily weighted genre-match score and dominate the top results**. The adaptive agent does not automatically remove that bias. In some circumstances, adaptation could reinforce it.

### Feedback-Loop / Filter-Bubble Risk

Resonance learns from its own recommendations.

That creates a feedback-loop risk:

```text
System recommends similar music
        ↓
Listener positively rates some of it
        ↓
Profile shifts toward that music
        ↓
System recommends even more similar music
```

If left unchecked, this could narrow recommendations over time rather than encourage discovery.

Artist-diversity behavior, recent-song avoidance, quality warnings, and controlled candidate selection help reduce repetition, but they do not fully solve the broader filter-bubble problem.

### Simplified Listener Model

A person's music taste is more complicated than a single genre, mood, target tempo, valence value, or danceability value.

The original project made this limitation especially obvious: real preferences such as "acoustic sometimes" or moods that combine qualities like playful, intense, and epic do not fit neatly into one boolean or one categorical field.

Resonance v2.0 improves the situation by allowing those values to evolve from behavior, but the underlying representation is still simplified.

### Ambiguous Feedback

A Skip does not necessarily mean:

> "I dislike music like this."

A listener may skip because:

- they recently heard the song;
- they are not in the mood for it right now;
- they like the artist but not that particular track;
- they were interrupted;
- they want something different temporarily.

The agent therefore treats feedback conservatively, but it still cannot know the listener's true motivation.

### Rule-Based Adaptation

The agent's preference drift is evidence-based and stateful, but it is still implemented through explicit rules and thresholds rather than a model trained on large-scale listening behavior.

That is useful for transparency and reproducibility, but it limits the complexity of patterns the system can learn.

### No Persistent Long-Term Identity

The Streamlit application currently keeps the active listener state within the session. It does not maintain a database-backed user identity across devices or future sessions.

Therefore, the current system demonstrates adaptive learning during a listening session rather than true long-term personalization.

### Controlled Randomness

The recommendation engine is deterministic, but the listening interface intentionally introduces weighted randomness among strong candidates.

As a result, two unseeded sessions with identical profiles may show songs in a different order even though the underlying recommendation ranking is the same.

---

# 8. Required Reflection: Potential Misuse and Safeguards

## Could the AI be misused, and how would I prevent that?

Resonance is a relatively low-risk application compared with systems used for healthcare, finance, public safety, employment, or cybersecurity decision-making. However, it can still be misused or misrepresented.

### Artificial Feedback Manipulation

A user or automated process could repeatedly submit Likes, Skips, or Replays in order to force the profile toward a particular genre, mood, or numeric target.

In the current project this primarily affects the user's own session, but the same weakness would become more important if feedback were later shared across users or used to influence public rankings.

Current safeguards include:

- validation of feedback event types;
- validation that feedback refers to a known song;
- minimum evidence requirements before adaptation;
- bounded numeric profile changes; and
- categorical thresholds before categorical preferences shift.

A production system could additionally implement rate limits, anomaly detection, account-level controls, and stronger event provenance.

### Overstating What the System Knows

A more realistic misuse would be presenting the inferred listener profile as an objective psychological description of a person.

Resonance does not know _why_ someone likes or skips a song. Its profile is only a working recommendation representation based on limited metadata and limited behavioral signals.

For that reason, the interface and documentation should describe profile changes as recommendation preferences rather than personality traits or factual conclusions about the listener.

### Misrepresenting the System as a Learned Production Model

Resonance should not be described as if it were trained on millions of users or powered by a hidden large-scale machine-learning model.

Its recommendation engine is deterministic, and its adaptive behavior is rule-based and agentic.

Preventing this form of misuse is primarily a transparency issue. The README, model card, architecture diagram, and source code explicitly document what the system does and does not do.

### Privacy Considerations for Future Versions

The current session-based implementation avoids storing long-term personal listening histories.

If persistent accounts are added later, feedback and listening history would become personal behavioral data. A production version should minimize collected data, clearly explain retention, restrict access, and allow users to delete their history and profile.

---

# 9. Required Reflection: Reliability Surprise

## What surprised me while testing the AI's reliability?

The biggest surprise was discovering that the original automated tests were passing even though they were not testing the recommendation path the application actually used.

The original code contained two disconnected implementations:

- a dictionary-based functional path used by the real CLI; and
- a `Song` / `UserProfile` / `Recommender` object-oriented path containing stub behavior.

The tests exercised the stub path rather than the real scoring and ranking functions. One test appeared to prove that recommendations were sorted correctly, but the stub simply returned the first `k` songs. The fixture happened to already contain the expected song first, so the test passed by coincidence.

That was an important reliability lesson:

> **A green test suite does not prove that the system works if the tests are attached to the wrong behavior.**

The fix was not simply to add more tests. The recommendation paths were unified so the `Recommender` wrapper delegated to the validated scoring engine, and the test suite was rewritten around actual behavior.

Regression tests were then pinned to documented recommendation outputs so future refactoring cannot silently change the established scoring behavior.

Testing the adaptive agent produced a second useful lesson: stateful AI behavior is easier to trust when adaptation is bounded and configurable. By testing different `AgentConfig` thresholds, I could verify not only that profile drift occurred, but that it occurred **when and by how much** the configuration said it should.

By the current milestone, the project has grown from a small test suite that gave false confidence to **54 passing tests** across the recommendation engine, agent, candidate-selection layer, and Streamlit application.

---

# 10. Required Reflection: Collaboration With AI

## How did I collaborate with AI during this project?

Generative AI was used as an engineering collaborator throughout the development of Resonance v2.0.

I primarily worked with **ChatGPT** and **Claude Code**, but they served different roles in the workflow.

ChatGPT was used heavily for:

- project planning;
- interpreting the assignment and rubric;
- architectural discussion;
- deciding project scope;
- reviewing proposed implementation plans;
- evaluating trade-offs;
- documentation planning;
- debugging guidance; and
- acting as a second reviewer of changes proposed by Claude.

Claude Code was used primarily inside the repository for:

- reading and auditing the existing codebase;
- identifying technical debt;
- proposing implementation plans;
- making approved code changes;
- adding automated tests;
- running the test suite;
- verifying CLI behavior;
- testing the Streamlit application; and
- reporting exactly which files changed.

The workflow was intentionally iterative rather than:

```text
Prompt AI → Accept Everything → Submit
```

It was closer to:

```text
Define Goal
    ↓
Ask AI to Analyze
    ↓
Review Proposal
    ↓
Question / Modify the Proposal
    ↓
Approve a Narrow Change
    ↓
Run Tests
    ↓
Review Results
    ↓
Commit a Meaningful Milestone
```

This process was especially useful because the two AI tools could effectively provide different perspectives: one could propose or implement a change while the other helped review whether that change fit the architecture and project requirements.

I still made the project-level decisions about what Resonance should become, which features belonged in the final scope, which suggestions should be accepted or rejected, and when a development phase was ready to commit.

---

## One Helpful AI Suggestion

One of the most helpful AI contributions came from Claude's initial codebase review.

Claude identified that `src/recommender.py` contained **two disconnected recommendation paths**. The dictionary-based functions contained the real scoring logic used by the application, while the `Recommender` class used by the tests still contained stub behavior.

That observation exposed both an architectural problem and a reliability problem: the tests could pass without validating the application that users actually ran.

The recommended solution was to make the `Recommender` class a thin wrapper around the existing validated functional engine rather than create a second implementation.

That suggestion was valuable because it:

- eliminated duplicate conceptual paths;
- preserved the already validated scoring formula;
- made the object-oriented API usable by the future agent;
- allowed tests to exercise real application behavior; and
- provided a stable foundation for ResonanceAgent without rewriting the original engine.

This became one of the key architectural decisions in the v2.0 project.

---

## One Flawed or Incorrect AI Suggestion

An important example of a suggestion I chose **not** to follow was an early recommendation to immediately split the small recommendation module into numerous files such as:

```text
domain.py
catalog.py
scoring.py
ranking.py
agent.py
evaluation.py
logging_config.py
```

The proposed boundaries were reasonable in isolation, but implementing all of them immediately would have added substantial structural complexity before the project had actually demonstrated a need for every abstraction.

After reviewing the proposal, we chose a narrower approach:

- preserve the validated recommendation module;
- unify its real and stubbed paths;
- add the agent as a genuinely new responsibility;
- add logging where needed;
- add song-selection logic only when the interactive listening workflow required it; and
- avoid refactoring simply for the sake of having more modules.

This was a useful reminder that AI can produce technically plausible architecture that is still **too elaborate for the size and maturity of the project**.

The suggestion was not malicious or nonsensical—it was simply premature.

Rejecting it helped keep the project understandable and allowed abstractions to be added when the implementation actually earned them.

---

# 11. Responsible AI Design Decisions

Several design decisions were made specifically to keep Resonance understandable and controllable.

## Transparency Over Hidden Complexity

The project intentionally retains a deterministic recommendation engine rather than replacing it with an opaque model simply to make the system appear more sophisticated.

A user or reviewer can inspect the scoring logic and the reasons attached to recommendations.

## Gradual Adaptation

The system does not assume that one click reveals a stable preference.

Multiple feedback events are required before adaptation, and numeric changes are bounded.

## Human Feedback Remains Central

The listener supplies the behavioral evidence that drives adaptation.

The system does not claim that inferred profile changes are objectively correct. They are working hypotheses used to improve subsequent recommendations.

## Quality Warnings Are Observations, Not Hidden Overrides

The agent can flag conditions such as:

- empty recommendation results;
- repeated artists; and
- single-genre dominance.

These warnings are exposed diagnostically rather than silently replacing recommendations behind the user's back.

## Reproducibility

The local CSV catalog was deliberately retained for the final project instead of making an external music API mandatory.

This means another person can clone the repository, install the requirements, and reproduce the core system without API credentials, network availability, rate limits, or changing third-party data.

---

## 12. What Changed From Resonance v1.0?

Several ideas listed as future work in the original model card became actual v2.0 functionality.

| Resonance v1.0 Limitation / Future Idea  | Resonance v2.0                                                           |
| ---------------------------------------- | ------------------------------------------------------------------------ |
| Static profile supplied entirely upfront | Profile evolves from behavioral feedback                                 |
| CLI-only experience                      | Interactive Streamlit listener interface                                 |
| No ongoing listener behavior             | Like / Skip / Replay feedback                                            |
| No adaptation                            | Bounded preference drift                                                 |
| Recommendation explanation only          | Recommendation + adaptation explanations                                 |
| Fixed recommendation presentation        | Continuous one-song listening workflow                                   |
| Limited diversity handling               | Artist diversity behavior + recent-song avoidance + controlled selection |
| Minimal reliability evidence             | 54-test automated suite                                                  |
| No agent                                 | Stateful ResonanceAgent orchestrates recommendation cycles               |

The project therefore did not discard v1.0. It extended the reliable parts of the original system and directly addressed several limitations identified during the first project's reflection. The original model card documented the limits of a fixed taste profile and specifically proposed learning from skips, likes, and repeat listens as future work.

---

## 13. Remaining Limitations and Future Work

Potential future improvements include:

### Larger and More Diverse Catalog

Introduce an optional external music API while retaining the local CSV as a reproducible fallback.

### Persistent Profiles

Store user profiles, feedback events, and recommendation-cycle history in a database so adaptation can continue across sessions.

### More Behavioral Signals

Incorporate signals such as:

- listening duration;
- early versus late skips;
- playlist additions;
- favorites;
- searches; and
- repeated listening across multiple sessions.

### Stronger Diversity Controls

Extend diversity beyond artist repetition to include genre, language, decade, popularity, and geographic origin.

### Learned Preference Models

Compare the transparent rule-based baseline with embeddings, collaborative filtering, or other learned recommendation approaches.

### Optional Natural-Language Explanation Layer

A language model could eventually convert the agent's structured, deterministic explanation data into more conversational language while leaving the underlying recommendation and adaptation decisions unchanged.

---

## 14. Final Reflection

The most important thing I learned from Resonance v2.0 is that building an applied AI system is not only about choosing a sophisticated model.

The larger challenge is designing the behavior around the intelligence:

- What should the system observe?
- What should it remember?
- When is there enough evidence to act?
- How large should an adaptation be?
- How can a user understand why something changed?
- How do I know the system is actually doing what I think it is doing?
- What happens when the data or feedback is incomplete, biased, or misleading?

Resonance began as a program that answered:

> **"Which songs best match this profile?"**

The final project asks a more interesting question:

> **"How should a recommendation system respond as it learns more about the listener?"**

The resulting architecture preserves the deterministic recommendation engine while surrounding it with a stateful, explainable workflow that observes feedback, reasons about evidence, adapts conservatively, requests new recommendations, evaluates results, explains changes, and remembers previous cycles.

That evolution also strengthened the meaning behind the project's name.

The system continually **resonates with the listener by adapting over time**. Every Like, Skip, and Replay creates feedback that can change future recommendations. The listener influences the agent, and the agent responds through the next recommendation cycle.

In other words, the listener and Resonance continually **resonate with each other**.

---

## 15. Related Documentation

- [`README.md`](README.md) — project overview, setup, architecture, usage, testing, and reproducible execution evidence
- [`ai_interactions.md`](ai_interactions.md) — AI-assisted development interactions and reasoning traces
- [`changelog.md`](changelog.md) — development history
- [`diagrams/resonance_v2_architecture.mmd`](diagrams/resonance_v2_architecture.mmd) — final Mermaid architecture source
- [`docs/model_card_v1.md`](docs/model_card_v1.md) — archived Resonance v1.0 model card
- [`docs/README_v1.md`](docs/README_v1.md) — archived Resonance v1.0 README

← [Back to Resonance](README.md)