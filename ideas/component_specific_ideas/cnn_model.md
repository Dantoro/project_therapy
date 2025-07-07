# Character-Level CNN Structure Model

**Last updated: 2025-07-07**

---

## Overview

This document describes the character-level convolutional neural network (CNN) architecture and usage within Project Therapy. This lightweight, highly-regularized CNN is designed to capture character-level nuances in text, supplementing higher-level word embeddings with fine-grained information about writing style, spelling, punctuation, and informal language features.

## Purpose

The character-level CNN is introduced to explicitly model and extract stylistic and orthographic features that word-level embeddings cannot capture. These include:

- Typos, slang, and creative spellings
- Emoticons, emojis, and special characters
- Run-on words, split words, and inconsistent spacing
- Patterns in capitalization and punctuation
- General patterns of user text that might indicate distress, urgency, or instability (e.g., keyboard smash, repeated characters)

This approach improves robustness to misspellings, internet slang, and noisy or highly emotional input typical in real-world mental health text.

## Placement in the Pipeline

- **User Inputs:**

  - The CNN processes each new user message immediately after it is received and before further modules (e.g., emotion classifier) operate on the text.
  - Both the raw text and its resulting CNN vector (cnnVector) are stored in the Short-Term Memory (STM) buffer.
- **Chatbot Outputs:**

  - The CNN also processes each new chatbot-generated response at the end of the pipeline, before it is appended to the STM.
- **STM Structure:**

  - Each STM entry thus consists of both the raw text and the corresponding 64-dimensional cnnVector. This structure enables the Hierarchical Attention Network (HAN) to access character-level style information for every entry in the conversational buffer, regardless of whether it originated from the user or the chatbot.
- **HAN Preprocessing:**

  - During each run of the HAN, every word in each STM entry receives a unique 1024-dimensional vector, constructed by concatenating:
    - The 64d cnnVector for that entry (shared across all its words)
    - 300d GloVe embedding (general English)
    - 340d word2vec embedding (clinical dialogue)
    - 320d learned embedding (task-specific, emotion-rich)

---

## Architecture

- **Tokenization:**

  - Input text is tokenized at the character level (including letters, punctuation, emojis, whitespace, etc.).
  - Each character is embedded into a 16-dimensional vector (learned during training).
- **Convolutional Filters:**

  - The embedded sequence is processed in parallel by three sets of 1D convolutional filters:
    - 21 filters of width 3 (trigrams)
    - 21 filters of width 5 (pentagrams)
    - 22 filters of width 7 (heptagrams)
  - All filters have 16 input channels and produce a single output channel each. Filter sizes were chosen to balance short-term character dependencies (typos, local repeats) with slightly longer n-gram patterns (emoji sequences, multi-word interjections).
- **Pooling:**

  - Each filter produces a sequence of activations. Global max pooling is applied to each filter’s output, retaining the most salient activation (highest value) per filter.
  - This results in a 64-dimensional vector summarizing the strongest n-gram pattern detected by each filter across the entry.
- **Output:**

  - The final output is a fixed-size (64d) vector representing the character-level style and orthographic features of the entire entry.

---

## Rationale for Design

- **Why not BiGRU?**

  - Initial designs used a BiGRU to process STM entries at each timestep, but this was computationally expensive and provided marginal benefit over a CNN for capturing typo/orthographic cues. A character-level CNN is significantly faster and easier to interpret, while being robust to variable-length inputs and generalizing well to noisy user text.
- **Why once per entry?**

  - Each entry (user or chatbot) passes through the CNN only once, immediately after creation, and the resulting vector is cached. This ensures that redundant computation is avoided and that character-level information is always available to the HAN without reprocessing entire buffers each step.
- **Why these filter sizes and counts?**

  - Filters of size 3, 5, and 7 efficiently cover the range from micro-patterns (typos, "lol", "omg", common emoji clusters) to slightly longer motifs (keyboard smash, expressive onomatopoeia). The total of 64 filters matches the output dimensionality used in previous BiGRU experiments, for seamless integration with existing preprocessing.

---

## Key Points

- Character-level CNN is a preprocessing step for all entries (user and chatbot), run once per entry.
- Produces a 64d vector encoding character-level style and noise features.
- Combined with GloVe, word2vec, and learned embeddings as input to HAN for deep context modeling.
- Replaces the previous BiGRU character-level approach for better efficiency and similar or improved effectiveness.
- Further technical and implementation details may be tracked in code or supplementary design notes.

---
