# PAIR Dataset

**PAIR** (Patient–Assistant Interaction Responses) is a dataset designed to support research and development in reflective listening, active listening, and therapeutic conversation modeling. It provides high-quality, human-written responses to patient prompts, demonstrating both ideal and suboptimal counseling dialogue styles.

## Contents

- **prompt**: Patient/client utterance or statement, reflecting a concern or issue they are facing.
- **hq1**: High-quality, therapist-modeled response 1. Demonstrates reflective, empathetic, and supportive listening.
- **hq2**: High-quality, therapist-modeled response 2. An alternative, equally strong therapist response for the same prompt.
- **mq1**: Medium-quality response. Less skillful, somewhat empathetic or reflective, but not ideal.
- **lq1 – lq5**: Low-quality responses. Examples of what *not* to say; lacking empathy, warmth, or clinical appropriateness.

## Usage Notes

- **Recommended use:** For mental health chatbot and dialogue modeling projects, use only the `hq1` and `hq2` columns paired with their associated `prompt`. These represent the highest standard of therapist response for each patient statement.
- **Not recommended:** Do not use `mq1` or any `lq#` columns for training dialogue agents; they are included for contrast and research on error analysis or empathy grading only.

## Example Format

| prompt                                              | response                                          |
| --------------------------------------------------- | ------------------------------------------------- |
| I don’t trust doctors. I don’t trust the CDC. ... | You feel that your immune systems is strong ...   |
| I don’t trust doctors. I don’t trust the CDC. ... | Putting your trust in others is hard for you. ... |

## Source & Licensing

- All responses are **human-written** for research and development in counseling/psychotherapy dialogue systems.
- If using for publication or redistribution, check the original source or dataset provider for licensing terms.
