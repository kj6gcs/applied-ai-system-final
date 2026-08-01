# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Optional Challenge 1 (Add Advanced Song Features): introduce 5+ complex attributes not in the baseline data, update `data/songs.csv` and the scoring logic in `src/recommender.py` to account for them, and expand the catalog with 10 more real songs first so the new attributes had a solid base of real chart/release data to work with.

**Prompts used:**

- "let's go with eras based upon the decade the song was released in... detailed mood tags... popularity based upon the official billboard rankings both at the time of their release and overall"
- "Let's keep those original ten [fictional songs] in that case and mark them as non charting... Let's add ten more to give us a solid fifty real charting songs to compare against. Feel free to add in some real lo fi indie pop and synthwave in those new ten."
- "Looks good to me. Go ahead and implement it." (approving the proposed scoring design: decade closeness up to +0.5, mood tag OR-match +0.5, popularity alignment +0.5)

**What did the agent generate or change?**

- `data/songs.csv`: added 10 new real songs (Nujabes, MGMT, Kavinsky, Dave Brubeck Quartet, Brian Eno, Luis Fonsi ft. Daddy Yankee, B.B. King, Red Hot Chili Peppers, Pearl Jam, BTS) bringing the catalog to 60 songs, then added 5 new columns to all 60 rows: `release_decade`, `mood_tag_primary`, `mood_tag_secondary`, `billboard_peak_at_release`, `billboard_peak_overall` (blank for the 10 original non-charting fictional songs).
- `src/recommender.py`: added the 5 new fields to the `Song` dataclass and 3 new fields (`target_decade`, `target_mood_tag`, `prefers_mainstream_hits`) to `UserProfile`; updated `load_songs()` to parse the new columns (including converting blank Billboard values to `None`); added a `song_popularity()` helper that converts a Billboard peak into a 0-1 score; added three new scoring components to `score_song()` (decade closeness, mood tag match, popularity alignment), raising the max possible score from 5.5 to 7.0.
- `tests/test_recommender.py`: updated both fixtures with the new required fields.
- `README.md`: updated the `Song`/`UserProfile` feature lists and the Algorithm Recipe table with the 3 new rows.

**What did you verify or fix manually?**

- Ran `pytest` (2 passed) and `python -m src.main` after the dataclass changes to confirm nothing broke, since adding required fields to `Song`/`UserProfile` risks breaking every existing constructor call.
- Caught and fixed a naming inconsistency: the agent initially used `target_decade`/`target_mood_tag` as the functional dict keys inside `score_song()`, which didn't match the established convention (the functional `user_prefs` dict uses the _Song field name_ — `tempo_bpm`, `valence`, `danceability` — not the `UserProfile`'s `target_`-prefixed names). Corrected to `release_decade`/`mood_tag` before moving on.
- Manually spot-checked the new scoring math with an ad hoc script (scoring "Back In Black," "Thunderstruck," "Alive," and "Blitzkrieg Bop" against a rock/intense/1980s/resilience/mainstream profile) to confirm decade closeness, the mood-tag OR-match, and the popularity alignment bonus all fired correctly before trusting the feature.

## Diversity and Fairness Logic (Challenge 3)

> Not tied to a specific stretch-feature code in this template, but documented here anyway since it's a meaningful agentic change to the ranking logic.

**What task did you give the agent?**

Optional Challenge 3 (Diversity and Fairness Logic): implement a "Diversity Penalty" that prevents the recommender from suggesting too many songs from the same artist in the top results, by penalizing a song's score if its artist is already present in the results being built.

**Prompts used:**

- "Let's go into challenge three, the diversity in fairness logic. We decided that would be a good extended option... but see if we can go ahead and implement it."

**What did the agent generate or change?**

- `src/recommender.py`: rewrote `recommend_songs()` from a single `sorted()` call into a greedy loop — after each pick, any remaining candidate whose artist is already in the selected results gets a flat `DIVERSITY_ARTIST_PENALTY` (-1.0) applied before the next pick is chosen. When a penalized song is still selected, its returned score reflects the penalty and its reasons list gets an extra `"diversity penalty (-1.0, <artist> already in results)"` entry, so the explanation stays honest about why it ranked where it did.
- `README.md`: updated the "How songs are chosen" bullet to describe the greedy, penalty-based ranking instead of a single sort.

**What did you verify or fix manually?**

- Ran `pytest` (2 passed) to confirm the existing OOP-path tests were unaffected, since this change only touched the functional `recommend_songs()` path.
- Manually re-ran the "Intense Rock" profile before and after the change: the top 5 previously included 3 AC/DC songs (Thunderstruck, Back In Black, Big Balls); after the penalty, it dropped to 2, with Queen's "Don't Stop Me Now" taking the 5th spot instead — confirmed the penalty was doing real work, not just adding an unused code path.
- Decided the penalty should apply per-artist only (not genre), since the challenge's own wording ("penalize a song's score if its artist is already present") only asked for artist-level diversity, and adding a genre penalty too would have been scope creep beyond what was requested.

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
