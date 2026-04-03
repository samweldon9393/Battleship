from Board import Board
from Ship import Ship
from util import BOARD_SIZE, CellState, Coordinate

class Displayer(object):
    def __init__(self, player_board: Board, opp_board: Board, ships: list[Ship]):
        self.player_board   = player_board  # player one's guess grid (opponent's board)
        self.opp_board      = opp_board     # player two's guess grid (opponent's board)
        self.ships          = ships         # player one's ship list 

    def display(self, label="OPPONENT's BOARD"):
        #TODO label
        self._draw_boards_side_by_side()
        self._draw_ships()

    def _draw_boards_side_by_side(self):
        GAP = "     "
        col_headers = "    " + "   ".join("ABCDEFGHIJ"[:BOARD_SIZE])

        h_line_top = "  ┌" + "───┬" * (BOARD_SIZE - 1) + "───┐"
        h_line_mid = "  ├" + "───┼" * (BOARD_SIZE - 1) + "───┤"
        h_line_bot = "  └" + "───┴" * (BOARD_SIZE - 1) + "───┘"

        def board_rows(board):
            lines = []
            for row in range(BOARD_SIZE):
                row_label = f"{row + 1:<2}"
                cells = ""
                for col in range(BOARD_SIZE):
                    cell = board.get_cell(Coordinate(col, row))
                    if cell == CellState.HIT:
                        symbol = " X "
                    elif cell == CellState.MISS:
                        symbol = " · "
                    else:
                        symbol = "   "
                    cells += f"{symbol}│"
                lines.append(f"{row_label}│{cells}")
                if row < BOARD_SIZE - 1:
                    lines.append(h_line_mid)
            return lines

        left_label  = "YOUR BOARD".center(len(col_headers))
        right_label = "OPPONENT'S BOARD".center(len(col_headers))
        print(f"\n  {left_label}{GAP}  {right_label}\n")

        print(col_headers + GAP + col_headers)
        print(h_line_top  + GAP + h_line_top)

        left_rows  = board_rows(self.player_board)
        right_rows = board_rows(self.opp_board)
        for left, right in zip(left_rows, right_rows):
            print(left + GAP + right)

        print(h_line_bot + GAP + h_line_bot)
        print("\n  X = Hit   · = Miss   (blank) = Unknown\n")

    def _draw_ships(self):
        print("  YOUR SHIPS\n")

        # Build each ship's display block as a list of lines
        blocks = []
        for ship in self.ships:
            name_line = f"{ship.name}"
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

        col_gap = "     "
        print(col_gap + col_gap.join(b[0] for b in blocks))
        print(col_gap + col_gap.join(b[1] for b in blocks))
        print()

    """
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
        """
