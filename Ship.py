from util import BOARD_SIZE, Coordinate, Orientation
from dataclasses import dataclass

"""
Ship: Represents a ship in the game Battleship. Common base class that is
    extended by each ship type in the game.
"""
class Ship(object):
    def __init__(self, sid:int, name: str, size: int):
        self.sid  = sid
        self.name = name
        self.size = size
        self.hits = 0
        self.occupied: list[Coordinate] = None

    def place(self, ships: list,
              orientation: Orientation,
              origin: Coordinate) -> bool:
        """
        Returns true if placement is ok, sets self.occupied to a list of 
        all occupied Coordinates
        """
        spaces = [None] * self.size
        cur = Coordinate(row=origin.row, col=origin.col)
        for i in range(self.size):
            if cur.row >= BOARD_SIZE or cur.col >= BOARD_SIZE:
                return False
            spaces[i] = Coordinate(row=cur.row, col=cur.col)
            if orientation == Orientation.HORIZONTAL:
                cur.col += 1
            else:
                cur.row += 1
        self.occupied = spaces
        return self._can_occupy(ships)

    def occupies(self, coor: Coordinate) -> bool:
        return coor in self.occupied

    def is_sunk(self) -> bool:
        self.hits += 1
        if self.hits == self.size:
            self.sunk = True
            return True
        return False

    def _can_occupy(self, ships: list) -> bool:
        for ship in ships:
            for coor in ship.occupied:
                if self.occupies(coor):
                    return False
        return True

    def __hash__(self) -> int:
        return hash(self.name) + self.sid


class AircraftCarrier(Ship):
    # Temporary ships can have default sid=0, persistent ships need a unique
    # id for hashing
    def __init__(self, sid: int = 0):
        super().__init__(sid, "Aircraft Carrier", 5)

class Battleship(Ship):
    def __init__(self, sid: int = 0):
        super().__init__(sid, "Battleship", 4)

class Cruiser(Ship):
    def __init__(self, sid: int = 0):
        super().__init__(sid, "Cruiser", 3)

class Destroyer(Ship):
    def __init__(self, sid: int = 0):
        super().__init__(sid, "Destroyer", 2)

class Submarine(Ship):
    def __init__(self, sid: int = 0):
        super().__init__(sid, "Submarine", 1)

@dataclass
class AttackResult:
    hit:  bool
    sunk: bool
    ship: Ship
