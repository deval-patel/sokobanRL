from .Pieces import Pieces
from .RewardSystem import *
from .SokobanBoard import *
from .SokobanStack import *
from .SokobanGame import *

from gym.envs.registration import register

register(
    id='498-sokoban-v0',
    entry_point='gym_498_sokoban.envs:SokobanCustomEnvV0',
)
# register(
#     id='foo-extrahard-v0',
#     entry_point='gym_foo.envs:FooExtraHardEnv',
# )
