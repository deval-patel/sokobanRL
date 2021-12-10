from __future__ import annotations
from Pieces import Pieces
from typing import List
from random import randint
from Exceptions import InvalidActionError


class Player:
    """
    A class includes the essential functionalities for human player and
    random player (A.I.)

    This class gives implemented constructors and functions: get_tokens,
    get_styles, get_valid_turns and set_sokoban. The functions may need
    to re-implemented in the sub class.

    get_turn function should implement in the sub class which heritage
    the Player class.

    """
    INVALID_ACTION_ERROR = 'That is not a valid Action. Please enter one of (W, A, S, D)\n'

    def __init__(self) -> None:
        """
        Initialize this player with their player_id which is either G1 or G2.
        """
        pass

    def get_move(self) -> int:
        """
        Get an action for this player.
        """
        raise NotImplementedError

    def set_sokoban(self, sokoban):
        self.sokoban = sokoban
    def get_valid_moves(self) -> List[int]:
        """
        Get's all of the valid moves that this player can make on this move.
        """
        return []



class PlayerRandom(Player):
    '''
    The random player (A.I.) class which inherits from the player class.
    '''

    def __init__(self) -> None:
        """
        Initialize a new random player
        """
        super().__init__()

    def get_move(self) -> int:
        turns = self.get_valid_turns()
        if len(turns) == 0:
            return None
        return turns[randint(0, len(turns) - 1)]


class PlayerHuman(Player):
    prompt: str = 'Choose your Action: '

    def __init__(self) -> None:
        super().__init__()

    def get_move(self) -> int:
        """
        Get's a single move that the player wants to make through the console.

        @return the move that the player wants to make.
        """
        while True:
            try:
                move = input(self.prompt).lower()
                if move == 'w':
                    return 0
                elif move == 's':
                    return 1
                elif move == 'a':
                    return 2
                elif move == 'd':
                    return 3
                raise InvalidActionError
            except InvalidActionError:
                print(Player.INVALID_ACTION_ERROR)


