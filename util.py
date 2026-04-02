from enum import Enum
from dataclasses import dataclass

@dataclass
class Coordinate:
    row: int
    col: int

class Cell(Enum):
    UNKNOWN = 0
    MISS    = 1
    HIT     = 2

class Orientation(Enum):
    HORIZONTAL  = 0
    VERTICAL    = 1
