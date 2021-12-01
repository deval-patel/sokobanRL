from typing import List, Union
from Pieces import Pieces

class SokobanBoard:
    """
    An SokobanBoard class consisting of a game board, and keeping track of grid state.

    === Attributes === 
    size : A board's width and height.
    player : Player object representing a player.

    === Private Attributes ===
    _board : 
        A nested list representing a grid layout for the board.
    """
    size: int
    _board: List[List[str]]

    def __init__(self, size: int, board: List[List[int]]) -> None:
        """
        Initialize this SokobanBoard with the given player and board.
        """
        self.size = size
        self._board = [row.copy() for row in board]

    def get_token_count(self,token: int, board=None) -> int:
        if board:
            return sum([row.count(token) for row in board])
        return sum([row.count(token) for row in self._board])

    def valid_coordinate(self, row: int, col: int) -> bool:
        """
        Returns true iff the provided coordinates are valid (exists on the board).
        """
        return row >= 0 and col >= 0 and row < self.size and col < self.size

    def get_token(self, row: int, col: int) -> str:
        """
        Returns the token that is in the given <row> <col> position, or -1 on invalid position.
        """
        if not self.valid_coordinate(row, col):
            return -1
        return self._board[row][col]

    def set_token(self, row: int, col: int, token: str) -> None:
        """
        Sets the given position on the board to be the given <token>.
        """
        if self.valid_coordinate(row, col):
            self._board[row][col] = token

    def get_board(self) -> List[List[str]]:
        """
        DO NOT MODIFY THIS!!! 
        Creates and returns a deep copy of this SokobanBoard's
        current state.
        """
        return [row.copy() for row in self._board]

    def set_board(self, board: List[List[str]]) -> None:
        """
        Sets the current board's state to the state of the board which is passed in as a parameter.
        """
        self._board = [row.copy() for row in board]

    def __str__(self) -> str:
        """
        Returns a string representation of this game board.
        """
        s = '  '
        for col in range(self.size):
            s += str(col) + ' '

        s += '\n'

        s += ' +'
        for col in range(self.size):
            s += "-+"

        s += '\n'

        for row in range(self.size):
            s += str(row) + '|'
            for col in range(self.size):
                s += str(self._board[row][col]) + '|'

            s += str(row) + '\n'

            s += ' +'
            for col in range(self.size):
                s += '-+'

            s += '\n'

        s += '  '
        for col in range(self.size):
            s += str(col) + ' '

        s += '\n'
        return s
