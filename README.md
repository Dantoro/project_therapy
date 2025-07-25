
# Project Therapy – README

**Last updated: 2025-07-25**

---

## Overview

Project Therapy is a multi-component, research-oriented mental health chatbot system. Its architecture is built for real-world, privacy-conscious, emotionally intelligent conversation and ongoing user support. All modules are modular, extensible, and focus on explainable, context-aware behavior.

## Core Pipeline

1. **User Prompt** →
2. **EmotionRegressor** : Dual transformer regression on latest input (35d: 28 GoEmotions + 7 Ekman categories), outputting mood/confidence vector
3. **TrendTracker** : Tracks 10 most recent mood_vectors + derivatives (full emotional trend, 210d)
4. **STM** : Short-term memory buffer of 10 user-chatbot utterance pairs (raw text only)
5. **HAN** : Hierarchical Attention Network over STM + new prompt, contextually aware, trained end-to-end with internal char-level CNN, GloVe, word2vec
6. **LTM** : Long-term memory—rolling buffer of 10 seq2seq summaries (dense vectors + SOAP notes)
7. **ThreatAssessor** : Safety layer (self-harm, risk, escalation)
8. **DecisionMaker** : Aggregates outputs from HAN, TrendTracker, ThreatAssessor, and LTM for chatbot planning
9. **Chatbot** : Decoder-only LLM (MentalGPT preferred) generates response
10. **Cycle continues**

## Key Model Components

### EmotionRegressor

* Two transformers: one GoEmotions-based, one Ekman-based
* Outputs 35d mood vector for current prompt; combines with rolling buffer for 210d TrendTracker feature
* See emotion_regressor.md for details

### HAN (Hierarchical Attention Network)

* End-to-end: char-level CNN → GloVe (300d) → custom word2vec (500d) → Dense (1000d→512d)
* Stacks of BiLSTM and multi-head attention over words, sentences, utterances
* Operates live on STM (raw text); no embedding caching
* Trained jointly with CNN on both GoEmotions (pretrain) and custom dialogue superset (fine-tune)
* See han_model.md and cnn_model.md for technical breakdowns

### Memory

* **STM:** 10 most recent user+chatbot utterance pairs, raw text only
* **LTM:** 10 block FIFO (summary + dense vector)
* See memory_module_logic.md

### TrendTracker

* 210d vector: [current, EMA, 1st and 2nd derivatives of mood vectors]
* Only tracks user utterances (not chatbot)

### Chatbot (LLM)

* Decoder-only transformer (MentalGPT or compatible LLM)
* Trained/fine-tuned on the same dialogue superset as word2vec/HAN

---

## Dialogue Dataset (Custom Superset)

* Target: 25,000 context-response pairs
* 70% mental health (patient-therapist/psychologist/counselor)
* 15% clinical (patient-doctor, symptoms/meds/records)
* 10% emotionally-charged (peers/friends: venting + consoling)
* 5% generic dialogue (non-social-media, e.g. TV/movie scripts)
* Used for word2vec, HAN, chatbot

---

## Project Goals

* Realistic, emotionally supportive chatbot for mental health
* Modular, privacy-focused, and extensible design
* Multi-granular emotion tracking and contextual memory
* Explainable architecture for research, portfolio, and potential future publication

---

## Change Log

* 2025-07-25: Major update for new STM/LTM/HAN conventions, batch processing, modular pipeline, dialogue superset definition, documentation formatting
* 2025-07-16: STM/HAN logic rewrite, emotion tracking clarification
* 2025-06: (Legacy) Multiple architecture revisions, pre-transformer pipeline

---

*See han_model.md, cnn_model.md, and memory_module_logic.md for in-depth architecture. For dataset details, see /datasets/custom_corpus/*
