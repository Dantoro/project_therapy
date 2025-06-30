# Clinical Dialogues Dataset

This folder contains the "Mental Health Counseling Conversations" dataset, a large collection of real-world clinical dialogues between individuals seeking support and licensed therapists. Each example consists of a user's context/question and a detailed therapist response, making it well-suited for research in empathetic language modeling, dialogue systems, and word embedding training for mental health applications.

- **Source:** [Kaggle: Mental Health Counseling Conversations](https://www.kaggle.com/datasets/melissamonfared/mental-health-counseling-conversations-k)
- **Original Data/Writeup:** [Medium Article](https://medium.com/data-science/counsel-chat-bootstrapping-high-quality-therapy-data-971b419f33da)
- **HuggingFace version:** [counsel-chat](https://huggingface.co/datasets/nbertagnolli/counsel-chat)
- **GitHub:** [counsel-chat repo](https://github.com/nbertagnolli/counsel-chat)

## File Structure

- `combined_dataset.json`: Main dataset; a JSON lines file, each entry with "Context" (patient input) and "Response" (therapist reply).
- Other CSV files may be present but are not primary sources for this project.

## Citation

If you use this data, please cite the medium article:

```
@misc{bertagnolli2020counsel,
  title={Counsel chat: Bootstrapping high-quality therapy data},
  author={Bertagnolli, Nicolas},
  year={2020},
  publisher={Towards Data Science. https://towardsdatascience.com/counsel-chat-bootstrapping-high-quality-therapy-data-971b419f33da}
}
```

