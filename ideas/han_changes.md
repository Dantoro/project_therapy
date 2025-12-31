# HAN changes and training plan (Ariadne)

**Scope:** This note captures the *important new decisions and ideas* from today’s HAN discussion. It’s written to be pasted into the repo as `han_changes.md` and revisited later.

---

## 0) Executive summary

- Keep the **char-level CNN** for stylometric/tone cues, but **stop treating it as an emotion classifier** trained on GoEmotions.
- Update the HAN into a **braided (dual-branch) hierarchy**: a **linear/time encoder** (BiLSTM) + a **structural encoder** (tree/graph/state) *at each tier*, with **per-branch attention** and a **fusion step** back to a fixed-size vector.
- Train the HAN (or a simpler first version of it) using **self-supervised contrastive next-response ranking** (retrieval-style), using **in-batch negatives**. This trains conversational-state representations without generation.
- Transformers are optional, but can be used as a **teacher** (distillation) to speed learning, then discarded at inference.

---

## 1) Character-level CNN: objective change (from GoEmotions → stylometry)

### 1.1 What stays

- The CNN’s *role* stays: **character-level stylometric fingerprinting** capturing spacing, capitalization, typos, punctuation, emojis/emoticons, repetition, internet-speak, etc.
- The CNN still produces a **single 200d utterance vector** that can be concatenated with word-level embeddings.

### 1.2 What changes

- **Do not pretrain the CNN as an emotion classifier on GoEmotions.** GoEmotions is label-aligned to emotions, not style; it risks teaching the CNN “emotion shortcuts” instead of “how the text is written.”

### 1.3 Recommended pretraining targets (pick one; simplest first)

**Option A (simplest): self-supervised stylometry objectives on your dialogue superset**

- **Character corruption + reconstruction:** randomly delete/insert/swap characters, mask spans, normalize casing/punctuation, etc., and train the CNN to predict the original character distribution or a compact reconstruction target.
- **Augmentation consistency:** produce two lightly-augmented versions of the same utterance (typo-like edits, emoji removal, punctuation perturbation) and train embeddings to stay close.

**Option B: author/style discrimination (weak labels)**

- If you have multi-utterance samples from the same speaker/session: train the CNN to predict “same speaker vs different speaker” or “same source vs different source.” This is cheap and directly stylometric.

**Option C: auxiliary style-tag heads (very small label set; can be weakly labeled)**

- predict coarse style signals: “question vs statement,” “high punctuation,” “high emoji,” “all-caps,” etc. These can be heuristics without being your main objective.

### 1.4 Integration during HAN training

- Keep the CNN **inside** the pipeline.
- During initial HAN training, you can still do a freeze/unfreeze schedule, but now the CNN is being tuned toward **style utility**, not emotion prediction.

---

## 2) Braided HAN (dual-branch tiers) and attention placement

### 2.1 Motivation

The original design used **two stacked BiLSTMs per tier**. Adding a structural model (tree/graph/state) replaces “more sequential depth” with “orthogonal structure.” This typically yields *at least* as much representational gain as stacking another BiLSTM.

### 2.2 The braided tier block

For each tier, keep a clean interface:

- Input: a sequence of vectors in **R^d** (typically d = 512)
- Output: a single vector in **R^d** for the next tier

Compute two encoders **on the same input**:

- **Linear encoder:** BiLSTM over the sequence (time/ordering)
- **Structural encoder:** tree/graph/state module over the same units (structure/roles)

**Attention placement:**

- Each branch gets **its own attention pooling** (multi-head optional) to produce:
  - `v_linear` in R^d
  - `v_struct` in R^d

**Fusion:** combine back to one vector for the next tier. Two recommended fusion methods:

1) **Concat + projection (default):**

- concatenate `[v_linear; v_struct]` then apply a learned linear layer back to R^d.
- pros: stable, simple, interpretable

2) **Gated fusion (optional):**

- compute a gate `g` in [0,1]^d from `[v_linear; v_struct]` and output `g ⊙ v_linear + (1-g) ⊙ v_struct`.
- pros: model learns when to trust which branch
- cons: slightly more finicky; debug later

