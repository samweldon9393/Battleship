from util import BOARD_SIZE, CellState, Coordinate
from Ship import Ship

"""
Board: Represents player B's board from the perspective of player A.
    The class is a thin wrapper on a matrix (list[list[CellState]]).
"""
class Board(object):
    def __init__(self):
        self.cell_grid = self._init_cell_grid()

    def _init_cell_grid(self) -> list[list[CellState]]:
        return [[CellState.UNKNOWN] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    def get_cell(self, coor: Coordinate) -> CellState:
        """
        Coordinates are used elsewhere in the form (col, row), as it is more
        natural with the [letter, number] format, so in the Board class, that
        is corrected to (row, col) to work with the data structure properly
        """
        return self.cell_grid[coor.row][coor.col]

    def update(self, coor: Coordinate, state: CellState):
        self.cell_grid[coor.row][coor.col] = state
