from Board import Board
import util

class Player(object):
    def __init__(self):
        self.board = Board()

    @abstractmethod
    def place_ships(self):
        pass

    @abstractmethod
    def take_turn(self):
        pass
