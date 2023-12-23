import gymnasium as gym
from gymnasium.spaces import Discrete, Box
import numpy as np
from sklearn.metrics import accuracy_score
import random


class ContinuousStatesDiscreteActions(gym.Env):
    """непрерывные состояния, дискретные действия"""
    attempts = random.randint(100, 1000)
    reward = 0
    tick = 0
    predicted_actions = []
    true_actions = []

    def __init__(self, render_mode=None):
        self.observation_space = Box(low=-100, # любая температура, попробуйте low = -273.15, high = np.inf
                                     high=201,
                                     shape=(1,),
                                     dtype=np.float32)
        self.action_space = Discrete(3, seed=42)  # {0, 1, 2}
        self.action_in_words = ["лёд", "вода", "пар"]

    def _get_obs(self):
        return self.observation_space.sample()[0]

    def _get_info(self):
        return {"attempts": self.attempts}

    def step(self, timecount, action):
        observation = self._get_obs()
        self.predicted_actions.append(action)
        # вознаграждение за правильное решение
        if observation >= -273.15 and observation <= 0:
            self.true_actions.append(0)
            if action == 0:
                self.reward += 3
            else:
                self.reward -= 1

        if observation > 0 and observation < 100:
            self.true_actions.append(1)
            if action == 1:
                self.reward += 3
            else:
                self.reward -= 1

        if observation >= 100 and observation <= np.inf:
            self.true_actions.append(2)
            if action == 2:
                self.reward += 3
            else:
                self.reward -= 1

        self.attempts -= 1
        if timecount % 100 == 0:
            print(f"t={observation:.2f}  a={self.action_in_words[action]}",
                  f"\tr={self.reward:.2f}",
                  f"\tsteps {timecount:,d} accuracy={accuracy_score(self.true_actions, self.predicted_actions):.2f}")
            predicted_actions = []
            true_actions = []

        terminated = self.attempts <= 0
        info = self._get_info()
        return float(observation), self.reward, terminated, False, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        print("reset", f"\tвознаграждение {self.reward:.2f}",
              f"\tпопыток {self.attempts}  accuracy={accuracy_score(self.true_actions, self.predicted_actions):.2f}",
              "*" * 10)
        self.attempts = random.randint(100, 1000)
        self.reward = 0
        observation = self._get_obs()
        info = self._get_info()
        return observation, info

    def close(self):
        print("close", f"\tвознаграждение {self.reward:.2f}",
              f"\tпопыток {self.attempts}  accuracy={accuracy_score(self.true_actions, self.predicted_actions):.2f}",
              "*" * 10)


###чтобы посмотреть работу модели - раскомментирйте этот блок 
# env = ContinuousStatesDiscreteActions()
# env.action_space.seed(42)
# observation, info = env.reset(seed=42)
#
# for tick in range(20000):
#     observation, reward, terminated, truncated, info = env.step(tick, env.action_space.sample())
#
#     if terminated or truncated:
#         observation, info = env.reset()
#
# env.close()
