import gym
import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3 import DQN, A2C, PPO
from stable_baselines3.common.env_util import make_vec_env
from agents.agents import RandomAgent
import torch as th
from stable_baselines3.common.logger import configure
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import BaseCallback
import stable_baselines3.common.results_plotter as results_plotter
import os
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import load_results, ts2xy

LOG_PATH = 'logs/'

def runRandom():
    envName ="gym_498_sokoban:498-sokoban-v0"
    env = gym.make(envName)
    random_agent = RandomAgent(env.observation_space, env.action_space)
    env = gym.make("gym_498_sokoban:498-sokoban-v0")
    obs = env.reset()
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
    #
    print("Average return: {}".format(rewards.sum(1).mean()))
    print("Standard deviation: {}".format(rewards.sum(1).std()))
class LearningAgent:
    '''
        A base class for learning agents, used to train, save, load, validate and use models of varying types.

    '''
    def __init__(self):
        self.envName ="gym_498_sokoban:498-sokoban-v0"
        self.env = gym.make(self.envName)
        self.savePath = None
        self.logger = None

    def applyMonitor(self):
        print("Set logging to:" + self.getLogPath())
        self.env = Monitor(self.env, self.getLogPath())

    def getName(self):
        return self.name

    def getLogPath(self):
        ''' Gets the logging path for the agent.'''
        return LOG_PATH + self.name

    def learn(self, timesteps=25000):
        if not self.logger:
            self.logger = configure(LOG_PATH + self.name, [ "stdout","log", "csv", "tensorboard"])
        self.model = self.model.learn(total_timesteps=timesteps)

    def predict(self, obs):
        '''Given an observation, outputs a predicted action.'''
        return self.model.predict(obs)

    def save(self, path=None):
        if path == None and self.savePath == None:
            path = self.name
        elif path == None:
            path = self.savePath
        self.savePath = path
        self.model.save(path)
    
    def load(self, path=None):
        if path == None and self.savePath == None:
            path = self.name
        elif path == None:
            path = self.savePath
        self.model.load(path)

class DQNLearningAgent(LearningAgent):
    '''DQN -Learning agent'''
    def __init__(self,verbose=1):
        super().__init__()
        self.model = DQN("MlpPolicy", self.env, verbose=verbose)
        self.name = "DQN_Agent_V2"
        self.applyMonitor()

class A2CLearningAgent(LearningAgent):
    '''A2C -Learning agent'''
    def __init__(self,verbose=1):
        super().__init__()
        self.name = "A2C_Agent_V2"
        self.applyMonitor()
        self.env = make_vec_env(self.envName, n_envs=8)
        policy_kwargs = dict(activation_fn=th.nn.ReLU,
                     net_arch=[dict(pi=[32, 32,32], vf=[32, 32,32])])
        self.model = A2C("MlpPolicy", self.env,policy_kwargs=policy_kwargs, verbose=verbose)

class PPOLearningAgent(LearningAgent):
    '''PPO -Learning agent
    '''
    def __init__(self,verbose=1):
        super().__init__()
        self.name = "PPO_Agent_V2"
        self.applyMonitor()
        self.env = make_vec_env(self.envName, n_envs=8)
        self.model = PPO("MlpPolicy", self.env, verbose=1)


def iterativelyTrainAll(doesPreload = False, steps = 1):
    '''Trains a list of predefined agents for a given number of steps. If preload is enabled, loads from their defined save locations.'''
    agents = [DQNLearningAgent(),A2CLearningAgent(), PPOLearningAgent()]
    os.makedirs(LOG_PATH, exist_ok=True)
    if doesPreload:
        for agent in agents:
            agent.load()
    for agent in agents:
        agent.learn(timesteps=steps)
        agent.save()
    return agents

def evaluateAll(agents, steps):
    for agent in agents:
        monitor_path = agent.getLogPath()
        plt.show()

def runFullTraining():
    ''' Acts as an entrypoint to the program. Runs training for all agents, 
        and evaluates or aggregates their plots and logs.
        Furthermore, also saves the trained agents.
        There is an issue such that logs are never collected when "learn" is called.
    '''
    steps = 100
    agents = iterativelyTrainAll(steps)
    # evaluateAll(agents, steps)
    # NOTE: Commented out as this function no longer works, and was the main 
    # blocker for the assessment portion of this assignment.

if __name__ == '__main__':
    runFullTraining()