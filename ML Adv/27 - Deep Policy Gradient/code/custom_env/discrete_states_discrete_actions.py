import gymnasium as gym
from gymnasium.spaces import Discrete
import numpy as np
import random

class DiscreteStatesDiscreteActions(gym.Env):
    """дискретные состояния, дискретные действия"""
    balance = 100
    reward = 0
    tick = 0
    def __init__(self, render_mode=None):
        self.observation_space = Discrete(3, seed=42)                       # {0, 1, 2}
        self.action_space = Discrete(3, seed=42)                            # {0, 1, 2}
        self.observation_in_words = ["снизилась","не изменилась","увеличилась"]
        self.action_in_words = ["продать","владеть","купить"]

    def _get_obs(self):
        return random.randint(0,2)

    def _get_info(self):
        return {"balance":self.balance}

    def step(self,timecount, action):
        observation = self._get_obs()

        old_balance = self.balance
        if  action ==0: self.balance +=1
        if  action ==2: self.balance -=1
        self.reward +=self.balance - old_balance                          #вознаграждение за правильное решение
        if timecount % 10000 ==0:
            print("\tobservation\t", self.observation_in_words[observation],
                "\taction",self.action_in_words[action], f"\tбыло {old_balance:.4f} \tстало {self.balance:.4f}",f"\treward {self.reward:.4f}",timecount)

        terminated = self.balance <=0
        info = self._get_info()
        return observation, self.reward, terminated, False, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        print("reset",f"\tвознаграждение {self.reward:.2f}", f"\tбаланс {self.balance:.2f}","*"*20)
        self.balance = 100
        self.reward = 0
        observation = self._get_obs()
        info = self._get_info()
        return observation, info

    def close(self):
        print("\tclose",f"\tвознаграждение {self.reward:.2f}", f"\tбаланс {self.balance:.2f}","*"*20)


def main():
    """Демонстрация работы модели
    """
    env = DiscreteStatesDiscreteActions()
    env.action_space.seed(142)
    observation, info = env.reset(seed=42)
    
    for tick in range(2000000): #обучается за 1е6 шагов
        observation, reward, terminated, truncated, info = env.step(tick,env.action_space.sample())
    
        if terminated or truncated:
            observation, info = env.reset()
    
    env.close()

if __name__ == "__main__":
    main()
