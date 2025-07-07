# Trend Tracker Logic

## Purpose

The Trend Tracker maintains a continuous, quantitative summary of the user’s recent emotional state—tracking not just the latest predicted emotions, but their momentum and trends over time. This is used both for internal state modeling (e.g., the DecisionMaker) and to generate human-readable summaries for the user or clinicians.

## Data Model & Structure

**Inputs:**

- 28d vector (GoEmotions probabilities) from the EmotionClassifier for each user input
- 6d vector (Ekman categories) derived from the same 28 classes, using a static mapping
- Rolling buffer: Last 10 user entries

**Outputs:**

- For each user input, internally store (as a single row):
  - `current_emotion_vector` (28d)
  - `current_ekman_vector` (6d)
  - `current_emotion_1st_deriv` (28d)
  - `current_ekman_1st_deriv` (6d)
  - `current_emotion_2nd_deriv` (28d)
  - `current_ekman_2nd_deriv` (6d)
  - `ema_emotion_vector` (28d)
  - `ema_ekman_vector` (6d)
  - `ema_emotion_1st_deriv` (28d)
  - `ema_ekman_1st_deriv` (6d)
  - `ema_emotion_2nd_deriv` (28d)
  - `ema_ekman_2nd_deriv` (6d)
- These can be concatenated into a single 204d vector per row for passing to the DecisionMaker.

**Public/Human-Readable Output:**

- For each row, display only:
  1. `top_current_ekman` (label)
  2. `current_1st_emotion` (label)
  3. `current_2nd_emotion` (label)
  4. `current_3rd_emotion` (label)
  5. `current_4th_emotion` (label)
  6. `top_ema_ekman` (label)
  7. `ema_1st_emotion` (label)
  8. `ema_2nd_emotion` (label)
  9. `ema_3rd_emotion` (label)
  10. `ema_4th_emotion` (label)
- Confidence values for top emotions/categories may optionally be included.

## Core Algorithm

On each new user input:

1. Append new emotion vector to rolling buffer (10 most recent rows)
2. Compute for both 28d (emotions) and 6d (Ekman):
   - **First derivative:** Change from previous row (local slope)
   - **Second derivative:** Change in slope (acceleration)
   - **EMA:** Exponential moving average (with tunable α)
   - **EMA derivatives:** As above, but on EMA
3. Store all results in a single row of the tracker (shape: [10 rows, 204 columns])
4. Human-readable columns are derived from argmax/top-k in the current and EMA vectors (for both emotion and Ekman categories)

## Usage Notes

- **Internally:** Only the most recent row is required for DecisionMaker; the full buffer can be passed for richer context, but is usually unnecessary
- **Externally:** Only the 10 human-readable summary columns are displayed
- **No chatbot responses** are fed into the trend tracker—only user entries
- Confidence values are for display and are not passed as additional features

## Implementation Details

- All vectors are fully vectorized and support efficient computation with numpy or pandas
- Mapping from emotions to Ekman is static and performed at each step
- Buffer length, EMA α, and derivative order are tunable hyperparameters

---

This version supersedes the earlier “trend_tracker_algorithm.md” and describes the full 204d vector output as well as the public summary. All details reflect current use in Project Therapy as of July 2025.
