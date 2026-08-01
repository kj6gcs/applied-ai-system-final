# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**Resonance (v1.0)**

## 2. Intended Use

_Resonance_ generates a ranked top-k list of songs from a fixed 50-song catalog, scored against a single taste profile using content-based matching (genre, mood, tempo, valence, danceability, and an acoustic preference) — it doesn't use any other users' behavior, so it can't do the "people who liked this also liked..." style of recommendation.

This is classroom exploration, not a system built for real users. The clearest sign of that is what it assumes about the user: that their entire taste can be reduced to _one_ genre, _one_ mood, and a handful of precise numeric targets, all stated upfront. Real listeners don't work that way — we proved this directly while building a personal profile, when "playful, intense, and epic" couldn't fit into a single mood field, and "acoustic sometimes, but not usually" couldn't fit into a boolean. A real system would also need to _infer_ those numeric targets from actual behavior (plays, skips, saves) rather than have a user type in "my target danceability is 0.55," which is a much harder problem than anything this simulation solves.

That said, the assumption gap isn't really an architecture problem. `load_songs()`, `score_song()`, and `recommend_songs()` all operate on plain dictionaries, so nothing structurally prevents swapping the static CSV for a real catalog or a live music API (Spotify's audio-features endpoint returns almost this exact shape: tempo, valence, danceability). Doing that would fix the _scale_ problem, but not the _profile_ problem — building an accurate `target_tempo`/`target_valence` for a real person still requires solving the harder, unaddressed piece: turning real behavior into a taste profile in the first place.

## 3. How the Model Works

**What features of each song are used?**
Every song has a genre (like rock or pop), a mood (like happy or intense), a tempo (how fast or slow it is), a valence (how happy or sad it sounds), a danceability (how easy it is to move to), and an acousticness (how "unplugged" it sounds versus produced/electronic).

**What user preferences are considered?**
A person's taste is written down the same way: their favorite genre, their favorite mood, a preferred tempo, a preferred valence, a preferred danceability, and whether they generally like acoustic-sounding songs or not.

**How does the model turn those into a score?**
Think of it like a checklist that hands out points. If a song's genre matches what you asked for, it gets a big chunk of points. If the mood matches too, it gets a smaller chunk on top of that. Then, instead of just checking yes/no on tempo, valence, and danceability, it gives partial credit based on _how close_ the song is to what you wanted — a song doesn't have to be a perfect match to earn some points, but the closer it is, the more it earns. Finally, there's a small bonus if the song's "acoustic-ness" lines up with whether you said you like acoustic songs. All those points get added up into one final score, every song in the catalog gets scored this way, and the songs are then lined up from highest score to lowest — the top 5 are what gets recommended.

**What changed from the starter logic?**
The starter version used a feature called "energy," but that got removed early on, since "how energetic a song feels" seemed more like something that depends on the listener's own mood in the moment, not something that belongs to the song itself. Tempo took its place as the more consistent, song-owned stand-in for that same "how intense does this feel" idea. Two more features, valence and danceability, were also added to give the scoring more to work with, and — importantly — all three of those numeric features (tempo, valence, danceability) use the "how close is it" partial-credit approach instead of a strict match/no-match check, since real taste isn't usually all-or-nothing.

## 4. Data

**How many songs are in the catalog?**
50 songs.

**What genres or moods are represented?**
19 different genres — pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, novelty, country, funk, disco, grunge, r&b, reggae, edm, metal, punk, folk, and classical — and a wide range of moods (happy, chill, intense, relaxed, moody, focused, playful, passionate, somber, anxious, upbeat, rowdy, confident, romantic, heartbroken, carefree, vengeful, soulful, epic, euphoric, angsty, determined, hopeful, peaceful, dark, aggressive, rebellious, reflective, melancholic, wistful, flirty, elegant, dramatic, and more).

**Did you add or remove data?**
Started from a 10-song starter catalog and added 40 more songs, including real, recognizable artists (AC/DC, Weird Al, Johnny Cash, Dolly Parton, Queen, Michael Jackson, Metallica, Bob Marley, Mozart, and many others) to make the results feel more real and relatable. On the removal side, the "energy" column was dropped from every song entirely, since it seemed more like a listener's in-the-moment feeling than a fixed property a song actually has.

**Are there parts of musical taste missing in the dataset?**
Quite a bit. There's no lyrics or language information, so nothing about what a song is actually _about_. Each song only gets one mood label, even though real songs can shift feeling throughout, or mean different things to different listeners. The genres aren't broken into sub-genres (just "rock," not "classic rock" vs. "arena rock" vs. "punk rock"), so a lot of nuance gets flattened into one word. There's also no release date, era, or production-style information, and no popularity or cultural-context signal at all. Finally, the numeric values (tempo, valence, danceability, acousticness) for the real songs are best-effort estimates, not pulled from an actual audio-analysis tool, so they should be read as reasonable approximations rather than verified facts.

