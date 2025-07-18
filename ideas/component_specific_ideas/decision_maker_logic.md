# Decision Maker Logic

## Purpose & High-Level Overview

The **DecisionMaker** is the core orchestration module in Project Therapy. It serves as the central control logic that receives all upstream data signals (emotion, context, risk, and extracted entities), and determines:

* **Whether to escalate or intervene in a crisis** (e.g., refer to a human, trigger emergency protocol)
* **Whether to provide factual/clinical information** (retrieval-based response)
* **Whether/how to generate a chatbot response** (select style/tone/content)

It is intended to blend *transparent, explainable logic* (rules-based, decision trees) with flexible, data-driven analysis (including ML-based threat detection, if required).

---

## Inputs to DecisionMaker

1. **TrendTracker output:** 210d mood vector (emotional trends, velocity, acceleration, EMA)
2. **HAN output:** 256d vector (contextual representation of recent conversation)
3. **LTM output:** Raw text (SOAP notes of up to 10 LTM blocks) + 128–256d vector representing full LTM
4. **Clipboard:** Stanza-based dictionary of entities/dependencies/relations with timestamp histories
5. **ThreatAssessor:** MentalBERT-based vector of crisis class probabilities for latest user input

---

## Data Format

* **Vectors** (for model-driven logic, weighted splits, or classification): TrendTracker, HAN, LTM (vectorized)
* **Raw text** (for context, retrieval, and generative models): STM (recent raw dialogue), LTM (block SOAP notes)
* **Dictionaries/lists** (for lookup and rules-based logic): Clipboard

---

## Sample Rules-Based Logic

1. **Crisis Escalation:**
   * IF ThreatAssessor["suicidal_ideation"] > 0.7 OR ThreatAssessor["self_harm"] > 0.6:
     * IMMEDIATELY refer user to crisis hotline or escalate to human moderator.
   * ELSE IF clipboard includes {"symptom": "suicidal thoughts"} with recent timestamp:
     * Double-check with user, raise system alert.
2. **Information Retrieval:**
   * IF user explicitly requests info (drug, symptom, resource) as detected by clipboard entity or HAN context:
     * Query vetted database, return factual response.
3. **General Chatbot Response:**
   * Use HAN (STM), TrendTracker (emotion), LTM (long-term context), and Clipboard (entities/timestamps) to determine:
     * Style: empathetic, supportive, instructive, neutral, or motivational
     * Length: short reassurance vs long step-by-step
     * Tone: calming, energizing, validating, etc.
   * Pass full context to chatbot decoder to generate reply.
4. **Override/Fail-safes:**
   * IF no upstream component can resolve the intent:
     * Fall back to safe default message or transfer to human.

---

## Example: Decision Tree/Hybrid Logic

* **First Node:** Is there a crisis risk (via ThreatAssessor or clipboard)?
  * Yes: escalate immediately, bypass normal response generation.
  * No: continue.
* **Second Node:** Is the user requesting clinical information (detected by entity extraction/intent)?
  * Yes: retrieval mode.
  * No: continue.
* **Third Node:** Default to chatbot response, factoring emotion/context/long-term memory.

---

## Design Principles

* **Transparency:** Favor explicit rules for safety-critical decisions; avoid unnecessary blackboxes.
* **Auditability:** Every action must be explainable from input to output.
* **Modularity:** Each upstream input can be replaced, upgraded, or debugged independently.
* **Safety:** Crisis escalation always takes precedence.

---

## Future Directions

* Decision tree logic can be upgraded to more sophisticated methods (random forests, lightweight neural nets) if justified.
* Retrieval modules can integrate with real EHRs, med databases, or crisis intervention resources.
* DecisionMaker should always provide a full log/trace for any clinical interaction for audit/QA.
