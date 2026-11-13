# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

VibeMatch suggests 5 songs from a small catalog that match one listener's stated taste: a favorite genre, a favorite mood, a target energy level, and optionally a liking for acoustic sound.

- It assumes the user can describe their taste with one genre and one mood.
- It assumes taste stays the same over time (no history, no context).
- **Intended use:** classroom exploration of how recommenders turn data into ranked suggestions.
- **Not intended for:** real users, real music platforms, or any decision that matters. It shouldn't be used to judge which artists or genres are "better," and it shouldn't be used on a large catalog without fixing the biases below.

---

## 3. How the Model Works

Every song gets points:

- It gets **2 points** if its genre is the user's favorite genre.
- It gets **1 point** if its mood is the user's favorite mood.
- It gets **up to 1 point** for energy. A song with exactly the energy the user wants gets the full point, and the further away it is, the fewer points it gets.
- If the user likes acoustic music, it gets **up to 0.5 points** depending on how acoustic it is.

The points are added up, songs are sorted from highest to lowest, and the top 5 are shown. Each recommendation lists the reasons it got its points, such as "genre match (+2.00)".

Changes from the starter: I filled in the CSV loader, the scoring rule, and the ranking rule. I added the acoustic bonus, made the weights adjustable for experiments, and connected the `Recommender` class to the same scoring function.

---

## 4. Data

- **18 songs** (10 starter songs plus 8 I added with AI help).
- **Genres:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, classical, metal, country, reggae, edm, r&b, folk.
- **Moods:** happy, chill, intense, relaxed, moody, focused, confident, peaceful, angry, nostalgic, euphoric, romantic, sad.
- The added songs cover genres and moods that weren't in the starter file.
- **Gaps:** lofi has 3 songs and pop has 2, but most genres have only 1. There are no lyrics, languages, release years, popularity, or artist info beyond the name. All songs are made up.

---

## 5. Strengths

- It works well when the user's taste matches a well-covered genre. *Chill Lofi* returned three lofi tracks and then other calm, acoustic songs (ambient, jazz). That felt right.
- The energy-closeness rule works as intended. It rewards songs *near* the target instead of always favoring the loudest or quietest songs, so the "filler" picks after the genre matches still have the right energy.
- Every score comes with readable reasons, so it's easy to see *why* a song was picked.

---

## 6. Limitations and Bias

The biggest weakness I found is that **genre is worth too much compared with how a song actually feels.** For the "high energy + sad" folk user, *Paper Boats* ranked #1 with 3.40 points even though its energy (0.30) is the opposite of what they asked for, because the genre and mood labels alone gave it 3 points. Every high-energy song was stuck below 1.0 point. Genre matching is also exact text, so *Rooftop Lights* ("indie pop") gets no genre credit from a "pop" fan, and a "k-pop" fan never gets any genre points at all. Since most genres have only one song in the catalog, a user with a niche genre gets one strong match and then four songs chosen only by energy. That's a small "filter bubble" built from category labels instead of actual sound.

---

## 7. Evaluation

I tested six profiles, three normal and three adversarial, and looked at whether the top 5 "felt" right.

### Core profiles

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

```
========================================================================
Profile: Chill Lofi
Prefs:   genre=lofi, mood=chill, energy=0.35, likes_acoustic=True
------------------------------------------------------------------------
1. Library Rain by Paper Lanterns [lofi/chill]  Score: 4.43
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.35 vs target 0.35 (+1.00)
     - acousticness 0.86 (+0.43)
2. Midnight Coding by LoRoom [lofi/chill]  Score: 4.29
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.42 vs target 0.35 (+0.93)
     - acousticness 0.71 (+0.35)
3. Focus Flow by LoRoom [lofi/focused]  Score: 3.34
     - genre match (+2.00)
     - energy 0.40 vs target 0.35 (+0.95)
     - acousticness 0.78 (+0.39)
4. Spacewalk Thoughts by Orbit Bloom [ambient/chill]  Score: 2.39
     - mood match (+1.00)
     - energy 0.28 vs target 0.35 (+0.93)
     - acousticness 0.92 (+0.46)
5. Coffee Shop Stories by Slow Stereo [jazz/relaxed]  Score: 1.43
     - energy 0.37 vs target 0.35 (+0.98)
     - acousticness 0.89 (+0.45)
```

