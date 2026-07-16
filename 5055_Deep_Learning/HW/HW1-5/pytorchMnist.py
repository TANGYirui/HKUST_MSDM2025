import torch
import numpy as np
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import torch.optim as optim

batch_size = 200

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data', train=True, download=True,
                   transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ])),batch_size=batch_size, shuffle=True)

test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data', train=False, transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])),
    batch_size=batch_size, shuffle=False)

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        '''
        Implement your model
        '''
        raise Exception("No implementation")

    def forward(self, x):
        '''
        Implement your model
        '''
        raise Exception("No implementation")

def train(net):
    '''
    Train your model
    '''
    raise Exception("No implementation")

if __name__ == "__main__":
    net = NeuralNetwork()
    train(net)
    torch.save(net, 'mnistNet.pth')

