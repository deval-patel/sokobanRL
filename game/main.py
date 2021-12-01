# Import the pygame module
import pygame
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    MOUSEBUTTONUP,
    K_ESCAPE,
    K_w,
    K_a,
    K_s,
    K_d,
    KEYDOWN,
    QUIT,
)
from Player import Player, PlayerRandom
from SokobanGame import SokobanGame
from Pieces import Pieces
from Button import Button
from Tile import Tile
from typing import List, Tuple


class Screen:
    """
    The main Screen for this pygame GUI.
    """
    # Define constants for the screen width and height
    SCREEN_WIDTH: int = 1000
    SCREEN_HEIGHT: int = 800
    BG: Tuple[int, int, int] = (0, 255, 0)
    BG_IMG: str = './assets/img/space.png'
    # BG_IMG: str = './assets/img/sayu_cry.gif'
    tiles: List[Tile]
    buttons: List[Button]
    pieces: Pieces
    mouse_pos: Tuple[int, int]
    # 0: HvH, 1: HvR 2: RvR
    game_mode: int = 0
    # Variable to keep the main loop running
    running: bool = True
    game_running: bool = True

    def __init__(self):
        """
        Initialize the Screen of the GUI
        """
        self.mouse_pos = (-1, -1)
        # Initialize pygame
        pygame.init()

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.pieces = Pieces(pygame, Tile.width, Tile.height)
        # Load the background
        img = pygame.image.load(self.BG_IMG).convert()
        img = pygame.transform.smoothscale(
            img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(img, (0, 0))
        self.reset()  # Initialize the game, tiles and style cards.
        # Create buttons that will be needed for the game.
        # Different Game Modes
        hvh = Button(self.screen, self.sokoban, 775, 175, 'Human')
        hvr = Button(self.screen, self.sokoban, 775, 275, 'Random')
        # Utility buttons to Undo a move and Reset the game.
        undo = Button(self.screen, self.sokoban, 775, 475, 'Undo')
        reset = Button(self.screen, self.sokoban, 775, 575, 'Reset')
        self.buttons = [hvh, hvr, undo, reset]
        # Update the display
        self.draw()
        pygame.display.flip()

    def init_tiles(self, offset_x, offset_y) -> None:
        """
        Initialize the tiles of the SokobanBoard.
        """
        board = self.sokoban.get_board()
        for i, row in enumerate(board):
            for j, _ in enumerate(row):
                self.tiles.append(
                    Tile(screen=self.screen,
                         sokoban=self.sokoban,
                         pieces=self.pieces,
                         row=i,
                         col=j,
                         offset_x=offset_x,
                         offset_y=offset_y
                         ))

    def reset_clicks(self) -> None:
        """
        Reset all clicked status on the tiles and style cards.
        """
        for tile in self.tiles:
            tile.clicked = False

        self.tile_origin = None
        self.tile_dest = None
        self.dest_tiles = []
        self.chosen_style = None

    def reset(self) -> None:
        """
        Reset this game of Sokoban to a new game and reset all relevant variables to their initial state.
        """
        self.sokoban = SokobanGame()
        self.tiles = []
        offset_x = (self.SCREEN_WIDTH -
                    self.sokoban.size * Tile.width) // 2
        offset_y = (self.SCREEN_HEIGHT -
                    self.sokoban.size * Tile.height) // 2

        self.init_tiles(offset_x, offset_y)

    def check_winner(self) -> None:
        """
        Check's the Sokoban game's status on a winner and updates game_running accordingly.
        """
        if self.sokoban.is_game_won():
            # TODO: Add who won somewhere on the screen.
            self.game_running = False

    def move_ai(self) -> None:
        """
        Make an AI player's move on sokoban if needed.
        """
        pass

    def move(self, action) -> None:
        """
        Make a human player's move on sokoban.
        """
        if self.sokoban.move(action):
            self.reset_clicks()

        self.check_winner()

    def undo(self) -> None:
        """
        Undo's a move in Sokoban and update's the styles as well as resets clicks on the tiles and style cards.
        """
        if not self.game_running:
            self.game_running = True
            self.set_op(0)
        self.sokoban.undo()
        if self.game_mode == 1:
            self.sokoban.undo()
        self.update_styles()
        self.reset_clicks()

    def btn_click(self, btn: Button) -> None:
        """
        Check which button was clicked and perform the respective actions.
        """
        if btn.text == 'Undo':
            self.undo()
            btn.clicked = False
        elif btn.text == 'Reset':
            self.reset()
            btn.clicked = False
            self.game_running = True

    def draw(self):
        """
        Draw all of the entities onto the screen.
        """
        # Draw tiles
        for tile in self.tiles:
            tile.draw()

        # Draw all buttons
        for btn in self.buttons:
            btn.draw()

        # Update the current game_mode button to highlight it.
        self.buttons[self.game_mode].set_highlight(True)

    def hover(self):
        """
        Check if any of the entities are being hovered.
        """
        mouse_pos = pygame.mouse.get_pos()

        for tile in self.tiles:
            # Check if hovered
            if tile.hover(mouse_pos):
                return
        for btn in self.buttons:
            if btn.hover(mouse_pos):
                break

    def click(self):
        """
        Check if any of the entities have been clicked.
        """
        mouse_pos = pygame.mouse.get_pos()
        clicked = None

        # Check if any of the buttons have been clicked and handle them appropriately.
        for btn in self.buttons:
            # Reset all button highlights statuses
            btn.set_highlight(False)
            if btn.click(mouse_pos):
                clicked = btn

        if clicked:
            self.btn_click(clicked)
            return
        # If the game is not running, we do not want any clicks on the game.
        if not self.game_running:
            return

    def render(self):
        """
        Renders the screen for the pygame GUI.
        This is the main loop of the code.
        """
        # Main loop

        while self.running:
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        self.running = False
                    elif event.key == K_w:
                        self.move(0)
                    elif event.key == K_s:
                        self.move(1)
                    elif event.key == K_a:
                        self.move(2)
                    elif event.key == K_d:
                        self.move(3)
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    self.running = False

                if event.type == MOUSEBUTTONUP:
                    # Check for click event
                    self.click()
            # If the game is moving, check if we need to move the AI.
            if self.game_running:
                self.move_ai()
            # Update the display
            self.draw()
            self.hover()

            # Update the display
            pygame.display.flip()


if __name__ == '__main__':
    screen = Screen()
    screen.render()