```
========================================================================
Profile: Deep Intense Rock
Prefs:   genre=rock, mood=intense, energy=0.9
------------------------------------------------------------------------
1. Storm Runner by Voltline [rock/intense]  Score: 3.99
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.91 vs target 0.90 (+0.99)
2. Gym Hero by Max Pulse [pop/intense]  Score: 1.97
     - mood match (+1.00)
     - energy 0.93 vs target 0.90 (+0.97)
3. Laser Bloom by Pulse Theory [edm/euphoric]  Score: 0.95
     - energy 0.95 vs target 0.90 (+0.95)
4. Iron Tempest by Graveforge [metal/angry]  Score: 0.93
     - energy 0.97 vs target 0.90 (+0.93)
5. Sunrise City by Neon Echo [pop/happy]  Score: 0.92
     - energy 0.82 vs target 0.90 (+0.92)
```

### Adversarial / edge-case profiles

```
========================================================================
Profile: Conflicted (high energy + sad)
Prefs:   genre=folk, mood=sad, energy=0.9
------------------------------------------------------------------------
1. Paper Boats by Hollow Pines [folk/sad]  Score: 3.40
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.30 vs target 0.90 (+0.40)
2. Storm Runner by Voltline [rock/intense]  Score: 0.99
     - energy 0.91 vs target 0.90 (+0.99)
3. Gym Hero by Max Pulse [pop/intense]  Score: 0.97
     - energy 0.93 vs target 0.90 (+0.97)
4. Laser Bloom by Pulse Theory [edm/euphoric]  Score: 0.95
     - energy 0.95 vs target 0.90 (+0.95)
5. Iron Tempest by Graveforge [metal/angry]  Score: 0.93
     - energy 0.97 vs target 0.90 (+0.93)
```

```
========================================================================
Profile: Unknown Genre (k-pop)
Prefs:   genre=k-pop, mood=happy, energy=0.7
------------------------------------------------------------------------
1. Rooftop Lights by Indigo Parade [indie pop/happy]  Score: 1.94
     - mood match (+1.00)
     - energy 0.76 vs target 0.70 (+0.94)
2. Sunrise City by Neon Echo [pop/happy]  Score: 1.88
     - mood match (+1.00)
     - energy 0.82 vs target 0.70 (+0.88)
3. Night Drive Loop by Neon Echo [synthwave/moody]  Score: 0.95
     - energy 0.75 vs target 0.70 (+0.95)
4. Concrete Crown by Kilo Verse [hip hop/confident]  Score: 0.92
     - energy 0.78 vs target 0.70 (+0.92)
5. Dusty Porch Swing by Willow Creek Band [country/nostalgic]  Score: 0.85
     - energy 0.55 vs target 0.70 (+0.85)
```

```
========================================================================
Profile: Energy Only (no genre/mood)
Prefs:   energy=0.5
------------------------------------------------------------------------
1. Island Time by Sunny Roots [reggae/relaxed]  Score: 1.00
     - energy 0.50 vs target 0.50 (+1.00)
2. Velvet Hours by Amara Lane [r&b/romantic]  Score: 0.98
     - energy 0.48 vs target 0.50 (+0.98)
3. Dusty Porch Swing by Willow Creek Band [country/nostalgic]  Score: 0.95
     - energy 0.55 vs target 0.50 (+0.95)
4. Midnight Coding by LoRoom [lofi/chill]  Score: 0.92
     - energy 0.42 vs target 0.50 (+0.92)
5. Focus Flow by LoRoom [lofi/focused]  Score: 0.90
     - energy 0.40 vs target 0.50 (+0.90)
```

### Comparing profiles

- **High-Energy Pop vs Chill Lofi:** Pop gets bright, high-energy tracks (0.75–0.93). Lofi gets slow, acoustic tracks (0.28–0.42). This makes sense because the energy targets are far apart, and the acoustic bonus pushes jazz and ambient into the lofi list.
- **High-Energy Pop vs Deep Intense Rock:** Both lists include *Gym Hero*. Pop picks it for the genre and rock picks it for the "intense" mood, so one song can fit two different users for different reasons. Rock has only one rock song, so spots 3–5 are just "anything loud" (edm, metal, pop).
- **Chill Lofi vs Deep Intense Rock:** The two lists share no songs. The system clearly separates "chill lofi" from "intense rock."
- **Deep Intense Rock vs Conflicted (sad + 0.9 energy):** Spots 2–5 are almost the same loud songs. The conflicted user's #1 is a quiet sad folk song, chosen only because its labels match and not because it sounds right.
- **High-Energy Pop vs Unknown Genre (k-pop):** Without any genre credit, the k-pop user's list is decided by mood and energy. *Rooftop Lights* even slightly beats *Sunrise City*. The results are reasonable, but only by luck.
- **Unknown Genre vs Energy Only:** The energy-only user gets mid-energy songs (reggae, r&b, country) that all score around 1.0. The ranking is close to random, which shows the system needs more than one preference to say anything useful.

