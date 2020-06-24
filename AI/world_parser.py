from enum import Enum, auto

from action import ActionType
from ai import AI


class Agent:
    DIRECTIONS = ["RIGHT", "DOWN", "LEFT", "UP"]

    def __init__(self):
        self.X = 0
        self.Y = 0

        self.direction_index = 0    # Decided to use ints rather than an enum to make turning easier

        self.has_arrow = True
        self.has_gold = False


class World:
    class TileType(Enum):
        BLANK = auto()
        GOLD = auto()
        WUMPUS = auto()
        PIT = auto()

    def __init__(self, filename, debug=False):
        self.AI = AI()
        self.agent = Agent()
        self.score = 0

        self.send_breeze = False
        self.send_bump = False
        self.send_glitter = False
        self.send_scream = False
        self.send_stench = False

        with open(filename) as file:
            self.board = self.create_board(file)

    def run(self):
        while True:
            action = self.AI.get_action(self.get_senses())  # TODO: write get_senses function
            self.score -= 1

            if action == ActionType.FORWARD:
                if self.agent.direction_index == 3:     # UP
                    if self.agent.Y + 1 > 0:
                        self.send_bump = True
                    self.agent.Y = min(self.agent.Y + 1, 3)
                elif self.agent.direction_index == 1:   # DOWN
                    if self.agent.Y - 1 < 0:
                        self.send_bump = True
                    self.agent.Y = max(self.agent.Y - 1, 0)
                elif self.agent.direction_index == 2:   # LEFT
                    if self.agent.X - 1 < 0:
                        self.send_bump = True
                    self.agent.X = max(self.agent.X - 1, 0)
                elif self.agent.direction_index == 0:   # RIGHT
                    if self.agent.X + 1 > 3:
                        self.send_bump = True
                    self.agent.X = min(self.agent.X + 1, 3)

                if self.board[self.agent.X][self.agent.Y] in (self.TileType.WUMPUS, self.TileType.PIT):
                    self.score -= 1000
                    break
                # TODO: Check if agent moved into squares adjacent to pit or wumpus and
                #       send breeze or stench signals
                #       Check if agent moved into gold square and send glitter signal
            elif action == ActionType.TURNLEFT:
                self.agent.direction_index = (self.agent.direction_index - 1) % 4
            elif action == ActionType.TURNRIGHT:
                self.agent.direction_index = (self.agent.direction_index + 1) % 4
            elif action == ActionType.GRAB:
                if self.board[self.agent.X][self.agent.Y] == self.TileType.GOLD:
                    self.agent.has_gold = True
                    self.board[self.agent.X][self.agent.Y] == self.TileType.BLANK
            elif action == ActionType.SHOOT:
                if self.agent.has_arrow:
                    pass    # TODO: Check if wumpus is in front of agent. If it is, kill it and send scream signal.
            elif action == ActionType.CLIMB:
                if (self.agent.X, self.agent.Y) == (0, 0) and self.agent.has_gold:
                    self.score += 1000
                    break

        return self.score

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
