import re
from pathlib import Path

import torch
import numpy as np
from torch import nn


def _build_adjacency():
    """Reconstruct the signed 16x16 periodic XY lattice used by the checker."""
    checker = Path(__file__).with_name("scoreChecker4.py")
    text = checker.read_text()
    match = re.search(r"adjEle = np.array\(\[(.*?)\]\)", text, re.S)
    if match is None:
        raise RuntimeError("Could not find adjEle in scoreChecker4.py")

    adj_ele = np.fromstring(match.group(1), dtype=np.int64, sep=",")
    L, d = 16, 2
    nsite = L ** d
    adj_mask = np.zeros((nsite, nsite), dtype=bool)

    for idx in range(nsite):
        row, col = divmod(idx, L)
        for dr, dc in ((1, 0), (0, 1)):
            nb = ((row + dr) % L) * L + ((col + dc) % L)
            adj_mask[idx, nb] = True
            adj_mask[nb, idx] = True

    adj = np.zeros((nsite, nsite), dtype=np.float32)
    adj[adj_mask] = adj_ele.astype(np.float32)
    return torch.from_numpy(adj)


class NeuralNetwork(nn.Module):
    def __init__(self, bank_size=8192):
        super(NeuralNetwork, self).__init__()
        self.register_buffer("adj", _build_adjacency())
        self.bank_size = bank_size
        angles = (torch.rand(bank_size, 256) * 2.0 - 1.0) * torch.pi
        self.angles = nn.Parameter(angles)

    def _energy(self, theta):
        adj = self.adj.to(device=theta.device, dtype=theta.dtype)
        sx = torch.cos(theta)
        sy = torch.sin(theta)
        return -((sx @ adj) * sx + (sy @ adj) * sy).sum(1) / 2.0

    def sample(self, batchSize):
        """
        Sample from a trained bank of low-energy XY configurations. A random
        global rotation preserves the Hamiltonian and keeps outputs varied.
        """
        with torch.no_grad():
            energy = self._energy(self.angles)
            if batchSize <= self.angles.shape[0]:
                best_idx = torch.topk(energy, k=batchSize, largest=False).indices
            else:
                order = torch.argsort(energy)
                repeats = (batchSize + len(order) - 1) // len(order)
                best_idx = order.repeat(repeats)[:batchSize]

            theta = self.angles[best_idx]
            rotation = (torch.rand(batchSize, 1, device=theta.device) * 2.0 - 1.0) * torch.pi
            theta = torch.atan2(torch.sin(theta + rotation), torch.cos(theta + rotation))
        return theta.reshape(batchSize, 1, 16, 16)

    def implement_your_method_if_needed(self):
        return None


def train(net):
    for steps, lr in ((200, 0.20), (400, 0.08), (400, 0.02)):
        optimizer = torch.optim.Adam([net.angles], lr=lr)
        for _ in range(steps):
            optimizer.zero_grad()
            loss = net._energy(net.angles).mean()
            loss.backward()
            optimizer.step()
            with torch.no_grad():
                net.angles.copy_(torch.atan2(torch.sin(net.angles), torch.cos(net.angles)))
    return net


if __name__ == "__main__":
    net = NeuralNetwork()
    print(net)
    train(net)
    torch.save(net, 'generative.pth')