**Regularization tip:** optionally use “branch dropout” during training (randomly zero one branch sometimes) so neither branch becomes dead weight.

### 2.3 Compute scheduling

- Run branches **sequentially in time** (for GPU simplicity) while keeping **parallel-in-dataflow** (both see the same input). This avoids CPU/GPU split headaches.

---

## 3) Recommended orthogonal models per tier

### 3.1 Word tier (words within a sentence)

- **Linear:** word-level BiLSTM
- **Structural:** **bidirectional Tree-LSTM** over a dependency/constituency parse
  - captures grammatical composition as orthogonal to sequence order

Notes:

- You do *not* need special supervision for the Tree-LSTM. It trains end-to-end via the top loss.
- You *do* need a parser to supply trees (tooling), but you don’t need to train a transformer parser yourself.

### 3.2 Sentence tier (sentences within an utterance)

Two candidates:

**A) Sentence graph + GNN (recommended first)**

- Nodes = sentence vectors
- Edges = adjacency (i↔i±1) at minimum; optionally add cheap cue edges (discourse markers, entity overlap)
- GNN message passing yields structure-aware sentence aggregation
- pros: robust to messy discourse; handles multi-links naturally

**B) Sentence discourse tree (more brittle, more interpretable)**

- Nodes = sentence vectors
- Edges = rhetorical relations (cause/contrast/elaboration)
- pros: clean “main point vs support” backbone
- cons: requires stronger relation inference; fragile under informal text

Recommendation: start with **sentence graph + shallow GNN** (1–2 layers).

### 3.3 Utterance tier (utterances across the dialogue window)

Two candidates:

**A) Speaker-state modeling (recommended first; DialogueRNN-style)**

- Maintain evolving states per participant (User vs Assistant) plus optional global state
- Each new utterance updates its speaker’s state
- pros: aligns with therapy interaction; models co-evolution of roles

**B) Dialogue graph / reply-to threading**

- Nodes = utterances; edges = adjacency + “reply-to/mentions/callback” links
- pros: explicit threading of tangents/callbacks
- cons: requires reply-to inference; can be noisy

Recommendation: start with **speaker-state modeling** as the structural companion.

---

## 4) Final projection notes

- Because each tier already fuses to a single R^d vector, the end should be **boring**.
- Default: **final concat+proj (if needed) → small MLP (optional) → output dense**.
- Avoid adding a “special guest” encoder at the end unless you have evidence it helps; the hierarchy is where the value is.

---

## 5) Training the HAN: self-supervised contrastive next-response ranking

### 5.1 Why this objective

The HAN is no longer responsible for generation; DecisionMaker owns policy and a downstream generator owns wording. The HAN should learn a **conversational state representation**.

A clean training signal without hand-labeling:

- Given dialogue context ending in the user/patient turn, learn an embedding such that the **true next assistant response** is more compatible than other candidate responses.

This is **retrieval-style learning**, not lookup at inference.

### 5.2 How “negatives” work (no k-fold nonsense)

- Training is done in **batches**.
- Batch contains N true pairs: `(C1,R1)…(CN,RN)`.
- Compute an N×N similarity matrix between all contexts and all responses.
- For each context Ci, the positive is Ri (diagonal). The other responses in the batch act as negatives.

In plain terms: *make the correct response score higher than the other batch responses for that context.*

### 5.3 Encoder design for training

- Context encoder: your HAN (or a simplified first-stage encoder)
- Response encoder: can be the same encoder or a lighter sibling encoder, but should produce vectors in the same space.

At inference, you typically keep only the **context encoder** output vector for DecisionMaker.

### 5.4 Dataset format tolerance

- The superset can be messy across sources.
- You only need stable `(context, response)` pairing identity.
- Mixed examples are fine:
  - single-turn pairs (context length = 1)
  - multi-turn windows for datasets that support it

### 5.5 Practical training curriculum (recommended)

1) **Baseline sanity check:** TF-IDF / BM25 retrieval evaluation (no training)
2) **Bootstrap model:** GloVe + small BiLSTM + attention (no sentence tier) trained contrastively
3) **Upgrade inputs:** add char-CNN + custom word2vec + projection (your 1000→512 stack)
4) **Upgrade hierarchy:** add utterance-tier (windowed contexts)
5) **Add structural branches:** tree/GNN/speaker-state as braided companions

