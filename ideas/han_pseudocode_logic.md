stm_buffer = [utterance_1, utterance_2, ..., utterance_n]
utterance_vectors = []
for utter in stm_buffer:
    cnn_vec = cnn(utter)  # 200d
    words = word_tokenize(utter)
    word_embs = []
    for w in words:
        glove_vec = glove[w]
        w2v_vec = word2vec[w]
        full_vec = concat([cnn_vec, glove_vec, w2v_vec])  # 1000d
        word_embs.append(dense_1000to512(full_vec))
    word_bilstm_out = word_bilstm(word_embs)  # seq of 512d
    word_attention_out = attention(word_bilstm_out)  # collapse to 512d
    utterance_vectors.append(word_attention_out)
utter_bilstm_out = utter_bilstm(utterance_vectors)  # seq of 512d
final_context = utter_attention(utter_bilstm_out)   # collapse to 512d
final_output = dense_512to256(final_context)        # 256d
