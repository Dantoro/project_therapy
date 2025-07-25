l

# Memory Module Logic

**Last updated: 2025-07-25**

---

## Key Points

* STM buffer stores up to 10 utterance-pairs (userUtterance, chatbotUtterance), raw text only
* LTM is a rolling buffer of 10 summary blocks (seq2seq + dense vector)
* TrendTracker maintains a rolling 210d vector for emotional/temporal context on user utterances
* All word/utterance embeddings now computed on-the-fly by the HAN (no STM caching)

---

## Overview

This module manages all short- and long-term memory for the conversational agent, providing persistent context to the DecisionMaker, TrendTracker, and chatbot.

---

## Short-Term Memory (STM)

* **Structure:** Buffer of 10 utterance-pairs:
  * `userUtterance = (rawText)`
  * `chatbotUtterance = (rawText)`
* **Content:**
  * Each utterance is raw text (could be a sentence, paragraph, etc)
  * No cached embeddings; all vectorization is performed by HAN
* **Lifecycle:**
  * STM accepts new utterance-pairs
  * When full (10 pairs), triggers summarization into LTM and resets

---

## Long-Term Memory (LTM)

* **Structure:** FIFO buffer of 10 blocks
* **Each block includes:**
  * Seq2seq summary (5–10 sentences) covering last 10 STM pairs
  * Dense vector representation (128d/256d) for fast retrieval/attention
  * Optionally: timestamp, metadata, summary of emotional state

---

## TrendTracker

* **Feature:** 210d emotion vector per user utterance
* **Components:**
  * [current_emotion_vector (28d), current_ekman_vector (7d)]
  * [first and second derivatives of both]
  * [EMA of last 10 user utterances, plus derivatives]
* **Rolling buffer:** Only user utterances tracked (not chatbot responses)

---

## Data Flow

1. New user input processed by EmotionRegressor and TrendTracker
2. Input appended to STM
3. Chatbot generates and returns response, appended to STM
4. When STM full, STM passed to LTM summarizer, and reset

---

## Output/Interface

* STM: Last 10 utterance-pairs, as raw text
* LTM: Last 10 summary blocks (text, dense vector, metadata)
* TrendTracker: Last 10 user utterances, with 210d vectors and summary stats

---

## Notes

* STM and LTM window sizes are tunable, but 10 is default (matches HAN and LTM transformer design)
* No caching of per-utterance or per-word embeddings—HAN computes these live on demand
* Module designed for extension to multi-user/multimodal future versions

---

## Change Log

* 2025-07-25: Clarified that STM now stores only raw text, no cached embeddings; improved TrendTracker details; added explicit key points section
* 2025-07-16: Previous minor update—aligned STM window size with HAN
* Earlier: (legacy) Cached vectors, extra metadata
