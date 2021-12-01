import pygame

from ImageGenerator import ImageGenerator


class Pieces(ImageGenerator):
    """
    A class which contains constants for piece representations.
    Also returns images to represent each piece.

    === Attributes ===
    EMPTY: A character which identifies an empty space on the map.
    WALL: A character which identifies a wall on the map.
    BOX: A character which identifies a box on the map.
    GOAL: A character which identifies a goal on the map.
    PLAYER: A character which identifies a player on the map.
    """
    EMPTY: int = 0
    WALL: int = 1
    TARGET: int = 2
    BOX: int = 3
    BOX_ON_TARGET: int = 4
    PLAYER: int = 5
    PLAYER_ON_TARGET: int = 6

    def __init__(self, pygame: pygame, width: int, height: int) -> None:
        """
        Initialize all of the pygame images based on the images in the assets folder.
        """
        super().__init__(pygame)
        images = {
            self.EMPTY: 0,
            self.WALL:  1,
            self.BOX: 2,
            self.GOAL: 3,
            self.PLAYER: 4,
        }
        self.add_images(images)
        self.scale_images(width, height)

    def get_image(self, piece: str, i: int = -1, j: int = -1) -> pygame.Surface:
        """
        Returns the pygame image based on the piece and coordinate of the piece.
        """
        return self.images.get(piece, self.EMPTY).copy()
