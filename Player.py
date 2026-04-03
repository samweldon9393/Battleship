from Board import Board
from abc import abstractmethod
from util import Coordinate
from Ship import Ship

class Player(object):
    def __init__(self):
        self.board = Board()
        self.ships = list()

    @abstractmethod
    def place_ships(self) -> list[Ship]:
        pass

    @abstractmethod
    def take_turn(self) -> Coordinate:
        pass
