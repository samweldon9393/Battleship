from util import BOARD_SIZE, Orientation, Coordinate
from dataclasses import dataclass

"""
Ship: Represents a ship in the game Battleship. Common base class that is
    extended by each ship type in the game.
"""
class Ship(object):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.hits = 0
        self.occupied: list[Coordinate] = None

    def _can_occupy(self, ships: list) -> bool:
        for ship in ships:
            for coor in ship.occupied:
                if self.occupies(coor):
                    return False
        return True

    
    # TODO do something more efficient
    def place(self, ships: list,
                    orientation: Orientation,
                    origin: Coordinate) -> bool:
        """
        Returns true if placement is ok, sets self.occupied to a list of 
        all occupied Coordinates
        """
        spaces = [None] * self.size
        cur = Coordinate(origin.col, origin.row)
        for i in range(self.size):
            if cur.row >= BOARD_SIZE or cur.col >= BOARD_SIZE:
                return False
            spaces[i] = Coordinate(cur.col, cur.row)
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


class Carrier(Ship):
    def __init__(self):
        super().__init__("Carrier", 5)

class Battleship(Ship):
    def __init__(self):
        super().__init__("Battleship", 4)

class Destroyer(Ship):
    def __init__(self):
        super().__init__("Destroyer", 3)

class Submarine(Ship):
    def __init__(self):
        super().__init__("Submarine", 3)

class PatrolBoat(Ship):
    def __init__(self):
        super().__init__("Patrol Boat", 2)

@dataclass
class AttackResult:
    hit:  bool
    sunk: bool
    ship: Ship
    def __hash__(self):
        return hash(ship.name)
