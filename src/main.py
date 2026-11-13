"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python -m src.main
    python -m src.main --experiment   # also run the weight-shift experiment
"""

import sys

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:  # allows `python src/main.py` too
    from recommender import load_songs, recommend_songs


PROFILES = {
    # Core profiles
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    # Adversarial / edge-case profiles
    "Conflicted (high energy + sad)": {"genre": "folk", "mood": "sad", "energy": 0.9},
    "Unknown Genre (k-pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.7},
    "Energy Only (no genre/mood)": {"energy": 0.5},
}

# Experiment: double the importance of energy, halve the importance of genre.
WEIGHT_SHIFT = {"genre": 1.0, "energy": 2.0}


def format_profile(prefs: dict) -> str:
    """Return a compact one-line description of a user profile."""
    return ", ".join(f"{k}={v}" for k, v in prefs.items())


def print_recommendations(name: str, prefs: dict, songs: list, k: int = 5, weights=None) -> None:
    """Print a readable ranked list of recommendations for one profile."""
    print("=" * 72)
    print(f"Profile: {name}")
    print(f"Prefs:   {format_profile(prefs)}")
    if weights:
        print(f"Weights: {weights}")
    print("-" * 72)
    for rank, (song, score, explanation) in enumerate(recommend_songs(prefs, songs, k, weights), start=1):
        print(f"{rank}. {song['title']} by {song['artist']} [{song['genre']}/{song['mood']}]  Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)

    if "--experiment" in sys.argv:
        print("#" * 72)
        print("EXPERIMENT: weight shift (genre 2.0 -> 1.0, energy 1.0 -> 2.0)")
        print("#" * 72 + "\n")
        for name in ("High-Energy Pop", "Conflicted (high energy + sad)"):
            print_recommendations(name, PROFILES[name], songs, weights=WEIGHT_SHIFT)


if __name__ == "__main__":
    main()
