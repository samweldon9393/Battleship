from util import BOARD_SIZE, CellState, Coordinate
from Ship import Ship

"""
Board: Represents player B's board from the perspective of player A.
    The class is a wrapper on a matrix (list[list[CellState]]).
"""
class Board(object):
    def __init__(self):
        self.cell_grid = self._init_cell_grid()

    def get_cell(self, coor: Coordinate) -> CellState:
        """
        Returns the state of the cell at coor
        """
        # Bounds checking handled in Coordinate constructor
        if not coor.is_valid():
            raise IndexError("Invalid Coordinate")
        return self.cell_grid[coor.row][coor.col]

    def update(self, coor: Coordinate, state: CellState):
        """
        Updates cell at coor to state
        """
        if not coor.is_valid():
            raise IndexError("Invalid Coordinate")
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
        state = self.get_cell(coor)
        if not (state == CellState.UNKNOWN or state == CellState.HIT):
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
        """
        Initialzie a [BOARD_SIZE x BOARD_SIZE] matrix, all cells start unknown
        """
        return [[CellState.UNKNOWN] * BOARD_SIZE for _ in range(BOARD_SIZE)]
