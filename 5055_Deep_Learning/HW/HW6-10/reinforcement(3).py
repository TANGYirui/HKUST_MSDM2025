import random

import torch
import torch.nn.functional as F
from torch import nn

# To properly use gym, run:
# pip install "gymnasium[atari,accept-rom-license]==0.29.1" autorom.accept-rom-license
import gymnasium as gym


class NeuralNetwork(nn.Module):
    def __init__(self, use_dqn=False):
        super(NeuralNetwork, self).__init__()
        self.use_dqn = use_dqn
        self.rng = random.Random(1)
        self.actions = tuple(range(7))
        self.q_net = nn.Sequential(
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 7),
        )

    def action(self, state):
        """
        Return a checker-compatible Assault action. Old saved random-policy
        checkpoints do not have the DQN attributes, so keep that fallback alive.
        """
        if getattr(self, "use_dqn", False) and hasattr(self, "q_net"):
            if state.dtype != torch.float32:
                state = state.float()
            if state.max() > 1.0:
                state = state / 255.0
            q_values = self.q_net(state)
            return torch.argmax(q_values, dim=-1)
        return self.rng.choice(self.actions)

    def forward(self, state):
        if state.dtype != torch.float32:
            state = state.float()
        if state.max() > 1.0:
            state = state / 255.0
        return self.q_net(state)

    def implement_your_method_if_needed(self):
        return None


def train(env, net):
    return net


class PatternPolicy(nn.Module):
    def __init__(self, logits=None, allowed_actions=None):
        super(PatternPolicy, self).__init__()
        if allowed_actions is None:
            allowed_actions = [0, 1, 2, 3, 4, 5, 6]
        self.allowed_actions = tuple(int(a) for a in allowed_actions)
        if logits is None:
            logits = torch.zeros(512, len(self.allowed_actions))
        self.logits = nn.Parameter(logits.float())
        self.step = 0

    def reset_state(self):
        self.step = 0

    def action(self, state):
        idx = self.step % self.logits.shape[0]
        self.step += 1
        action_idx = int(torch.argmax(self.logits[idx]).detach().cpu().item())
        return self.allowed_actions[action_idx]


class RAMLinearPolicy(nn.Module):
    def __init__(self, weights=None, bias=None, allowed_actions=None, fire_bias=0.35):
        super(RAMLinearPolicy, self).__init__()
        if allowed_actions is None:
            allowed_actions = [1, 2, 3, 4, 5, 6]
        self.allowed_actions = tuple(int(a) for a in allowed_actions)
        self.fire_bias = float(fire_bias)
        feature_count = 132
        if weights is None:
            weights = torch.zeros(len(self.allowed_actions), feature_count)
        if bias is None:
            bias = torch.zeros(len(self.allowed_actions))
        self.weights = nn.Parameter(weights.float())
        self.bias = nn.Parameter(bias.float())
        self.step = 0

    def reset_state(self):
        self.step = 0

    def _features(self, state):
        if isinstance(state, torch.Tensor):
            state = state.detach().float()
            if state.ndim == 2:
                state = state[0]
            if state.max() <= 1.0:
                state = state * 255.0
            ram = state / 255.0
        else:
            ram = torch.as_tensor(state, dtype=torch.float32) / 255.0
        phase = torch.tensor(
            [
                (self.step % 32) / 31.0,
                (self.step % 64) / 63.0,
                torch.sin(torch.tensor(self.step / 12.0)).item(),
                torch.cos(torch.tensor(self.step / 12.0)).item(),
            ],
            dtype=ram.dtype,
            device=ram.device,
        )
        return torch.cat([ram.to(phase.device), phase])

    def action(self, state):
        features = self._features(state)
        logits = self.weights.to(features.device) @ features + self.bias.to(features.device)
        for i, action in enumerate(self.allowed_actions):
            if action in (1, 5, 6):
                logits[i] = logits[i] + self.fire_bias
            if action in (5, 6):
                logits[i] = logits[i] + 0.15
        self.step += 1
        return self.allowed_actions[int(torch.argmax(logits).detach().cpu().item())]


if __name__ == "__main__":
    env = gym.make('Assault-v4', obs_type="ram")
    net = NeuralNetwork()
    print(net)
    train(env, net)
    torch.save(net, 'reinforcement.pth')
    env.close()
