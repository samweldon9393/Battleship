from Board import Board
from util import BOARD_SIZE, CellState, Coordinate

class Displayer(object):
    def __init__(self, board: Board):
        self.board = board  # opponent's guess grid

    def display(self, label="OPPONENT's BOARD"):
        self._draw_board(self.board, label=label)

    def _draw_board(self, board: Board, label: str):
        print(f"\n  {label}\n")

        col_headers = "    " + "   ".join("ABCDEFGHIJ"[:BOARD_SIZE])
        print(col_headers)

        h_line_mid = "  ├" + "───┼" * (BOARD_SIZE - 1) + "───┤"
        h_line_top = "  ┌" + "───┬" * (BOARD_SIZE - 1) + "───┐"
        h_line_bot = "  └" + "───┴" * (BOARD_SIZE - 1) + "───┘"

        print(h_line_top)
        for row in range(BOARD_SIZE):
            row_label = f"{row + 1:<2}"
            print(f"{row_label}│", end="")
            for col in range(BOARD_SIZE):
                cell = board.get_cell(Coordinate(col, row))
                if cell == CellState.HIT:
                    symbol = " X "
                elif cell == CellState.MISS:
                    symbol = " · "
                else:
                    symbol = "   "
                print(f"{symbol}│", end="")
            print()
            if row < BOARD_SIZE - 1:
                print(h_line_mid)
        print(h_line_bot)

        print("\n  X = Hit   · = Miss   (blank) = Unknown\n")
