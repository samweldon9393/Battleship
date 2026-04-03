from Board import Board
from util import CellState

class Displayer(object):
    def __init__(self, board: Board):
        self.board = board

    def display(self):
        print("OPPONENT'S BOARD")
        for row in self.board.cell_grid:
            print("-" * 40)
            print("|", end="")
            for cell in row:
                if cell == CellState.UNKNOWN:
                    print("   |", end="")
                elif cell == CellState.HIT:
                    print(" H |", end="")
                elif cell == CellState.MISS:
                    print(" M |", end="")
            print("")
        print("-" * 40)

        print("PLAYER'S BOARD")
        print("coming soon")
