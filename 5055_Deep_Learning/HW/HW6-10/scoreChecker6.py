import torch
import numpy as np
from torch import nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from sequential import NeuralNetwork

def create_dataset(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size - 1):
        X.append(data[i:i+window_size])
        y.append(data[i+window_size])
    return np.array(X), np.array(y)


class DipeptideDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return self.data.shape[0]

    def __getitem__(self, idx):
        dat = self.data[idx]
        lab = self.labels[idx]

        return dat, lab


device = torch.device('cuda:0')
data = np.load('./testDipeptide.npy')
batch = 256

data, labels = [torch.from_numpy(term).float() for term in create_dataset(data, 200)]
testset = DipeptideDataset(data, labels)
test_loader = torch.utils.data.DataLoader(testset, batch_size=batch,
                                          shuffle=False)

criterion = nn.MSELoss()
net = torch.load("sequential.pth", map_location=device, weights_only=False)
params = list(net.parameters())
params = list(filter(lambda p: p.requires_grad, params))
nparams = sum([np.prod(p.size()) for p in params])
print('total number of trainable parameters:', nparams)

test_loss_Lst = []
net.eval()
with torch.no_grad():
    for idx, data in enumerate(test_loader):
        data = [term.to(device) for term in data]
        test_outputs = net(data[0])
        test_loss = criterion(test_outputs, data[1])
        test_loss_Lst.append(test_loss.item())
    print(f'Test Loss: {np.mean(test_loss_Lst):.4f}')
