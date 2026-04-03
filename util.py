from enum import Enum
from dataclasses import dataclass

BOARD_SIZE = 10

@dataclass
class AttackResult:
    hit: bool
    sunk: bool
    ship = None # Ship type

@dataclass
class Coordinate:
    row: int
    col: int

class CellState(Enum):
    UNKNOWN = 0
    MISS    = 1
    HIT     = 2

class Orientation(Enum):
    HORIZONTAL  = 0
    VERTICAL    = 1

class Difficulty(Enum):
    EASY    = 0
    MEDIUM  = 1
    HARD    = 2

ShipTypes = [
        "Carrier",
        "Battleship",
        "Destroyer",
        "Submarine",
        "Patrol Boat"
        ]
