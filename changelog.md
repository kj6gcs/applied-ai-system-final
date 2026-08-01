# Change Log

[README](README.md) •
[Model Card](model_card.md) •
[AI Interactions](ai_interactions.md) •
[Changelog](changelog.md) •
[Architecture](diagrams/resonance_v2_architecture.mmd) •
[License](LICENSE)

---

## Resonance v2.0

### Applied AI Final Project

> Resonance v2.0 evolves the original deterministic music recommender into a stateful, adaptive recommendation agent that learns from listener feedback while preserving the transparent scoring engine developed in v1.0.

## [2.0.0-beta.1] - 2026-08-01

### Added

- Added a complete Resonance v2.0 `README.md` covering project purpose, the v1.0 foundation, architecture, setup, listener workflow, recommendation logic, adaptive behavior, reliability, responsible-AI considerations, and portfolio context.
- Added a dedicated Resonance v2.0 `model_card.md` covering intended use, limitations and biases, misuse and safeguards, reliability findings, and human-AI collaboration.
- Rebuilt `ai_interactions.md` as a v2.0 development log documenting representative ChatGPT and Claude Code collaboration, architectural decisions, agentic development traces, verification milestones, and AI suggestions that were accepted, modified, rejected, or deferred.
- Added an MIT `LICENSE`.
- Added consistent navigation among the README, model card, AI interaction log, changelog, architecture source, and license.
- Added documentation badges/links near the top of the README.
- Preserved original Resonance v1.0 documentation under `docs/`, including historical README, model-card, and AI-interaction artifacts.

### Changed

- Reworked root-level documentation to describe Resonance v2.0 while preserving Module 1–3 materials as historical references.
- Expanded documentation of bounded preference drift, listener feedback, explainability, testing, guardrails, and human review of AI-assisted development.
- Documented the decision to defer persistent user accounts/database storage and a live external music API beyond the current course-project scope.

### Verified

- Current implementation milestone remains **54 automated tests passing**.
- No recommendation-engine, agent, song-selection, or Streamlit behavior was intentionally changed during this documentation milestone.
- Final `2.0.0` release remains pending completion of the v2 architecture diagram, reproducible execution evidence, final test run, and rubric audit.

---

## [2.0.0-alpha.5] - 2026-07-31

### Added

- Introduced a two-stage Streamlit interface consisting of listener profile setup and a continuous listening session.
- Added quick-start listening presets alongside a fully customizable profile builder.
- Added `src/song_selection.py` for weighted candidate selection while preserving the existing recommendation engine.
- Added repeat avoidance using a rolling history of recently recommended songs.
- Added listener-friendly recommendation explanations with technical scoring details available through an expandable panel.
- Added real-time recommendation-cycle tracking and preference-drift notifications.
- Added `tests/test_song_selection.py` and `tests/test_app.py`.

### Changed

- Redesigned the application from an engineering-oriented demonstration into an interactive music recommendation experience.
- Recommendations are now presented one song at a time.
- Like, Skip, and Replay feedback advances the listening session while allowing the `ResonanceAgent` to refine the active profile in recommendation cycles.
- Moved raw profile data, technical history, and diagnostics into an **Advanced AI Details** panel.
- Added weighted random selection among highly ranked candidates so strong matches remain favored without always showing the same top result.
- Kept scoring and ranking inside the validated recommendation engine; the selection layer only chooses among already-ranked candidates.

### Verified

- All **54 automated tests** pass successfully.
- Streamlit was verified through automated `AppTest` coverage and manual execution.
- Feedback applies to the active song and advances the listening session.
- Three feedback events trigger the next recommendation cycle under the default configuration.
- Existing CLI and deterministic recommendation-engine behavior remain unchanged.

---

## [2.0.0-alpha.4] - 2026-07-31

### Added

- Added the first Streamlit graphical interface for Resonance v2.0.
- Added displays for the current profile, recommendations, scores, explanations, recommendation cycles, preference drift, quality information, and agent history.
- Added Like, Skip, and Replay controls connected directly to the `ResonanceAgent`.
- Added `Recommender.score()` so the UI could display scores through the existing scoring engine.
- Added two focused recommender tests for the new score accessor.

### Changed

- Added Streamlit as a second application entry point while preserving the CLI.
- Kept the UI as a composition/presentation layer rather than duplicating recommendation or adaptation logic.
- Added defensive project-path handling after Streamlit `AppTest` exposed an import-context issue.

### Verified

- All **40 automated tests** pass successfully.
- Streamlit behavior was verified with `AppTest` and a real server smoke test returning HTTP 200.
- Existing CLI output remained unchanged.
- Manual review found that this first interface behaved more like an engineering dashboard than the intended listener-facing recommender, directly motivating `2.0.0-alpha.5`.

