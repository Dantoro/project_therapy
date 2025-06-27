## Component Overview

This document summarizes the architecture and logic for the **Emotion Classifier** and **Trend Tracker** in Project Therapy, including data structure, feature engineering, and how emotional trends are quantitatively analyzed.

---

### 1. Dataset: Kaggle Simple Emotion Dataset

* **Source:** [Kaggle Simple Emotion Dataset](https://www.kaggle.com/datasets) (local copy in `datasets/simple_emotion_dataset.csv`)
* **Structure:**
  * **Text:** User-generated sentences scraped from social media (Reddit, Twitter, etc.)
  * **Emotion:** One of six classes: `anger`, `fear`, `joy`, `love`, `sadness`, `surprise`
* **Distribution Example:**
  ```
  Emotion
  joy         6761
  sadness     5797
  anger       2709
  fear        2373
  love        1641
  surprise     719
  ```
* **Usage:** Used as the initial training and prototyping data for emotion classification.

---

### 2. Input Preprocessing: Character-Level BiGRU Cleaner

* **Purpose:** Clean and standardize each new user input before classification.
* **Process:**
  * **Tokenization:**
    * Tokenize the input sentence at the character level.
    * Capture unigrams (single chars), bigrams (2-char combos), and trigrams (3-char combos).
    * Preserve all case, punctuation, and emoji.
  * **Model:**
    * A shallow BiGRU (Bidirectional Gated Recurrent Unit) sweeps over the sequence.
    * Its role is NOT to rewrite or alter text, but to help recognize typos, odd punctuation, and other “messy” features for robust downstream processing.
    * The cleaned text is passed forward unaltered for maximum transparency and user trust.

---

### 3. Emotion Classifier: Autoencoder Transformer

* **Purpose:** Classify the user’s cleaned input into one of six emotion classes.
* **Architecture:**
  * **Tokenizer:** Subword tokenization (e.g., BPE or WordPiece, as used in modern transformers).
  * **Model:**
    * Autoencoding transformer model (e.g., DistilBERT, MiniLM, etc.).
    * Output is a 6-dimensional vector of probabilities (one per emotion class).
* **Output:**
  * **Predicted Class:** The emotion with the highest probability.
  * **Probability Vector:** Confidence scores for all 6 emotion classes (sums to 1.0).
  * **Example:**
    * Input: “I feel terrible today.”
    * Output: `[0.15, 0.10, 0.03, 0.02, 0.67, 0.03]`
      * Classes: `[anger, fear, joy, love, sadness, surprise]`
      * Predicted: `sadness`, Confidence: `0.67`

---

### 4. Trend Tracker: Rolling Buffer and EMA

#### **Structure:**

* **Buffer:** A table of 10 rows, each containing:
  * **Raw Prediction (6d vector):** The probability vector for that input.
  * **EMA (6d vector):** Exponential Moving Average across all buffered vectors (recent entries weighted more heavily).

#### **EMA Calculation:**

* **Formula (for each emotion dimension):**

  ```
  EMA_t = α * x_t + (1-α) * EMA_{t-1}
  ```

  * `x_t`: Current probability for that emotion
  * `EMA_{t-1}`: Previous EMA
  * `α`: Smoothing factor (e.g., 0.3–0.5; tune to taste)
* **Snapshot:** Each row “freezes” the raw prediction and EMA at the moment of input.

#### **Rolling Buffer Logic:**

* **At each new input:**
  1. Classify input → 6d vector of probabilities.
  2. Compute new EMA.
  3. Add new row:

     `[raw_prediction, new_EMA]`
  4. If >10 rows, remove oldest.

#### **Columns per Row:**

* **Raw Probability Vector** (6d, sums to 1): Output from the classifier for the current input.
* **First Derivative (Raw)** (6d): Difference from previous step: `raw_pred[t] - raw_pred[t-1]`
* **Second Derivative (Raw)** (6d): Change in first derivative: `raw_d1[t] - raw_d1[t-1]`
* **EMA Probability Vector** (6d, sums to 1): Exponential moving average (trend-smoothed) vector up to this step.
* **First Derivative (EMA)** (6d): Difference from previous step: `ema[t] - ema[t-1]`
* **Second Derivative (EMA)** (6d): Change in first derivative: `ema_d1[t] - ema_d1[t-1]`
* **(For logs/UI/explainability; always derivable from vectors):**

  * **Predicted Class (Raw):** Label of max in raw prediction vector.
  * **Predicted Confidence (Raw):** Max value in raw prediction vector.
  * **Predicted Class (EMA):** Label of max in EMA vector.
  * **Predicted Confidence (EMA):** Max value in EMA vector.

---

### 5. Why This Matters

* **Raw predictions:** Capture immediate, local emotional state and volatility.
* **EMA:** Smooths out short-term noise, reveals sustained trends, and identifies slow or sudden shifts.
* **First and Second Derivatives:** Quantify both the *direction* and *rate* of emotional change—useful for assessing urgency, instability, or positive recovery.
* **6D Vectors:** Preserve the *entire* emotional landscape, not just the top class, allowing for nuanced “mixed emotions” and emerging trends.

---

### 6. Output

The Emotion Classifier and Trend Tracker provide the rest of Project Therapy with:

* **Current emotion class** and **confidence**
* **Full 6d probability vectors** (raw and EMA)
* **Local and trend-based derivatives**
* **Rolling 10-entry buffer** for context-aware decision-making

---

#### Next Steps

These outputs serve as foundational features for:

* The multi-tiered memory system (STM/LTM)
* Adaptive response generation in the chatbot
* Alert/flag systems in the decision maker for clinical risk assessment

---

*Last updated: June 2025*
