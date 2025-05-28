
# Project Therapy — Structure Description

## High-Level Overview

**Project Therapy** is a modular, multi-stage natural language understanding and generation system designed to classify user emotion and generate emotionally aware therapeutic chatbot responses.It is built around three core modules:

1. **Emotion Classifier:**
   - Sentence-level emotion classification via a stacked BiLSTM with attention, using SBERT sentence embeddings as input.
2. **Memory Modules:**
   - Short-Term Emotion Trend: Rolling trend via Exponential Moving Average (EMA) of softmax outputs.
   - Long-Term Conversational Memory: Sequence of recent message embeddings, periodically summarized by a seq2seq model.
3. **Chatbot Engine:**
   - GPT-style decoder-only transformer, conditioned on current input, memory states, and a strategy prompt.

---

## Data Flow and Component Roles

1. **Input:**

   - User message(s) (potentially multi-sentence).
2. **Sentence Embedding:**

   - Each sentence is embedded using a pretrained **SBERT** model.
   - Output: Sequence of dense sentence vectors (one per sentence).
3. **Emotion Classifier:**

   - Inputs the sequence of SBERT embeddings.
   - Architecture:
     - **Stacked BiLSTM layers** to contextualize sentence order and flow.
     - **Attention layer** to weight sentence contributions.
     - **Dense layers** for classification.
     - **Softmax output** gives emotion probabilities for each message.
4. **Short-Term Emotion Trend Module:**

   - Maintains a rolling vector trend of recent emotions using **EMA** (Exponential Moving Average).
   - Optionally, this may be replaced with a lightweight **BiGRU** for learnable trends in future iterations.
   - Output: Current “trend” emotion (for tone modulation).
5. **Long-Term Conversational Memory:**

   - Stores the last *N* (e.g., 50) message embeddings (from SBERT).
   - Periodically, a **seq2seq (encoder-decoder) transformer** summarizes a chunk (e.g., every 10) of messages into a “block,” compacting memory usage.
   - The long-term memory contains several recent blocks + current messages.
6. **Decision-Maker / Strategy Prompt Generator:**

   - Accepts the current user input, emotion classification, trend, and memory blocks.
   - Generates a strategy prompt for the chatbot (e.g., encouraging, validating, reflective, directive, etc.).
7. **Chatbot Engine:**

   - **Decoder-only transformer (GPT-style)**.
   - Takes as input:
     - Current user message
     - Short- and long-term memory context
     - Generated strategy prompt
   - Outputs a final, emotionally aware, context-sensitive reply.

---

## Summary Flow (Bulleted)

- User input → SBERT sentence embeddings
- Embeddings → BiLSTM-based emotion classifier (softmax)
- Softmax outputs update EMA for trend tracking
- Embeddings are added to long-term memory; seq2seq compresses memory blocks as needed
- Decision-maker generates prompt based on current input, emotion, trend, memory
- GPT-style chatbot generates response, conditioned on all of the above

---

## Notes

- All modules are modular—can be swapped or upgraded independently.
- SBERT is used **only for embedding**; emotion classifier and chatbot are trained separately.
- Short-term and long-term memory allow for trend detection and context persistence, critical for therapeutic conversation.
- Future upgrades may add:
  - More sophisticated trend modeling (BiGRU or even transformer trend tracker)
  - Persona/context adaptation in the chatbot
  - Multilingual or multimodal support

---
