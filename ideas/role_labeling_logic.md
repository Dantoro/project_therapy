# Role Labeling Logic

**Last updated: 2025-08-03**

---

## Purpose

This document outlines the *current state*, *intended goals*, and *required steps* for implementing robust semantic role labeling, entity linking, and relationship extraction within the Clipboard module of Project Therapy.

---

## Current State (Clipboard Prototype as of 2025-08-01)

### What Works

- **Named entity extraction** (NER) is fully implemented using Stanza’s biomedical/clinical models (see clipboard_logic.md). All unique entities (symptoms, drugs, organizations, etc.) are logged with timestamp lists and raw text of their first/latest occurrence.
- **Basic dependency relations** (subject-verb-object triples) are extracted and included in the clipboard output, but only as shallow, contextless lists, not as rich relationship graphs or entity-linked relations.

### What’s Missing

- **Semantic role labeling** (SRL): No explicit labeling of agent/patient/target roles within utterances (e.g., recognizing that "Robyn" is the patient’s mother, or that "my mom" == Robyn).
- **Entity linking/coreference resolution**: Mentions like "my mom" or "she" are not resolved to their real-world referents (e.g., to the entity Robyn).
- **Relation extraction**: Only the most basic dependency parsing is present. No advanced relation types (e.g., family member, prescribes, experiences, recommends, is-a, part-of, etc.)
- **Expansion of vocabularies**: The prototype uses Stanza’s default biomedical/clinical vocab. There is no custom extension for psychiatric drugs, colloquial symptom mentions, or non-standard clinical concepts.
- **Heuristic or rule-based logic**: No custom rules exist for inferring roles from conversational context (e.g., deducing that the speaker is the patient, or that "my mom" is a parent role).

---

## Intended Goals (Where We Want to Be)

1. **Full SRL (Semantic Role Labeling)**

   - Assign explicit roles such as AGENT, PATIENT, EXPERIENCER, TARGET, FAMILY_MEMBER, PRESCRIBER, etc., to each entity mention within an utterance.
   - Enable the system to answer queries like “Who is Sarah’s mother?”, “Who recommended Lexapro?”, “Who is the patient?”
2. **Entity Linking & Coreference Resolution**

   - Resolve pronouns (“she,” “her”), and nominal phrases (“my mom,” “the doctor”) to their corresponding named entities (e.g., Robyn, Dr. Carter).
   - Maintain a persistent map of aliases and coreferents for each entity.
3. **Rich Relation Extraction**

   - Go beyond (subj, verb, obj) to extract labeled relations: FAMILY_OF, RECOMMENDS, PRESCRIBED_BY, EXPERIENCES, SYMPTOM_OF, etc.
   - Represent relations as edges in a graph where nodes are linked entities (not just flat text).
4. **(Optional) Incorporate Syntactic Parse Information**

   - Store relevant dependency or constituency subtrees within entity entries if it assists with role identification or relation extraction. Only include if beneficial for relationship clarity, not just as raw parse output.
5. **(Optional) Heuristic and Rule-Based Reasoning**

   - Supplement model-based SRL with custom rules: e.g., “speaker in user utterances = patient,” “my mom” is parent of patient, etc. (Implemented only if high-value and low-overhead.)
6. **(Optional) Expanded Vocabularies**

   - Allow for future extension with custom drug/symptom dictionaries or user-curated ontologies.

---

## Required Improvements / Technical Pathways

### 1. **SRL, Entity Linking, and Relation Extraction**

- **Stanza’s Capabilities**: While Stanza provides strong NER, its built-in SRL is limited, and coreference resolution is not included in its main clinical models. (It does have some support in the general English pipeline, but it is not fine-tuned for biomedical context.)
- **AllenNLP**: The gold standard open-source toolkit for SRL and coreference resolution is AllenNLP, which includes:
  - **SRL models** (PropBank-style) that can label agent/patient/theme/target for each predicate in a sentence.
  - **Coreference resolution** models that can resolve pronouns and nominal mentions to canonical entities.
  - **Relation extraction** models and pipelines, including some tuned for clinical/biomedical text (check model zoo).
- **Heuristic/Rule-Based Augmentation**: Where model output is insufficient (e.g., family relationships in first-person dialogue), supplement with rules like:
  - “my mom” → FAMILY_MEMBER role, parent of speaker.
  - “she”/“her” in context of last-mentioned female entity = likely coreferent.
- **Integration**: The ideal pipeline is:
  1. Run Stanza for NER and dependencies.
  2. Run AllenNLP for SRL and coreference.
  3. Combine outputs: For each utterance, map entity mentions to roles, resolve aliases/corefs, and update entity entries accordingly.

### 2. **Expanding Vocabularies**

- Not essential for core SRL, but recommended for improved accuracy in psychiatric/psychological contexts.
- Can be done via merging public drug/symptom lists (RxNorm, UMLS, etc.) into the lookup tables for entity extraction, or using tools like scispaCy with custom vocab.

### 3. **Making Use of Dependency/Constituency Parses**

- Only retain parse info inside dictionary entries if it is *actually* used to clarify a relation (e.g., tree shows "my mom" as possessor of "history of migraine"). Otherwise, keep out of main clipboard for clarity.

### 4. **Implementation Steps**

1. Prototype AllenNLP SRL + coref on sample utterances; validate outputs in a clinical/therapy dialogue context.
2. Build a linking module to join Stanza entities with AllenNLP roles/corefs for each utterance, updating the clipboard dictionary entries with roles and coreferent maps.
3. Add relation extraction pipeline (AllenNLP, Stanza, or custom heuristic/rule-based layer).
4. Document design for handling ambiguous/missing role assignments.

---

## Dependencies & Prerequisites

- Python environment supporting Stanza (biomed/clinical models) **and** AllenNLP (with allennlp-models extras).
- Optionally, scispaCy for expanded biomedical vocabularies.
- If AllenNLP is not feasible (due to OS/library/Apple Silicon incompatibilities), consider lightweight alternatives (spaCy+neuralcoref for general English, or rule-based mapping for the most common clinical roles).

---

## Summary Table: Current vs. Desired State

| Feature                        | Now (Prototype)        | Desired (Future)                |
| ------------------------------ | ---------------------- | ------------------------------- |
| Named Entity Recognition       | Stanza Biomed/Clinical | Stanza (plus extended vocab)    |
| SRL (Semantic Roles)           | None                   | AllenNLP (PropBank), plus rules |
| Coreference Resolution         | None                   | AllenNLP coref, plus rules      |
| Relation Extraction            | Shallow dependencies   | AllenNLP/heuristic, labeled RE  |
| Entity Linking/Aliasing        | None                   | Coref + alias map in clipboard  |
| Dependency/Constituency Parses | Raw list only          | Used only for role/RE support   |
| Vocabulary Expansion           | Stanza default         | Custom list/scispaCy (optional) |

---

## References / Further Reading

- clipboard_logic.md (for clipboard data structure)
- AllenNLP: https://allennlp.org/models
- Stanza biomedical models: https://stanfordnlp.github.io/stanza/biomed.html
- scispaCy: https://allenai.github.io/scispacy/
