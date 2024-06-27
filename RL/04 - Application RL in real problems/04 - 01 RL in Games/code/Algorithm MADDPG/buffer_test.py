from collections import deque

import numpy as np
import random
import torch

class replayBuffer:
    def __init__(self, buffer_size: int):
        self.buffer_size = buffer_size
        self.buffer = []
        self._next_idx = 0

    def add(self, item):
        if len(self.buffer) > self._next_idx:
            self.buffer[self._next_idx] = item
        else:
            self.buffer.append(item)
        if self._next_idx == self.buffer_size - 1:
            self._next_idx = 0
        else:
            self._next_idx = self._next_idx + 1

    def sample(self, batch_size):
        indices = [random.randint(0, len(self.buffer) - 1) for _ in range(batch_size)]
        states   = [self.buffer[i][0] for i in indices]
        actions  = [self.buffer[i][1] for i in indices]
        n_states = [self.buffer[i][2] for i in indices]
        n_actions = [self.buffer[i][3] for i in indices]
        rewards = [self.buffer[i][4] for i in indices]
        dones    = [self.buffer[i][5] for i in indices]
        return states, actions, n_states, n_actions, rewards, dones

    def length(self):
        return len(self.buffer)


def main():
    buffer_len = 10
    buffer = replayBuffer(buffer_size=buffer_len)
    batch_size = 5
    for i in range(buffer_len):
        state = [random.randint(0, 100) for i in range(5)]
        action = [random.randint(0, 100) for i in range(2)]
        n_state = [random.randint(0, 100) for i in range(5)]
        n_action = [random.randint(0, 100) for i in range(2)]
        reward = random.random()
        done = bool(random.randint(0, 1))
        buffer.add([state, action, n_state, n_action, reward, done])

    exp_obs, exp_acts, exp_next_obs, exp_next_acts, exp_rew, exp_termd = buffer.sample(batch_size=batch_size)
    print(f'xp_obs: {exp_obs}')
    # print(f'exp_acts: {exp_acts}')
    # print(f'exp_next_obs: {exp_next_obs}')
    # print(f'exp_next_acts: {exp_next_acts}')
    # print(f'exp_rew: {exp_rew}')
    # print(f'exp_termd: {exp_termd}')

    # Конвертируем данные в тензор
    exp_obs = [x for x in exp_obs]
    obs_agentsT = torch.FloatTensor([exp_obs]).to('cpu')
    exp_acts = [x for x in exp_acts]
    act_agentsT = torch.FloatTensor([exp_acts]).to('cpu')

    print(f'obs_agentsT: {obs_agentsT}')

if __name__ == "__main__":
    main()
