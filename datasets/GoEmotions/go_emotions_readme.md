# GoEmotions Dataset

This folder contains the [GoEmotions](https://github.com/google-research/google-research/tree/master/goemotions) dataset, a large-scale corpus for fine-grained emotion classification built on English Reddit comments.

- **Source:** [GitHub: google-research/goemotions](https://github.com/google-research/google-research/tree/master/goemotions)
- **Paper:** [Demszky et al., 2020](https://arxiv.org/abs/2005.00547)

## Description

- **Size:** 58,000+ carefully curated utterances, each labeled with one or more of 28 emotion categories or "neutral"
- **Format:** Text (TSV), each row contains the utterance and its label(s)
- **Label Set:** See `emotions.txt` for all 28 emotions
- **Mappings:**
  - `ekman_mapping.json` – Groups emotions by Ekman categories
  - `sentiment_mapping.json` – Maps emotions to positive/negative/ambiguous sentiment

## Files

- `train.tsv`, `dev.tsv`, `test.tsv`: Main data splits
- `emotions.txt`: Full emotion list
- `ekman_mapping.json`, `sentiment_mapping.json`: Emotion-to-superclass dictionaries

## Usage

Suitable for emotion classification, nuanced sentiment analysis, and building emotion-aware language models.

## Citation

If you use this dataset, please cite:

```
@inproceedings{demszky2020goemotions,
  title={GoEmotions: A Dataset of Fine-Grained Emotions},
  author={Demszky, Dorottya and Movshovitz-Attias, Dana and Ko, Yichao and Cowen, Alan and Nemade, Gaurav and Ravi, Sujith},
  booktitle={Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics},
  year={2020}
}
```

