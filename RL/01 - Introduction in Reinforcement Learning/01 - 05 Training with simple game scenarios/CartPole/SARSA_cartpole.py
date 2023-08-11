import gym
import numpy as np
import math
import matplotlib.pyplot as plt
import warnings


class SARSA:
    def __init__(self, env, epsilon=0.2, learning_rate=0.25, discount=0.95):
        self.env = env
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.discount = discount
        self.theta_minmax = self.env.observation_space.high[2]
        self.theta_dot_minmax = math.radians(50)
        self.theta_state_size = 50
        self.theta_dot_state_size = 50
        self.q_table = np.random.randn(self.theta_state_size, self.theta_dot_state_size, self.env.action_space.n)

    def discretised_state(self, state):
        discrete_state = np.array([0, 0])
        theta_window = (self.theta_minmax - (-self.theta_minmax)) / self.theta_state_size
        discrete_state[0] = (state[2] - (-self.theta_minmax)) // theta_window
        discrete_state[0] = min(self.theta_state_size - 1, max(0, discrete_state[0]))

        theta_dot_window = (self.theta_dot_minmax - (-self.theta_dot_minmax)) / self.theta_dot_state_size
        discrete_state[1] = (state[3] - (-self.theta_dot_minmax)) // theta_dot_window
        discrete_state[1] = min(self.theta_dot_state_size - 1, max(0, discrete_state[1]))

        return tuple(discrete_state.astype(int))

    def get_action(self, discrete_state):
        if np.random.random() > self.epsilon:
            return np.argmax(self.q_table[discrete_state])
        else:
            return np.random.randint(0, self.env.action_space.n)

    def update_q_table(self, state, action, reward, next_state, next_action):
        current_q = self.q_table[state + (action,)]
        next_q = self.q_table[next_state + (next_action,)]
        updated_q = current_q + self.learning_rate * (reward + self.discount * next_q - current_q)
        self.q_table[state + (action,)] = updated_q

    def train(self, episodes, episode_display=500):
        ep_rewards = []
        ep_rewards_table = {'ep': [], 'avg': [], 'min': [], 'max': []}

        for episode in range(episodes):
            episode_reward = 0
            done = False

            if episode % episode_display == 0:
                render_state = True
            else:
                render_state = False

            curr_discrete_state = self.discretised_state(self.env.reset())
            curr_action = self.get_action(curr_discrete_state)

            while not done:
                new_state, reward, done, _ = self.env.step(curr_action)
                new_discrete_state = self.discretised_state(new_state)
                new_action = self.get_action(new_discrete_state)

                if render_state:
                    self.env.render()

                if not done:
                    self.update_q_table(curr_discrete_state, curr_action, reward, new_discrete_state, new_action)

                curr_discrete_state = new_discrete_state
                curr_action = new_action

                episode_reward += reward

            ep_rewards.append(episode_reward)

            if not episode % episode_display:
                avg_reward = sum(ep_rewards[-episode_display:]) / len(ep_rewards[-episode_display:])
                ep_rewards_table['ep'].append(episode)
                ep_rewards_table['avg'].append(avg_reward)
                ep_rewards_table['min'].append(min(ep_rewards[-episode_display:]))
                ep_rewards_table['max'].append(max(ep_rewards[-episode_display:]))
                print(
                    f"Episode:{episode} avg:{avg_reward} min:{min(ep_rewards[-episode_display:])} max:{max(ep_rewards[-episode_display:])}")

        self.env.close()

        plt.plot(ep_rewards_table['ep'], ep_rewards_table['avg'], label="avg")
        plt.plot(ep_rewards_table['ep'], ep_rewards_table['min'], label="min")
        plt.plot(ep_rewards_table['ep'], ep_rewards_table['max'], label="max")
        plt.legend(loc=4)  # bottom right
        plt.title('CartPole SARSA')
        plt.ylabel('Average reward/Episode')
        plt.xlabel('Episodes')
        plt.show()


def main():
    warnings.filterwarnings('ignore')
    env = gym.make("CartPole-v1")

    # Hyperparamters
    EPISODES = 10000
    EPISODE_DISPLAY = 1000
    LEARNING_RATE = 0.25
    EPSILON = 0.2
    DISCOUNT = 0.95

    agent = SARSA(env, epsilon=EPSILON, learning_rate=LEARNING_RATE, discount=DISCOUNT)
    agent.train(EPISODES, EPISODE_DISPLAY)


if __name__ == '__main__':
    main()
