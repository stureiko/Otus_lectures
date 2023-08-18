import gym
import gym_maze
import numpy as np
import random
import time

env = gym.make('maze-sample-5x5-v0')
state_n = 25
action_n = 4


class RandomAgent():
    def __init__(self, action_n):
        self.action_n = action_n
        return None
    
    def get_action(self, state):
        return random.randint(0, self.action_n - 1)

class CEM():
    def __init__(self, state_n, action_n):
        self.state_n = state_n
        self.action_n = action_n
        self.policy = np.ones((self.state_n, self.action_n)) / self.action_n
    
    def get_action(self, state):
        return int(np.random.choice(np.arange(self.action_n), p=self.policy[state]))
    
    def update_policy(self, elite_trajectories):
        pre_policy = np.zeros((self.state_n, self.action_n))
        
        for trajectory in elite_trajectories:
            for state, action in zip(trajectory['states'], trajectory['actions']):
                pre_policy[state][action] += 1
                
        for state in range(self.state_n):
            if sum(pre_policy[state]) == 0:
                self.policy[state] = np.ones(self.action_n) / self.action_n
            else:
                self.policy[state] = pre_policy[state] / sum(pre_policy[state])
                
        return None
                

def get_state(obs):
    return int(obs[1] * np.sqrt(state_n) + obs[0])

def get_trajectory(agent, trajectory_len):
    trajectory = {'states':[], 'actions': [], 'total_reward': 0}
    
    obs = env.reset()
    state = get_state(obs)
    trajectory['states'].append(state)
    
    for _ in range(trajectory_len):
        
        action = agent.get_action(state)
        trajectory['actions'].append(action)
        
        obs, reward, done, _ = env.step(action)
        state = get_state(obs)
        trajectory['total_reward'] += reward
        
        if done:
            break
            
        trajectory['states'].append(state)
            
    return trajectory

def get_elite_trajectories(trajectories, q_param):
    total_rewards = [trajectory['total_reward'] for trajectory in trajectories]
    quantile = np.quantile(total_rewards, q=q_param) 
    return [trajectory for trajectory in trajectories if trajectory['total_reward'] > quantile]


agent = CEM(state_n, action_n)
episode_n = 50
trajectory_n = 100
trajectory_len = 100
q_param = 0.9


for _ in range(episode_n):
    trajectories = [get_trajectory(agent, trajectory_len) for _ in range(trajectory_n)]
    
    mean_total_reward = np.mean([trajectory['total_reward'] for trajectory in trajectories])
    print(mean_total_reward)
    
    elite_trajectories = get_elite_trajectories(trajectories, q_param)
    
    if len(elite_trajectories) > 0:
        agent.update_policy(elite_trajectories)

#test
obs = env.reset()
state = get_state(obs)

for _ in range(trajectory_len):

    action = agent.get_action(state)

    obs, reward, done, _ = env.step(action)
    state = get_state(obs)
    
    env.render()
    time.sleep(0.5)

    if done:
        break
