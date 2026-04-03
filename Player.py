from Board import Board
from abc import abstractmethod
from util import Coordinate

class Player(object):
    def __init__(self):
        self.board = Board()

    @abstractmethod
    def place_ships(self):
        pass

    @abstractmethod
    def take_turn(self) -> Coordinate:
        pass
