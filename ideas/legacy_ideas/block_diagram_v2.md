 ┌───────────────┐        ┌──────────────────────────┐
 │ User Message  │───────▶│ Emotion Classifier       │
 │  (sentence/   │        │ (Encoder-only Transformer│
 │   paragraph)  │        │   e.g. BERT/SBERT)      │
 └───────────────┘        └─────────┬───────────────┘
                                    │
                                    │
           ┌────────────────────────┼────────────────────────────┐
           │                        │                            │
           ▼                        ▼                            ▼
 ┌─────────────────┐     ┌─────────────────────────┐  ┌─────────────────────┐
 │ One-hot Emotion │     │   Sentence Embedding    │  │ Add to Short-Term   │
 │ Classification  │     │  (vector from BERT)     │  │ Emotion Memory      │
 └─────────────────┘     └─────────────────────────┘  │   (EMA/BiGRU, last │
           │                   │                      │   10 emotions)      │
           │                   │                      └─────────────────────┘
           │                   ▼
           │         ┌────────────────────────────┐
           │         │ Add to Long-Term Memory    │
           │         │  (stores recent sentences) │
           │         └───────────┬────────────────┘
           │                     │
           │      Every N sentences/turns:        │
           │      ┌─────────────────────────────┐ │
           └─────▶│ Seq2Seq Summarizer         │◀┘
                  │ (Encoder-Decoder: T5, BART)│
                  └──────────┬─────────────────┘
                             ▼
               ┌─────────────────────────────┐
               │  Summarized "Block"         │
               │ (represents N messages)     │
               └──────┬──────────────────────┘
                      ▼
            ┌───────────────────────────────┐
            │ Long-Term Memory (sliding     │
            │ window of K summary blocks +  │
            │ recent raw sentences)         │
            └─────────┬─────────────────────┘
                      │
                      ▼
           ┌──────────────────────────────┐
           │ Decision Maker/Strategy      │
           │  (optional)                  │
           └─────────┬────────────────────┘
                     │
                     ▼
           ┌──────────────────────────────┐
           │  Chatbot Engine (GPT-style)  │
           │  (Decoder-only Transformer)  │
           │  Inputs:                     │
           │   - Current message          │
           │   - Short-term emotion trend │
           │   - Long-term memory context │
           │   - Strategy prompt          │
           └──────────┬───────────────────┘
                      │
                      ▼
               ┌───────────────┐
               │   Reply to    │
               │     User      │
               └───────────────┘