**Why does *Gym Hero* keep showing up for people who just want "Happy Pop"?** Because it's labeled "pop." That label alone is worth 2 points, which is more than a perfect mood match and a perfect energy match combined would earn a non-pop song. The system doesn't know that *Gym Hero* is an intense workout track and not a happy one.

### Experiment: weight shift (genre ×0.5, energy ×2)

```
========================================================================
Profile: High-Energy Pop
Prefs:   genre=pop, mood=happy, energy=0.8
Weights: {'genre': 1.0, 'energy': 2.0}
------------------------------------------------------------------------
1. Sunrise City by Neon Echo [pop/happy]  Score: 3.96
     - genre match (+1.00)
     - mood match (+1.00)
     - energy 0.82 vs target 0.80 (+1.96)
2. Rooftop Lights by Indigo Parade [indie pop/happy]  Score: 2.92
     - mood match (+1.00)
     - energy 0.76 vs target 0.80 (+1.92)
3. Gym Hero by Max Pulse [pop/intense]  Score: 2.74
     - genre match (+1.00)
     - energy 0.93 vs target 0.80 (+1.74)
4. Concrete Crown by Kilo Verse [hip hop/confident]  Score: 1.96
     - energy 0.78 vs target 0.80 (+1.96)
5. Night Drive Loop by Neon Echo [synthwave/moody]  Score: 1.90
     - energy 0.75 vs target 0.80 (+1.90)
```

```
========================================================================
Profile: Conflicted (high energy + sad)
Prefs:   genre=folk, mood=sad, energy=0.9
Weights: {'genre': 1.0, 'energy': 2.0}
------------------------------------------------------------------------
1. Paper Boats by Hollow Pines [folk/sad]  Score: 2.80
     - genre match (+1.00)
     - mood match (+1.00)
     - energy 0.30 vs target 0.90 (+0.80)
2. Storm Runner by Voltline [rock/intense]  Score: 1.98
     - energy 0.91 vs target 0.90 (+1.98)
3. Gym Hero by Max Pulse [pop/intense]  Score: 1.94
     - energy 0.93 vs target 0.90 (+1.94)
4. Laser Bloom by Pulse Theory [edm/euphoric]  Score: 1.90
     - energy 0.95 vs target 0.90 (+1.90)
5. Iron Tempest by Graveforge [metal/angry]  Score: 1.86
     - energy 0.97 vs target 0.90 (+1.86)
```

What I found: for the pop user, *Rooftop Lights* moved ahead of *Gym Hero*. That's **more accurate**, because a happy song beats an intense one for a happy-pop fan. For the conflicted user, the order stayed the same but the gaps got smaller, so the result was **different, not fixed**. The labels still win.

**Surprise:** even with simple addition, the lists "felt" like real recommendations most of the time. The odd results only showed up when I designed profiles to break the system.

---

## 8. Future Work

1. **Partial genre credit.** Treat related genres (pop / indie pop / k-pop, rock / metal) as close matches instead of all-or-nothing.
2. **Diversity penalty.** Lower the score of a song whose artist or genre is already in the top results so the list isn't one-note.
3. **More features and data.** Use valence and tempo in the score, add more songs per genre, and let users list several genres or moods with different weights.

---

## 9. Personal Reflection

**Biggest learning moment:** seeing the "high energy + sad folk" profile get a slow, quiet song (energy 0.30) at #1 when the user asked for energy 0.9. The code was doing exactly what it was designed to do, and it was still the wrong answer for that user. Weights are design decisions with consequences, not just numbers.

**How AI helped and when I double-checked it:** I used my AI coding assistant to compare collaborative and content-based filtering, to decide which CSV columns to use, to propose point weights and edge-case profiles, and to implement and format the code. I did not trust the output just because it ran: I read the "reasons" printed for every recommendation to check that the math matched my recipe, I made sure the energy rule rewards being close to the target instead of just higher energy, and I ran the tests after each change. I also found that the starter `main.py` used `from recommender import ...`, which fails with `python -m src.main`, so the import had to be fixed before anything worked.

**What surprised me:** how much a simple weighted score and a sort already feel like a real recommendation. Because the system shows its reasons, it looks trustworthy, even when those reasons are only labels like "pop" that don't say anything about how the song actually sounds.

**What I would try next:** a diversity penalty so the top 5 are not all from the same genre or artist, partial genre matching ("indie pop" close to "pop"), and a small collaborative-filtering version with a few fake users to compare its suggestions with this content-based one.
