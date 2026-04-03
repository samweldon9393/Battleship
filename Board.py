from util import CellState
from Ship import Ship

BOARD_SIZE = 10

class Board(object):
    """
    A Board represents the game board from the POV of one player
    meaning it has a known grid of its own ships, and an unknown
    grid representing its opponent's ships
    """
    def __init__(self):
        self.ship_grid:   list[list[Ship | None]] = None
        self.cell_grid:   list[list[CellState]]   = self._init_cell_grid()

    def _init_cell_grid(self):
        return [[CellState.UNKNOWN] * BOARD_SIZE] * BOARD_SIZE
