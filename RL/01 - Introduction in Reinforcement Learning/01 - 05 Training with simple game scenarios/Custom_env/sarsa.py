import matplotlib.pyplot as plt
import numpy as np


# class SARSA:
#     def __init__(self, env, epsilon=0.2, learning_rate=0.25, discount=0.95):
#         self.env = env
#         self.epsilon = epsilon
#         self.learning_rate = learning_rate
#         self.discount = discount
#         self.n_bacteria_state_size = 50
#         self.observation_state_size = 50
#         self.action_state_size = env.action_space.shape[0]
#         self.q_table = np.random.randn(self.n_bacteria_state_size, self.observation_state_size,
#                                        self.observation_state_size, self.observation_state_size,
#                                        self.action_state_size)
#
#     def discretised_state(self, n_bacteria, observation):
#         discrete_state = np.array([0, 0, 0, 0, 0])
#         n_bacteria_window = n_bacteria / self.n_bacteria_state_size
#         if n_bacteria_window == 0:
#             discrete_state[0] = n_bacteria
#         discrete_state[0] = min(self.n_bacteria_state_size - 1, max(0, discrete_state[0]))
#
#         for i in range(1, 5):
#             window = 2 / self.observation_state_size
#             discrete_state[i] = (observation[i - 1] + 1) // window
#             discrete_state[i] = min(self.observation_state_size - 1, max(0, discrete_state[i]))
#
#         return tuple(discrete_state.astype(int))
#
#     def get_action(self, discrete_state):
#         if np.random.random() > self.epsilon:
#             # print(discrete_state)
#             return np.argmax(self.q_table[discrete_state, :])
#         else:
#             return np.random.randint(0, self.action_state_size)
#
#     def update_q_table(self, n_bacteria, observation, action, reward, next_n_bacteria, next_observation, next_action):
#         current_q = self.q_table[observation, :]
#         next_q = self.q_table[next_observation, :]
#         updated_q = current_q + self.learning_rate * (reward + self.discount * next_q - current_q)
#         self.q_table[observation, :] = updated_q
#
#     def train(self, episodes, episode_display=100):
#         ep_rewards = []
#         ep_rewards_table = {'ep': [], 'avg': [], 'min': [], 'max': []}
#
#         for episode in range(episodes):
#             episode_reward = 0
#             done = False
#
#             if episode % episode_display == 0:
#                 render_state = True
#             else:
#                 render_state = False
#
#             # n_bacteria, curr_observation = self.env.reset()
#             curr_observation = self.env.reset()
#             n_bacteria = self.env.n_bacteria
#             curr_discrete_state = self.discretised_state(n_bacteria, curr_observation)
#             curr_action = self.get_action(curr_discrete_state)
#
#             while not done:
#                 next_observation, reward, done, _ = self.env.step(curr_action)
#                 next_n_bacteria = self.env.n_bacteria
#                 next_discrete_state = self.discretised_state(next_n_bacteria, next_observation)
#                 next_action = self.get_action(next_discrete_state)
#
#                 if render_state:
#                     self.env.render()
#
#                 if not done:
#                     self.update_q_table(n_bacteria, curr_discrete_state, curr_action, reward,
#                                         next_n_bacteria, next_discrete_state, next_action)
#
#                 n_bacteria, curr_observation = next_n_bacteria, next_observation
#                 curr_discrete_state = next_discrete_state
#                 curr_action = next_action
#
#                 episode_reward += reward
#
#             ep_rewards.append(episode_reward)
#
#             if not episode % episode_display:
#                 avg_reward = sum(ep_rewards[-episode_display:]) / len(ep_rewards[-episode_display:])
#                 ep_rewards_table['ep'].append(episode)
#                 ep_rewards_table['avg'].append(avg_reward)
#                 ep_rewards_table['min'].append(min(ep_rewards[-episode_display:]))
#                 ep_rewards_table['max'].append(max(ep_rewards[-episode_display:]))
#                 print(
#                     f"Episode:{episode} avg:{avg_reward} min:{min(ep_rewards[-episode_display:])} max:{max(ep_rewards[-episode_display:])}")
#
#         self.env.close()
#
#         plt.plot(ep_rewards_table['ep'], ep_rewards_table['avg'], label="avg")
#         plt.plot(ep_rewards_table['ep'], ep_rewards_table['min'], label="min")
#         plt.plot(ep_rewards_table['ep'], ep_rewards_table['max'], label="max")
#         plt.legend(loc=4)  # bottom right
#         plt.title('Cure SARSA')
#         plt.ylabel('Average reward/Episode')
#         plt.xlabel('Episodes')
#         plt.show()

