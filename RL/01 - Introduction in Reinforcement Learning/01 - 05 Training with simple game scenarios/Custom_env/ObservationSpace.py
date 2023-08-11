import numpy as np

class observationSpace:
    def __init__(self):
        self.shape = (5,)  # Форма пространства состояний
        self.num_bins = 10  # Количество интервалов для каждого элемента массива состояний
        self.bins = [np.linspace(-1, 1, self.num_bins) for _ in range(self.shape[0])]

    def sample(self, seed=None):
        # TODO: Реализовать метод для генерации случайного состояния
        pass

    def contains(self, x):
        # TODO: Реализовать метод для проверки, что состояние x принадлежит пространству состояний
        pass

    def to_discrete(self, observation):
        discrete_obs = []
        for i in range(self.shape[0]):
            discrete_val = np.digitize(observation[i], self.bins[i]) - 1
            discrete_obs.append(discrete_val)
        return tuple(discrete_obs)
