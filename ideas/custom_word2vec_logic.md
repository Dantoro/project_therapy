# Custom word2vec Embeddings

**Last updated: 2025-07-16**

---

## Purpose

This document explains the design, curation, and preparation of the custom word2vec embeddings used in Project Therapy. The goal is to create word-level representations that reflect authentic clinical language in mental health counseling, providing more accurate context for dialogue-based models than general-purpose embeddings (like GloVe) or embeddings trained on informal/social media data.

## Why Not GloVe Alone?

While GloVe vectors are powerful for broad semantic meaning, they are trained on general English (news, Wikipedia, web) and do not capture the specialized vocabulary, patterns, and context of clinical conversations. Many mental health terms, therapeutic turns of phrase, or nuances of doctor-patient communication are rare or missing in general corpora.

## Why Clinical Dialogue, Not Social Media?

Project Therapy’s Hierarchical Attention Network (HAN) is built to interpret patient-provider dialogues, not tweets or Reddit threads. Training word2vec on real, anonymized clinical conversations ensures the model understands:

* The structure and cadence of therapy and counseling sessions
* Specialist vocabulary (e.g., “change talk”, “reflection”, “MI quality”, symptoms)
* The turn-taking and politeness of therapeutic dialogue (vs. casual online banter)

Social media datasets, even those labeled for emotion, often feature slang, sarcasm, and out-of-domain language, reducing embedding quality for clinical purposes.

## Datasets Used

Custom word2vec embeddings are trained on a blended corpus of four open-source datasets, each chosen for diversity and realism in clinical conversation:

1. **Depression Detection** ([Kaggle](https://www.kaggle.com/datasets/ziya07/depression-detection))
   * 300 pairs of anonymized patient-doctor messages
   * Each row contains a doctor’s input and a patient’s reply, and a binary variable indicating whether or not the patient shows signs of depression
   * Used here for data augmentation; small, but authentic
   * **Format:** Each row contains two separate dialogue utterances (doctor, patient)
2. **Mental Health Counseling Conversations** ([Kaggle](https://www.kaggle.com/datasets/melissamonfared/mental-health-counseling-conversations-k))
   * ~3,500 pairs of real counseling sessions, anonymized
   * Each row: `user` **and** `counselor` columns with conversational turns
   * Focused on a wide range of mental health topics
   * **Format:** Two utterances per row (one from each speaker)
3. **AnnoMI: Annotated Motivational Interviewing Conversations** ([Kaggle](https://www.kaggle.com/datasets/rahulbaburaj/annomi), [GitHub](https://github.com/uccollab/AnnoMI))
   * ~9,700 individual utterances from real motivational interviewing sessions
   * Each row: **`utterance_text` and** `speaker_type` (“therapist” or “client”)
   * Annotated for MI quality and conversational type
   * **Format:** Each row is a single utterance
4. **NLP Mental Health Conversations** ([Kaggle](https://www.kaggle.com/datasets/thedevastator/nlp-mental-health-conversations/data))
   * ~3,500 anonymized counseling dialogues
   * Structure varies: some rows are pairs, some contain grouped turns
   * **Format:** Must be split into single-utterance utterances

## Preprocessing and Corpus Preparation

Each dataset is first split into its constituent conversational utterances. This means:

* For datasets with paired dialogue in one row (Depression Detection, Mental Health Counseling, NLP Mental Health), **split each row into two separate samples** (one for each speaker)
* For datasets with grouped utterances (some rows contain multi-sentence responses), **split into single sentences** for maximal diversity
* For datasets already at the utterance level (AnnoMI), include each row as-is

**Final corpus:**

* Each sample is a single sentence/utterance from a real clinical dialogue, regardless of original dataset format
* All samples are anonymized and stripped of any protected health information
* Duplicates, empty strings, and non-informative responses are removed

## Estimated Corpus Size

Based on available data and after splitting:

* **Depression Detection:** 300 pairs = 600 utterances, further split into sentences = ~800-1,000 samples
* **Mental Health Counseling:** 3,500 pairs = 7,000 utterances, further split = ~8,000-10,000 samples
* **AnnoMI:** ~9,700 utterances (already single sentences)
* **NLP Mental Health Conversations:** 3,500 pairs = 7,000 utterances, further split = ~8,000-10,000 samples
* **TOTAL:** **~26,000 to 30,000+ samples** after full preprocessing

This is a strong size for a domain-specific word2vec, and helps prevent overfitting to any single data source or topic. Additional datasets could be added in the future for even broader coverage.

## Summary

* Custom word2vec embeddings are trained on 26,000-30,000+ real, single-sentence clinical dialogue samples.
* This provides coverage of both therapist and patient language in a variety of mental health contexts.
* Embeddings are used alongside GloVe and a tunable character-level CNN as part of Project Therapy’s HAN for rich, robust representation of every word in conversation.

---

**See also:**

* [han_model.md](han_model.md)
* [cnn_model.md](cnn_model.md)
* Individual dataset READMEs for more format/annotation details
