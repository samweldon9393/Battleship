from Board import Board
from Displayer import Displayer
from abc import abstractmethod
from util import CellState, Coordinate
from Ship import AttackResult, Ship

class Player(object):
    def __init__(self, name: str = "Player"):
        self.board      = Board()
        self.ships      = list()
        self.ships_left = 5
        self.name       = name
        self.moves_made = set()

    @abstractmethod
    def place_ships(self) -> list[Ship]:
        pass

    @abstractmethod
    def take_turn(self) -> Coordinate:
        pass

    @abstractmethod
    def turn_result(self, move: Coordinate, result: AttackResult) -> Coordinate:
        pass

    def take_hit(self, coor: Coordinate) -> AttackResult:
        for ship in self.ships:
            if coor in ship.occupied:
                self.board.update(coor, CellState.HIT)
                return AttackResult(hit=True, sunk=ship.is_sunk(), ship=ship)
        self.board.update(coor, CellState.MISS)
        return AttackResult(hit=False, sunk=False, ship=None)

    def save_move(self, move: Coordinate):
        if move in self.moves_made:
            return False
        self.moves_made.add(move)
        return True
