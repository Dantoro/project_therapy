# Hierarchical Attention Network (HAN) Model

**Last updated: 2025-07-07**

---

## Overview

This file canonizes the current best design for the Hierarchical Attention Network (HAN) at the core of Project Therapy. The HAN is responsible for deep context modeling of recent conversation history—synthesizing the 21 most recent entries (10 user-bot pairs + latest user input), each entry potentially spanning multiple sentences. This structure enables highly nuanced understanding of patient dialogue, emotional context, and conversational flow, ultimately driving the DecisionMaker and Chatbot modules.

The HAN integrates four sources of embeddings:

- **GloVe**: 300d, trained on general English text (for broad semantic context)
- **word2vec**: 340d, custom-trained on clinical dialogues (for domain-specific, localized meaning)
- **CNN**: 64d, character-level vector to catch typos and gain insight from patterns in writing style (see cnn_model.md).
- **Learned embeddings**: 320d, learned during model training (initialized on GoEmotions dataset)

These are concatenated, forming a 1024-dimensional per-word representation, projected down to 512d for model efficiency.

Key regularization and optimization tools used:

- **L2 regularization** on dense and recurrent layers
- **Batch normalization** after projection and before each major block
- **Layer normalization** within BiLSTM blocks
- **Dropout** at all major hidden stages (word-level, entry-level, additional hidden)
- **Recurrent dropout** inside BiLSTM layers

This deep, regularized, multi-granular HAN provides the main context vector for the DecisionMaker, fused with LTM summaries and trend tracking data for response generation.

---

## Full Model Structure

### PREPROCESSING:

- **1. Input + GloVe (300) + word2vec (340) + CNN (64) + Learned embeddings (320):**

  - All four embedding sources are concatenated for each word (1024d total)
- **2. Dense 1 (Decay 1024 → 512):**

  - Projects concatenated embeddings down to 512d (includes batch normalization, L2 regularization)

### WORD-LEVEL (Steady state at 512):

- **3. Word BiLSTM 1:**
  - BiLSTM (hidden size: 512); recurrent dropout; layer norm
- **4. Highway 1:**
  - Enables information routing, mitigates vanishing gradient
- **5. Dropout 1:**
  - Standard dropout (rate ≈ 0.3–0.5)
- **6. Word BiLSTM 2:**
  - Stacked for increased capacity
- **7. Word attention:**
  - Multi-head attention aggregates word context into entry vectors

### ENTRY-LEVEL (Steady state at 512):

- **8. Entry BiLSTM 1:**
  - Processes sequences of entry vectors across STM
- **9. Highway 2**
- **10. Dropout 2**
- **11. Entry BiLSTM 2**
- **12. Entry attention:**
  - Multi-head attention over entry representations

### ADDITIONAL HIDDEN LAYERS:

- **13. Dense 3 (decay 512 → 256)**
- **14. Highway 3**
- **15. Dropout 3**
- **16. Dense 4 (decay 256 → 128)**

### RESULTS:

- **17. Output layer (128d):**
  - Main summary/context vector for DecisionMaker/Chatbot

---

## Layer-wise Function

- **Input + Embeddings**: Brings together general, domain, typo-robust, and trainable representations for rich word-level context.
- **Projection**: Reduces to a tractable size while retaining as much information as possible.
- **Word-level BiLSTMs + attention**: Capture intra-entry dependencies and focus attention on key words per entry.
- **Entry-level BiLSTMs + attention**: Model sequence of conversation turns, focus on most relevant exchanges.
- **Highways**: Allow the network to dynamically route information across layers.
- **Dropout/regularization**: Prevent overfitting, encourage robust learning.
- **Final output**: Fixed-size, context-rich vector handed off to downstream modules.

---

## PyTorch Visualization Example

While PyTorch does not have a direct `model.summary()` equivalent, you can use [torchsummary](https://github.com/sksq96/pytorch-summary) or [torchinfo](https://github.com/TylerYep/torchinfo) for similar output. Example:

```python
from torchinfo import summary
model = HAN(...)  # your HAN instance
summary(model, input_size=(batch_size, seq_len, word_len))
```

**Example (illustrative only):**

====================================================================================
Layer (type:depth-idx)                    Output Shape              Param #
====================================================================================
Embedding (GloVe)                         [batch, seq, 300]         0 (frozen)
Embedding (word2vec)                      [batch, seq, 340]         0 (frozen)
CNN (char-level)                          [batch, seq, 64]          65,000
LearnedEmbedding                          [batch, seq, 320]         ~2M
Dense (proj)                              [batch, seq, 512]         524,800
BatchNorm1d                               [batch, seq, 512]         1,024
WordBiLSTM-1                              [batch, seq, 512]         2M
Highway-1                                 [batch, seq, 512]         263,168
Dropout                                   [batch, seq, 512]         0
WordBiLSTM-2                              [batch, seq, 512]         2M
WordAttention                             [batch, 512]              262,144
EntryBiLSTM-1                             [batch, STM, 512]         2M
Highway-2                                 [batch, STM, 512]         263,168
Dropout                                   [batch, STM, 512]         0
EntryBiLSTM-2                             [batch, STM, 512]         2M
EntryAttention                            [batch, 512]              262,144
Dense-3                                   [batch, 256]              131,328
Highway-3                                 [batch, 256]              131,328
Dropout                                   [batch, 256]              0
Dense-4                                   [batch, 128]              32,896
Output (final)                            [batch, 128]              varies
====================================================================================

---

## Notes

- This design is subject to change as more empirical results become available.
- For maximal clarity, keep all dimensionality and data source details up to date in this file.
- Document major architectural changes as a new dated section at the bottom of this file.
