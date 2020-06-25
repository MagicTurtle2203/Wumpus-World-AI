from enum import Enum, auto

from .action import ActionType


class World:
    class Agent:
        def __init__(self):
            self.X = 0
            self.Y = 0

            # DIRECTIONS = ["RIGHT", "DOWN", "LEFT", "UP"]
            self.direction_index = 0    # Decided to use ints rather than an enum to make turning easier

            self.has_arrow = True
            self.has_gold = False

    class TileType(Enum):
        BLANK = auto()
        GOLD = auto()
        WUMPUS = auto()
        PIT = auto()

    def __init__(self, filename, AI_type, debug=False):
        self.AI = AI_type
        self.agent = self.Agent()
        self.score = 0

        self.wumpus_X = 0
        self.wumpus_Y = 0

        self.send_breeze = False
        self.send_bump = False
        self.send_glitter = False
        self.send_scream = False
        self.send_stench = False

        with open(filename) as file:
            self.board = self.create_board(file)

    def run(self) -> (bool, int):
        """Handles all actions of the AI agent."""
        suceeded = False

        while True:
            action = self.AI.get_action(self.get_senses())
            self.score -= 1

            if action == ActionType.FORWARD:
                if self.agent.direction_index == 3:     # UP
                    if self.agent.Y + 1 > 3:
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

                if self.board[self.agent.Y][self.agent.X] in (self.TileType.WUMPUS, self.TileType.PIT):
                    self.score -= 1000
                    break
            elif action == ActionType.TURNLEFT:
                self.agent.direction_index = (self.agent.direction_index - 1) % 4
            elif action == ActionType.TURNRIGHT:
                self.agent.direction_index = (self.agent.direction_index + 1) % 4
            elif action == ActionType.GRAB:
                if self.board[self.agent.Y][self.agent.X] == self.TileType.GOLD:
                    self.agent.has_gold = True
                    self.board[self.agent.Y][self.agent.X] == self.TileType.BLANK
            elif action == ActionType.SHOOT:
                if self.agent.has_arrow:
                    self.score -= 10
                    self.agent.has_arrow = False

                    if self.agent.direction_index == 3:     # UP
                        if self.agent.X == self.wumpus_X and self.agent.Y < self.wumpus_Y:
                            self.board[self.wumpus_Y][self.wumpus_X] = self.TileType.BLANK
                            self.send_scream = True
                    elif self.agent.direction_index == 1:   # DOWN
                        if self.agent.X == self.wumpus_X and self.agent.Y > self.wumpus_Y:
                            self.board[self.wumpus_Y][self.wumpus_X] = self.TileType.BLANK
                            self.send_scream = True
                    elif self.agent.direction_index == 2:   # LEFT
                        if self.agent.X > self.wumpus_X and self.agent.Y == self.wumpus_Y:
                            self.board[self.wumpus_Y][self.wumpus_X] = self.TileType.BLANK
                            self.send_scream = True
                    elif self.agent.direction_index == 0:   # RIGHT
                        if self.agent.X < self.wumpus_X and self.agent.Y == self.wumpus_Y:
                            self.board[self.wumpus_Y][self.wumpus_X] = self.TileType.BLANK
                            self.send_scream = True
            elif action == ActionType.CLIMB:
                if (self.agent.X, self.agent.Y) == (0, 0) and self.agent.has_gold:
                    self.score += 1000
                    suceeded = True
                    break
            # For testing only
            # else:
            #     break

        return suceeded, self.score

    def get_senses(self) -> [bool]:
        """
        Returns a list of boolean values based on flags set in the class.
        The list follows a format of [stench, breeze, glitter, bump, scream].
        """
        for (x, y) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_x = x + self.agent.X
            new_y = y + self.agent.Y

            if 0 <= new_x < 4 and 0 <= new_y < 4:
                if self.board[new_y][new_x] == self.TileType.WUMPUS:
                    self.send_stench = True
                elif self.board[new_y][new_x] == self.TileType.PIT:
                    self.send_breeze = True

        if self.board[self.agent.Y][self.agent.X] == self.TileType.GOLD:
            self.send_glitter = True

        senses = [
            True if self.send_stench else False,
            True if self.send_breeze else False,
            True if self.send_glitter else False,
            True if self.send_bump else False,
            True if self.send_scream else False
        ]

        self.send_stench = False
        self.send_breeze = False
        self.send_glitter = False
        self.send_bump = False
        self.send_scream = False

        return senses

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

        for row_idx, row in enumerate(board):
            for col_idx, item in enumerate(board[row_idx]):
                if item == self.TileType.WUMPUS:
                    self.wumpus_X = col_idx
                    self.wumpus_Y = row_idx
                    break
            else:
                continue
            break

        return board
