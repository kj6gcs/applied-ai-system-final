# Change Log

## Resonance v2.0

### Applied AI Final Project

## [2.0.1-dev] - In Development

### Changed

- Refactored the recommendation engine to eliminate duplicate implementations while preserving the validated scoring algorithm.
- Unified the object-oriented API with the existing recommendation logic, creating a single recommendation engine used throughout the application.
- Replaced diagnostic `print()` statements with structured logging to improve maintainability and debugging.
- Expanded the automated test suite from 2 to 19 tests, including regression tests based on documented recommendation outputs.
- Added regression testing to verify recommendation behavior remains consistent during future development.
- Improved project architecture in preparation for adaptive recommendation features planned for Resonance v2.0.

### Verified

- Existing recommendation scores, rankings, and explanations remain unchanged following the Phase 1 refactor.
- Command-line interface behavior remains fully compatible with Resonance v1.0.
- All automated tests pass successfully.

### Next

- Design and implement the Resonance Agent.
- Add adaptive listener behavior (likes, skips, and replay events).
- Introduce recommendation explainability, confidence scoring, and reliability evaluation.
- Develop the Streamlit user interface.

## [2.0.0] - 2026-07-31

### Changed

- Forked Resonance v1.0 into a dedicated final-project repository to preserve the original implementation while enabling iterative development.
- Reorganized project assets to align with AI-110 final project requirements, including a dedicated `diagrams/` directory for Mermaid architecture diagrams.
- Updated project configuration and dependencies, including correcting package requirements and improving virtual environment exclusions in `.gitignore`.
- Began redesigning Resonance as an adaptive AI system centered around an agentic workflow rather than a static recommendation engine.

### Planned

- Implement a behavioral recommendation agent that adapts user preferences based on simulated listening behavior (likes, skips, and replays).
- Introduce recommendation diversity reranking to reduce artist and genre repetition.
- Add explainable recommendation reasoning, confidence scoring, logging, guardrails, and automated evaluation.
- Expand documentation, architecture diagrams, and model card to reflect the redesigned system.

### Added

- Adaptive listener-feedback agent
- Like, skip, and replay behavior tracking
- Preference-profile updates
- Recommendation reliability evaluation
- Expanded diversity reranking
- Streamlit user interface
- Structured logging and guardrails

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