---

## [2.0.0-alpha.3] - 2026-07-31

### Added

- Added `AgentConfig` with configurable preference-drift parameters:
  - `min_feedback_for_drift`
  - `categorical_shift_threshold`
  - `max_tempo_step`
  - `max_valence_step`
  - `max_danceability_step`
  - `max_decade_step`
- Added four focused tests confirming that defaults preserve prior behavior and custom thresholds/step sizes measurably change adaptation behavior.

### Changed

- `ResonanceAgent` now accepts an optional `config: AgentConfig` constructor parameter.
- Replaced hard-coded adaptation thresholds with configuration values while preserving identical defaults.

### Verified

- All **38 automated tests** pass successfully.
- Recommendation-engine behavior and CLI output remain unchanged.
- The public agent interface remains `observe_feedback()`, `run_cycle()`, `get_profile()`, and `get_history()`.

---

## [2.0.0-alpha.2] - 2026-07-31

### Added

- Added the initial **ResonanceAgent**, responsible for observing listener feedback, detecting preference drift, updating listener profiles, and orchestrating the existing recommendation engine.
- Added Like, Skip, and Replay feedback events.
- Added bounded, evidence-based preference drift.
- Added recommendation-cycle history containing profile snapshots, feedback, recommendations, explanations, and quality warnings.
- Added a second explainability layer describing **why recommendations changed** between cycles.
- Added quality checks for empty recommendation lists, repeated artists, and excessive genre dominance.
- Added `tests/test_agent.py` covering feedback validation, preference drift, recommendation delegation, history, explainability, defensive-copy behavior, deterministic cycles, and quality checks.

### Changed

- Expanded Resonance from a static recommender into a stateful, adaptive **agentic AI system**.
- Introduced the public agent interface:
  - `observe_feedback()`
  - `run_cycle()`
  - `get_profile()`
  - `get_history()`
- Preserved the deterministic recommendation engine as a validated service used by the agent rather than replacing its scoring algorithm.

### Verified

- All **34 automated tests** pass successfully.
- Existing CLI behavior remains compatible with Resonance v1.0.
- Existing recommendation scores, rankings, explanations, diversity behavior, and catalog remain unchanged.

---

## [2.0.0-alpha.1] - 2026-07-31

### Added

- Forked Resonance v1.0 into a dedicated final-project repository to preserve the original implementation while enabling v2.0 development.
- Added a dedicated `diagrams/` directory for Mermaid architecture sources.
- Preserved the original architecture diagram as historical v1.0 documentation.
- Added structured logging through `src/logging_config.py`.
- Expanded the test suite from 2 tests to **19 meaningful recommendation-engine tests**, including regression tests based on documented v1.0 outputs.

### Changed

- Corrected project dependency/configuration issues discovered during setup.
- Improved virtual-environment exclusions in `.gitignore`.
- Refactored the recommendation engine to eliminate disconnected real/stub behavior while preserving the validated scoring algorithm.
- Unified the object-oriented `Recommender` API with the real functional recommendation logic.
- Replaced diagnostic `print()` calls with structured logging.
- Reworked tests so they exercise the recommendation logic actually used by the application.
- Began redesigning Resonance around an agentic workflow rather than a static recommendation engine.

### Verified

- Existing recommendation scores, rankings, and explanations remain unchanged.
- CLI behavior remains compatible with Resonance v1.0.
- All **19 automated tests** pass successfully.

### Planned at This Milestone

- Implement the behavioral recommendation agent.
- Add bounded preference drift and cycle history.
- Add explainability and recommendation-quality checks.
- Develop the Streamlit interface.
- Expand final-project testing and documentation.

---

## Resonance v1.0

### Original starter project

### Substantial Changes to Starter Code

## 07-09-2026

- Removed the "energy" feature entirely. It didn't really make sense as something a song permanently _has_ — it's more about how the listener feels in the moment than a fixed trait of the song. Tempo took its place as the main "intensity" signal instead. Updated the data file, the code, and the tests to match.
  - Left `README.md` and `model_card.md`'s original wording alone on purpose, to keep the assignment's original grading text intact.

## 07-14-2026

