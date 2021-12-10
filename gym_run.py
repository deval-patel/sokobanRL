import gym
import numpy as np
from agents.agents import RandomAgent
env = gym.make("gym_498_sokoban:498-sokoban-v0")
obs = env.reset()

random_agent = RandomAgent(env.observation_space, env.action_space)

episodes = 1000
num_steps = 100 # Not really needed, since the environment will cap the steps based on levelgit add
rewards = np.zeros((episodes, 100))
for run in range(episodes):
    obs = env.reset()
    for step in range(num_steps):
        act = random_agent(obs)
        obs, rew, done, info = env.step(act)
        rewards[run, step] = rew
        # Render the game
        # env.render()
        if done:
            break

print("Average return: {}".format(rewards.sum(1).mean()))
print("Standard deviation: {}".format(rewards.sum(1).std()))

env.close()
