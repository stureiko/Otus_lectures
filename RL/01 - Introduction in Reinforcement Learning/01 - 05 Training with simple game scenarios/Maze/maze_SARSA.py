import random
import time
import numpy as np
import gym
import gym_maze
import warnings

# Словарь для перекодировки дискретных действий в действия окружения
ACTION_MAPPING = {
    0: 'N',
    1: 'E',
    2: 'S',
    3: 'W'
}


class SARSA:
    def __init__(self, state_n, action_n, alpha=0.5, gamma=0.99, epsilon=0.1):
        self.state_n = state_n
        self.action_n = action_n
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        # Инициализация q-функции нулями
        self.qfunction = np.zeros((self.state_n, self.action_n))

    def get_action(self, state):
        # Выбор действия на основе эпсилон-жадной стратегии
        if random.random() < self.epsilon:
            return random.randint(0, self.action_n - 1)
        else:
            return np.argmax(self.qfunction[state])

    def update_qfunction(self, state, action, reward, next_state, next_action):
        # Обновление q-функции с использованием алгоритма SARSA
        current_q = self.qfunction[state][action]
        next_q = self.qfunction[next_state][next_action]
        updated_q = current_q + self.alpha * (reward + self.gamma * next_q - current_q)
        self.qfunction[state][action] = updated_q


def main():
    warnings.filterwarnings('ignore')

    # Создание окружения сетки
    # env = gym.make('maze-sample-5x5-v0')
    env = gym.make('maze-random-10x10')

    state_n = 100
    action_n = 4
    # Создание агента SARSA с определенным количеством состояний и действий
    agent = SARSA(state_n, action_n)
    episode_n = 1000
    # episode_n = 100
    trajectory_len = 200

    for i in range(episode_n):
        obs = env.reset()
        state = get_state(obs, state_n)
        action = agent.get_action(state)

        for _ in range(trajectory_len):
            # Выполнение выбранного действия и получение нового состояния и вознаграждения
            obs, reward, done, _ = env.step(ACTION_MAPPING[action])
            next_state = get_state(obs, state_n)

            # Выбор следующего действия на основе нового состояния
            next_action = agent.get_action(next_state)

            # Обновление q-функции по алгоритму SARSA
            agent.update_qfunction(state, action, reward, next_state, next_action)

            # Переход к следующему состоянию и действию
            state = next_state
            action = next_action

            if done:
                break

    # Визуализация обученной модели
    obs = env.reset()
    state = get_state(obs, state_n)

    for _ in range(trajectory_len):
        # Выбор действия с помощью обученной модели
        action = agent.get_action(state)

        # Выполнение действия в окружении и получение нового состояния
        obs, _, done, _ = env.step(ACTION_MAPPING[action])
        state = get_state(obs, state_n)

        env.render()  # Визуализация окружения
        time.sleep(0.2)

        if done:
            break


def get_state(obs, state_n):
    # Преобразование наблюдения в состояние для дискретизации
    return int(obs[1] * np.sqrt(state_n) + obs[0])


if __name__ == '__main__':
    main()