This avoids building the full mega-model before you’ve proven the objective/data pipeline.

### 5.6 Optional transformer assistance (teacher → distill → discard)

If training is painful or data is noisy, use a transformer **only as a teacher**, then throw it away:

**Teacher style A: seq2seq scorer (dialogue model)**

- Teacher scores candidate responses given a context.
- Student learns to match teacher’s ranking/probabilities over candidates.

**Teacher style B: embedding teacher (sentence embedding model)**

- Teacher produces embeddings; student is trained to mimic geometry + contrastive loss.

Recommendation: if you do this, keep your **student’s embedding stack** (char-CNN + GloVe + custom w2v) in place from the beginning, so you’re not swapping foundations later.

---

## 6) Notes on “just word-level” vs full hierarchy

- Training on single-turn context→response pairs is a valid **bootstrap** objective.
- However, to actually train “conversation state,” you need at least some training examples where context spans multiple alternating utterances, so the utterance-tier learns how to aggregate across turns.
- You can mix window sizes: many examples can be 1-turn; some should be multi-turn.

---

## 7) Action items (minimal next steps)

- Update CNN pretraining objective away from GoEmotions; choose Option A (self-supervised stylometry) first.
- Implement contrastive training loop with in-batch negatives.
- Start with a small baseline encoder before full braided HAN.
- When moving to braided tiers, implement per-branch attention + concat+proj fusion.
- Add structural modules incrementally: Tree-LSTM at word tier first; speaker-state at utterance tier next; sentence graph GNN last.

---

## 8) Additional Notes

### 8.1 Dataset scale and purpose

- Large targets like **25k dialogue pairs** were artifacts of earlier designs where the HAN was expected to generate or directly supervise responses.
- In the current architecture, the HAN’s role is **conversational state understanding**, not generation. This dramatically reduces data requirements.
- For this role, **diversity and coverage matter more than raw volume**. Practical prototypes can be trained with **~5k–10k well-mixed pairs/windows**.

### 8.2 Separation of concerns: embeddings vs HAN training

- **Custom word2vec** should be trained only on **domain-relevant text** (mental health, clinical, emotional support). Generic dialogue (e.g., movie scripts) should be excluded to avoid semantic dilution.
- **GloVe** continues to cover general English semantics.
- **Generic dialogue datasets** (e.g., Cornell Movie-Dialogs) are useful **only for HAN training**, and only as **subsampled structural data**, not for embedding training.

### 8.3 Agreed sampling mix for HAN training

- Final agreed guideline for HAN training batches:

  - **50% mental health** (therapy-style)
  - **25% friendly / emotional peer support**
  - **20% clinical**
  - **5% generic dialogue** (structural only, subsampled)
- This yields **~75% direct support-oriented signal** while retaining enough structure to learn long-range conversational mechanics.

### 8.4 Use of generic dialogue

- Generic dialogue is included **only to teach conversational structure** (turn-taking, callbacks, topic drift), not semantics.
- A small fraction (≈5%) is sufficient if samples emphasize **longer multi-turn windows**.

### 8.5 Transformers and philosophy

- Transformers are optional tooling, not architectural dependencies.
- Acceptable uses include:
  - teacher models for ranking/distillation during training
  - hard-negative mining or scoring
- Transformers are **discarded at inference**; the deployed system relies on the HAN, TrendTracker, DecisionMaker, and downstream LLM only for surface realization.

### 8.6 CNN training reality check

- The character-level CNN does **not** require a standalone labeled dataset to be useful.
- It can be trained end-to-end with the HAN via the contrastive objective, optionally with a brief self-supervised warm start.
- Freeze/unfreeze schedules remain optional optimization tools, not requirements.

### 8.7 Guiding principle (to avoid future re-litigation)

> The HAN learns *state*, not text.
> Datasets exist to shape geometry and inductive bias, not to exhaustively encode knowledge.

This principle should be used to evaluate future dataset, architecture, and training decisions.
