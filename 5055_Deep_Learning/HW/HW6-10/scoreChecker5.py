import torch
import numpy as np
from reinforcement import NeuralNetwork
import gymnasium as gym
import random

seed = 42

random.seed(seed)
torch.manual_seed(seed)
np.random.seed(seed)

device = torch.device("cpu")

trialTime = 20
maxStep = int(4e3)


def simulate(net, trialTime=20, maxStep=4000):
    env = gym.make('Assault-v4', obs_type="ram")
    env.reset(seed=seed)
    maxReward = 0
    for episode in range(trialTime):
        s, info = env.reset()
        totalReward = 0
        for step in range(maxStep):
            with torch.no_grad():
                action = net.action(torch.from_numpy(s).unsqueeze(0)/255)
            if type(action) is torch.Tensor:
                action = action.detach().item()
            s2, r, term, trun, info = env.step(action)
            totalReward += r
            s = s2
            #print("episode", episode, ", timeStep", step, ", action", action, ", reward", r)

            if term:
                #print("ending episode.")
                break

        if totalReward > maxReward:
            maxReward = totalReward
    env.close()
    return maxReward


net = torch.load("reinforcement.pth", map_location=device, weights_only=False)

params = list(net.parameters())
params = list(filter(lambda p: p.requires_grad, params))
nparams = sum([np.prod(p.size()) for p in params])
print('total number of trainable parameters:', nparams)

maxReward = simulate(net, trialTime=trialTime, maxStep=maxStep)
print('best total reward:', maxReward)
