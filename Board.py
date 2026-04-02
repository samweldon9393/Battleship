import util
from Ship import Ship

BOARD_SIZE = 10

class Board(object):
    def __init__(self):
        ship_grid = None
        cell_grid = self._init_cell_grid()

    def _init_cell_grid(self):
        return [[UNKNOWN] * BOARD_SIZE] * BOARD_SIZE
