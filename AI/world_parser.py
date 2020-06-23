from enum import Enum, auto
from pathlib import Path

import ai


class Agent:
    class Direction(Enum):
        UP = auto()
        DOWN = auto()
        LEFT = auto()
        RIGHT = auto()

    def __init__(self):
        self.agent_X = 0
        self.agent_Y = 0

        self.agnet_direction = self.Direction.RIGHT

        self.has_arrow = True
        self.has_gold = False


class World:
    class TileType(Enum):
        BLANK = auto()
        GOLD = auto()
        WUMPUS = auto()
        PIT = auto()

    def __init__(self, filename, debug=False):
        self.agent = Agent()

        with open(filename) as file:
            self.board = self.create_board(file)

    def create_board(self, file: open) -> [[str]]:
        """
        Creates a 2D list of Tiles representing the Wumpus World world specified by the inputted text file.
        """
        tile_dict = {
            '0': self.TileType.BLANK,
            'G': self.TileType.GOLD,
            'W': self.TileType.WUMPUS,
            'P': self.TileType.PIT
        }

        board = [[tile_dict.get(char) for char in line.strip()] for line in file]

        return board
