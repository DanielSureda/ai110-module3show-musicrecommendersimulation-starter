# 🎵 Music Recommender Simulation

## Project Summary

This project is a small, CLI-first **content-based music recommender** written in Python. It loads an 18-song catalog from `data/songs.csv`, compares each song to a user's "taste profile" (favorite genre, favorite mood, target energy, and optionally a liking for acoustic sound), gives every song a score with a list of reasons, and prints the top 5 in the terminal. It was built to show how data becomes a prediction, and where even a simple scoring rule can be biased.

---

## How The System Works

**How real recommenders work.** Platforms like Spotify and YouTube mix two main approaches. **Collaborative filtering** uses the behavior of many users ("people who liked what you liked also liked X"). It learns from likes, skips, replays, saves, playlist adds, and listening time, and it doesn't need to know anything about the music itself. **Content-based filtering** uses the attributes of the items themselves (genre, mood, tempo, energy, acousticness, and even audio or lyric embeddings) and recommends things similar to what a user already enjoys. Real systems combine both, add context like time of day and device, and retrain constantly on huge amounts of data.

**What my version prioritizes.** My simulation is **purely content-based**: there are no other users, only song attributes and one profile. It focuses on the *vibe* of a song: genre first, then mood, then how close the song's energy is to what the user wants.

**Features used**

| Object | Features |
| --- | --- |
| `Song` | `id`, `title`, `artist`, `genre`, `mood`, `energy` (0–1), `tempo_bpm`, `valence`, `danceability`, `acousticness` (scoring uses `genre`, `mood`, `energy`, `acousticness`) |
| `UserProfile` | `favorite_genre`, `favorite_mood`, `target_energy` (0–1), `likes_acoustic` (bool) |

The functional API uses an equivalent dictionary, e.g. `{"genre": "pop", "mood": "happy", "energy": 0.8}`.

### Algorithm Recipe

For every song in the catalog (the **Scoring Rule**):

- **+2.0** if the song's genre equals the user's favorite genre
- **+1.0** if the song's mood equals the user's favorite mood
- **+1.0 × (1 − |song energy − target energy|)** energy-closeness points. This rewards songs *close* to the target rather than just "higher" or "lower" ones: a perfect match earns 1.0, and a song 0.5 away earns 0.5.
- **+0.5 × acousticness**, only if the user likes acoustic music

Then the **Ranking Rule** sorts all scored songs from highest to lowest and returns the top *k* (default 5). Both rules are needed: the scoring rule judges one song by itself, and the ranking rule turns those separate judgments into an ordered list.

```
User prefs ──► for each song in songs.csv ──► score_song() ──► (score, reasons)
                                                                   │
                                     Top K  ◄── sorted(desc) ◄─────┘
```

### Expected biases (written before testing)

- Genre is worth twice as much as mood, so the system will probably **over-prioritize genre** and miss great songs that match the user's mood.
- Genre matching is **exact text matching**, so related genres ("indie pop" vs "pop") get no credit.
- Most genres in the catalog have only one song, so users with niche tastes will get one good match and then filler.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main                # six user profiles
   python -m src.main --experiment   # also runs the weight-shift experiment
   ```

### Running Tests

```bash
pytest
```

---

## Sample Recommendation Output

Default "pop / happy" profile from `python -m src.main`:

```
========================================================================
Profile: High-Energy Pop
Prefs:   genre=pop, mood=happy, energy=0.8
------------------------------------------------------------------------
1. Sunrise City by Neon Echo [pop/happy]  Score: 3.98
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.82 vs target 0.80 (+0.98)
2. Gym Hero by Max Pulse [pop/intense]  Score: 2.87
     - genre match (+2.00)
     - energy 0.93 vs target 0.80 (+0.87)
3. Rooftop Lights by Indigo Parade [indie pop/happy]  Score: 1.96
     - mood match (+1.00)
     - energy 0.76 vs target 0.80 (+0.96)
4. Concrete Crown by Kilo Verse [hip hop/confident]  Score: 0.98
     - energy 0.78 vs target 0.80 (+0.98)
5. Night Drive Loop by Neon Echo [synthwave/moody]  Score: 0.95
     - energy 0.75 vs target 0.80 (+0.95)
```

Output for all six profiles (core and adversarial) is in [model_card.md](model_card.md#7-evaluation).

---

## Experiments You Tried

- **Weight shift (genre 2.0 → 1.0, energy 1.0 → 2.0).** For the pop/happy user, *Rooftop Lights* (indie pop, happy) moved up past *Gym Hero* (pop, intense). This felt **more accurate**: a happy indie-pop song fits a "happy pop" listener better than an intense workout track. For the "high energy + sad folk" user, *Paper Boats* stayed #1 even though its energy (0.30) is far from 0.9. The gap between it and the high-energy songs got much smaller (2.80 vs 1.98), so the results were **different but not fixed**.
- **Adversarial profiles.** I tested a user with conflicting preferences (sad mood but 0.9 energy), a user whose genre isn't in the catalog (k-pop), and a user with only an energy preference. Details are in the model card.

---

## Limitations and Risks

- The catalog is tiny (18 songs) and most genres have only one song.
- Genre and mood have to match exactly as text, so "indie pop" ≠ "pop".
- Genre weight is high enough that a category match beats a much better "vibe" match.
- It doesn't understand lyrics, language, artists, or listening history, and there are no other users.

See the [Model Card](model_card.md) for more detail.

---

## Reflection

Read the full [**Model Card**](model_card.md).

Building VibeMatch showed me that a recommender is basically data plus a scoring rule plus a sort. With only four signals (genre, mood, energy and acousticness) and some hand-picked weights, the top results already "feel" like real recommendations for clear profiles like chill lofi or intense rock. But every number is a decision: making genre worth 2.0 decided that a pop song with the wrong mood (Gym Hero) beats an indie pop song with the right mood, and that a user who asks for high energy can still get a slow, sad folk song first.

Bias shows up in two places. In the data, whoever builds the catalog decides which genres exist and how many songs each one has, so a k-pop or classical fan gets far fewer good options than a lofi fan. In the weights, exact genre matching keeps users inside the genre they already like, which is how filter bubbles start. Real platforms have the same problems at a much larger scale, which is why recommenders need to be explained and evaluated, not just optimized.
