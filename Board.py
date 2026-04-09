from util import BOARD_SIZE, CellState, Coordinate
from Ship import Ship

"""
Board: Represents player B's board from the perspective of player A.
    The class is a thin wrapper on a matrix (list[list[CellState]]).
"""
class Board(object):
    def __init__(self):
        self.cell_grid = self._init_cell_grid()

    def get_cell(self, coor: Coordinate) -> CellState:
        """
        Coordinates are used elsewhere in the form (col, row), as it is more
        natural with the [letter, number] format, so in the Board class, that
        is corrected to (row, col) to work with the data structure properly
        """
        if not (0 <= coor.row < BOARD_SIZE) or not (0 <= coor.col < BOARD_SIZE):
            return CellState.INVALID
        return self.cell_grid[coor.row][coor.col]

    def update(self, coor: Coordinate, state: CellState):
        """
        Updates cell at coor to state
        """
        self.cell_grid[coor.row][coor.col] = state

    def ship_sunk(self, ship: Ship):
        """
        Updates all cells occupied by ship to sunk status
        """
        for coor in ship.occupied:
            self.update(coor, CellState.SUNK)

    def ship_can_occupy(self, ship: Ship, coor: Coordinate) -> bool:
        """
        Returns True if ship can occupy coor, else False
        """
        if self.get_cell(coor) != CellState.UNKNOWN:
            return False
        up, down, left, right = 0, 0, 0, 0
        go_up, go_down, go_left, go_right = True, True, True, True
        for i in range(ship.size - 1):
            state = self.get_cell(Coordinate(row=coor.row+i, col=coor.col))
            if go_right and (state == CellState.UNKNOWN or state == CellState.HIT):
                right += 1
            else:
                go_right = False
            state = self.get_cell(Coordinate(row=coor.row-i, col=coor.col))
            if go_left and (state == CellState.UNKNOWN or state == CellState.HIT):
                left += 1
            else:
                go_left = False
            state = self.get_cell(Coordinate(row=coor.row, col=coor.col+1))
            if go_down and (state == CellState.UNKNOWN or state == CellState.HIT):
                down += 1
            else:
                go_down = False
            state = self.get_cell(Coordinate(row=coor.row, col=coor.col-1))
            if go_up and (state == CellState.UNKNOWN or state == CellState.HIT):
                up += 1
            else:
                go_up = False

        return (up + down + 1 >= ship.size) or (left + right + 1 >= ship.size)

    def _init_cell_grid(self) -> list[list[CellState]]:
        return [[CellState.UNKNOWN] * BOARD_SIZE for _ in range(BOARD_SIZE)]
