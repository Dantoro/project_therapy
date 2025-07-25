# Emotion Regressor Logic

**Last updated: 2025-07-16**

---

## Overview

The Emotion Regressor in Project Therapy is responsible for generating a fine-grained, multidimensional representation of user emotion from text. Rather than a traditional single-label classifier, the regressor outputs a vector of confidence scores ("soft labels") for a comprehensive range of emotions, capturing the complexity and ambiguity of human affective expression.

The final 35-dimensional mood vector is built by combining the predictions of two large transformer-based models:

* **A GoEmotions-derived model** for 28 discrete emotions (including neutral)
* **A Hartmann Ekman-derived model** for 6 broad Ekman emotion categories (plus a 7th neutral category)

This ensemble approach leverages the strengths of both fine-grained and broad emotional categorization, across a diverse set of training corpora.

---

## Model Details

### 1. **Discrete Emotion Model (GoEmotions-based)**

* **Model:** [SamLowe/roberta-base-go_emotions](https://huggingface.co/SamLowe/roberta-base-go_emotions)
* **Classes:** 28 emotions + neutral
* **Training Data:** Google’s GoEmotions dataset (Demszky et al., 2020) — 58k Reddit comments labeled for 28 nuanced emotions. Highly diverse, covers a wide spectrum of social media language, slang, and ambiguous affect.
* **Why included:** Provides nuanced emotional insight; sensitive to internet speech, casual tone, and fine shades of sentiment that are underrepresented in formal text datasets.

### 2. **Ekman Emotion Model (Hartmann-based)**

* **Model:** [j-hartmann/emotion-english-roberta-large](https://huggingface.co/j-hartmann/emotion-english-roberta-large)
* **Classes:** 6 classic Ekman categories (anger, disgust, fear, joy, sadness, surprise) **plus neutral** (7 total)
* **Training Data:** Aggregated from six major emotion corpora, spanning social media, dialogues, and emotion-annotated datasets. The full list includes:
  1. **Crowdflower (2016):** Short social media posts/tweets, labeled for emotion (crowdsourced).
  2. **Emotion Dataset / Saravia et al. (2018) & Elvis et al. (2018):** SMS, blogs, news headlines, and forum text — diverse genres, global English.
  3. **GoEmotions (Demszky et al., 2020):** Reddit comments; fine-grained, but mapped to broad Ekman classes for this model.
  4. **ISEAR (International Survey on Emotion Antecedents and Reactions):** Real-world personal experiences, semi-formal prose; includes a cleaned/variant version by Vikash (2018).
  5. **MELD (Poria et al., 2019):** TV show transcripts (Friends), conversational multi-party dialogue.
  6. **SemEval-2018 Task 1, EI-reg (Mohammad et al., 2018):** Twitter and other short text, emotion intensity regression labels.
* **Why included:** Trained for generalization across social, conversational, and formal registers; brings a robust "big picture" emotional context that complements the discrete model.
* **Note on Neutral:** The "neutral" class is included explicitly as a seventh category in the Hartmann model (in addition to the six Ekman classes). It typically denotes the absence of strong emotion, and may be mapped to instances labeled as "neutral" in the datasets above (especially GoEmotions, MELD, and Crowdflower).

---

## Ensemble Construction

* Both models are applied **in parallel** to every input (user text or chatbot output).
* Their output vectors are concatenated, yielding a **35d mood vector**: 28 GoEmotions + 7 Ekman/neutral.
* This mood vector provides both highly specific and broadly generalized emotional information.
* The vector is immediately fed to the **TrendTracker** module, which computes derivatives, moving averages, and other features over recent inputs to build a time-aware profile of user emotion.

---

## Why This Design?

* **Why two models?**
  * Single-dataset emotion models are brittle; social media-specific models may miss clinical/therapeutic context, while dialogue- or literature-based models may miss slang, sarcasm, or internet speech. This ensemble guarantees both coverage and precision.
  * Fine-grained emotion (GoEmotions) = nuanced understanding of internet-native, informal language.
  * Broad Ekman categories = alignment with psychology literature, supporting higher-level affective analysis and trend tracking.
* **Why these datasets?**
  * Combined, they represent millions of real-world examples, from Reddit to TV scripts, from global Twitter to crowdsourced SMS, enabling the regressor to handle everything from "keyboard smash" venting to formal help-seeking dialogue.
* **Why a regressor?**
  * Real user emotion is rarely one-hot. Allowing for "soft labels" and overlapping emotion is more true to the experience of clinical text and real conversations.

---

## Output

* **Dimension:** 35d (per input)
* **Interpretation:** Each dimension is a confidence score (0–1) for a specific emotion or category. Sum does*not* necessarily equal 1.
* **Next step:** The mood vector is passed to TrendTracker for further emotional calculus and tracking.

---

## Change Log

* 2025-07-16: Rewrote logic for EmotionRegressor to reflect transformer ensemble, multi-dataset coverage, and shift to regression paradigm.
* 2025-07-07: (legacy) Previous classifier design; built on custom GoEmotions-based model only.

---
