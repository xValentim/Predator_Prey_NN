from gym import Env
from gym.spaces import Discrete, Box, MultiDiscrete
import random
import gym
import numpy as np

class PPEnv(Env):
    def __init__(self, L=5, time_limit=40, pos=(0, 0)):
        self.L = L
        self.pos = (self.L // 2, self.L // 2)
        self.action_space = Discrete(4)
        self.obs_shape = (5, 5)
        self.observation_space = gym.spaces.utils.flatten_space(MultiDiscrete(np.array([[1 for i in range(5)] for j in range(5)]))) #MultiDiscrete(np.array([[1 for i in range(5)] for j in range(5)]))
        self.types = Discrete(3)
        self.array = np.array([[Discrete(2).sample() * 2 for i in range(self.L)] for j in range(self.L)])
        # Put one predator
        self.array[self.pos[0], self.pos[1]] = 1               
        self.time = 0
        self.time_limit = time_limit
    
    def get_obs(self):
        obs = []
        i, j = self.pos
        for ii in range(-2, 3, 1):
            row = []
            for jj in range(-2, 3, 1):
                row.append(self.array[(i + ii) % self.L][(j + jj) % self.L])
            obs.append(row)     
        return np.array(obs)
    
    # Jump
    def apply_action(self, action):
        i, j = self.pos
        L = self.L
        if action == 0:
            self.array[i][j], self.array[i][(j + 1) % L] = self.array[i][(j + 1) % L], self.array[i][j]
            self.pos = (i, (j + 1) % L)
        elif action == 1:
            self.array[i][j], self.array[i][(j - 1) % L] = self.array[i][(j - 1) % L], self.array[i][j]
            self.pos = (i, (j - 1) % L)
        elif action == 2:
            self.array[i][j], self.array[(i - 1) % L][j] = self.array[(i - 1) % L][j], self.array[i][j]
            self.pos = ((i - 1) % L, j)
        elif action == 3:
            self.array[i][j], self.array[(i + 1) % L][j] = self.array[(i + 1) % L][j], self.array[i][j]
            self.pos = ((i + 1) % L, j)
    
    def get_neighboors(self):
        i, j = self.pos
        adress = [
            (i, (j + 1) % self.L), 
            (i, (j - 1) % self.L), 
            ((i - 1) % self.L, j), 
            ((i + 1) % self.L, j)
        ]
        right, left, up, down = self.array[adress[0][0]][adress[0][1]], self.array[adress[1][0]][adress[1][1]], self.array[adress[2][0]][adress[2][1]], self.array[adress[3][0]][adress[3][1]]
        return [right, left, up, down]
    
    def step(self, action):
        # Get obs
        obs = self.get_obs()
        
        # Colect reward
        ngbs = [obs[2][2 + 1], obs[2][2 - 1], obs[2 - 1][2], obs[2 + 1][2]] #self.get_neighboors()
        reward = 2 ** ngbs.count(2)
        
        # Get info
        info = {}
        
        # Check if done
        if self.time >= self.time_limit:
            done = True
            return obs, reward, done, info
        else: 
            done = False
            
        # apply action
        self.apply_action(action)
        self.time += 1
        return obs.reshape(1, -1), reward, done, info
    
    def render(self):
        print('-' * self.L)
        print(self.array)
        print('-' * self.L)
    
    def reset(self):
        self.pos = (self.L // 2, self.L // 2)
        self.action_space = Discrete(4)
        self.observation_space = gym.spaces.utils.flatten_space(MultiDiscrete(np.array([[1 for i in range(5)] for j in range(5)]))) # MultiDiscrete(np.array([[3 for i in range(5)] for j in range(5)]))
        self.types = Discrete(3)
        self.array = np.array([[Discrete(2).sample() * 2 for i in range(self.L)] for j in range(self.L)])
        # Put one predator
        self.array[self.pos[0], self.pos[1]] = 1               
        self.time = 0
        return self.get_obs().reshape(1, -1)