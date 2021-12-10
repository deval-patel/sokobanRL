from SokobonCustomEnv import PlayerCustomEnv

env = PlayerCustomEnv(9, 8, 72)
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