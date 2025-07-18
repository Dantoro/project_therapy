## Threat Assessor Module: Design & Role

### Overview

The Threat Assessor is a standalone module designed to provide immediate clinical risk assessment of user input in Project Therapy. It leverages MentalBERT to analyze the *most recent* user input for signs of crisis—such as suicidality, self-harm, acute depression, or other urgent threats—rather than long-term trends or broad emotional states.

**Key Points:**

* Not a regressor: The Threat Assessor is a *classifier* that outputs probability scores for a set of clinical risk categories.
* It does *not* process the entire STM buffer or TrendTracker history—just the latest user message.
* The output is immediately actionable and meant to inform crisis logic upstream (e.g., the DecisionMaker).
* This module is separate from the DecisionMaker to maintain clarity and make it easy to audit or swap out for other models.

---

### Inputs & Outputs

**Input:**

* The** ***raw text* of the most recent user input (e.g., a single message or utterance).

**Output:**

* A dictionary or vector of probability/confidence scores for each clinical risk class. Example:

{
  "suicidal_ideation": 0.71,
  "depression": 0.82,
  "anxiety": 0.55,
  "ptsd": 0.21,
  "self_harm": 0.44
}

Or, in discrete classification mode, the most likely class (e.g., “suicidal_ideation”).

---

### Use in the Pipeline

* The DecisionMaker queries ThreatAssessor with each  *new user input* .
* If any score (or class) exceeds a configured threshold (e.g., `suicidal_ideation > 0.6`), the DecisionMaker escalates—immediately routing the session to human intervention, authorities, or specialist resources.
* Otherwise, the outputs are used as one signal among many (HAN, TrendTracker, LTM, Clipboard) to guide normal chatbot response selection.

---

### Model Details

* **MentalBERT** : A BERT-family transformer pretrained on clinical and mental health text, fine-tuned for risk detection and threat assessment in psychiatric contexts.
* Designed for sentence/utterance-level risk, not dialogue-level context or broad emotion trends.
* Supports both binary and multi-label classification.
* Is *not* intended to provide diagnosis or broad emotion regression.

---

### Example Use Case

User:

> “I’m so tired of all this. I just want the pain to stop. I don’t know how much longer I can take it.”

ThreatAssessor output:

{
  "suicidal_ideation": 0.71,
  "depression": 0.82,
  "anxiety": 0.55,
  "ptsd": 0.21,
  "self_harm": 0.44
}

DecisionMaker receives these scores, compares them to escalation thresholds, and triggers an urgent safety protocol.

---

### Placement in the Architecture

* **Standalone Module:** NOT embedded within DecisionMaker for transparency and modularity.
* Receives only the latest user message.
* Outputs are passed as part of the full set of inputs to the DecisionMaker.

---

### Design Choices & Justification

* **Focus on immediacy:** By analyzing only the newest user input, we minimize delay and maximize responsiveness to acute threats.
* **Classifier not regressor:** We want distinct “red flag” signals rather than ambiguous continuous scores.
* **Transparency:** Keeping it out of the main DecisionMaker logic makes it auditable, swappable, and upgradable as better threat models become available.
* **Not responsible for trend or context:** That’s handled by TrendTracker, HAN, LTM, and the Clipboard.
