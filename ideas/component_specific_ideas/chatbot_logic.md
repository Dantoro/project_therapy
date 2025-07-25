# Chatbot Logic

**Last updated: 2025-07-18**

---

## Purpose

The chatbot is the generative component of Project Therapy—responsible for producing natural, empathetic, and clinically sound responses. It is built on a decoder-only transformer model (GPT, Llama, Falcon, etc.), ideally with domain pretraining for mental health, clinical, or biomedical topics.

## Decoder Model Options

### 1. **MentalGPT** (Preferred if available)

* Pretrained/fine-tuned on mental health dialogue, advice, and patient–provider conversations
* Pros: Most likely to generate relevant, supportive, and context-aware replies
* Cons: Scarcity, may require custom finetuning

### 2. **Clinical GPT/BioGPT**

* Clinical GPT models (e.g., GPT-2/3/4, BioGPT, MedGPT, Clinical-Llama) trained on medical records, doctor–patient conversations, and biomedical corpora
* Pros: Strong medical/clinical domain knowledge
* Cons: May lack emotional nuance; requires careful filtering/finetuning to avoid overly technical language

### 3. **Generic GPT/T5/Llama**

* Used if no mental/clinical GPTs are available
* Pros: Readily available, large model sizes
* Cons: Weak on therapy-specific language, needs prompt engineering and tuning

## Corpus and Data Considerations

* **Ideal training data:** Alternating rows of user (patient) and chatbot (therapist) dialogue, drawn from real or synthetic mental health conversations
* **Custom word2vec corpus:** I can use the same clinical dialogue corpus for both word2vec and chatbot training. In fact, close alignment improves cross-module understanding.
* **Corpus expansion:** More is better. I should seek out additional clinical/mental health dialogue sets for both word2vec and chatbot pretraining/fine-tuning. Datasets should be cleaned, anonymized, and, if possible, expanded for diversity and realism.

## Corpus Formatting

* For chatbot pretraining: Format as alternating speaker rows (User, Chatbot) with each utterance as a single utterance
* For word2vec: Split utterances further into individual sentences (maximize context diversity)
* Many datasets require preprocessing to ensure compatible formatting

## Model Selection Factors

* **Mental health/clinical pretraining:** Increases safety and relevance
* **Token/sequence length:** Must handle multi-turn dialogues, long utterances, and context from LTM/SOAP notes
* **Hardware constraints:** Large models may need to be swapped out for smaller ones on lower-end devices

## Pros and Cons Summary

* **MentalGPT:** Best for therapy. Rare, but ideal.
* **ClinicalGPT/BioGPT:** Good for medical facts, less for support/empathy.
* **Generic GPT/Llama/T5:** Flexible, but less precise and less safe out of the box.

## Final Notes

* Whichever model is chosen, chatbot input should include context from STM (recent dialogue) and LTM (SOAP notes), plus relevant Clipboard facts.
* Post-processing (filtering, re-ranking, prompt engineering) may be necessary for clinical safety.
* Periodic retraining and prompt audits recommended.

---

**See also:**

* [custom_word2vec_logic.md](custom_word2vec_logic.md)
* [memory_module_logic.md](memory_module_logic.md)
* [han_model.md](han_model.md)
