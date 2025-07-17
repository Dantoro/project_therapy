# Character-Level CNN Structure Model

**Major Revision: 2025-07-16**

---

## Overview

This document describes the character-level convolutional neural network (CNN) architecture and its integration into the Hierarchical Attention Network (HAN) within Project Therapy. This regularized, trainable CNN models character-level nuances in text, supplementing higher-level word embeddings with information about spelling, writing style, punctuation, and internet/social media language. The CNN is now a full part of the HAN, with its weights tuned end-to-end along with the rest of the model.

---

## Purpose

The CNN is designed to extract stylistic, orthographic, and emotional cues from text that word-level embeddings cannot capture. These include:

* Typos, creative spellings, and keyboard smashes
* Emoticons, emojis, and special characters
* Inconsistent spacing and punctuation
* Patterns in capitalization and emphasis
* General markers of distress, urgency, or informality

---

## Placement in the Pipeline

* The CNN is** ****not** a preprocessing step any longer.
* Instead, it is called on-the-fly as part of the HAN for every entry in the Short-Term Memory (STM) buffer (user and bot entries alike).
* The CNN's weights are trained jointly with the rest of the HAN, so its output will change and improve over time.
* The STM now only stores raw text entries.

---

## Architecture

* **Tokenization:**
  * Each entry is tokenized at the character level (letters, punctuation, whitespace, emojis, etc.).
* **Embedding:**
  * Each character is embedded into a 16d vector (learned during training).
* **Convolutional Filters:**
  * Three parallel 1D convolutional layers:
    * 21 filters of width 3 (trigrams)
    * 21 filters of width 5 (pentagrams)
    * 22 filters of width 7 (heptagrams)
* **Pooling:**
  * Global max pooling across sequence for each filter.
* **Output:**
  * The resulting vectors from each filter are concatenated into a fixed-size 64d/128d/200d vector (final dimensionality configurable, currently 200d recommended).

---

## Output and Integration

* For each STM entry (user or bot), the CNN produces a single vector (e.g., 200d).
* During HAN construction,** ****every word** in that entry is assigned the same CNN vector, concatenated with its unique GloVe (300d) and word2vec (500d) vectors, forming a 1000d embedding per word.
* The 1000d word vector is then projected to 512d via a learned dense layer at the start of the HAN.
* The CNN parameters are updated as part of HAN training.

---

## Rationale for Joint Training

* Previously, the CNN ran as a static feature extractor and cached its outputs, but this missed out on useful adaptation.
* With joint training, the CNN can:
  * Learn which stylistic/textual cues matter for context and emotional understanding
  * Adapt to the user's unique language and writing habits over time
  * Increase robustness to spelling errors, neologisms, and informal language
* This change simplifies the STM (now raw text only), and better integrates character-level features into the HAN's deep context modeling.

---

## Notes

* Previous versions cached and reused CNN vectors; this is now deprecated.
* This CNN is conceptually similar to approaches for noisy/real-world text in clinical NLP and social media analysis, but is trained end-to-end for the context-sensitive goals of Project Therapy.
* See han_model.md for full details on the hierarchy and how these embeddings are used.
