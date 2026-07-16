import torch
import numpy as np
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import torch.optim as optim

batch_size = 100
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                           shuffle=True)

testset = datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
test_loader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False)


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
    print(net)
    train(net)
    torch.save(net, 'cifarNet.pth')

