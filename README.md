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

### TrendTracker

* Performs mathematical analysis on EmotionRegressor output to expand emotional analysis of a single input into deep analysis of emotion-over-time.
* 210d vector: [current, EMA, 1st and 2nd derivatives of mood vectors]
* Only tracks user utterances (not chatbot)

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
* **Clipboard:** Uses STANZA to create lookup-dictionary of all important entities, dependencies, and relationships, along with a time-stamped list of all occurences of said entities.

### ThreatAssessor

* Looks at only the most recent userPrompt.
* Urgency classifier as an early warning system.

### DecisionMaker

* Takes in output from all prior components, using a combination of rule-based, retrieval-based, and possibly decision tree-based algorithms to determine how the Chatbot will respond.

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

## Licensing & Attribution

This repository contains code and datasets under a mix of open (MIT, Apache 2.0, CC0) and research/noncommercial licenses (e.g., Creative Commons BY-NC-SA 4.0).

* **Code** is licensed under the MIT License (see LICENSE.md).
* **Datasets** are individually licensed. Some are public domain or MIT; others are restricted to research and noncommercial use.
* If you use any data, models, or code from this repository in research or publications, please see [CITATIONS.md]()for proper attribution.

**Summary of included datasets/models:**

* Emotional Support Conversations ([ESConv](https://github.com/thu-coai/Emotional-Support-Conversation)): CC BY-NC 4.0 (research/noncommercial only)
* Counsel Chat ([Counsel Chat](https://huggingface.co/datasets/nbertagnolli/counsel-chat)): MIT License
* NLP Mental Health Conversations ([Kaggle](https://www.kaggle.com/datasets/thedevastator/nlp-mental-health-conversations)): CC0 Public Domain
* MentalChat16K ([Hugging Face](https://huggingface.co/datasets/ShenLab/MentalChat16K)): Research use only (see dataset page for details)
* PAIR Dataset ([PAIR - UMichigan](https://lit.eecs.umich.edu/downloads.html#PAIR)): Research use only (see original** **[EMNLP 2022 paper](https://lit.eecs.umich.edu/files/min_pair_2022.pdf))
* Depression Detection ([Kaggle](https://www.kaggle.com/datasets/ziya07/depression-detection)): CC0 Public Domain
* AnnoMI ([Kaggle](https://www.kaggle.com/datasets/rahulbaburaj/annomi)): Citation required; see dataset page.
* GoEmotions ([Google Research](https://github.com/google-research/google-research/tree/master/goemotions)): Apache 2.0 License
* ZahrizhalAli Mental Health Conversational ([Hugging Face](https://huggingface.co/datasets/ZahrizhalAli/mental_health_conversational_dataset)): Intended for research, check Hugging Face for details.
* Stanza ([Stanford NLP](https://stanfordnlp.github.io/stanza/)): Apache 2.0 License

See [LICENSE.md](LICENSE.md) for full details and attributions.

---

## Change Log

* 2025-07-25: Major update for new STM/LTM/HAN conventions, batch processing, modular pipeline, dialogue superset definition, documentation formatting
* 2025-07-16: STM/HAN logic rewrite, emotion tracking clarification
* 2025-06: (Legacy) Multiple architecture revisions, pre-transformer pipeline

---

*See han_model.md, cnn_model.md, and memory_module_logic.md for in-depth architecture. For dataset details, see /datasets/custom_corpus/*
