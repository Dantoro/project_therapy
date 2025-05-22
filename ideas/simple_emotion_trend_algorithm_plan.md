# Simple Emotion Trend Algorithm Plan

**Purpose:**
Maintain a short‐term emotion trend over the last 10 sentences using a **nonlinear recency bias**. This plan describes the chosen **Exponential Moving Average (EMA)** approach, provides clear pseudocode, a 10‐point weight demo, and explains how it works and why it was selected.

---

## 1. Chosen Approach: Exponential Moving Average (EMA)

* **Input:** A sequence of predicted emotions, one‐hot encoded as 6‐dim vectors (e.g. `[1,0,0,0,0,0]` for “anger”).
* **Method:** At each new sentence $t$, update the trend vector $T_t$ by blending the previous trend $T_{t-1}$ with the new one‐hot vector $e_t$:

  $$
  T_t = \alpha \;T_{t-1} \;+\; (1-\alpha)\;e_t
  $$

  * $0 < \alpha < 1$ is the **decay factor** (e.g. 0.8).
  * Older inputs fade exponentially; recent inputs dominate.
* **Trend Extraction:**
  $\text{trend}_t = \argmax(T_t)$
  The index of the highest component in $T_t$ gives the **current emotion trend**.

---

## 2. Implementation Pseudocode

```python
# PARAMETERS
alpha = 0.8                # decay factor
T = [0.0]*6                # initial trend vector (6 dims)

for each new_emotion_label in conversation:
    e = one_hot(new_emotion_label, num_classes=6)
    T = [alpha * T[i] + (1 - alpha) * e[i] for i in range(6)]
    trend_label = argmax(T)
    # trend_label is the weighted emotion trend
```

* **one\_hot(...)** converts a label to a 6‐dim binary vector.
* **argmax(...)** picks the index of the maximum value in $T$.

---

## 3. 10‐Point Demo (α = 0.8)

We normalize the raw EMA weights so they sum to **10 points** for a 10‐slot sliding window.

|            Slot | Raw Weight (`0.8^(10 - k)`) | Normalized (%) |  Points (of 10) |
| --------------: | ----------------------------- | -------------: | --------------: |
|               1 | 0.8⁹ = 0.1342                |           3.0% |            0.30 |
|               2 | 0.8⁸ = 0.1678                |           3.8% |            0.38 |
|               3 | 0.8⁷ = 0.2097                |           4.7% |            0.47 |
|               4 | 0.8⁶ = 0.2621                |           5.9% |            0.59 |
|               5 | 0.8⁵ = 0.3277                |           7.3% |            0.73 |
|               6 | 0.8⁴ = 0.4096                |           9.2% |            0.92 |
|               7 | 0.8³ = 0.5120                |          11.5% |            1.15 |
|               8 | 0.8² = 0.6400                |          14.4% |            1.44 |
|               9 | 0.8¹ = 0.8000                |          17.9% |            1.79 |
|              10 | 0.8⁰ = 1.0000                |          22.4% |            2.24 |
| **Total** | —                            | **100%** | **10.00** |

* **Interpretation:** Slot 10 (most recent) holds 2.24 points; Slot 1 (oldest) only 0.30.
* On each new sentence, slide the window: the latest becomes slot 10 (2.24), others shift down.

---

## 4. Why EMA Was Chosen

1. **Nonlinear Recency Bias** — captures the intuition that recent sentences should matter disproportionately more.
2. **Simplicity & Efficiency** — zero extra trainable parameters; fast, constant‐time update per sentence.
3. **Interpretability** — you can precisely trace each sentence’s contribution via the point demo.
4. **Upgrade Path** — if needed, replace EMA with a small BiGRU for learnable, complex temporal patterns.
