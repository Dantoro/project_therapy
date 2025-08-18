# Emotion Regressor Logic

**Last updated: 2025-07-16**

---

## Overview

The Emotion Regressor in Project Therapy is responsible for generating a fine-grained, multidimensional representation of user emotion from text. Rather than a traditional single-label classifier, the regressor outputs a vector of confidence scores ("soft labels") for a comprehensive range of emotions, capturing the complexity and ambiguity of human affective expression.

The final 28-dimensional mood vector is built by using a  **GoEmotions-derived model** for 28 discrete emotions (including neutral)

This approach leverages the strength of broad emotional categorization, across a diverse set of training samples.

---

## Model Details

### **Discrete Emotion Model (GoEmotions-based)**

* **Model:** [SamLowe/roberta-base-go_emotions](https://huggingface.co/SamLowe/roberta-base-go_emotions)
* **Classes:** 28 emotions
* **Training Data:** Google’s GoEmotions dataset (Demszky et al., 2020) — 58k Reddit comments labeled for 28 nuanced emotions. Highly diverse, covers a wide spectrum of social media language, slang, and ambiguous affect.
* **Why included:** Provides nuanced emotional insight; sensitive to internet speech, casual tone, and fine shades of sentiment that are underrepresented in formal text datasets.

## Ensemble Construction

* Both models are applied **in parallel** to every input (user text or chatbot output).
* Their output vectors are concatenated, yielding a **35d mood vector**: 28 GoEmotions + 7 Ekman/neutral.
* This mood vector provides both highly specific and broadly generalized emotional information.
* The vector is immediately fed to the **TrendTracker** module, which computes derivatives, moving averages, and other features over recent inputs to build a time-aware profile of user emotion.

---

## Why a regressor?

* Real user emotion is rarely one-hot. Allowing for "soft labels" and overlapping emotion is more true to the experience of clinical text and real conversations.

---

## Output

* **Dimension:** 28d (per input)
* **Interpretation:** Each dimension is a confidence score (0–1) for a specific emotion or category. Sum does *not* necessarily equal 1.
* **Next step:** The mood vector is passed to TrendTracker for further emotional calculus and tracking.

---

## Change Log

* 2025-08-18: Removed j-hartmann/emotion-english-roberta-large from the model, since tacking 7 columns worth of Ekman categories onto the end of 28 columns worth of individual emotions was redundant and confusing while providing little additional benefit and skewing the importance of each feature by directly comparing individual emotions and umbrella categories consisting of a variable amount of said emotions.
* 2025-07-16: Rewrote logic for EmotionRegressor to reflect transformer ensemble, multi-dataset coverage, and shift to regression paradigm.
* 2025-07-07: (legacy) Previous classifier design; built on custom GoEmotions-based model only.

---
