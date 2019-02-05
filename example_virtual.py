
################################################################################
#                                                                              #
# Basic Q-Learning: Virtual Robot                                              #
#                                                                              #
################################################################################

# Learning environment for Q-Bot
from rlbotenv import *

#  Virtual Robot
from qbot_virtual import *

# Utility class to render robot onscreen using Python turtle graphics.
from renderer import Renderer

e = RlBotEnv(QvBot(sensor_sectors=12,degrees_per_sensor_sector=30.0,turn_sectors=8))
r = Renderer(100)

# create the q-table
q = np.random.rand(e.bot.observation_space(), e.bot.action_space())

# try changing these hyper-parameters...

# exploration rate (odds of taking a random action)
# 0.0 - 1.0
explore = 0.1   

# learning rate (proportional weight of new v. old information)
# 0.00 - 1.00
alpha = 0.01    

# discount rate (relative value of future v. current reward)
# 0.0 - 1.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
gamma = 0.6     

try:
    # default is range(1000000)
    for n in range(1000000):
        state = e.reset(obstacle_count=1)
        r.render_reset(e, raytrace=False)
        done = False
        steps = 0
        while not done:
            steps += 1
            if np.random.random() < explore:   # explore the state-action space
                action = e.bot.sample()        # ...random action
            else:                              # exploit the info in the q-table
                action = np.argmax(q[state])   # ...best known action
            next_state, reward, done = e.step(action)
            # update the q-table (see https://en.wikipedia.org/wiki/Q-learning)
            q[state][action] = (1-alpha) * q[state][action] + alpha * (reward + gamma * np.max(q[next_state]))
            state = next_state
            r.render_step(e)
        print(n)

except KeyboardInterrupt:
    print(q)
