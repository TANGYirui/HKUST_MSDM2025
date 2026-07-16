import torch
import numpy as np
from torch import nn
from generative import NeuralNetwork
import bz2
import random

seed = 42

random.seed(seed)
torch.manual_seed(seed)
np.random.seed(seed)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

adjEle = np.array([-1,-1,-1,-1,1,1,1,-1,-1,1,-1,1,-1,1,1,1,-1,1,-1,1,1,1,1,-1,1,-1,-1,1,-1,-1,-1,1,-1,-1,-1,-1,-1,1,1,1,-1,-1,-1,-1,-1,-1,-1,1,-1,1,-1,-1,1,1,1,1,1,1,-1,-1,-1,1,1,1,1,1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,-1,1,-1,1,-1,1,1,-1,1,1,-1,1,-1,-1,1,-1,1,1,-1,-1,1,-1,1,-1,1,1,1,-1,1,1,1,1,-1,1,-1,1,1,1,1,-1,1,1,-1,-1,1,1,1,-1,1,1,1,1,1,-1,-1,-1,-1,1,-1,1,-1,-1,1,1,1,1,-1,-1,1,1,1,1,-1,1,-1,1,1,1,1,1,1,1,-1,1,-1,1,1,-1,-1,1,-1,-1,-1,1,-1,1,-1,1,-1,-1,1,-1,-1,1,-1,1,1,-1,1,1,1,-1,-1,-1,-1,-1,1,1,-1,-1,-1,1,1,-1,1,1,-1,-1,1,1,-1,1,1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,-1,1,1,1,-1,-1,1,-1,1,1,-1,1,-1,-1,1,-1,-1,1,1,1,1,1,1,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1,1,-1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,1,1,-1,1,-1,-1,-1,1,-1,1,1,1,1,1,1,1,1,1,1,-1,1,1,1,-1,1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,1,1,-1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,1,-1,1,1,-1,-1,-1,-1,1,1,-1,1,-1,1,1,-1,-1,1,1,-1,1,1,1,-1,1,1,1,-1,1,-1,-1,1,-1,-1,-1,1,-1,-1,1,-1,1,1,-1,-1,-1,-1,-1,1,-1,-1,1,-1,1,-1,-1,-1,1,1,-1,-1,-1,1,1,-1,-1,1,-1,1,-1,1,-1,1,1,-1,1,-1,-1,1,1,-1,-1,-1,1,-1,1,-1,-1,1,1,-1,-1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,1,1,-1,1,-1,1,1,1,1,-1,1,-1,1,-1,-1,-1,-1,1,1,-1,1,1,-1,1,-1,-1,-1,-1,1,1,1,-1,-1,-1,-1,-1,1,1,-1,1,-1,-1,-1,1,1,1,-1,-1,-1,1,1,-1,1,-1,1,-1,-1,1,1,1,1,-1,1,-1,1,1,-1,-1,-1,-1,1,-1,-1,1,-1,-1,1,1,-1,1,-1,1,-1,1,1,1,-1,-1,1,1,1,1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,1,-1,1,1,1,-1,1,-1,-1,1,-1,1,-1,-1,-1,1,-1,-1,-1,-1,1,1,-1,1,-1,1,1,1,1,-1,-1,1,1,-1,1,-1,-1,1,-1,-1,1,1,-1,1,1,1,1,1,1,1,-1,1,-1,1,-1,-1,1,1,1,-1,1,-1,1,1,1,1,1,1,-1,-1,1,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1,1,-1,-1,-1,1,-1,1,-1,1,1,-1,-1,-1,1,1,1,-1,1,1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,1,1,-1,1,-1,1,1,1,1,1,-1,-1,1,1,1,1,1,1,-1,-1,-1,-1,1,-1,1,1,1,1,1,-1,1,1,1,-1,-1,-1,1,1,1,1,-1,1,-1,1,1,1,1,1,-1,1,1,1,1,-1,1,1,1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,-1,1,-1,1,1,-1,-1,1,1,1,1,1,-1,1,-1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,1,1,-1,-1,1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,-1,1,-1,1,-1,-1,-1,1,-1,-1,1,1,1,1,1,-1,-1,-1,1,-1,1,1,-1,-1,-1,1,1,-1,1,-1,-1,-1,1,-1,1,1,-1,-1,-1,-1,1,1,-1,-1,-1,1,-1,1,-1,-1,-1,-1,1,-1,-1,-1,1,-1,-1,1,-1,1,1,1,-1,-1,-1,1,-1,1,-1,-1,-1,1,1,-1,-1,-1,1,1,-1,1,1,-1,-1,1,-1,-1,-1,1,1,1,-1,-1,1,-1,-1,1,-1,-1,1,1,1,1,-1,-1,1,-1,1,-1,1,-1,1,-1,1,1,1,1,1,-1,-1,1,-1,1,1,-1,-1,1,-1,1,1,-1,-1,1,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,1,-1,1,1,-1,-1,-1,-1,-1,1,1,-1,-1,-1,1,1,-1,1,1,-1,1,-1,-1,-1,-1,1,-1,1,1,1,1,1,1,-1,-1,-1,1,-1,1,1,-1,1,-1,1,1,1,-1,1,1,-1,1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,-1,-1,-1,1,-1,-1,1,-1,1,-1,1,-1,-1,1,1,-1,1,1,1])

