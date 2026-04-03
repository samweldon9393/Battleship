from Board import Board
from abc import abstractmethod
from util import CellState, Coordinate
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

    def take_hit(self, coor: Coordinate) -> AttackResult:
        for ship in self.ships:
            if coor in ship.occupied:
                self.board.update(coor, CellState.HIT)
                return AttackResult(hit=True, sunk=ship.is_sunk(), ship=ship)
        self.board.update(coor, CellState.MISS)
        return AttackResult(hit=False, sunk=False, ship=None)
