"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from tabulate import tabulate

from src.logging_config import configure_logging
from src.recommender import load_songs, recommend_songs

# Candidate personas from the Phase 2 design step (see README.md), saved here
# for later stress-testing against the recommender.
HAPPY_POP_PROFILE = {
    "genre": "pop",
    "mood": "happy",
    "tempo_bpm": 120,
    "valence": 0.80,
    "danceability": 0.80,
    "likes_acoustic": False,
}

INTENSE_ROCK_PROFILE = {
    "genre": "rock",
    "mood": "intense",
    "tempo_bpm": 140,
    "valence": 0.50,
    "danceability": 0.55,
    "likes_acoustic": False,
}

CHILL_LOFI_PROFILE = {
    "genre": "lofi",
    "mood": "chill",
    "tempo_bpm": 75,
    "valence": 0.58,
    "danceability": 0.60,
    "likes_acoustic": True,
}

# Adversarial / edge-case profiles (Phase 4 Step 1): designed to see if the
# scoring logic can be "tricked" by internally contradictory preferences.
CONFLICTING_PROFILE = {
    "genre": "metal",
    "mood": "peaceful",
    "tempo_bpm": 170,
    "valence": 0.85,
    "danceability": 0.85,
    "likes_acoustic": True,
}

NO_GENRE_MOOD_MATCH_PROFILE = {
    "genre": "classical",
    "mood": "euphoric",
    "tempo_bpm": 200,
    "valence": 0.95,
    "danceability": 0.95,
    "likes_acoustic": False,
}

# Personal profile, built from the developer's own stated taste (rock, a mix of
# intense/playful/epic, mid-to-fast tempo, not particularly acoustic).
ROBBYS_PROFILE = {
    "genre": "rock",
    "mood": "intense",
    "tempo_bpm": 115,
    "valence": 0.55,
    "danceability": 0.55,
    "likes_acoustic": False,
}

STRESS_TEST_PROFILES = {
    "Happy Pop": HAPPY_POP_PROFILE,
    "Intense Rock": INTENSE_ROCK_PROFILE,
    "Chill Lofi": CHILL_LOFI_PROFILE,
    "Conflicting (metal + peaceful + fast + acoustic)": CONFLICTING_PROFILE,
    "No genre+mood match (classical + euphoric)": NO_GENRE_MOOD_MATCH_PROFILE,
    "Robby's Profile": ROBBYS_PROFILE,
}


def print_recommendations(profile_name: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print(f"=== {profile_name} ===")
    print(f"User profile: {user_prefs}\n")

    rows = [
        [rank, song["title"], song["artist"], f"{score:.2f}", explanation]
        for rank, (song, score, explanation) in enumerate(recommendations, start=1)
    ]
    print(tabulate(
        rows,
        headers=["Rank", "Title", "Artist", "Score", "Reasons"],
        tablefmt="grid",
        maxcolwidths=[None, 20, 18, None, 50],
        disable_numparse=True,
    ))
    print()


def main() -> None:
    configure_logging()
    songs = load_songs("data/songs.csv")
    print()

    for profile_name, user_prefs in STRESS_TEST_PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()