## 5. Strengths

**User types for which it gives reasonable results:**
It works best for someone with a single, clear, consistent vibe — a "Happy Pop" fan, an "Intense Rock" fan, a "Chill Lofi" fan. When genre, mood, and tempo all point in the same direction, the top 5 results come back sensible and coherent. It also worked well once tested against a real personal profile instead of a made-up persona — once the actual genre, mood, and tempo targets were real, the results tracked with actual listening preferences.

**Patterns the scoring captures correctly:**
The "how close is it" scoring (rather than a strict yes/no) correctly rewards near-misses over extremes — a song doesn't need to hit a tempo target exactly to still score well, which matches how real taste actually works. Genre also acts like a strong gate: two profiles that ask for opposite things (say, Happy Pop vs. Chill Lofi) reliably return completely non-overlapping top-5 lists, showing the system isn't accidentally blending unrelated tastes together.

**Cases where the recommendations matched intuition:**
For the Intense Rock persona, the top picks were AC/DC and Voltline tracks — genuinely fitting the "amp you up" feeling that mood/genre combo is going for. On a real personal profile, lowering the tempo target to 115 BPM correctly bumped "Back In Black" to the #1 spot, which lined up with an actual personal reaction about that song's more consistent, steady feel compared to a faster track like "Thunderstruck."

## 6. Limitations and Bias

The catalog is heavily imbalanced by genre: country makes up 22% of the 50 songs (11 tracks), while nine genres — r&b, funk, disco, grunge, jazz, ambient, synthwave, indie pop, and punk — have exactly one song each. Because genre match is worth the most points (+2.0) in the scoring recipe, a user whose favorite genre falls into one of those single-song genres is effectively locked into the same one recommendation every time, no matter how their mood, tempo, or other preferences vary, while a country fan gets 11 different candidates to choose from. This is a real filter bubble, but it comes from the underlying data rather than the scoring logic itself — the recommender can only ever be as diverse as the catalog it's given, and this catalog was hand-curated rather than sampled to represent genres evenly. It's made worse by the fact that mood is an exact string match: even within a genre, a song tagged "aggressive" gets zero credit against a "peaceful" or "intense" preference, so a thin genre with only one mood label offers no flexibility at all.

---

## 7. Evaluation

