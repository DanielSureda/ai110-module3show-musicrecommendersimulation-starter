import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional

# Algorithm Recipe (default weights).
#   genre match      -> +2.0
#   mood match       -> +1.0
#   energy closeness -> up to +1.0, scaled by 1 - |song energy - target energy|
#   acoustic bonus   -> up to +0.5 (only if the user likes acoustic music), scaled by acousticness
DEFAULT_WEIGHTS: Dict[str, float] = {
    "genre": 2.0,
    "mood": 1.0,
    "energy": 1.0,
    "acoustic": 0.5,
}

INT_FIELDS = {"id"}
FLOAT_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}


@dataclass
class Song:
    """A song and its attributes (one row of songs.csv)."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """A user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

    def to_prefs(self) -> Dict:
        """Convert this profile into the dict format used by score_song."""
        return {
            "genre": self.favorite_genre,
            "mood": self.favorite_mood,
            "energy": self.target_energy,
            "likes_acoustic": self.likes_acoustic,
        }


class Recommender:
    """OOP wrapper around the functional score_song / recommend_songs logic."""

    def __init__(self, songs: List[Song], weights: Optional[Dict[str, float]] = None):
        """Store the catalog and the scoring weights to use."""
        self.songs = songs
        self.weights = weights

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user, highest score first."""
        ranked = sorted(
            self.songs,
            key=lambda s: score_song(user.to_prefs(), asdict(s), self.weights)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of a song's score for this user."""
        score, reasons = score_song(user.to_prefs(), asdict(song), self.weights)
        return f"Score {score:.2f}: " + "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting numeric columns to int/float."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in INT_FIELDS:
                row[key] = int(row[key])
            for key in FLOAT_FIELDS:
                row[key] = float(row[key])
            songs.append(row)
    return songs


def score_song(
    user_prefs: Dict, song: Dict, weights: Optional[Dict[str, float]] = None
) -> Tuple[float, List[str]]:
    """Score one song against user preferences; return (score, list of reasons)."""
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    score = 0.0
    reasons: List[str] = []

    if "genre" in user_prefs and song["genre"].lower() == str(user_prefs["genre"]).lower():
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.2f})")

    if "mood" in user_prefs and song["mood"].lower() == str(user_prefs["mood"]).lower():
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.2f})")

    if "energy" in user_prefs:
        gap = abs(song["energy"] - float(user_prefs["energy"]))
        points = w["energy"] * (1.0 - gap)
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs target {float(user_prefs['energy']):.2f} (+{points:.2f})")

    if user_prefs.get("likes_acoustic"):
        points = w["acoustic"] * song["acousticness"]
        score += points
        reasons.append(f"acousticness {song['acousticness']:.2f} (+{points:.2f})")

    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Optional[Dict[str, float]] = None
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest-first, and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, "; ".join(reasons)))
    # sorted() returns a new list and leaves the caller's `songs` list untouched.
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
