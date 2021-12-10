import numpy as np
class Agent():

    def __init__(self, observation_space, action_space):
        self.actions = action_space
        self.states = observation_space

        self.policy = np.zeros((self.states,), dtype=np.int)
        self.value  = np.zeros((self.states,), dtype=np.int)



    def __call__(self, obs):
        return self.policy[obs]
