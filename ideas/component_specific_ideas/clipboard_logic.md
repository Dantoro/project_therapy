# Clipboard Logic

**Last updated: 2025-07-18**

---

## Purpose and Motivation

The Clipboard is a permanent, queryable memory structure for Project Therapy. It exists to store all clinically-relevant named entities, dependencies, relationships, and key event markers extracted from user dialogue, using a state-of-the-art clinical/biomedical NLP toolkit (Stanza). Unlike the STM (which holds raw conversation), or the LTM (which holds periodic summaries/SOAP notes), the Clipboard preserves a running log of all *entities and relationships* found, along with their full occurrence histories (timestamps), for as long as the user interacts with the system.

## Why Stanza?

Stanza is a Python NLP toolkit from Stanford, providing highly accurate syntactic analysis and named entity recognition (NER). Project Therapy uses Stanza’s *biomedical and clinical models*, which are specifically trained to recognize symptoms, medications, procedures, anatomy, clinical findings, and other health-relevant information—far beyond what general-purpose NLP tools can provide. This means the Clipboard can track medication mentions, symptoms, interventions, time markers, and even abstract constructs like "coping mechanism" or "treatment adherence."

## What Does the Clipboard Store?

* **Named entities:** Symptoms, interventions, drugs, anatomical terms, mental states, etc.
* **Relationships and dependencies:** Who did what, to whom, and why (dependency parsing and relation extraction)
* **Timestamps:** When each entity/relationship was mentioned (chronological, optionally most-recent-first)
* **Speaker:** Typically only user utterances (unless chatbot suggests a concrete intervention or medication)

All data is de-identified and indexed for rapid retrieval by downstream modules.

## Data Structure Example

The Clipboard is implemented as a lookup dictionary, with each unique entity/relation as the key and a list of timestamped occurrences as values. For example:

```json
{
  "named_entities": {
    "breathing exercise": {
      "type": "INTERVENTION",
      "timestamps": [3, 18, 34]
    },
    "school": {
      "type": "TOPIC",
      "timestamps": [1, 2, 5, 8]
    }
  },
  "symptoms": {
    "needs a break": {
      "timestamps": [4, 18]
    }
  },
  "dependency_relations": [
    {"subj": "I", "verb": "need", "obj": "a break", "timestamp": 18},
    {"subj": "breathing thing", "verb": "sounds like", "obj": "it might help", "timestamp": 18}
  ]
}
```

* Timestamps can be stored either as chronological lists or sorted with most recent first. Chronological (oldest to newest) is usually more natural, but most recent first may be useful for queries like “when was X last mentioned?”
* If a value/entity is seen more than once, it updates the timestamp list (rather than storing duplicate keys).

## Permanent vs. Rolling Memory

The Clipboard is a *persistent* memory feature: it is *not* cleared when STM or LTM are overwritten. As a result, it grows steadily over time, but the memory footprint is minimal compared to storing full raw text. Entity dictionaries with timestamp lists are very compact, especially for long-term use.

If needed, it is possible to prune older timestamps for ultra-long-term users, or add a "last accessed" flag for efficient lookups, but by design the Clipboard is intended to keep as much clinically relevant entity history as possible.

## Why This Matters

* **Complements abstraction:** While LTM summaries (SOAP notes) and generative models may lose specific details, the Clipboard preserves every recognized clinical entity.
* **Powers downstream modules:** DecisionMaker, ThreatAssessor, and the chatbot can query the Clipboard for real-time facts about symptoms, meds, or patterns (e.g., “has self-harm been mentioned before?”)
* **Transparency:** The Clipboard is easily exportable as a timeline or event log for audit or clinical review.

## Stanza Biomedical/Clinical Model

Project Therapy uses Stanza’s [biomedical and clinical syntactic analysis and NER models](https://stanfordnlp.github.io/stanza/biomed.html), which are among the most accurate for medical/psychological text. These models are trained on a mix of clinical notes (MIMIC-III), biomedical papers (PubMed), and related corpora, and can detect symptoms, medications, anatomical sites, procedures, mental states, and many more.

> **Note:** While Stanza’s biomedical model is more focused on physical/clinical entities, it still performs well on many psychological constructs (e.g., stress, anxiety, mood, intervention names), making it well-suited for a digital therapy context.

---

**See also:**

* [memory_module_logic.md](memory_module_logic.md)
* [stanza.readme](../research/stanza.readme)
* [decision_maker_logic.md](decision_maker_logic.md) (for how Clipboard is used in decisions)
