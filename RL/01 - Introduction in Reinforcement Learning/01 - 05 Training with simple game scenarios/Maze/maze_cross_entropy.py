"""
Код представляет собой реализацию алгоритма Cross-Entropy Method (CEM)
для решения задачи обучения с подкреплением на среде maze-sample-5x5-v0 из библиотеки OpenAI Gym.

Igor Stureyko stureiko@mail.ru

Для курса Otus Reinforcement learning
"""

# Imports
import random
import time

import numpy as np

import gym
import gym_maze  # requirement for Maze

import warnings


class RandomAgent:
    """
    Агент RandomAgent, который случайным образом выбирает действие из пространства действий
    """
    def __init__(self, action_n):
        self.action_n = action_n

    def get_action(self):
        return random.randint(0, self.action_n - 1)


class CEM:
    """
    Класс CEM, который реализует алгоритм Cross-Entropy Method.
    У агента есть параметр policy, который представляет текущую политику.
    В методе get_action агент выбирает действие на основе текущей политики.
    Метод update_policy обновляет политику на основе лучших траекторий (elite_trajectories) из последних эпизодов.
    """
    def __init__(self, state_n, action_n):
        self.state_n = state_n
        self.action_n = action_n
        self.policy = np.ones((self.state_n, self.action_n)) / self.action_n

    def get_action(self, state):
        """
        Выбирает действие на основе текущей политики
        """
        return int(np.random.choice(np.arange(self.action_n), p=self.policy[state]))

    def update_policy(self, elite_trajectories):
        """
        Обновляет политику на основе лучших траекторий (elite_trajectories) из последних эпизодов.
        """
        pre_policy = np.zeros((self.state_n, self.action_n))

        for trajectory in elite_trajectories:
            for state, action in zip(trajectory['states'], trajectory['actions']):
                pre_policy[state][action] += 1

        for state in range(self.state_n):
            if sum(pre_policy[state]) == 0:
                self.policy[state] = np.ones(self.action_n) / self.action_n
            else:
                self.policy[state] = pre_policy[state] / sum(pre_policy[state])

        # return None


def main():
    """
    Инициализируется окружение сетки maze-sample-5x5-v0, и создается агент класса CEM.
    Здесь также определены параметры для обучения, такие как количество эпизодов (episode_n),
    количество траекторий (trajectory_n), длина траектории (trajectory_len) и параметр q_param,
    который определяет порог для отбора лучших траекторий для обновления политики.
    """
    warnings.filterwarnings('ignore')

    env = gym.make('maze-random-10x10-plus-v0')

    state_n = 100
    action_n = 4
    agent = CEM(state_n, action_n)
    episode_n = 50
    trajectory_n = 100
    trajectory_len = 100
    q_param = 0.9

    for i in range(episode_n):
        trajectories = [get_trajectory(env, agent, trajectory_len, state_n) for _ in range(trajectory_n)]

        # mean_total_reward = np.mean([trajectory['total_reward'] for trajectory in trajectories])

        elite_trajectories = get_elite_trajectories(trajectories, q_param)

        if len(elite_trajectories) > 0:
            agent.update_policy(elite_trajectories)

    obs = env.reset()
    state = get_state(obs, state_n)

    for _ in range(trajectory_len):

        action = agent.get_action(state)

        obs, reward, done, _ = env.step(action)
        state = get_state(obs, state_n)

        env.render()
        time.sleep(0.2)

        if done:
            break


def get_elite_trajectories(trajectories, q_param):
    total_rewards = [trajectory['total_reward'] for trajectory in trajectories]
    quantile = np.quantile(total_rewards, q=q_param)
    return [trajectory for trajectory in trajectories if trajectory['total_reward'] > quantile]


def get_state(obs, state_n):
    return int(obs[1] * np.sqrt(state_n) + obs[0])


def get_trajectory(env, agent, trajectory_len, state_n):
    trajectory = {'states': [], 'actions': [], 'total_reward': 0}

    obs = env.reset()
    state = get_state(obs, state_n)
    trajectory['states'].append(state)

    for _ in range(trajectory_len):

        action = agent.get_action(state)
        trajectory['actions'].append(action)

        obs, reward, done, _ = env.step(action)
        state = get_state(obs, state_n)
        trajectory['total_reward'] += reward

        if done:
            break

        trajectory['states'].append(state)

    return trajectory


if __name__ == '__main__':
    main()
