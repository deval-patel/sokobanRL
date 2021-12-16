# sokobanRL
Testing different RL agents on Sokoban.

Implements OpenAI Gym Custom Gym environment for both the player and the game generation engine.

# Installation Instructions
Please run these from the parent directory of this repository.
`pip install gym`

### We use stable baselines to test our environment on different RL algorithms.
`pip install stable-baselines[mpi]`

### This is for our custom gym environment.
`pip install -e sokobanRL`

Documentation for installing our custom gym environment from the official openAI gym docs can be found here: 
https://github.com/openai/gym/blob/master/docs/creating_environments.md 


# Running the Sokoban game and training scripts

## Sokoban game

To run the Sokoban game, ensure that you have activated your python environment, and if desired, installed requirements via running `pip install -r requirements.txt` from the repository root.

To run the Sokoban game, use `python3 gym_498_sokoban/SokobanController.py`


## Training Scripts

To run the Sokoban environments, ensure that you have activated your python environment, and if desired, installed requirements via running `pip install -r requirements.txt` from the repository root.

To run the training scripts, use `python3 gym_run.py`