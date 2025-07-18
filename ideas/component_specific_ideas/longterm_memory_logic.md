# LTM (Long-Term Memory) Logic

**Last updated: 2025-07-18**

---

## Purpose and Overview

LTM (Long-Term Memory) in Project Therapy is a rolling buffer of high-level summaries of prior conversations. Each LTM “block” is generated from 20 STM entries (10 user–chatbot dialogue pairs). Rather than storing raw text, each block is distilled into a clinical SOAP note—an industry-standard for summarizing patient encounters—via a seq2seq transformer such as **MentalBART** or a similar clinical/mental-health-oriented encoder–decoder model.

* **SOAP notes:** Structured summaries of clinical conversations, consisting of Subjective, Objective, Assessment, and Plan sections. This provides a concise, yet comprehensive, narrative of the most salient issues and interventions discussed in each dialogue window.

## Why SOAP Notes Instead of Paragraph Summaries?

* **Precision:** SOAP format enforces coverage of symptoms (Subjective), observed/measured data (Objective), diagnostic reasoning (Assessment), and next steps/interventions (Plan).
* **Clinical interpretability:** Mirrors real-world clinical/therapeutic documentation for easier human review.
* **Enables both extraction and abstraction:** Summarizes key info but retains enough structure for downstream retrieval/analysis.

### Example SOAP Note (summarizing 20 entries):

**S:** The user reports high stress and fatigue due to academic workload (three midterms, group project), poor sleep, difficulty focusing, and feeling isolated. Expresses frustration with lack of group support and frequent parental inquiries about grades and eating habits. Feels overwhelmed and misunderstood by peers.

**O:** User appears exhausted, admits to late nights (up to 4am working), describes low energy, and mentions unhealthy eating habits due to time pressure. Emotional tone is persistently anxious and despondent.

**A:** Chronic academic stress with evidence of burnout, poor sleep hygiene, and low social support. High risk for academic disengagement and possible depressive symptoms.

**P:** Recommend prioritizing sleep hygiene, scheduling short daily breaks for mental rest, and setting realistic academic goals. Encourage user to seek support from counseling services or trusted adults. Discussed basic relaxation techniques and healthy snack options.

## Block Structure and Lifecycle

* Each LTM block corresponds to a rolling window of 20 STM entries.
* LTM holds up to 10 blocks at a time (200 STM entries).
* When a new block is created, the oldest is dropped (FIFO).

## Vectorizing the LTM

While raw SOAP notes are essential for human- and chatbot-level review, vectorized summaries are needed for downstream ML modules (e.g., DecisionMaker):

* **Full concatenation:** All SOAP notes are concatenated into a single document (or dataframe column).
* **Transformer vectorization:** The entire concatenated SOAP corpus is fed to a transformer encoder (e.g., MentalBART’s encoder, ClinicalBERT, or a compatible clinical transformer with high token limits—ideally 7,500+ tokens).
* **No pooling if possible:** Rather than averaging or attention-weighting individual block vectors, the entire text is embedded at once, producing a single (128d or 256d) vector.
* **Rationale:** This ensures the full canon of important long-term information is preserved, with minimal information loss or arbitrary weighting.

## Storage and Memory Footprint

* SOAP notes are compact compared to raw STM entries; 10 blocks typically consume a few kilobytes.
* Vectors are small (128–256d float arrays).

## Why Not Just Use the STM or Clipboard?

* STM covers only recent dialogue, and is overwritten quickly.
* Clipboard holds only *entities* —not the narrative, reasoning, or plan behind them.
* LTM is the only module providing a canonical, clinically-structured record of the user’s journey over time, both for the chatbot’s reference and for explainability/audit.

## Model Selection

* **Primary:** MentalBART, ClinicalBART, or similar (clinical/mental-health seq2seq models).
* **Secondary (vectorization):** Encoder-only transformer (ClinicalBERT, Longformer, etc) chosen for domain relevance and high max token limit.
* **Fallback:** Generic BART, T5, or Longformer if no domain-specific model is available.

## Future Considerations

* Model caching and hardware-aware loading to keep memory use low.
* Clinical explainability: Optionally, LTM text could be available for export/audit.
* Further research into mental-health-specific summarization models.

---

**See also:**

* [memory_module_logic.md](memory_module_logic.md)
* [trend_tracker_logic.md](trend_tracker_logic.md)
* [clipboard_logic.md](clipboard_logic.md)
