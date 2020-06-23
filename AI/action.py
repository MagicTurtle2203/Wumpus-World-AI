from enum import Enum, auto


class ActionType(Enum):
    FORWARD = auto()
    TURNLEFT = auto()
    TURNRIGHT = auto()
    GRAB = auto()
    SHOOT = auto()
    CLIMB = auto()
