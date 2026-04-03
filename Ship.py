from util import Orientation, Coordinate
from dataclasses import dataclass

class Ship(object):
    def __init__(name: str,
                 size: int,
                 orientation: Orientation,
                 origin: Coordinate):
        self.name = name
        self.size = size
        self.hits = 0
        self.occupied = self._get_occupied(size, orientation, origin)

    # TODO
    @classmethod
    def can_occupy(cls, size: int,
                      orientation: Orientation,
                      origin: Coordinate) -> list[Coordinate]:
        pass
    
    def _get_occupied(self, size: int,
                      orientation: Orientation,
                      origin: Coordinate) -> list[Coordinate]:
        spaces = [None] * size
        cur = Coordinate(origin.row, origin.col)
        for i in range(size):
            spaces[i] = Coordinate(cur.row, cur.col)
            if orientation == HORIZONTAL:
                cur.row += 1
            else:
                cur.col += 1
        return spaces

    def occupies(self, coor: Coordinate) -> bool:
        return coor in self.occupied

    def take_hit(self) -> bool:
        self.hits += 1
        if self.hits == self.size:
            self.sunk = True
            return True
        return False


class Carrier(Ship):
    def __init__(orientation: Orientation,
                 origin: Coordinate):
        super().__init__("Carrier", 5, orientation, origin)

class Battleship(Ship):
    def __init__(orientation: Orientation,
                 origin: Coordinate):
        super().__init__("Battleship", 4, orientation, origin)

class Destroyer(Ship):
    def __init__(orientation: Orientation,
                 origin: Coordinate):
        super().__init__("Destroyer", 3, orientation, origin)

class Submarine(Ship):
    def __init__(orientation: Orientation,
                 origin: Coordinate):
        super().__init__("Submarine", 3, orientation, origin)

class PatrolBoat(Ship):
    def __init__(orientation: Orientation,
                 origin: Coordinate):
        super().__init__("Patrol Boat", 2, orientation, origin)

@dataclass
class AttackResult:
    hit: bool
    sunk: bool
    ship: Ship | None
