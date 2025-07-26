# Emotional Support Conversations (ESConv) – Subset Extraction README

**Last updated: 2025-07-25**

---

## What is ESConv?

The ****Emotional Support Conversations (ESConv)** dataset is a large-scale, multi-turn dialogue corpus originally collected to facilitate research on emotional support in conversational AI. It contains over a thousand annotated conversations between a “seeker” (person experiencing distress or seeking help) and a “supporter” (a volunteer providing emotional support). Each conversation is tagged with a primary** `emotion_type` (e.g., anxiety, sadness, anger) and often covers a wide range of real-world emotional challenges.

* **Source:** https://github.com/thu-coai/Emotional-Support-Conversation

---

## How was this subset created?

This repository includes a **highly curated subset** of the ESConv data, extracted and transformed for use as emotionally charged, real-world dialogue for training/evaluating conversational AI (especially as part of a broader dialogue superset for Project Therapy).

### Sampling Protocol

* Only conversations where the **seeker** speaks first were included (for clean context-response structure).
* A target number of conversations was set for each emotion type, sampled at random *without replacement* from the full set:
  * anxiety: 40
  * depression: 40
  * sadness: 40
  * anger: 30
  * fear: 20
  * shame: 11
  * disgust: 10
  * nervousness: 6
  * jealousy: 1
  * (pain/guilt were excluded due to lack of eligible samples)
* The resulting subset comprises **198 full dialogues** with this emotion distribution.

### Preprocessing and Transformation

1. **Speaker turn concatenation:** Consecutive utterances by the same speaker were merged into a single turn (to prevent split/incomplete thoughts).
2. **Context-Response extraction:** Each conversation was decomposed into dyadic pairs:
   * Each  `Context` is a seeker utterance (after merging).
   * Each corresponding `Response` is the immediate next supporter utterance.
   * Only clear seeker→supporter exchanges were retained; all others were discarded.
3. **Cleaning:** HTML artifacts, escape characters, and line breaks were removed/normalized.
4. **Result:** The final dataset consists of **2255 context-response pairs**, evenly sourced from across the targeted emotions, and suitable for emotionally-rich, conversational modeling.

---

## Intended Use

* This subset is designed for the *emotionally-charged dialogue* portion of the Project Therapy dialogue superset (10% of the 25k total target set).
* It is not intended as a clinical/therapeutic dataset, but rather as realistic, everyday conversation centered around emotional support, empathy, and peer-to-peer comfort.

---

## Change Log

* 2025-07-25: Initial extraction and transformation, context-response format, with explicit emotion balancing.

---

For further info or reproduction code, see `emotional_casual_chat_data.ipynb` or contact Daniel Santoro.
