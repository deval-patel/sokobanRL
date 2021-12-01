from typing import List
from SokobanBoard import SokobanBoard
from Pieces import Pieces
from SokobanStack import SokobanStack
from RewardSystem import RewardSystem
import csv

class SokobanGame:
    """
    An SokobanGame class consisting of a game board, and keeping track of which player's
    move it currently is and some statistics about the game (e.g. how many tokens each player
    has). It knows who the winner of the game is, and when the game is over.

    === Attributes === 
    size : the size of this sokoban game.
    player1 : Player object representing player 1(Michael).
    player2 : Player object representing player 2(Ilir).
    whose_turn : Player whose move it is.
    board_stack : A stack of Sokoban boards that 

    === Private Attributes ===

    _board: 
        Sokoban board object with information on player positions and board layout.

    === Representation Invariants ===
    - Size must be an odd number greater or equal to 5

    """
    # Actions
    UP : int = 0
    DOWN : int = 1
    LEFT: int = 2
    RIGHT: int = 3
    size: int
    _board: SokobanBoard
    sokoban_stack: SokobanStack

    def __init__(self, board_filename: str = './assets/default.csv') -> None:
        """
        Constructs a game of Sokoban with 2 players passed in as parameters
        Sets <whose_turn> to <player1>
        Sets the <self.size> of Sokoban to the passed in <size> if valid.
        Precondition: The size must be odd and greater than or equal to 5.
        """
        turn_limit, player_pos, board = self.get_board_from_file(board_filename)
        self.turn_limit = turn_limit
        self.player_pos = player_pos
        self.size = len(board)
        self._board = SokobanBoard(self.size, board)
        self.og_map = self._board.get_board()
        self._board.set_token(*self.player_pos, Pieces.PLAYER)
        self.num_targets = self._board.get_token_count(Pieces.TARGET)
        self.sokoban_stack = SokobanStack()

    def get_board_from_file(self, filename: str) -> List[List[int]]:
        # File must contain
        # Line 1: turn limit
        # Line 2: player_pos_row, player_pos_col
        # Rest of the board in csv
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        assert(len(data) >= 3)
        turn_limit = int(data[0][0])
        player_pos = (int(data[1][0]), int(data[1][1]))
        board = [list(map(int, rec)) for rec in data[2:]]
        return turn_limit, player_pos, board

    def get_token(self, row: int, col: int) -> str:
        """
        Returns the player token that is in the given position, or the empty
        character if no player token is there or if the position provided is invalid.
        """
        return self._board.get_token(row, col)
    
    def get_destination(self, row: int, col: int, action: int) -> int:
        """
        Get's the destination position if this action was made at this position.
        Return a tuple containing new position or (-1, -1) on invalid action.
        """
        if action == self.UP:
            return (row - 1, col)
        elif action == self.DOWN:
            return (row + 1, col)
        elif action == self.LEFT:
            return (row, col - 1)
        elif action == self.RIGHT:
            return (row, col + 1)
        return (-1, -1)

    def is_valid_box_move(self, row: int, col: int, action: int) -> bool:
        """
        Checks if this box can be moved if this action was made.
        @return True on valid move, False otherwise
        """
        assert self.get_token(row, col) == Pieces.BOX or self.get_token(
            row, col) == Pieces.BOX_ON_TARGET
        row_d, col_d = self.get_destination(row, col, action)
        target = self.get_token(row_d, col_d)
        # Out of bounds
        if target == -1:
            return False
        # Can only move onto empty spaces or goals.
        return target == Pieces.EMPTY or target == Pieces.TARGET
        
    def is_valid_move(self, row: int, col: int, action: int) -> bool:
        """
        Checks if a move with the given parameters would be valid based on the
        origin and action taken.
        This method should specifically check for the following 3 conditions:
            1)  The movement is in the bounds of this game's board.
            3)  The destination is valid (cannot move into walls, or move boxes into walls).
        """
        # Check for valid destination target
        row_d, col_d = self.get_destination(row, col, action)
        target = self.get_token(row_d, col_d)
        # Player cannot move into a wall
        if target < 0 or target == Pieces.WALL:
            return False
        # If player is moving onto a box, make sure it is a valid move for the box
        elif (target == Pieces.BOX or target == Pieces.BOX_ON_TARGET) and not self.is_valid_box_move(row_d, col_d, action):
            return False

        return True

    def get_reward(self, old_board: List[List[int]]) -> float:
        """
        Returns the reward for the resulting move and change in game state.
        """
        old_boxes_on_target = self._board.get_token_count(
            Pieces.BOX_ON_TARGET, old_board)
        new_boxes_on_target = self._board.get_token_count(
            Pieces.BOX_ON_TARGET)
        if old_boxes_on_target < new_boxes_on_target:
            return RewardSystem.get_reward_for_box_on_target()
        elif old_boxes_on_target > new_boxes_on_target:
            return RewardSystem.get_reward_for_box_off_target()
        return RewardSystem.get_reward_for_move()

    def move(self, action: int) -> bool:
        """
        Attempts to make a move on the board state from position <row_o>, <col_o>
        using action <action>.

        On a successful move, it stores the old state of the board to <self.sokoban_stack> 
        by calling the <self.sokoban_stack.push(var1)> method.

        After storing the move, it will make the valid move and modify the board with new state.

        Returns the reward based on this move.
        """
        row, col = self.player_pos
        # Check for valid move
        if not self.is_valid_move(row, col, action):
            return RewardSystem.get_reward_for_invalid_move()
        old_board_state = self._board.get_board()
        # Store current state in stack
        self.sokoban_stack.push(old_board_state)
        row_d, col_d = self.get_destination(row, col, action)
        # Move box if needed
        if self.get_token(row_d, col_d) == Pieces.BOX or self.get_token(row_d, col_d) == Pieces.BOX_ON_TARGET:
            box_row_d, box_col_d = self.get_destination(row_d, col_d, action)
            if self.get_token(box_row_d, box_col_d) == Pieces.TARGET:
                self._board.set_token(box_row_d, box_col_d, Pieces.BOX_ON_TARGET)
            else:
                self._board.set_token(box_row_d, box_col_d, Pieces.BOX)
        # Move player
        if self.get_token(row_d, col_d) == Pieces.TARGET:
            self._board.set_token(
                    row_d, col_d, Pieces.PLAYER_ON_TARGET)
        else:
            self._board.set_token(row_d, col_d, Pieces.PLAYER)
        self.player_pos = (row_d, col_d)
        # Mark old spot as original position.
        self._board.set_token(row, col, self.og_map[row][col])
        return self.get_reward(old_board_state)

    def is_game_won(self):
        """
        Returns if the game is won or not. As per Sokoban's rules,
        the game is over if all the boxes have reached the goals. 
        """
        # Count how many targets are left.
        return self._board.get_token_count(Pieces.BOX_ON_TARGET) == self.num_targets
    
    def is_game_lost(self):
        """
        Returns if the game is lost or not. As per Sokoban's rules,
        the game is over if a box is stuck. 
        """
        # check if any box is stuck
        board = self.sokoban_stack.top()
        if not board:
            return False
        box_positions = []
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == Pieces.BOX:
                    box_positions.append((i, j))
        # Check if any box is blocked by checking valid moves from all directions.
        for row, col in box_positions:
            # This can be cleaned up to use a loop.
            row_d, col_d = self.get_destination(row, col, self.UP)
            if self.is_valid_move(row_d, col_d, self.DOWN):
                continue
            row_d, col_d = self.get_destination(row, col, self.DOWN)
            if self.is_valid_move(row_d, col_d, self.UP):
                continue
            row_d, col_d = self.get_destination(row, col, self.LEFT)
            if self.is_valid_move(row_d, col_d, self.RIGHT):
                continue
            row_d, col_d = self.get_destination(row, col, self.RIGHT)
            if self.is_valid_move(row_d, col_d, self.LEFT):
                continue
            return True

        return False

    def undo(self) -> None:
        """
        Undo's the Sokoban game's state to the previous move's state if possible.
        """
        if not self.sokoban_stack.empty():
            # The pop call here returns a board and a list of styles that we use
            # to revert to the previous state of the game
            board = self.sokoban_stack.pop()
            self._board.set_board(board)

    def get_board_string(self) -> str:
        """
        Returns string representation of this board.

        @return a string representation of this board
        """
        return str(self._board)

    def get_board(self) -> List[List[str]]:
        """
        Gets a copy of this SokobanBoard from SokobanBoard.getBoard()

        @return a copy of the current game board.
        """
        return self._board.get_board()

    def set_board(self, size: int, board: List[List[str]]) -> None:
        """
        Construct a new SokobanBoard with the given size and preset board.

        @param size the dimension of the SokobanBoard
        @param board the preset board state of the SokobanBoard
        """
        self.size = size
        self._board = SokobanBoard(self.size, board=board)

