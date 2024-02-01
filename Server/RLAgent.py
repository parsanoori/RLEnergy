import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class DQNAgent:
    def __init__(self, input_size, output_value, learning_rate=0.001, epsilon=1.0, epsilon_decay=0.9995,
                 epsilon_min=0.01, memory_size=1000000, batch_size=64):
        self.input_size = input_size
        self.output_size = output_value * 2 + 1
        self.output_value = output_value
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.memory = deque(maxlen=self.memory_size)
        self.model = DQN(self.input_size, self.output_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.loss = nn.MSELoss()
        self.last_reward = None
        self.goods = 0
        self.bads = 0

    def act(self, state):
        if self.epsilon <= self.epsilon_min:
            theta = np.random.beta(self.goods + 1, self.bads + 1)
            if 0.1 > theta:
                with torch.no_grad():
                    state = torch.tensor(state, dtype=torch.float).view(-1, self.input_size)
                    res = torch.argmax(self.model(state)).item() - self.output_value
                    return res
            else:
                return random.randint(self.output_value * -1, self.output_value)
        else:
            if np.random.rand() <= self.epsilon:
                return random.randint(self.output_value * -1, self.output_value)
            else:
                with torch.no_grad():
                    state = torch.tensor(state, dtype=torch.float).view(-1, self.input_size)
                    res = torch.argmax(self.model(state)).item() - self.output_value
                    return res

    def remember(self, state, action, reward, next_state, done):
        if self.last_reward is not None:
            if reward > self.last_reward:
                self.goods += 1
            else:
                self.bads += 1
        self.memory.append((state, action, reward, next_state, done))
        self.last_reward = reward

    def replay(self):
        if len(self.memory) - 1 < self.batch_size:
            return

        batch = list(self.memory)
        batch.pop(0)
        batch = random.sample(batch, self.batch_size)
        states = torch.tensor([i[0] for i in batch], dtype=torch.float).view(-1, self.input_size)
        actions = torch.tensor([i[1] + self.output_value for i in batch], dtype=torch.long).view(-1, 1)
        rewards = torch.tensor([i[2] for i in batch], dtype=torch.float).view(-1, 1)
        next_states = torch.tensor([i[3] for i in batch], dtype=torch.float).view(-1, self.input_size)

        q_values = self.model(states).gather(1, actions)
        next_q_values = self.model(next_states).max(1)[0].view(-1, 1)
        target_q_values = rewards + next_q_values
        loss = self.loss(q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.memory = deque(maxlen=self.memory_size)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

