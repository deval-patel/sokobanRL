# from SokobonCustomEnv import PlayerCustomEnv
import gym
# env = PlayerCustomEnv(9, 8, 72)
env = gym.make("gym_498_sokoban:498-sokoban-v0")
obs = env.reset()

episodes = 1000
for i in range(episodes):
    # Take a random action
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    
    # Render the game
    env.render()
    
    if done == True:
        break

env.close()
