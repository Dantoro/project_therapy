# Hierarchical Attention Network (HAN) Model

**Last updated: 2025-07-25**

---

## Key Points

* All embeddings (CNN, GloVe, word2vec) are concatenated per word; the CNN vector is the same for every word in the utterance
* CNN output is not cached; it is recalculated every timestep as part of HAN training/inference
* The HAN provides context at character, word, sentence, utterance, and document (STM buffer) levels
* All trainable features (CNN, BiLSTMs, dense layers) are updated together during end-to-end training

## Embedding Sources

* **GloVe (300d):** Pretrained general-domain word embeddings (Common Crawl)
* **word2vec (500d):** Custom-trained on Project Therapy dialogue superset (70% mental health, 15% clinical, 10% emotional, 5% generic)
* **CNN (200d):** Character-level stylometric vector trained as a shallow emotion classifier (GoEmotions; multi-emotion rows split; fine-tuned on dialogue superset via HAN)
  * CNN output is identical for every word in the utterance, reflecting global writing style/context
* **Dense (1000→512):** Jointly trained with rest of HAN; compresses concatenated embeddings

---

## Training Schedule

### CNN Pretraining

* **Dataset:** GoEmotions (one emotion label per row)
* **Minimum:** 10 epochs
* **Early stopping:** After 10 epochs (patience=2–3)
* **Maximum:** 20 epochs
* **Optimizer:** Adam, batch size 128–256, lr=1e-3

### HAN Training (on Dialogue Superset)

* **Epochs 1–3:** CNN **frozen**
* **Epochs 4–5:** CNN **unfrozen** , learning rate reduced (lr=1e-4 for CNN)
* **Early stopping:** Enabled after epoch 5 (patience=2–3)
* **Maximum:** 10 epochs
* **Optimizer**: Adam, batch size 32–128, lr=1e-3 for HAN
* Best weights restored on early stop; validation loss monitored

---

## Full Model Structure

### PREPROCESSING (now internal to HAN)

1. **Character-level CNN** (per-utterance, first layer of HAN):
   * Input: Utterance text tokenized at the character level
   * Embedding: 16d trainable vector per character
   * Convolutions: Parallel 1D filters (21 trigram, 21 pentagram, 22 heptagram)
   * Global max pooling over each filter
   * Output: 200d vector summarizing style and character-level patterns (shared across all words in the utterance)
2. **Embedding concatenation**
   * For each word: [CNN output (200d)] + [GloVe (300d)] + [word2vec (500d)] → 1000d
3. **Dense projection**
   * Linear layer, projects 1000d → 512d (includes batch normalization, L2 regularization)

### WORD-LEVEL (512d per word):

4. **Word BiLSTM 1** : Bidirectional LSTM, hidden size 512 (with recurrent dropout and layer norm)
5. **Highway 1** : Enables flexible information routing
6. **Dropout 1** : Standard dropout
7. **Word BiLSTM 2**
8. **Word attention** : Multi-head attention aggregates word context into sentence vectors

### SENTENCE-LEVEL (512d per sentence):

9. **Sentence BiLSTM 1** : Processes sequence of sentence vectors within each utterance
10. **Highway 2**
11. **Dropout 2**
12. **Sentence BiLSTM 2**
13. **Sentence attention** : Multi-head attention over sentences in the utterance, outputs utterance vector

### UTTERANCE-LEVEL (512d per utterance):

14. **Utterance BiLSTM 1** : Processes sequence of utterance vectors across STM buffer
15. **Highway 3**
16. **Dropout 3**
17. **Utterance BiLSTM 2**
18. **Utterance attention** : Multi-head attention over utterance representations

### FINAL PROJECTION:

19. **Dropout 4** : Dropout before output layer (rate ≈ 0.2–0.3 recommended)
20. **Output layer (Dense 512 → 256)** : Produces final context vector for DecisionMaker

---

## Memory Integration

* **STM** stores only raw utterance text; all embeddings are generated live within HAN
* **LTM** block summarization and vectorization handled by separate transformer modules (see memory_module_logic.md)
* HAN operates on a moving buffer of 1–21 utterances (alternating user/chatbot)

---

## Change Log

* 2025-07-25: Major update—clarified CNN/HAN integration, expanded full model structure, added embedding sources section, refined training schedule, improved formatting
* 2025-07-16: Full HAN update—character-level CNN is now internal, learned embeddings removed, embedding dimensions finalized
* 2025-07-07: (legacy) Used cached CNN, separate learned embedding, different dimensions

---

*See cnn_model.md for detailed CNN architecture and training specifics. See memory_module_logic.md for STM/LTM structure and logic.*
