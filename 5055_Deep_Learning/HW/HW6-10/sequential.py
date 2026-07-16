import torch
import numpy as np
from torch import nn
from torch.utils.data import Dataset


batch = 4096


def create_dataset(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size - 1):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size])
    return np.array(X), np.array(y)


class DipeptideDataset(Dataset):
    def __init__(self, data, labels=None, history=10):
        self.data = data
        self.labels = labels
        self.history = history

    def __len__(self):
        if self.labels is not None:
            return self.data.shape[0]
        return self.data.shape[0] - self.history

    def __getitem__(self, idx):
        if self.labels is not None:
            return self.data[idx], self.labels[idx]
        return self.data[idx:idx + self.history], self.data[idx + self.history]


class NeuralNetwork(nn.Module):
    def __init__(self, history=10, hidden=768):
        super(NeuralNetwork, self).__init__()
        self.history = history
        self.hidden = hidden
        self.net = nn.Sequential(
            nn.Linear(history * 30, hidden),
            nn.SiLU(),
            nn.Linear(hidden, hidden),
            nn.SiLU(),
            nn.Linear(hidden, 30),
        )

    def forward(self, x):
        """
        Use the most recent history frames from the 200-step checker window.
        """
        x = x[:, -self.history:, :].reshape(x.shape[0], -1)
        return self.net(x)


class TCNBlock(nn.Module):
    def __init__(self, channels, dilation):
        super(TCNBlock, self).__init__()
        self.net = nn.Sequential(
            nn.Conv1d(channels, channels, kernel_size=3, padding=dilation, dilation=dilation),
            nn.SiLU(),
            nn.Conv1d(channels, channels, kernel_size=3, padding=dilation, dilation=dilation),
        )
        self.act = nn.SiLU()

    def forward(self, x):
        return self.act(x + self.net(x))


class TCNResidualNetwork(nn.Module):
    def __init__(self, history=50, hidden=192, levels=5, mean=None, std=None):
        super(TCNResidualNetwork, self).__init__()
        self.history = history
        self.hidden = hidden
        self.levels = levels
        if mean is None:
            mean = torch.zeros(30)
        if std is None:
            std = torch.ones(30)
        self.register_buffer("coord_mean", mean.float().reshape(1, 1, 30))
        self.register_buffer("coord_std", std.float().reshape(1, 1, 30).clamp_min(1e-6))
        self.input = nn.Conv1d(90, hidden, kernel_size=3, padding=1)
        self.blocks = nn.Sequential(*[TCNBlock(hidden, 2 ** i) for i in range(levels)])
        self.head = nn.Sequential(
            nn.SiLU(),
            nn.Linear(hidden, hidden),
            nn.SiLU(),
            nn.Linear(hidden, 30),
        )

    def _features(self, x):
        x = x[:, -self.history:, :]
        x_norm = (x - self.coord_mean) / self.coord_std
        v = torch.zeros_like(x_norm)
        v[:, 1:, :] = x_norm[:, 1:, :] - x_norm[:, :-1, :]
        a = torch.zeros_like(x_norm)
        a[:, 2:, :] = v[:, 2:, :] - v[:, 1:-1, :]
        return torch.cat([x_norm, v, a], dim=-1)

    def forward(self, x):
        features = self._features(x).transpose(1, 2)
        hidden = self.input(features)
        hidden = self.blocks(hidden)
        pooled = hidden[:, :, -1]
        delta_norm = self.head(pooled)
        last = x[:, -1, :]
        return last + delta_norm * self.coord_std.reshape(1, 30)


def train(net, train_loader, test_loader=None, epochs=18, lr=1e-3):
    optimizer = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    criterion = nn.MSELoss()

    for _ in range(epochs):
        for data, labels in train_loader:
            optimizer.zero_grad()
            outputs = net(data)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        scheduler.step()
    return net


if __name__ == "__main__":
    raw_data = torch.from_numpy(np.load('./trainDipeptide.npy')).float()
    trainset = DipeptideDataset(raw_data, history=10)
    train_loader = torch.utils.data.DataLoader(trainset, batch_size=batch, shuffle=True)

    net = NeuralNetwork(history=10, hidden=768)
    print(net)
    train(net, train_loader)
    torch.save(net, 'sequential.pth')