- Wrote up how the recommender actually works in the README: explained the difference between content-based recommendations (what this project does) and the "other users liked this too" style (which it doesn't do), and settled on the final scoring weights — a genre match is worth more than a mood match, and tempo is scored by how _close_ it is to what the listener wants, not just "faster is better." Also listed out exactly what info each song and each listener profile keeps track of.

---

- Added a missing piece to the listener profile — a target tempo — so the scoring math actually had something to compare a song's tempo against.
- Grew the song catalog from 10 to 50 songs, adding real, recognizable songs across a much wider mix of genres and moods (rock, country, funk, disco, hip hop, and more), with artists like AC/DC, Dolly Parton, Queen, and Beyoncé.
  - The exact tempo/mood/etc. numbers for these real songs are reasonable estimates, not pulled from an actual music database.

---

- Added two more preferences to the listener profile (target valence and target danceability) so those song attributes actually get used in scoring instead of just sitting there unused.
- Created two example listener personas — an "Intense Rock" fan and a "Chill Lofi" fan — to test the recommender against later, matching the format the rest of the code already expected listener data to look like.

---

- Finalized the actual point system the recommender uses (which factors matter most, and by how much) and wrote it down in the README, along with a note about a bias we expected going in.
- Added a simple flowchart sketching how a request flows through the system, from a listener's preferences all the way to a final list of song suggestions.

---

- Found and fixed a bug where running the app the documented way would crash with an import error — a leftover from early scaffolding.
- Wrote the actual code that reads the song catalog file into the program and gets the numbers into a usable format, and confirmed it correctly loads all 50 songs.

---

- Wrote the core scoring logic — the piece that takes one song and one listener's preferences and turns them into a single score, plus a plain-English explanation of why it scored that way.
  - Added a couple of small helper pieces so "how close is this to what you want" can be measured consistently across different song attributes.
  - Tested it by hand on a few songs to make sure the math behaved as expected.

---

- Wrote the code that scores every song in the catalog and picks out the best matches, sorted from highest score to lowest.
  - Confirmed it works by running it against a sample listener profile and checking that the top result made sense.

---

- Cleaned up how results print to the terminal — added numbering, the artist's name, and showed the listener profile being tested at the top.
  - Fixed a small display glitch with a special character that wasn't showing up right on Windows.
  - Pasted a real example of the output into the README so a reader can see what it actually looks like.

---

- Shortened the code documentation on a few functions down to one clear line each, and double-checked the app and tests still worked fine afterward.

---

- Set up several test listener profiles to see how the recommender handles different kinds of requests — including a couple of intentionally weird ones designed to try to trip it up (like asking for "peaceful metal," which doesn't really make sense).
  - Ran all of them and added the real results to the README.
  - Notable finding: even with a contradictory request, the recommender still confidently suggested an aggressive song, because matching the genre outweighed everything else that didn't fit.

---

- Added a profile based on my own actual music taste (rather than a made-up example) to sanity-check the recommender against real opinions, not just theory.
  - Compared it to a similar generic profile and found that one small tweak (lowering the target tempo) actually flipped which song came out on top.
  - Noticed one recommended song wasn't really something I'd normally pick, even though the math behind it was reasonable.
  - Wrote up a summary of everything tested so far in the model card.

---

- Ran two experiments to see how sensitive the recommender is to its own settings (both were undone afterward — this was just to see what would happen):
  - **Weight shift:** made genre matter less and tempo matter more. That alone was enough to knock some good genre-matched songs out of the results entirely.
  - **Turning off mood-matching:** a song I don't even like ended up jumping to the top, just because of its tempo and other numbers, once mood no longer counted.
  - Wrote up both experiments in the README.

---

- Finished writing every section of the model card — gave the project a name ("Resonance"), explained who it's meant for (this is a classroom project, not something built for real users) and what assumptions it makes about a listener, explained the scoring approach in plain terms, described the data, listed where it works well, and wrote a personal reflection on what I learned and how AI helped along the way.

---

- Optional stretch goal — richer song data: grew the catalog from 50 to 60 songs (adding 10 more real ones, filling in genres that were only represented by made-up songs before), and gave every song 5 new pieces of information: what decade it came from, two more detailed "feeling" tags beyond just one mood word, and how well it charted on Billboard (both when it came out and overall).
  - Updated the scoring so all of that new information actually counts toward a song's score, instead of just sitting there unused.
  - Documented how this was built, including a naming mistake that got caught and fixed along the way, in `ai_interactions.md`.

---

- Optional stretch goal — fairer, more varied results: made sure one artist can't hog the whole recommendation list. Now, once a song by a given artist has already been picked, any other song by that same artist gets a small penalty before the next pick is chosen — so a really strong match can still win, but it has to actually earn it.
  - Tested this and confirmed it now spreads recommendations across more artists than before.

---

- Optional stretch goal — easier-to-read output: instead of printing each recommendation as a few lines of plain text, results now show up in a clean, aligned table with columns for rank, title, artist, score, and the reasons behind the score.
  - Re-ran everything and updated the README to show both the old-style output and the new table side by side, so it's easy to see the improvement.

← [Back to Resonance](README.md)
