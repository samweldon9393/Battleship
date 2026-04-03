from util import BOARD_SIZE, CellState, Coordinate
from Ship import Ship

class Board(object):
    """
    A Board represents the game board from the POV of one player
    meaning it has a known grid of its own ships, and an unknown
    grid representing its opponent's ships
    """
    def __init__(self):
        self.cell_grid:   list[list[CellState]]   = self._init_cell_grid()

    def _init_cell_grid(self):
        return [[CellState.UNKNOWN] * BOARD_SIZE] * BOARD_SIZE

    def get_cell(self, coor: Coordinate):
        return self.cell_grid[coor.row][coor.col]

    def update(self, coor: Coordinate, state: CellState):
        self.cell_grid[coor.row][coor.col] = state
