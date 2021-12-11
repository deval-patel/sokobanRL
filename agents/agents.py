import numpy as np
class Agent():

    def __init__(self, observation_space, action_space):
        self.actions = action_space
        self.states = observation_space
        self.policy = np.zeros(self.states.shape, dtype=np.int)
        print(self.policy.shape)
        self.value  = np.zeros(self.states.shape, dtype=np.int)



    def __call__(self, obs):
        return self.policy[obs]

class RandomAgent(Agent):
    def __init__(self, observation_space, action_space):
        super().__init__(observation_space, action_space)

    def __call__(self, obs):
        return self.actions.sample()
