import torch
import torch.nn as nn
import torch.nn.functional as F

class Attention(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.attn = nn.Linear(dim, 1)
    def forward(self, seq):  # seq: (batch, seq_len, dim)
        scores = self.attn(seq).squeeze(-1)         # (batch, seq_len)
        weights = F.softmax(scores, dim=1)          # (batch, seq_len)
        return (seq * weights.unsqueeze(-1)).sum(dim=1)  # (batch, dim)

class BiLSTMClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        # --- 3 Stacked BiLSTM layers (input: batch, seq, 100) ---
        self.bilstm1 = nn.LSTM(100, 64, bidirectional=True, batch_first=True)
        self.dropout1 = nn.Dropout(0.3)
        self.bilstm2 = nn.LSTM(128, 64, bidirectional=True, batch_first=True)
        self.dropout2 = nn.Dropout(0.3)
        self.bilstm3 = nn.LSTM(128, 64, bidirectional=True, batch_first=True)
        # --- Attention layer ---
        self.attention = Attention(128)
        # --- 4 Dense + Dropout pairs ---
        self.dense1 = nn.Linear(128, 256)
        self.dropout3 = nn.Dropout(0.3)
        self.dense2 = nn.Linear(256, 128)
        self.dropout4 = nn.Dropout(0.3)
        self.dense3 = nn.Linear(128, 64)
        self.dropout5 = nn.Dropout(0.3)
        self.dense4 = nn.Linear(64, 32)
        self.dropout6 = nn.Dropout(0.3)
        # --- Output layer (6 emotion classes) ---
        self.output = nn.Linear(32, 6)
    def forward(self, x):  # x: (batch, seq_len, feat_dim)
        # 1. BiLSTM stack
        y, _ = self.bilstm1(x)       # (batch, seq_len, 128)
        y = self.dropout1(y)
        y, _ = self.bilstm2(y)       # (batch, seq_len, 128)
        y = self.dropout2(y)
        y, _ = self.bilstm3(y)       # (batch, seq_len, 128)
        # 2. Attention (aggregates sequence to single vector)
        y = self.attention(y)        # (batch, 128)
        # 3. Deep dense stack
        z = F.relu(self.dense1(y))
        z = self.dropout3(z)
        z = F.relu(self.dense2(z))
        z = self.dropout4(z)
        z = F.relu(self.dense3(z))
        z = self.dropout5(z)
        z = F.relu(self.dense4(z))
        z = self.dropout6(z)
        # 4. Output
        out = self.output(z)         # (batch, 6)
        return F.log_softmax(out, dim=-1)

# Example usage:
# model = BiLSTMClassifier()
# out = model(input_tensor)   # input_tensor: (batch, seq_len, 100)