class SARSA:
    def __init__(self, env, epsilon=0.2, learning_rate=0.25, discount=0.95):
        self.env = env
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.discount = discount
        self.n_bacteria_state_size = 50
        self.observation_state_size = 50
        self.action_state_size = env.action_space.shape[0]
        self.q_table = np.random.randn(self.n_bacteria_state_size, self.observation_state_size,
                                       self.observation_state_size, self.observation_state_size,
                                       self.action_state_size)

    def discretised_state(self, n_bacteria, observation):
        discrete_state = np.array([0, 0, 0, 0, 0])
        n_bacteria_window = n_bacteria / self.n_bacteria_state_size
        discrete_state[0] = min(self.n_bacteria_state_size - 1, max(0, int(n_bacteria_window)))

        for i in range(1, 5):
            window = 2 / self.observation_state_size
            discrete_state[i] = min(self.observation_state_size - 1, max(0, int((observation[i - 1] + 1) // window)))

        return tuple(discrete_state)

    def get_action(self, discrete_state):
        if np.random.random() > self.epsilon:
            return np.argmax(self.q_table[discrete_state, :])
        else:
            return np.random.randint(0, self.action_state_size)

    def update_q_table(self, n_bacteria, observation, action, reward, next_n_bacteria, next_observation, next_action):
        current_q = self.q_table[observation][action]
        next_q = self.q_table[next_observation][next_action]
        updated_q = current_q + self.learning_rate * (reward + self.discount * next_q - current_q)
        self.q_table[observation][action] = updated_q

    def train(self, episodes, episode_display=100):
        ep_rewards = []
        ep_rewards_table = {'ep': [], 'avg': [], 'min': [], 'max': []}

        for episode in range(episodes):
            episode_reward = 0
            done = False

            if episode % episode_display == 0:
                render_state = True
            else:
                render_state = False

            curr_observation = self.env.reset()
            n_bacteria = self.env.n_bacteria
            curr_discrete_state = self.discretised_state(n_bacteria, curr_observation)
            curr_action = self.get_action(curr_discrete_state)

            while not done:
                next_observation, reward, done, _ = self.env.step(curr_action)
                next_n_bacteria = self.env.n_bacteria
                next_discrete_state = self.discretised_state(next_n_bacteria, next_observation)
                next_action = self.get_action(next_discrete_state)

                if render_state:
                    self.env.render()

                if not done:
                    self.update_q_table(n_bacteria, curr_discrete_state, curr_action, reward,
                                        next_n_bacteria, next_discrete_state, next_action)

                n_bacteria, curr_observation = next_n_bacteria, next_observation
                curr_discrete_state = next_discrete_state
                curr_action = next_action

                episode_reward += reward

            ep_rewards.append(episode_reward)

            if not episode % episode_display:
                avg_reward = sum(ep_rewards[-episode_display:]) / len(ep_rewards[-episode_display:])
                ep_rewards_table['ep'].append(episode)
                ep_rewards_table['avg'].append(avg_reward)
                ep_rewards_table['min'].append(min(ep_rewards[-episode_display:]))
                ep_rewards_table['max'].append(max(ep_rewards[-episode_display:]))
                print(
                    f"Эпизод:{episode} средняя награда:{avg_reward} минимальная награда:{min(ep_rewards[-episode_display:])} максимальная награда:{max(ep_rewards[-episode_display:])}")

        self.env.close()

        plt.plot(ep_rewards_table['ep'], ep_rewards_table['avg'], label="Средняя награда")
        plt.plot(ep_rewards_table['ep'], ep_rewards_table['min'], label="Минимальная награда")
        plt.plot(ep_rewards_table['ep'], ep_rewards_table['max'], label="Максимальная награда")
        plt.legend(loc=4)  # справа снизу
        plt.title('Cure SARSA')
        plt.ylabel('Средняя награда/Эпизод')
        plt.xlabel('Эпизоды')
        plt.show()