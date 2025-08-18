# HRM DecisionMaker — Parallel L‑Modules → Generative H‑Modules → Actuator

*Last updated: 2025‑08‑16*

## Purpose

A concrete, explainable HRM layout for Project Therapy’s **DecisionMaker** that runs three **L‑modules** in parallel (Emergency, Rule‑Tree, Retrieval/RAG) and, only when needed, engages two **H‑modules** (EmoDynamiX for strategy; SMES for style) before the **Actuator** selects the final path (escalate ▸ retrieve ▸ structured prompt ▸ generative response).

---

## High‑level Diagram (HRM view)

```text
                    ┌──────────────────────────────────────────────────────────┐
Inputs              │                    SHARED INPUT BUS                      │
• STM (1–21 utt.)   │  STM text  •  TrendTracker(210d)  •  HAN(256d)  •  LTM  │
• TrendTracker(210) │  Clipboard entities/time • ThreatAssessor scores        │
• HAN(256)          └───────────────┬───────────────┬───────────────┬─────────┘
• LTM (SOAP + vec)                   │               │               │
• Clipboard                           ▼               ▼               ▼
• ThreatAssessor          ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐
                          │ L1: EMERGENCY  │  │ L2: RULE TREE  │  │ L3: RETRIEVAL   │
                          │ (hard‑coded)   │  │ (decision tree)│  │  (RAG + RF)     │
                          └──────┬─────────┘  └────────┬───────┘  └─────────┬────────┘
                                 │                     │                     │
                      Fires? ───►│YES                  │                     │
                                 │                     │                     │
                                 ▼                     ▼                     ▼
                      ┌────────────────┐    ┌────────────────┐    ┌──────────────────┐
                      │ ESCALATION     │    │ STRUCTURED     │    │ RETRIEVAL ANSWER │
                      │ (override)     │    │ PROMPT         │    │ (canned/synth)   │
                      └──────┬─────────┘    └────────┬───────┘    └─────────┬────────┘
                             │                         │                      │
                             └───────────────┬─────────┴──────────────┬───────┘
                                             ▼                        ▼
                                     ┌────────────────────────────────────────┐
                                     │           ACTUATOR / CONSENSUS         │
                                     │ Priority: Emergency > Retrieval > Tree │
                                     │ Else → GENERATIVE PATH                 │
                                     └───────────────┬────────────────────────┘
                                                     │ (if none above valid)
                                                     ▼
                                         ┌──────────────────────────────┐
                                         │      H1: EmoDynamiX          │
                                         │  (therapeutic strategy)      │
                                         └───────────────┬──────────────┘
                                                         ▼
                                         ┌──────────────────────────────┐
                                         │         H2: SMES             │
                                         │   (tone/style parameters)    │
                                         └───────────────┬──────────────┘
                                                         ▼
                                         ┌──────────────────────────────┐
                                         │  MentalGPT (generator)       │
                                         │  (prompted with plan+style)  │
                                         └──────────────────────────────┘
```

**Key:** L‑modules run **in parallel**. Emergency can **preempt**. If neither Rule‑Tree nor Retrieval produce a valid output, the actuator routes to the **generative path** (EmoDynamiX ▸ SMES ▸ MentalGPT).

---

## Data Contracts

### Shared Inputs

- **STM window (1–21 utt.)**: raw text with speaker tags.
- **TrendTracker (210d)**: emotion vector stack (current, EMA, 1st/2nd derivatives; Ekman + fine‑grained).
- **HAN (256d)**: contextual embedding of last 21 utt.
- **LTM**: list of SOAP notes + LTM embedding.
- **Clipboard**: entities (type, timestamps, first/latest mentions).
- **ThreatAssessor**: risk probabilities (e.g., suicidal\_ideation, self\_harm, manic\_risk…).

### L1: Emergency (if/else, hard‑coded)

- **Inputs:** ThreatAssessor, STM text (keyword heuristics), Clipboard.
- **Logic:** deterministic thresholds & phrases (e.g., `suicidal_ideation > 0.85` AND high‑lethality intent).
- **Output:** `escalate_now` (payload contains hotline/handoff bundle) **or** `null`.

### L2: Rule‑Tree (single learned tree)

- **Inputs (interpretable features only):**
  - Recent intent flags (help‑seeking, venting, info‑seeking).
  - Simple stylometrics (caps %, avg words/sentence),
  - Lightweight emotion summaries (volatility score; net drift),
  - Conversation state (turn count, time since last handoff, prior strategy).
- **Output:** structured prompt template **or** `null`.

### L3: Retrieval/RAG (Random Forest intent classifier)

- **Pipeline:** normalize ▸ NER/regex ▸ Clipboard join ▸ **Intent RF** (drug\_info / symptom\_info / resource\_lookup / unknown) ▸ query build ▸ top‑K semantic retrieve ▸ answer synth ▸ guardrails.
- **Output:** retrieval answer (with citations/IDs) **or** `null`.

