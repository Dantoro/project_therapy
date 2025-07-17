# Hierarchical Attention Network (HAN) Model

**Last updated: 2025-07-16**

---

## Overview

This document describes the architecture of the Hierarchical Attention Network (HAN) for Project Therapy, reflecting all recent changes. The HAN now includes an integrated, tunable character-level CNN as its first processing layer, enabling per-character, per-word, per-sentence, and per-entry representation learning from raw conversation text. There are no longer separate “learned embeddings”—all trainable features are learned as part of the HAN.

## Embedding Sources

Each word in each STM entry is represented by the concatenation of:

* **GloVe embedding** : 300d (pretrained on general English)
* **word2vec embedding** : 500d (custom-trained on clinical dialogue)
* **CNN embedding** : 200d (trainable character-level vector, learned as part of the HAN)

**Total: 1000 dimensions per word**

## Full Model Structure

### PREPROCESSING:

* **1. Character-level CNN** (per-entry, first layer of HAN):
  * Input: Entry text tokenized at the character level
  * Embedding: 16d trainable vector per character
  * Convolutions: Parallel 1D filters (recommended: widths 3, 5, 7; total 200 filters)
  * Global max pooling over each filter
  * Output: 200d vector summarizing style and character-level patterns
  * Shared across all words in the entry
* **2. Embedding concatenation** :
* For each word: [CNN output (200d)] + [GloVe (300d)] + [word2vec (500d)] → 1000d
* **3. Dense projection** :
* Linear layer, projects 1000d → 512d (includes batch normalization, L2 regularization)

### WORD-LEVEL (512d per word):

* **4. Word BiLSTM 1** : Bidirectional LSTM, hidden size 512 (with recurrent dropout and layer norm)
* **5. Highway 1** : Enables flexible information routing
* **6. Dropout 1** : Standard dropout
* **7. Word BiLSTM 2**
* **8. Word attention** : Multi-head attention aggregates word context into sentence vectors

### SENTENCE-LEVEL (512d per sentence):

* **9. Sentence BiLSTM 1** : Processes sequence of sentence vectors within each entry
* **10. Highway 2**
* **11. Dropout 2**
* **12. Sentence BiLSTM 2**
* **13. Sentence attention** : Multi-head attention over sentences in the entry, outputs entry vector

### ENTRY-LEVEL (512d per entry):

* **14. Entry BiLSTM 1** : Processes sequence of entry vectors across STM buffer
* **15. Highway 3**
* **16. Dropout 3**
* **17. Entry BiLSTM 2**
* **18. Entry attention** : Multi-head attention over entry representations

### FINAL PROJECTION:

* **19. Dropout 4** : Dropout before output layer (rate ≈ 0.2–0.3 recommended)
* **20. Output layer (Dense 512 → 256)** : Produces final context vector for DecisionMaker

---

## Key Points

* All embeddings (CNN, GloVe, word2vec) are concatenated per word; the CNN vector is the same for every word in the entry
* CNN output is not cached; it is recalculated every timestep as part of HAN training/inference
* The HAN provides context at character, word, sentence, entry, and document (STM buffer) levels
* All trainable features (CNN, BiLSTMs, dense layers) are updated together during end-to-end training

---

## Change Log

* 2025-07-16: Full HAN update—character-level CNN is now internal, learned embeddings removed, embedding dimensions finalized
* 2025-07-07: (legacy) Used cached CNN, separate learned embedding, different dimensions
