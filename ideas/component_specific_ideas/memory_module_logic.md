
# Memory Module Logic

## Overview

This module manages all short- and long-term memory for the conversational agent, providing context to the DecisionMaker and Chatbot.

**Key features:**

* 10-turn Short-Term Memory (STM)
* 10-block rolling Long-Term Memory (LTM), with each block summarizing the last 10 STM entries
* TrendTracker for emotional context, now with **28d** (or **6d Ekman**) emotion vectors and full trend stats

---

## STM (Short-Term Memory)

* STM now stores up to **10 entry-pairs** `<span>[userEntry, chatbotEntry]</span>`, where each entry consists of **both the raw text** and a **64d cnnVector**:
  * `<span>userEntry = (rawText, cnnVector)</span>`
  * `<span>chatbotEntry = (rawText, cnnVector)</span>`
* Each entry may be a full paragraph or more.
* When STM reaches 10 entry-pairs (buffer full), it is **summarized into a new LTM block** and reset.
* The **cnnVector** for each entry is produced ONCE per entry, via the character-level CNN (see `<span>cnn_model.md</span>`).
* All further processing (including word embeddings) happens at the HAN level, but the STM only stores (rawText, cnnVector) pairs for each entry.

---

## LTM (Long-Term Memory)

* Stores up to **10 blocks** (FIFO buffer).
* Each block:
  * 5–10 sentence seq2seq summary of the last 10 STM entry-pairs (rawText, optionally including cnnVector info)
  * 128d or 256d dense vector representation (for retrieval/attention)
  * Optionally includes timestamp, metadata, and average emotional state

---

## TrendTracker

* Now maintains a full **204d vector** per user entry:
  * `<span>[current_emotion_vector (28d), current_ekman_vector (6d), current_emotion_1st_deriv (28d), current_ekman_1st_deriv (6d), current_emotion_2nd_deriv (28d), current_ekman_2nd_deriv (6d), ema_emotion_vector (28d), ema_ekman_vector (6d), ema_emotion_1st_deriv (28d), ema_ekman_1st_deriv (6d), ema_emotion_2nd_deriv (28d), ema_ekman_2nd_deriv (6d)]</span>`
* Rolling buffer of the **last 10 user entries** (chatbot entries are NOT tracked).
* Human-readable summary of each row includes:
  * Top current Ekman category, top 4 current emotions
  * Top EMA Ekman, top 4 EMA emotions
* Confidence scores for each can be included if desired (optional, not part of core vector).

---

## Data Flow

1. **New user input:**
   * Processed via CNN → `<span>(rawText, cnnVector)</span>` tuple
   * Appended to STM
   * TrendTracker updates: full 204d vector calculated for user input
   * If chatbot responds, their output also processed via CNN and appended to STM
   * When STM is full (10 pairs), **STM passed to LTM summarizer**
2. **After STM summary:**
   * LTM block replaces oldest if full (FIFO)
   * STM reset for new round of interactions

---

## Output/Interface

* Provides last 10 entry-pairs (STM, as [(rawText, cnnVector), ...])
* Provides last 10 summary blocks (LTM, text + vectors)
* Provides full TrendTracker history (204d vectors, summary columns)

---

## Notes

* STM and LTM window sizes can be tuned, but 10 is the current default (based on HAN and empirical design).
* STM now always stores BOTH rawText and cnnVector per entry.
* TrendTracker now outputs a full 204d feature vector per entry.
* All emotion vectors can be 28d (fine) or 6d (Ekman), as preferred by the downstream component.
* This module is designed for easy extension to future multimodal or multi-user memory use cases.
