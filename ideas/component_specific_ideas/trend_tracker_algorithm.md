# Simple Emotion Trend Algorithm Plan

## Purpose

Track and summarize **recent emotional state trends** across 28 possible emotion categories (from GoEmotions) for conversational therapy applications. All calculations are performed **per category** (vectorized, 28d).

## Data

- Input: 28d vector of probabilities, output from the EmotionClassifier per user input (one value per GoEmotions class)
- Buffer: Store most recent 10 entries (default); all are 28-dimensional
- Output: Trends, smoothed values (EMA), and their derivatives (1st and 2nd) per emotion

## Core Algorithm

**On each new input:**

1. Append new 28d emotion vector to rolling buffer
2. Compute:
   - **First derivative:** change in each score compared to previous input
   - **Second derivative:** change in slope per score
   - **EMA:** exponential moving average per class, with custom α (recency weight)
   - **EMA derivatives:** same, but on EMA sequence

**Pseudocode:**

```python
BUFFER_SIZE = 10
trend_buffer = [[0.0]*28 for _ in range(BUFFER_SIZE)]
ema = [0.0]*28

def update_trend(new_vec, last_vec, last_ema, alpha=0.5):
    first_deriv = [n - l for n, l in zip(new_vec, last_vec)]
    second_deriv = [fd - (l - ll) for fd, l, ll in zip(first_deriv, last_vec, trend_buffer[-3])]
    new_ema = [alpha * n + (1-alpha) * e for n, e in zip(new_vec, last_ema)]
    # ...update buffer and store
    return new_ema, first_deriv, second_deriv
```

## Design Notes

- All calculations are fully vectorized (28d); code can scale easily with more classes if needed
- Designed for compatibility with GoEmotions, but can be adapted to any multi-class emotion classifier
- EMA, derivatives, and buffer length are all configurable hyperparameters

## Why 28d?

- To match GoEmotions’ 28 categories for maximal nuance in trend analysis
- Enables tracking of both primary and subtle emotional shifts over time