We tested six profiles: three intuitive "vibe" profiles (Happy Pop, Intense Rock, Chill Lofi), two adversarial profiles built to contain contradictory preferences (a "metal + peaceful + fast + acoustic-loving" profile, and a "classical + euphoric" profile pairing a real genre with a mood that doesn't exist anywhere in that genre in our catalog), and one personal profile built from my own actual stated taste (rock, intense, 115 BPM, moderate valence/danceability, non-acoustic). For each one, we looked at whether the top 5 results matched what the profile was clearly asking for, and whether the point breakdown ("Because: ...") made sense as a plain-language explanation. The biggest surprise was how the adversarial profiles exposed a real weakness: the "peaceful metal" profile still recommended an aggressive Black Sabbath song as its #1 pick, since the genre match (+2.0) alone was enough to outweigh a completely contradicted mood, tempo, and vibe — the system never noticed the preferences didn't make sense together. We also ran a direct side-by-side comparison between the generic Intense Rock profile and my personal profile: lowering the target tempo from 140 to 115 BPM flipped the #1 recommendation from "Thunderstruck" to "Back In Black," driven almost entirely by a tiny valence/danceability match rather than anything resembling "musical taste." On my own profile specifically, "Dreams" by Fleetwood Mac ranked in the top 5 despite having no mood match at all and not being a song I would normally choose — a good example of the system producing a technically defensible but not truly desired recommendation.

**Comparing pairs of profiles, in plain language:**

- **Happy Pop vs. Intense Rock:** these two ask for opposite things (upbeat pop at 120 BPM vs. gritty rock at 140 BPM), and their top-5 lists share zero songs. That makes sense — the genre match alone is usually enough to keep pop and rock from ever mixing, before mood or tempo even get a chance to weigh in.
- **Chill Lofi vs. Intense Rock:** these sit at opposite ends of the tempo range (75 BPM vs. 140 BPM) and opposite moods (chill vs. intense), and again share no songs in their results. This shows tempo closeness is correctly telling "laid-back" apart from "amped-up," not just riding on genre.
- **Intense Rock vs. my own profile:** same genre (rock) and mood (intense), but a different tempo target (140 vs. 115 BPM). This was our cleanest side-by-side test — changing one number (tempo) was enough to flip the #1 song from "Thunderstruck" to "Back In Black," even though every other part of the scoring stayed identical.
- **Conflicting vs. No-genre-mood-match (the two adversarial profiles):** both are designed to confuse the system, but they break it differently. The "Conflicting" profile still has a genre that exists in the catalog (metal), so genre match alone crowns a winner ("Paranoid") even with everything else contradicted. The "No-genre-mood-match" profile pairs a real genre (classical) with a mood no classical song has, so it comes down to a near-tie between a genre match (Mozart) and songs with only a mood match — showing the system gets shakier once genre alone can't settle it.
- **Happy Pop vs. Chill Lofi:** these two are about as far apart as two profiles can be — opposite valence/danceability targets (0.8/0.8 vs. 0.58/0.6), opposite tempo (120 vs. 75 BPM), and opposite acoustic preference (electric vs. acoustic-loving). Their top-5 lists share zero songs, which is exactly what should happen when nearly every dial is turned in the opposite direction.
- **Happy Pop vs. my own profile:** these have genuinely different genre and mood (pop/happy vs. rock/intense), but a nearly identical tempo target (120 vs. 115 BPM). Even with tempo almost matching, their top-5 lists still share zero songs — a good demonstration that genre match is doing the heavy lifting to keep the two lists separate, not tempo.
- **A simple, real example — "Gym Hero" showing up for "Happy Pop":** "Gym Hero" is actually tagged mood "intense," not "happy," so in plain terms: the system saw "this is an upbeat pop song" and let that outweigh the fact that it isn't really a _happy_ song. It's not wrong, exactly, but it's a good example of the system settling for "close enough" rather than a true match.

## 8. Future Work

**Additional features or preferences:**
Expand the catalog to include international and foreign-language genres, which would also help fix the genre-imbalance bias described in Section 6. Also connect to a real music API instead of a static CSV, both to grow the catalog far beyond 50 songs and to pull in genres and moods the hand-curated version doesn't cover. Add a UI option to view a song's lyrics — just for the listener to read, not something the scoring itself would use.

**Better ways to explain recommendations:**
Build a real graphical interface (web and/or app) instead of a CLI-only tool, so the score breakdown and explanations are easier to read and explore than scrolling through terminal text.

**Improving diversity among the top results:**
Add a diversity penalty: a rule that reduces a song's score if its artist (or genre) already appears earlier in that user's top results, so the list doesn't end up dominated by 3 songs from the same artist. This would directly soften the filter-bubble problem described in Section 6, even without growing the catalog.

**Handling more complex user tastes:**
Add a narrow agent that tracks real listening behavior — skips, likes, and repeat listens — instead of relying entirely on a person typing in exact numeric targets upfront. If a song gets replayed constantly, that's a much stronger, more honest signal of taste than a self-reported "target_valence: 0.55," and it starts to close the gap described in Section 2, where a real system needs to _infer_ preferences from behavior rather than assume someone can state them precisely.

## 9. Personal Reflection

The thing that really clicked for me, and changed how I think about recommendation systems in general, was closeness scoring. Before this project, I assumed a recommendation score just worked like a 1-to-100 scale — higher number, better match, simple as that. Building this out taught me that's not really how it works: the better approach is scoring how _close_ a song is to what the user actually asked for, not just rewarding the highest raw value. A song that's a little slower or a little faster than your target tempo should still score well if it's close, instead of only the fastest or most extreme song winning by default.

The other thing I learned, which also genuinely surprised me, is how much a recommender's quality depends on the size and variety of its dataset, not just the cleverness of its scoring logic. I hand-picked this catalog myself, and even with 50 songs across 19 genres, we still found real gaps — genres with only one song, moods that don't exist within a given genre, adversarial profiles the system couldn't reason its way out of. A user-curated, narrow dataset like this one just can't offer the same range a real, wide dataset would.

That combination changed how I think about apps like Spotify. It's not just that they have a "smarter" algorithm — it's that they're running closeness-style scoring against a massive, constantly growing dataset, which is what actually makes personalization feel accurate. A great scoring formula on a small dataset still hits a ceiling pretty fast.

As for how AI helped: the biggest value wasn't writing code for me, it was explaining _why_ something did or didn't work, and helping me decide when I was genuinely on the fence — like weighing genre against tempo when we were figuring out the scoring weights. Having something to talk a decision through with, rather than just guessing, made the design choices feel a lot more deliberate. If I were to extend this project further, the first thing I'd want is a larger dataset — one that isn't user-defined or hand-picked, so the catalog itself isn't the bottleneck on how good the recommendations can get.
