                                     ┌──────────────────────────┐
                                     │      User Input          │
                                     └──────────────────────────┘
                                                 │
                                                 ▼
                                  ┌───────────────────────────────────────────┐
                                  │ 1. Emotion Classifier                     │
                                  │   (Deep BiLSTM + Attention)               │
                                  │ ┌ Sentence embeddings (SBERT/BERT)        │
                                  │ ├ Stacked BiLSTM layers + Attention       │
                                  │ └ (No transformer layer inside model)     │
                                  │                                           │
                                  │  Outputs:                                 │
                                  │    • Emotion label (softmax)              │
                                  │    • Document vector (embedding)          │
                                  └───────────────────────────────────────────┘
                                                 │
                              ┌──────────────────┴──────────────┐
                              │                                 │
                              ▼                                 ▼
        ┌───────────────────────────────┐        ┌───────────────────────────┐
        │2. Short-Term Emotion Memory   │        │3. Long-Term Semantic      │
        │   (rolling buffer of last 10) │        │   Conversation Memory     │
        │ • Implemented via BiGRU over  │        │   (queue of last 20–50    │
        │   softmax-prob vectors        │        │   document embeddings)    │
        └───────────────────────────────┘        └───────────────────────────┘
                              │                                 │
                              └──────────────────┬──────────────┘
                                                 ▼
                                  ┌───────────────────────────────┐
                                  │4. Seq2Seq Decision Maker      │
                                  │  (T5/BART-style)              │
                                  │ • Input: emotion label +      │
                                  │   short-term trend + long-term│
                                  │   context vec                 │
                                  │ • Output: natural-language    │
                                  │   “strategy” prompt:          │
                                  │     – tone guide              │
                                  │     – urgency/inquiry style   │
                                  └───────────────────────────────┘
                                                 │
                                                 ▼
                                  ┌───────────────────────────────┐
                                  │5. Chatbot Engine              │
                                  │  (GPT-style autoregressive)   │
                                  │ • Input: raw text + strategy  │
                                  │   prompt + long-term context  │
                                  │ • Output: actual reply text   │
                                  └───────────────────────────────┘
                                                 │
                                                 ▼
                                     ┌──────────────────────────┐
                                     │      Bot Response        │
                                     └──────────────────────────┘
