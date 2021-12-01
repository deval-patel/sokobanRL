from Exceptions import GameModeError
from Pieces import Pieces
from SokobanGame import SokobanGame
from Player import Player, PlayerHuman, PlayerRandom


class SokobanController:
    """
    # TODO
    """
    GAME_MODE_PROMPT = f'Please enter the Game Mode you want to Play (H, R): '
    INVALID_GAME_MODE_ERROR = 'That game mode is not supported, please enter one of (HvH, HvR, RvR)\n'
    sokoban: SokobanGame
    player1: Player
    player2: Player

    def __init__(self, player: Player) -> None:
        """
        Constructs a new SokobanController with a new Sokoban game, ready to
        play with two users at the console.
        """
        self.player = player
        self.sokoban = SokobanGame()
        self.player.set_sokoban(self.sokoban)

    def play(self) -> None:
        """
        Plays a game of Sokoban between two human players. Takes moves as user
        input from the console.
        """
        while not self.sokoban.is_game_won():
            self.report()
            move = self.player.get_move()
            # self.report_turn(move)
            self.sokoban.move(move)
        self.report_final()

    # def report_turn(self, move) -> None:
    #     """
    #     Prints out the move information

    #     @param curr_player: the player who is making the current move.
    #     @param move:        the move that the current player made.
    #     """
    #     print(f'{curr_player.player_id} makes move {turn}\n')

    def report(self) -> None:
        """
        Prints out the game board, current styles and who's move it is next.
        """
        print(self.sokoban.get_board_string())

    def report_final(self) -> None:
        """
        Prints out the board's final state as well as the player who won the game of
        Sokoban.
        """
        string = self.sokoban.get_board_string() 
        print(string)


class SokobanControllerHuman(SokobanController):
    def __init__(self) -> None:
        """
        Constructs a new SokobanController with a new Sokoban game, ready to play
        with two users at the console.
        """
        super().__init__(PlayerHuman())


class SokobanControllerRandom(SokobanController):
    def __init__(self) -> None:
        """
        Constructs a new SokobanController with a new Sokoban game, ready to play
        with a user against a bot at the console.
        """
        super().__init__(PlayerRandom())




# Code to run this game
if __name__ == '__main__':
    oc = None
    while True:
        try:
            game_mode = str(input(SokobanController.GAME_MODE_PROMPT))
            if game_mode.lower() == 'h':
                oc = SokobanControllerHuman()
            elif game_mode.lower() == 'r':
                oc = SokobanControllerRandom()
            if oc is not None:
                break
            raise GameModeError
        except ValueError:
            print(SokobanController.INVALID_GAME_MODE_ERROR)
        except GameModeError:
            print(SokobanController.INVALID_GAME_MODE_ERROR)
    oc.play()
