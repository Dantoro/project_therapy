# Memory Module Logic

## Overview

This module manages all short- and long-term memory for the conversational agent, providing context to the DecisionMaker and Chatbot.

**Key features:**

- 10-turn Short-Term Memory (STM)
- 10-block rolling Long-Term Memory (LTM), with each block summarizing the last 10 STM entries
- TrendTracker for emotional context, now with **28d** emotion vectors

## STM (Short-Term Memory)

- Stores up to **10 entry-pairs**: `[userEntry, chatbotEntry]`
  - Each entry may be a full paragraph or more
  - Oldest entry-pair dropped when full and new input arrives
- At capacity, **STM is summarized** into a new LTM block and reset

## LTM (Long-Term Memory)

- Stores up to **10 blocks** (FIFO buffer)
- Each block:
  - 5–10 sentence seq2seq summary of the last 10 STM entry-pairs
  - 128d dense vector representation (for retrieval/attention)
  - Optionally includes timestamp, metadata, and average emotional state

## TrendTracker

- Receives 28d output, 1st & 2nd derivatives, and EMA vectors from EmotionClassifier
- Maintains rolling buffer of last 10 states (fully vectorized)
- EMA and derivatives also stored for 10 turns (each 28d)

## Data Flow

1. **New user input:**

   - Appended to STM (with paired chatbotEntry if available)
   - Full STM (10 entry-pairs) passed to LTM summarizer at buffer capacity
   - All 28d emotion vectors and trend features updated for use by DecisionMaker/Chatbot
2. **After STM summary:**

   - LTM block replaces oldest if buffer full (FIFO)
   - STM is reset for new set of interactions

## Output/Interface

- Provides last 10 entry-pairs (STM)
- Provides last 10 summary blocks (LTM, text + vectors)
- Provides full trend history (buffered vectors, derivatives, EMA)

## Notes

- STM and LTM window sizes can be tuned, but 10 is the current default (and recommended based on current HAN design and research)
- All vectors and trend calculations now **28d**
- Designed for easy extension to future multimodal or multi-user memory use cases
