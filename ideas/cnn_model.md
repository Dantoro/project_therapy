
# Character-Level CNN Model

**Last updated: 2025-07-25**

---

## Key Points

* The CNN is a fully internal, end-to-end trainable component of the HAN (no longer precomputes/caches outputs)
* All weights are updated jointly during HAN training, except when frozen during initial epochs
* The CNN models orthographic/stylistic information not captured by word-level embeddings: spelling, repetition, punctuation, emoji, social/informal cues, etc.
* Output is a 200d vector for each utterance (identical for every word within that utterance)
* Previous versions with output caching or independent learned embeddings are now deprecated

---

## Overview

This document describes the character-level convolutional neural network (CNN) used in Project Therapy’s Hierarchical Attention Network (HAN). The CNN augments word-level semantic vectors with rich character-level stylistic information, crucial for mental health NLP, which often involves spelling errors, internet-speak, emotional emphasis, and diverse user expression.

---

## Architecture

* **Tokenization:**
  * Utterance split into characters (letters, whitespace, emoji, punctuation, etc)
* **Character Embedding:**
  * Each character mapped to a trainable 16d vector
* **Convolutions:**
  * Parallel 1D Conv layers:
    * 21 trigram filters (width=3)
    * 21 pentagram filters (width=5)
    * 22 heptagram filters (width=7)
* **Global Max Pooling:**
  * Across the output of each filter
* **Output:**
  * 200d vector (concatenation of all pooled filter outputs)

---

## Placement in Pipeline

* **Integrated directly as the first layer of the HAN**
* At each HAN call (training or inference):
  * For every utterance (user/bot) in the STM, run through the CNN
  * Each word in the utterance is then assigned this CNN output vector (shared for the entire utterance)
  * Concatenate with GloVe and word2vec embeddings for 1000d per word
  * Projected to 512d by dense layer

---

## Training

* **Standalone Pretraining:**
  * Train as emotion classifier (GoEmotions, one label per row, min 10 epochs, early stop after 10, max 20 epochs)
* **Joint Training (HAN):**
  * CNN weights frozen for first 3 epochs of HAN
  * CNN weights unfrozen for epochs 4–5 (reduced learning rate), then early stopping (max 10 epochs)
  * Best weights restored via validation loss
* **Fine-tuning:**
  * Optionally, allow further joint fine-tuning on clinical/therapy superset during HAN training

---

## Output/Integration

* For each utterance in STM, a single 200d vector output
* Every word in utterance receives same 200d vector, concatenated with:
  * GloVe (300d, general)
  * word2vec (500d, custom-trained clinical+emotional dialogue superset)
* Output: 1000d per word, projected to 512d for downstream HAN layers

---

## Change Log

* 2025-07-25: Major update—clarified joint training, no more caching, explicit connection to HAN, fine-tuning recommendations
* 2025-07-16: (previous major version—moved CNN internal to HAN, removed separate learned embedding, finalized filter structure/dimensions)
* Pre-2025-07: (deprecated) Caching, independent output, decoupled training

---

See han_model.md for model hierarchy and training details.
