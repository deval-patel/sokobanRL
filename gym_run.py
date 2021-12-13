import gym
import numpy as np
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3 import DQN, A2C
from stable_baselines3.common.env_util import make_vec_env
from agents.agents import RandomAgent
import torch as th

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
        A base class for learning agents, used to train, save, load, and validate models.
    '''
    def __init__(self):
        self.envName ="gym_498_sokoban:498-sokoban-v0"
        self.env = gym.make(self.envName)
        self.savePath = None

    def learn(self, timesteps=25000):
        self.model = self.model.learn(total_timesteps=timesteps,
        
            )

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
    def __init__(self,verbose=1):
        super().__init__()
        self.model = DQN("MlpPolicy", self.env, verbose=verbose)
        self.name = "overnightdqnlearningagent"

    #def learn(self, timesteps=25000):
    #    self.model = self.model.learn(total_timesteps=timesteps)

class A2CLearningAgent(LearningAgent):
    '''Double Q-Learning agent
    '''
    def __init__(self,verbose=1):
        super().__init__()
        self.env = make_vec_env(self.envName, n_envs=8)
        policy_kwargs = dict(activation_fn=th.nn.ReLU,
                     net_arch=[dict(pi=[32, 32,32], vf=[32, 32,32])])
        self.model = A2C("MlpPolicy", self.env,policy_kwargs=policy_kwargs, verbose=verbose)
        self.name = "overnighta2clearningagent"

    #def learn(self, timesteps=25000):
    #    self.model.learn(total_timesteps=timesteps)

def iterativelyTrainAll(doesPreload = False, iters = 1):
    agents = [DQNLearningAgent(),A2CLearningAgent()]
    log_dir = "run_logs/"
    os.makedirs(log_dir, exist_ok=True)
    if doesPreload:
        for agent in agents:
            agent.load()
    for iter in range(iters):
        for agent in agents:
            agent.learn(timesteps=100000)
            agent.save()

iterativelyTrainAll()