import torch
import torch.nn as nn
import torch.nn.functional as F

class Highway(nn.Module):
    def __init__(self, size):
        super().__init__()
        self.proj = nn.Linear(size, size)
        self.gate = nn.Linear(size, size)
    def forward(self, x):
        h = torch.tanh(self.proj(x))
        t = torch.sigmoid(self.gate(x))
        return h * t + x * (1 - t)

class Attention(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.attn = nn.Linear(dim, 1)
    def forward(self, seq):  # seq: (batch, seq_len, dim)
        scores = self.attn(seq).squeeze(-1)       # (batch, seq_len)
        weights = F.softmax(scores, dim=1)        # (batch, seq_len)
        return (seq * weights.unsqueeze(-1)).sum(dim=1)  # (batch, dim)

class HANHighwayDeep(nn.Module):
    def __init__(self):
        super().__init__()
        # --- Word-level ---
        self.word_bilstm1 = nn.LSTM(100, 64, bidirectional=True, batch_first=True)
        self.word_highway1 = Highway(128)
        self.word_bilstm2 = nn.LSTM(128, 64, bidirectional=True, batch_first=True)
        self.word_highway2 = Highway(128)
        self.word_attention = Attention(128)

        # --- Sentence-level ---
        self.sent_bilstm1 = nn.LSTM(128, 64, bidirectional=True, batch_first=True)
        self.sent_highway1 = Highway(128)
        self.sent_bilstm2 = nn.LSTM(128, 64, bidirectional=True, batch_first=True)
        self.sent_highway2 = Highway(128)
        # Transformer encoder block for sentences
        encoder_layer = nn.TransformerEncoderLayer(d_model=128, nhead=4, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=1)
        self.sent_attention = Attention(128)

        # --- Deep Dense Stack with Highways and Dropouts ---
        self.dense1 = nn.Linear(128, 512)
        self.highway3 = Highway(512)
        self.dropout1 = nn.Dropout(0.3)

        self.dense2 = nn.Linear(512, 256)
        self.highway4 = Highway(256)
        self.dropout2 = nn.Dropout(0.3)

        self.dense3 = nn.Linear(256, 128)
        self.highway5 = Highway(128)
        self.dropout3 = nn.Dropout(0.3)

        self.dense4 = nn.Linear(128, 128)
        self.highway6 = Highway(128)
        self.dropout4 = nn.Dropout(0.3)

        self.dense5 = nn.Linear(128, 64)
        self.highway7 = Highway(64)
        self.dropout5 = nn.Dropout(0.3)

        self.dense6 = nn.Linear(64, 32)
        self.highway8 = Highway(32)

        self.output = nn.Linear(32, 6)

    def forward(self, x):  # x: (batch, sents, words, feat)
        # 1. Word-level BiLSTM+Highway+Attention per sentence (TimeDistributed)
        sents = []
        for i in range(x.shape[1]):  # Loop over sentences (5)
            w = x[:, i, :, :]                 # (batch, 20, 100)
            w, _ = self.word_bilstm1(w)       # (batch, 20, 128)
            w = self.word_highway1(w)
            w, _ = self.word_bilstm2(w)       # (batch, 20, 128)
            w = self.word_highway2(w)
            s = self.word_attention(w)        # (batch, 128)
            sents.append(s)
        sent_seq = torch.stack(sents, dim=1)  # (batch, 5, 128)

        # 2. Sentence-level BiLSTM+Highway+Transformer+Attention
        y, _ = self.sent_bilstm1(sent_seq)    # (batch, 5, 128)
        y = self.sent_highway1(y)
        y, _ = self.sent_bilstm2(y)           # (batch, 5, 128)
        y = self.sent_highway2(y)
        y = self.transformer_encoder(y)       # (batch, 5, 128)
        doc_vec = self.sent_attention(y)      # (batch, 128)

        # 3. Deep Dense + Highway + Dropout stack
        z = F.relu(self.dense1(doc_vec))
        z = self.highway3(z)
        z = self.dropout1(z)
        z = F.relu(self.dense2(z))
        z = self.highway4(z)
        z = self.dropout2(z)
        z = F.relu(self.dense3(z))
        z = self.highway5(z)
        z = self.dropout3(z)
        z = F.relu(self.dense4(z))
        z = self.highway6(z)
        z = self.dropout4(z)
        z = F.relu(self.dense5(z))
        z = self.highway7(z)
        z = self.dropout5(z)
        z = F.relu(self.dense6(z))
        z = self.highway8(z)

        # 4. Output
        out = self.output(z)
        return F.log_softmax(out, dim=-1)  # (batch, 6)

