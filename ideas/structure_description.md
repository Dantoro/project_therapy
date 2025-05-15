### Module Roles in Brief

1. **Emotion Classifier (HAN + Transformer)**
   * Deep, bidirectional LSTMs + word/sentence attention
   * Augmented with a light Transformer‐encoder at the sentence level
   * Produces both a discrete emotion label and a dense document embedding
2. **Short-Term Emotion Memory**
   * Keeps the last ~10 emotion softmax vectors
   * Runs a small BiGRU (or similar) over them to capture trend features
3. **Long-Term Conversational Memory**
   * Stores the last ~20–50 document embeddings
   * Provides semantic context continuity for the chatbot
4. **Seq2Seq Decision Maker**
   * A T5/BART‐style encoder–decoder
   * Takes emotion label + emotion trend + semantic context
   * Generates a *strategy prompt* guiding tone, style, and content of the reply
5. **Chatbot Engine**
   * A GPT-style decoder-only transformer
   * Conditions on the user input, long-term context, and strategy prompt
   * Produces the final natural-language response
