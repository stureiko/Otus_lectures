import numpy as np
import random


class ActionSpace:
    shape: tuple

    def __init__(self):
        self.shape = (1,)
        self.num_bins = 10
        self.bins = np.linspace(-1, 1, self.num_bins)  # Разбиваем интервал [-1, 1] на num_bins частей

    def sample(self, seed=None):
        if seed: random.seed(seed)
        return random.triangular(-1, 1)

    def contains(self, x):
        return abs(x) <= 1

    def to_discrete(self, action):
        action_idx = np.digitize(action, self.bins) - 1
        return action_idx.item()  # Возвращаем целочисленное значение