### Generative Path (only if needed)

- **H1: EmoDynamiX** → **Strategy Plan**
  - `strategy`: supportive\_listening | validation | directive\_steps | psychoeducation | motivational | values\_exploration | crisis\_deescalation | …
  - `rationale_scores`: per‑strategy scores (for audit).
  - `skills_focus`: e.g., normalization, reframing, summarization.
- **H2: SMES** → **Style Parameters**
  - `tone`: calm | warm | neutral | energizing …
  - `length`: short | medium | long
  - `complexity`: simple | standard | rich
  - `persona/register`: clinician | peer‑coach | educator …
  - `formatting`: bullets | numbered steps | paragraph | mix
  - `safety_overrides`: e.g., avoid certain triggers/claims.
- **MentalGPT**
  - Receives `{STM excerpt, LTM snippets, Strategy Plan, Style Parameters}` and generates the final text.

---

## Actuator / Arbitration Logic

1. **Emergency present?** If any Emergency rule fired → **return escalation** (preempts all).
2. **Retrieval present?** If RAG returns a vetted answer → **return retrieval**.
3. **Rule‑Tree present?** If a structured prompt exists → **return prompt**.
4. **Else → Generative:** Run EmoDynamiX + SMES → call MentalGPT.

*Why this order?* Safety first; factual answers next; structured dialogues before free generation.

---

## Interpretability & Logging (non‑negotiable)

### Per‑module logs

```json
{
  "timestamp": "2025-08-16T21:04:00Z",
  "inputs": {"stm_id": "conv#842-utt#120-140", "trend": "hash", "han": "hash"},
  "L1_emergency": {
    "fired": false,
    "rules_checked": ["SI>0.85+plan_present", "explicit_means", "third_party_report"],
    "matched": []
  },
  "L2_rule_tree": {
    "decision": null,
    "path": ["root -> not_high_risk", "intent=venting", "no_prior_handoff_recent"],
    "leaf_id": 42,
    "confidence": 0.62
  },
  "L3_rag": {
    "intent": "drug_info",
    "rf_votes": {"drug_info": 73, "symptom_info": 21, "resource_lookup": 6},
    "entities": ["Lexapro"],
    "retrieval": {"k": 3, "doc_ids": ["drugdb#2031","fda#lexapro","nhs#escitalopram"],
                   "guardrails": ["no dosing guidance"]},
    "answer": "…"
  },
  "H1_emodynamix": {
    "strategy": "supportive_listening",
    "scores": {"supportive_listening": 0.85, "directive_steps": 0.27, "psychoeducation": 0.22}
  },
  "H2_smes": {
    "tone": "calm", "length": "medium", "formatting": "paragraph+bullets"
  },
  "actuator": {"selected_path": "retrieval", "reason": "RAG_valid_and_priority=2"}
}
```

### Traceability guarantees

- **Emergency:** explicit rule IDs.
- **Rule‑Tree:** full decision path (node conditions → leaf).
- **RAG:** RF vote histogram + retrieved doc IDs.
- **EmoDynamiX/SMES:** per‑option scores + chosen parameters.
- **Actuator:** final choice + reason string.

---

## Failure & Tie‑breaks

- **RAG vs Rule‑Tree conflict:** Prefer **RAG** if intent confidence ≥ τ; else prefer **Rule‑Tree** if leaf confidence ≥ τ₂; else go **Generative**.
- **Multiple RAG intents:** ask a short disambiguation prompt (Rule‑Tree template).
- **H‑module low confidence:** fall back to **short supportive check‑in** template.

---

## Latency Budget (targets)

- L‑modules parallel wall‑time: **≤ 150 ms** (Emergency ≈0–5 ms; Rule‑Tree ≤ 5 ms; RAG ≤ 150 ms incl. vector search).
- H‑modules only on generative path: **EmoDynamiX ≤ 40 ms; SMES ≤ 40 ms; MentalGPT per reply ≤ 600 ms**.

---

## Integration Notes

- **Feature hygiene:** Trees/forests consume **interpretable features**, not raw embeddings. Keep a feature registry.
- **Guardrails:** Retrieval answers must pass safety filters (no dosing, no diagnosis claims, etc.).
- **A/B switches:** Actuator priority ordering and thresholds τ, τ₂ should be config‑driven.

---

## Checklist (MVP → v1)

---

## One‑page Summary

- **Parallel L‑modules** maximize safety + coverage without sequential bottlenecks.
- **Actuator** encodes clear precedence: Emergency ▸ Retrieval ▸ Rule‑Tree ▸ Generative.
- **Generative only when needed**; EmoDynamiX selects strategy, SMES shapes style; MentalGPT produces text.
- **Every path is auditable** via strict, structured logs.
