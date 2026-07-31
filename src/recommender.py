import csv
import logging
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    release_decade: int
    mood_tag_primary: str
    mood_tag_secondary: str
    billboard_peak_at_release: Optional[int]
    billboard_peak_overall: Optional[int]

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_tempo: float
    target_valence: float
    target_danceability: float
    likes_acoustic: bool
    target_decade: int
    target_mood_tag: str
    prefers_mainstream_hits: bool

def _user_profile_to_prefs(user: UserProfile) -> Dict:
    """
    Maps UserProfile's target_-prefixed field names to the keys score_song()
    expects, which mirror the Song field names instead (see ai_interactions.md
    for why this convention was chosen: tempo_bpm/valence/danceability/etc.,
    not target_tempo/target_valence/...).
    """
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "tempo_bpm": user.target_tempo,
        "valence": user.target_valence,
        "danceability": user.target_danceability,
        "likes_acoustic": user.likes_acoustic,
        "release_decade": user.target_decade,
        "mood_tag": user.target_mood_tag,
        "prefers_mainstream_hits": user.prefers_mainstream_hits,
    }


class Recommender:
    """
    Dataclass-friendly wrapper around the score_song/recommend_songs engine.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = _user_profile_to_prefs(user)
        song_dicts = [asdict(song) for song in self.songs]
        ranked = recommend_songs(user_prefs, song_dicts, k=k)
        songs_by_id = {song.id: song for song in self.songs}
        return [songs_by_id[song_dict["id"]] for song_dict, _score, _explanation in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = _user_profile_to_prefs(user)
        _score, reasons = score_song(user_prefs, asdict(song))
        return ", ".join(reasons) if reasons else "No matching attributes for this song."

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv into a list of dicts, converting numeric fields to float/int."""
    logger.debug("Loading songs from %s...", csv_path)
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "release_decade": int(row["release_decade"].rstrip("s")),
                "mood_tag_primary": row["mood_tag_primary"],
                "mood_tag_secondary": row["mood_tag_secondary"],
                "billboard_peak_at_release": int(row["billboard_peak_at_release"]) if row["billboard_peak_at_release"] else None,
                "billboard_peak_overall": int(row["billboard_peak_overall"]) if row["billboard_peak_overall"] else None,
            })
    logger.info("Loaded %d songs from %s", len(songs), csv_path)
    return songs

def normalize_tempo(tempo_bpm: float, min_bpm: float = 40.0, max_bpm: float = 200.0) -> float:
    """Scales tempo_bpm to a 0-1 range so it's comparable to the other 0-1 features."""
    normalized = (tempo_bpm - min_bpm) / (max_bpm - min_bpm)
    return max(0.0, min(1.0, normalized))

def closeness_score(value: float, target: float, max_diff: float) -> float:
    """Rewards values close to a target rather than simply higher/lower ones."""
    diff = abs(value - target)
    return max(0.0, 1 - (diff / max_diff))

def song_popularity(billboard_peak_overall: Optional[int]) -> float:
    """Converts a Billboard peak position into a 0-1 popularity score; non-charting songs score 0.0."""
    if billboard_peak_overall is None:
        return 0.0
    return max(0.0, min(1.0, 1 - (billboard_peak_overall - 1) / 99))

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user_prefs using the finalized Algorithm Recipe, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if user_prefs.get("genre") == song["genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if user_prefs.get("mood") == song["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    if "tempo_bpm" in user_prefs:
        tempo_points = closeness_score(
            normalize_tempo(song["tempo_bpm"]),
            normalize_tempo(user_prefs["tempo_bpm"]),
            max_diff=1.0,
        ) * 1.0
        score += tempo_points
        reasons.append(f"tempo closeness (+{tempo_points:.2f})")

    if "valence" in user_prefs:
        valence_points = closeness_score(song["valence"], user_prefs["valence"], max_diff=1.0) * 0.5
        score += valence_points
        reasons.append(f"valence closeness (+{valence_points:.2f})")

    if "danceability" in user_prefs:
        dance_points = closeness_score(song["danceability"], user_prefs["danceability"], max_diff=1.0) * 0.5
        score += dance_points
        reasons.append(f"danceability closeness (+{dance_points:.2f})")

    if "likes_acoustic" in user_prefs:
        song_is_acoustic = song["acousticness"] > 0.5
        if user_prefs["likes_acoustic"] == song_is_acoustic:
            score += 0.5
            reasons.append("acoustic alignment (+0.5)")

    if "release_decade" in user_prefs:
        decade_points = closeness_score(song["release_decade"], user_prefs["release_decade"], max_diff=60) * 0.5
        score += decade_points
        reasons.append(f"decade closeness (+{decade_points:.2f})")

    if "mood_tag" in user_prefs:
        target_tag = user_prefs["mood_tag"]
        if target_tag in (song["mood_tag_primary"], song["mood_tag_secondary"]):
            score += 0.5
            reasons.append("mood tag match (+0.5)")

    if "prefers_mainstream_hits" in user_prefs:
        song_is_mainstream = song_popularity(song["billboard_peak_overall"]) > 0.5
        if user_prefs["prefers_mainstream_hits"] == song_is_mainstream:
            score += 0.5
            reasons.append("popularity alignment (+0.5)")

    return score, reasons

DIVERSITY_ARTIST_PENALTY = 1.0

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song against user_prefs and greedily picks the top k, applying a
    diversity penalty (Challenge 3) to any song whose artist is already in the
    results, so one artist can't dominate the list unless clearly better than the rest.
    """
    remaining = [(song, *score_song(user_prefs, song)) for song in songs]
    selected = []
    seen_artists = set()

    while remaining and len(selected) < k:
        def effective_score(entry):
            song, score, _ = entry
            penalty = DIVERSITY_ARTIST_PENALTY if song["artist"] in seen_artists else 0.0
            return score - penalty

        remaining.sort(key=effective_score, reverse=True)
        song, score, reasons = remaining.pop(0)

        if song["artist"] in seen_artists:
            score -= DIVERSITY_ARTIST_PENALTY
            reasons = reasons + [f"diversity penalty (-{DIVERSITY_ARTIST_PENALTY:.1f}, {song['artist']} already in results)"]

        selected.append((song, score, reasons))
        seen_artists.add(song["artist"])

    return [(song, score, ", ".join(reasons)) for song, score, reasons in selected]
