import util
from Ship import Ship

BOARD_SIZE = 10

class Board(object):
    """
    A Board represents the game board from the POV of one player
    meaning it has a known grid of its own ships, and an unknown
    grid representing its opponent's ships
    """
    def __init__(self):
        player_ship_grid   = None
        opp_cell_grid      = self._init_cell_grid()

    def _init_cell_grid(self):
        return [[UNKNOWN] * BOARD_SIZE] * BOARD_SIZE
