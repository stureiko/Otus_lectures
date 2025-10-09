import gymnasium as gym
from gymnasium.spaces import Box
import numpy as np
import random


class ContinuousStatesContinuousActions(gym.Env):
    """непрерывные состояния, непрерывные действия"""
    terminate_after_attempts = random.randint(100, 1000)
    reward = 0
    tick = 0
    predicted_actions = []
    true_actions = []

    def to_fahrenheit(self, celsius):
        return (celsius * 1.8) + 32

    def __init__(self, render_mode=None):
        self.observation_space = Box(low=0, high=100, shape=(1,), dtype=np.float32)
        self.action_space = Box(low=32, high=212, shape=(1,), dtype=np.float32)

    def _get_info(self):
        return {"terminate_after_attempts": self.terminate_after_attempts}

    def step(self, timecount, action):
        observation = self.observation_space.sample()[0]
        self.predicted_actions.append(action[0])
        self.true_actions.append(self.to_fahrenheit(observation))
        # вознаграждение за правильное решение
        self.reward += -abs(action[0] - self.to_fahrenheit(observation))

        self.terminate_after_attempts -= 1
        if timecount % 100 == 0:
            print(f"observation={observation:.2f}",
                  f"\tpredicted_action={self.predicted_actions[-1]:.2f}",
                  f"true_actions={self.true_actions[-1]:.2f}",
                  f"\t\tr={self.reward:.2f} \tsteps {timecount:,d} ")

            self.predicted_actions = []
            self.true_actions = []

        terminated = self.terminate_after_attempts <= 0
        info = self._get_info()
        return float(observation), self.reward, terminated, False, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        print("reset", f"\tвознаграждение {self.reward:.2f}",
              f"\tпопыток {self.terminate_after_attempts}",
              "*" * 10)
        self.terminate_after_attempts = 10000
        self.reward = 0
        observation = self.observation_space.sample()[0]
        info = self._get_info()
        return observation, info

    def close(self):
        print("close", f"\tвознаграждение {self.reward:.2f}",
              f"\tпопыток {self.terminate_after_attempts}",
              "*" * 10)


##чтобы посмотреть работу модели - раскомментирйте этот блок 
# env = ContinuousStatesContinuousActions()
# env.action_space.seed(42)
# observation, info = env.reset(seed=42)
# # assert env.to_fahrenheit(20) ==68.0
# for tick in range(10000):
#     observation, reward, terminated, truncated, info = env.step(tick, env.action_space.sample())

#     if terminated or truncated:
#         observation, info = env.reset()

# env.close()
