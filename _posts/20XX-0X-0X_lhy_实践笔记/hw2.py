# coding=utf-8

'''
Author:franztao
Email:taoheng@stonewise.cn;franztaoheng@gmail.com
github:https://github.com/hengfanz
'''
import torch
import torch
from torch import nn
from torchcrf import CRF


class Crf(nn.Module):
    def __init__(self, class_size=41):
        super().__init__()
        self.class_size = class_size
        self.crf = CRF(self.class_size, batch_first=True)

    def likelihood(self, x, y):
        return self.crf(x, y)

    def forward(self, x):
        return torch.LongTensor(self.crf.decode(x))


class BILSTM_CRF(nn.Module):
    def __init__(self, class_size=41, input_dim=39, hidden_dim=128, dropout=0.5):
        super().__init__()
        self.input_dim = input_dim
        self.hiddin_dim = hidden_dim
        self.class_size = class_size
        self.lstm = nn.LSTM(input_dim, hidden_dim // 2, dropout=dropout, num_layers=3, bidirectional=True,
                            batch_first=True)
        self.hidden2tag = nn.Sequential(nn.Dropout(dropout), nn.Linear(hidden_dim, class_size))

        self.crf = CRF(self.class_size, batch_first=True)

    def get_emmisions(self, x):
        feats, _ = self.lstm(x)
        return self.hidden2tag(feats)

    def likelihood(self, x, y):
        emmisions = self.get_emmisions(x)
        loss = self.crf(emmisions, y)
        return loss

    def forward(self, x):
        emmisions = self.get_emmisions(x)
        seqs = self.crf.decode(emmisions)
        return torch.LongTensor(seqs)


class BiLSTM(nn.Module):
    def __init__(self, class_size=41, input_dim=39, hidden_dim=192, dropout=0.5):
        super().__init__()
        super().__init__()
        self.input_dim = input_dim
        self.hiddin_dim = hidden_dim
        self.class_size = class_size
        self.lstm = nn.LSTM(input_dim, hidden_dim // 2, dropout=dropout, num_layers=3, bidirectional=True,
                            batch_first=True)
        self.hidden2tag = nn.Sequential(nn.Dropout(dropout), nn.Linear(hidden_dim, class_size))

    def forward(self, x):
        feats, _ = self.lstm(x)
        return self.hidden2tag(feats)


device=0
learning_rate=0.01
bilstm=BiLSTM().to(device)
crf=Crf.to(device)
torch.optim.AdamW(crf.parameters(),lr=learning_rate*20,weight_decay=0.015)
schedule=torch.optim.lr_scheduler.CosineAnnealingWarmRestarts

bilstm.parameters()

nn.BatchNorm2d
