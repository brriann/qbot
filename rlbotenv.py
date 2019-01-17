import math
import numpy as np
from obstacle import Obstacle

################################################################################
#                                                                              #
# Learning environment for Q-Bot:                                              #
#    - creates discrete observations from continous sensor readings:           #
#         - sensor = [1000,1200,1110,90,1150,880]                              #
#         - observation = argmin(senor) = 3 (the index of the lowest reading)  #
#    - calculates reward based on change in distance to nearest object         #
#    - relies on robot to provide sensor readings, action space, actions       #
#                                                                              #
################################################################################

class RlBotEnv:

    MAX_ITERATIONS = 2000

    def __init__(self, bot):
        self.bot = bot        # could be a physical or virtual robot

    def reset(self, obstacle_count=0):
        self.iterations = 0
        self.bot.reset()
        self.obstacles = Obstacle.make_obstacles(obstacle_count)
        obs = self.bot.get_observation(self.obstacles)
        self.min_distance = min(obs)                    # for use in first call to step()
        return np.argmin(obs)                           # convert to discrete observation

    def step(self, action):
        self.iterations += 1
        self.bot.move(action)
        obs = self.bot.get_observation(self.obstacles)
        reward = self.min_distance-min(obs) # reward = reduction in distance
        self.min_distance = min(obs)        # for use in next call to step()
        state = np.argmin(obs)              # convert to discrete state
        done = min(obs) < self.bot.goal() or self.iterations > RlBotEnv.MAX_ITERATIONS
        return state, reward, done
