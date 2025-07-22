# AnnoMI: Annotated Motivational Interviewing Conversations

**Source**:

- Kaggle: https://www.kaggle.com/datasets/rahulbaburaj/annomi
- GitHub: https://github.com/uccollab/AnnoMI

**Description**:AnnoMI is a public dataset of therapist-client dialogues from real motivational interviewing (MI) sessions, fully annotated by MI experts.Each row represents a single utterance (either therapist or client), including:

- `utterance_text`: The spoken sentence/text.
- `speaker_type`: “therapist” or “client”.
- `transcript_id`: Grouping for full conversations.
- `mi_quality`: Expert rating of MI quality for the transcript.
- **Therapist utterances**: Annotated for main behavior type (e.g. question, reflection, information).
- **Client utterances**: Annotated for “change talk”, “neutral talk”, or “sustain talk” (client's orientation to change).

**Use in this project**:

- The `utterance_text` column is included in our word2vec corpus to ensure high-quality, domain-specific embeddings.
- Optionally, therapist and client utterances can be split for advanced modeling.
- MI and topic annotations enable future experiments in behavior recognition or MI quality estimation.

**License**:
See Kaggle/GitHub links for full licensing and usage terms.
