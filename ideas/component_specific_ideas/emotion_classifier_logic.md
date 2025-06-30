# EmotionClassifier Logic

## Overview

The EmotionClassifier is responsible for analyzing user input, cleaning and processing it, and classifying it into one or more of **28 possible emotion categories** using a transformer-based neural network. This enables nuanced real-time emotional state tracking and drives downstream modules like the TrendTracker and DecisionMaker.

**Primary dataset:**

- [GoEmotions (Google, 2020)](https://github.com/google-research/google-research/tree/master/goemotions/data)
  - 58,000 Reddit comments
  - 28 fine-grained emotion categories
  - Supports multi-label annotation (1–3 emotions per entry)

## Workflow

1. **Input Cleaning**

   - User raw input is cleaned (lowercased, punctuation removed as needed, etc.)
   - Tokenization is performed at the word level (using `word_tokenize` from NLTK or similar)
2. **Emotion Classification (Transformer Autoencoder)**

   - Cleaned text is fed into a transformer autoencoder (may include pre-trained embeddings and learned context)
   - Outputs a **28-dimensional probability vector** (`y_pred`), with each dimension representing the confidence for one of the 28 GoEmotions classes
3. **TrendTracker Interface**

   - The classifier's output vector (plus 1st & 2nd discrete derivatives, and EMA values for each emotion) is passed to the TrendTracker
   - All vectors are **28-dimensional**

## Outputs

- **Raw prediction vector**: 28d, `float32` between 0 and 1, can be multi-label (i.e., >1 emotion per input)
- **First derivative**: 28d, change in each score compared to previous input
- **Second derivative**: 28d, change in slope per score
- **EMA (Exponential Moving Average)**: 28d, running smoothed value per emotion
- **EMA derivatives**: 28d each, for 1st and 2nd derivative of the EMA

## Example (Pseudocode)

```python
# For each user input:
y_pred = classifier(cleanedText)      # 28d vector
trend_buffer.append(y_pred)           # Keep last N entries

# Compute derivatives and EMA
first_deriv = y_pred - trend_buffer[-2]
second_deriv = first_deriv - (trend_buffer[-2] - trend_buffer[-3])
ema = (alpha * y_pred) + (1 - alpha) * previous_ema
```

## Notes

- This module is designed for nuanced, clinical, multi-label emotion detection.
- Outputs feed directly into memory and trend modules for longer-term context tracking.
