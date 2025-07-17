ekman category transformer: https://huggingface.co/j-hartmann/emotion-english-roberta-large

"With this model, you can classify emotions in English text data. The model was trained on 6 diverse datasets (see Appendix below) and predicts Ekman's 6 basic emotions, plus a neutral class:

All datasets contain English text. The table summarizes which emotions are available in each of the datasets. The datasets represent a diverse collection of text types. Specifically, they contain emotion labels for texts from Twitter, Reddit, student self-reports, and utterances from TV dialogues. As MELD (Multimodal EmotionLines Dataset) extends the popular EmotionLines dataset, EmotionLines itself is not included here."

emotion transformer: https://huggingface.co/SamLowe/roberta-base-go_emotions

"Model trained from roberta-base on the go_emotions dataset for multi-label classification.

ONNX version also available
A version of this model in ONNX format (including an INT8 quantized ONNX version) is now available at https://huggingface.co/SamLowe/roberta-base-go_emotions-onnx. These are faster for inference, esp for smaller batch sizes, massively reduce the size of the dependencies required for inference, make inference of the model more multi-platform, and in the case of the quantized version reduce the model file/download size by 75% whilst retaining almost all the accuracy if you only need inference.

Dataset used for the model

go_emotions is based on Reddit data and has 28 labels. It is a multi-label dataset where one or multiple labels may apply for any given input text, hence this model is a multi-label classification model with 28 'probability' float outputs for any given input text. Typically a threshold of 0.5 is applied to the probabilities for the prediction for each label."
