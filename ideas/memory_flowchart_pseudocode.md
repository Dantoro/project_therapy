# Memory Flowchart Pseudocode – Project Therapy

## Overview (Plain English)

This document sketches how Project Therapy’s **multi-stage memory architecture** operates during a conversation.

- **Trend Tracker**: Keeps a rolling “emotional trend” based on the last 10 user inputs, using an exponential moving average (EMA). It updates every turn, always reflecting the most recent context.
- **Short-Term Memory (STM)**: Temporarily stores up to 10 pairs of (user input, chatbot response). At every turn, the entire STM buffer is analyzed by a BiGRU to create a rich local context. Once STM is full (10 pairs), it is summarized by a sequence-to-sequence model (seq2seq) into a compact summary “block” for long-term storage—then STM is emptied.
- **Long-Term Memory (LTM)**: Holds up to 5 of these summary blocks, representing the broader history of the session. As new blocks are added, the oldest are dropped (rolling buffer).

At each turn, the **chatbot’s response is generated based on**:

- The current emotional trend (from EMA)
- The detailed recent context (from BiGRU over STM)
- The overall session history (LTM summary blocks)

This structure allows the system to be *responsive to immediate emotion, sensitive to recent dialogue, and aware of the session’s big picture*—all with efficient, bounded memory.

Simply put: chatbot_response = autoregressor(LTM_blocks + STM_pairs, trend_tracker_vector)

Below, see the actual pseudocode logic for implementation.

## Initialization

trend_tracker = []      # Rolling buffer, max_len = 10
stm_buffer    = []      # Short-term memory buffer, max_len = 10 (FILL & CLEAR)
ltm_buffer    = []      # Long-term memory buffer, max_len = 5  (ROLLING)

## Per Turn (every user input/response pair)

for each (user_input, chatbot_response):

    # --- 1. Emotion Trend Tracker (rolling) ---
    emotion_score = classify_emotion(user_input)  # e.g., via autoencoder/HAN
    if len(trend_tracker) == 10:
        trend_tracker.pop(0)            # Remove oldest if full
    trend_tracker.append(emotion_score)
    trend_trend = update_ema(trend_tracker)  # Update EMA (can be in-place)

    # --- 2. Short-Term Memory (STM: fill then clear) ---
    stm_buffer.append((user_input, chatbot_response))

    # Run BiGRU (or similar) on*entire* current STM buffer
    stm_context = bigru(stm_buffer)

    # --- 3. Check for STM full (time to summarize to LTM) ---
    if len(stm_buffer) == 10:
        # Summarize STM to one "block" via seq2seq
        summary_block = seq2seq(stm_buffer)
        # --- 4. Long-Term Memory (LTM: rolling) ---
        if len(ltm_buffer) == 5:
            ltm_buffer.pop(0)            # Remove oldest if full
        ltm_buffer.append(summary_block)
        # Clear STM buffer for next batch
        stm_buffer = []

    # --- 5. Chatbot Generation ---
    # At every turn, generate chatbot reply conditioned on:
    # - trend_trend (from EMA)
    # - stm_context (BiGRU output, latest STM buffer)
    # - ltm_buffer (sequence of summarized history blocks)
    chatbot_response = autoregressive_chatbot(
        user_input,
        trend_trend,
        stm_context,
        ltm_buffer
    )
