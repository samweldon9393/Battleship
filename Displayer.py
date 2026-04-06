from Board import Board
from Ship import Ship
from util import BOARD_SIZE, CellState, Coordinate

"""
Displayer: This class handles printing the ASCII art board and ship states.
    A Displayer can print to the terminal or across a network connection by
    using a parameterized print function.
"""
class Displayer(object):
    def __init__(self,
                 player_board: Board = None,
                 opp_board: Board    = None,
                 ships: list[Ship]   = None,
                 print_fn            = print,
                 ):
        self.player_board   = player_board  # player A's guess grid (player B's board)
        self.opp_board      = opp_board     # player B's guess grid (player A's board)
        self.ships          = ships         # player A's ship list 
        self.print_fn       = print_fn

    def display(self):
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

        left_label  = "OPPONENT'S BOARD".center(len(col_headers))
        right_label = "YOUR BOARD".center(len(col_headers))
        self.print_fn(f"\n  {left_label}{GAP}  {right_label}\n")

        self.print_fn(col_headers + GAP + " " + col_headers)
        self.print_fn(h_line_top  + GAP + h_line_top)

        left_rows  = board_rows(self.player_board)
        right_rows = board_rows(self.opp_board)
        for left, right in zip(left_rows, right_rows):
            self.print_fn(left + GAP + right)

        self.print_fn(h_line_bot + GAP + h_line_bot)
        self.print_fn("\n  X = Hit   · = Miss   (blank) = Unknown\n")

    def _draw_ships(self):
        self.print_fn("  YOUR SHIPS\n")

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
        self.print_fn(col_gap + col_gap.join(b[0] for b in blocks))
        self.print_fn(col_gap + col_gap.join(b[1] for b in blocks))
        self.print_fn("")
