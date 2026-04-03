from Board import Board
from abc import abstractmethod
from util import Coordinate
from Ship import AttackResult, Ship

class Player(object):
    def __init__(self, name: str = "Player"):
        self.board      = Board()
        self.ships      = list()
        self.ships_left = 5
        self.name       = name

    @abstractmethod
    def place_ships(self) -> list[Ship]:
        pass

    @abstractmethod
    def take_turn(self) -> Coordinate:
        pass

    def take_hit(self, coor: Coordinate) -> Ship:
        for ship in self.ships:
            if coor in ship.occupied:
                return AttackResult(hit=True, sunk=ship.is_sunk(), ship=ship)
        return AttackResult(hit=False, sunk=False, ship=None)
