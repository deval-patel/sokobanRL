
import numpy as np
import gym
from gym import spaces
import gym_498_sokoban as gm
class SokobanCustomEnvV0(gym.Env):
    """
    Custom environment using openai gym Env
    """
    metadata = {'render.modes': ['human']}
    game: gm.SokobanGame
    def __init__(self):
        super(SokobanCustomEnvV0, self).__init__()
        self.game = gm.SokobanGame()
        NUM_ACTIONS = 4
        self.action_space = spaces.Discrete(NUM_ACTIONS)
        self.observation_space = spaces.Box(low = 0, high=6, shape=(self.game.height, self.game.width, 1), dtype=np.uint8)

    def step(self, action):
        """
            Makes a step in the game according to the action. 

        """
        reward = self.game.move(action)
        obs = self.game.get_board()
        if self.game.is_game_won():
            return obs, reward + gm.RewardSystem.get_reward_for_victory(), True, []

        if self.game.is_game_lost():
            return obs, reward + gm.RewardSystem.get_reward_for_loss(), True, []
            
        return obs, reward, False, []

    def reset(self):
        self.game = gm.SokobanGame()

    def render(self, mode='human', close=False):
        print(self.game.get_board_string())
