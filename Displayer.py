from Board import Board
from Ship import Ship
from util import BOARD_SIZE, CellState, Coordinate

class Displayer(object):
    def __init__(self, board: Board, ships: list[Ship]):
        self.board = board  # player's guess grid (opponent's board)
        self.ships = ships # player's ship list 

    def display(self, label="OPPONENT's BOARD"):
        self._draw_board(label=label)
        self._draw_ships()

    def _draw_ships(self):
        print("  YOUR SHIPS\n")

        # Build each ship's display block as a list of lines
        blocks = []
        for ship in self.ships:
            name_line = f"{ship.name}"# [{Coordinate.inds[ship.occupied[0].col]}, {ship.occupied[0].row + 1}]"
            cells = ""
            for i in range(ship.size):
                cells += "X" if i < ship.hits else "█"
            cell_line = f"[ {cells} ]"
            width = max(len(name_line), len(cell_line))
            blocks.append((
                name_line.ljust(width),
                cell_line.ljust(width),
                width
                ))

        # Print in rows of 3
        col_gap = "     "
        print(col_gap + col_gap.join(b[0] for b in blocks))
        print(col_gap + col_gap.join(b[1] for b in blocks))
        print()

    def _draw_board(self, label: str):
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
                cell = self.board.get_cell(Coordinate(col, row))
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
