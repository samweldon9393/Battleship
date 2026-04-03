from enum import Enum
from dataclasses import dataclass

BOARD_SIZE = 10

@dataclass
class Coordinate:
    col: int
    row: int
    cols = { "A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9 }
    inds = { 0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J" }

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

class Modes(Enum):
    HUNT    = 0
    TARGET  = 1

ShipTypes = [
        "Carrier",
        "Battleship",
        "Destroyer",
        "Submarine",
        "Patrol Boat"
        ]
