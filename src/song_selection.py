"""
Session-level song selection for the continuous listening UI.

This module does not score or rank songs -- it only decides which song, from
an already-ranked candidate list produced by Recommender.recommend(), to show
next. Scoring, ranking, and diversity behavior all remain entirely inside the
validated recommendation engine.
"""
import random
from typing import List, Optional, Sequence

from src.recommender import Song


def choose_next_song(
    ranked_songs: List[Song],
    recent_song_ids: Sequence[int] = (),
    pool_size: int = 5,
    rng: Optional[random.Random] = None,
) -> Song:
    """
    Picks one song from the top `pool_size` of an already-ranked candidate
    list, using weighted randomness that favors higher-ranked candidates.
    Songs in `recent_song_ids` are excluded when an alternative exists; if
    every ranked song was shown recently, repeats are allowed rather than
    raising, so a small catalog never runs out of choices.
    """
    if not ranked_songs:
        raise ValueError("Cannot choose a song from an empty candidate list")

    rng = rng if rng is not None else random.Random()

    fresh_candidates = [song for song in ranked_songs if song.id not in recent_song_ids]
    candidates = fresh_candidates if fresh_candidates else list(ranked_songs)

    pool = candidates[:pool_size]
    weights = list(range(len(pool), 0, -1))  # rank 0 (best match) gets the highest weight

    return rng.choices(pool, weights=weights, k=1)[0]
