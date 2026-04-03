from Board import Board
from util import BOARD_SIZE, CellState, Coordinate

class Displayer(object):
    def __init__(self, board: Board):
        self.board = board # human player's board

    def display(self):
        print("OPPONENT'S BOARD")
        for i in range(BOARD_SIZE):
            print("-" * 40)
            print("|", end="")
            for j in range(BOARD_SIZE):
                cell = self.board.get_cell(Coordinate(j, i))
                if cell == CellState.UNKNOWN:
                    print("   |", end="")
                elif cell == CellState.HIT:
                    print(" H |", end="")
                elif cell == CellState.MISS:
                    print(" M |", end="")
            print("")
        print("-" * 40)

        print("PLAYER'S SHIPS")