batchSize = 200


class Lattice:
    def __init__(self, L, d, BC='periodic'):
        self.L = L
        self.d = d
        self.shape = [L]*d
        self.Nsite = L**d
        self.BC = BC

    def move(self, idx, d, shift):
        coord = self.index2coord(idx)
        coord[d] += shift

        if self.BC != 'periodic':
            if (coord[d] >= self.L) or (coord[d] < 0):
                return None
        #wrap around because of the PBC
        if (coord[d] >= self.L): coord[d] -= self.L
        if (coord[d] < 0): coord[d] += self.L

        return self.coord2index(coord)

    def index2coord(self, idx):
        coord = np.zeros(self.d, int)
        for d in range(self.d):
            coord[self.d - d - 1] = idx % self.L
            idx /= self.L
        return coord

    def coord2index(self, coord):
        idx = coord[0]
        for d in range(1, self.d):
            idx *= self.L
            idx += coord[d]
        return idx


class Hypercube(Lattice):
    def __init__(self, L, d, BC='periodic'):
        super(Hypercube, self).__init__(L, d, BC)
        self.Adj = np.zeros((self.Nsite, self.Nsite), int)
        for i in range(self.Nsite):
            for d in range(self.d):
                j = self.move(i, d, 1)

                if j is not None:
                    self.Adj[i, j] = 1.0
                    self.Adj[j, i] = 1.0


def energy(batch, adjEle=adjEle):
    lattice = Hypercube(16, 2)
    adjMask = torch.from_numpy(lattice.Adj).bool()
    adjEle = torch.from_numpy(adjEle).long()

    adj = torch.zeros(adjMask.shape, dtype=torch.long)
    adj = adj.masked_scatter(adjMask, adjEle).to(batch)

    samples = torch.cat([torch.cos(batch), torch.sin(batch)], dim=1)
    energy = -((samples.flatten(-2) @ adj.to(torch.float32)) * samples.flatten(-2)).sum([-2, -1]).unsqueeze(-1)/2
    return energy


def testIfDuplicateWithDataset(batch, testPoints=20, tol=1e-2):
    randIdx = torch.randint(0, 256, [testPoints])
    dfile = bz2.BZ2File('./xyData.bz2')
    data = torch.from_numpy(np.load(dfile)).to(torch.float32)
    dfile.close()
    sampleData = torch.sin(data.reshape(-1, 256)[:, randIdx]).to(batch)
    sampleBatch = torch.cos(batch.reshape(-1, 256)[:, randIdx])
    difference = torch.abs(sampleBatch.unsqueeze(1) - sampleData).reshape(batch.shape[0], -1).mean(-1)
    num = torch.sum(difference <= tol)
    ratio = num.item() / batch.shape[0]
    return ratio

net = torch.load("generative.pth", map_location=device, weights_only=False)
params = list(net.parameters())
params = list(filter(lambda p: p.requires_grad, params))
nparams = sum([np.prod(p.size()) for p in params])
print('total number of trainable parameters:', nparams)

with torch.no_grad():
    batch = net.sample(batchSize)
    ratio = testIfDuplicateWithDataset(batch)
    meanenergy = energy(batch).mean().item()

if ratio > 0.1:
    print("!! duplicate with dataset:", ratio * 100)
print("mean energy:", meanenergy)




