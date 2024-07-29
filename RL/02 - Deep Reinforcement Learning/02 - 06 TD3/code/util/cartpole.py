"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from http://incompleteideas.net/sutton/book/code/pole.c
permalink: https://perma.cc/C9ZM-652R
"""

import math
import random
import gymnasium as gym
import numpy as np

class CartPole(gym.Env):
    def __init__(self):
        self._cart_mass = 0.31  # (kg)
        self._pole_mass = 0.055  # (kg)
        self._pole_length = 0.4  # (m)

        self.x_threshold = 1.0
        self.theta_threshold = 12 * 2 * math.pi / 360
        
        self._state = []
        self._done = True
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=np.array([-4.8000002e+00, -3.4028235e+38, -4.1887903e-01, -3.4028235e+38]), 
                                                high=np.array([4.8000002e+00, 3.4028235e+38, 4.1887903e-01, 3.4028235e+38]), 
                                                dtype=np.float32)


    def reset(self, seed=42):
        self._step = 0
        self._cart_position = math.tanh(random.gauss(0.0, 0.01)) * 4.8  # (m)
        self._cart_velocity = random.uniform(-0.05, 0.05)  # (m/s)
        initial_pole_angle=random.uniform(-0.05, 0.05)
        self._pole_angle =  (initial_pole_angle + math.pi) % (2 * math.pi) - math.pi  # (rad)
        self._pole_angular_velocity = random.uniform(-0.05, 0.05)  # (rad/s)

        # (CartPole-v0 uses numpy.ndarray for state,
        #  but here returns Python array.)
        self._state = [self._cart_position, self._cart_velocity, self._pole_angle, self._pole_angular_velocity]
        self._done = False
        return self._state

    def step(self, action: float):
        """ 
        Args:
            action: float value between -1.0 and 1.0
        """
        if self._done:
            raise Exception("Cannot run step() before reset")

        self._step += 1

        # Add a small random noise
        # (The agent won't succeed by applying zero force each time.)
        force = 1.0 * (action + random.uniform(-0.02, 0.02))

        total_mass = self._cart_mass + self._pole_mass
        pole_half_length = self._pole_length / 2
        pole_mass_length = self._pole_mass * pole_half_length

        cosTheta = math.cos(self._pole_angle)
        sinTheta = math.sin(self._pole_angle)

        temp = (
            force + pole_mass_length * self._pole_angular_velocity ** 2 * sinTheta
        ) / total_mass
        angularAccel = (9.8 * sinTheta - cosTheta * temp) / (
            pole_half_length
            * (4.0 / 3.0 - (self._pole_mass * cosTheta ** 2) / total_mass)
        )
        linearAccel = temp - (pole_mass_length * angularAccel * cosTheta) / total_mass

        self._cart_position = self._cart_position + 0.02 * self._cart_velocity
        self._cart_velocity = self._cart_velocity + 0.02 * linearAccel

        self._pole_angle = (
            self._pole_angle + 0.02 * self._pole_angular_velocity
        )
        self._pole_angle = (self._pole_angle + math.pi) % (2 * math.pi) - math.pi

        self._pole_angular_velocity = (
            self._pole_angular_velocity + 0.02 * angularAccel
        )

        # (CartPole-v0 uses numpy.ndarray for state,
        #  but here returns Python array.)
        self._state = [self._cart_position, self._cart_velocity, self._pole_angle, self._pole_angular_velocity]
        done = self._state[0] < -self.x_threshold or \
            self._state[0] > self.x_threshold or \
            self._state[2] < -self.theta_threshold or \
            self._state[2] > self.theta_threshold or \
            self._step == 500
        self._done = bool(done)
        return self._state, 1.0, self._done, {}
