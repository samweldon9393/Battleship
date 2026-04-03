from Board import Board
from Displayer import Displayer
from abc import abstractmethod
from util import BOARD_SIZE, CellState, Coordinate, TOTAL_SHIPS
from Ship import AttackResult, Ship
import random

class Player(object):
    def __init__(self, name: str = "Player"):
        self.board      = Board()
        self.ships      = list()
        self.ships_left = TOTAL_SHIPS
        self.name       = name
        self.unguessed  = Unguessed()

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
        """
        Receive opponent's move. Return the results of the move.
        """
        for ship in self.ships:
            if coor in ship.occupied:
                self.board.update(coor, CellState.HIT)
                return AttackResult(hit=True, sunk=ship.is_sunk(), ship=ship)
        self.board.update(coor, CellState.MISS)
        return AttackResult(hit=False, sunk=False, ship=None)

    def save_move(self, move: Coordinate):
        """
        Tries to record's a player's move. If that player already made that 
        move, return False, else True.
        """
        if move in self.unguessed:
            self.unguessed.remove(move)
            return True
        return False

class Unguessed(object):
    def __init__(self):
        self._list = [Coordinate(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
        self._set  = set(self._list)

    def __contains__(self, c: Coordinate):
        return c in self._set

    def __len__(self):
        return len(self._list)

    def remove(self, c: Coordinate):
        self._list.remove(c)
        self._set.remove(c)

    def random(self):
        return random.choice(self._list)
