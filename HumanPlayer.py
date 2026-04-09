from Displayer import Displayer
from Player import Player
from Ship import AttackResult, Ship
from util import BOARD_SIZE, Coordinate, Orientation, ShipTypes

"""
HumanPlayer: Maintain's game state for a player and handles I/O
"""
class HumanPlayer(Player):
    def __init__(self, name: str = "Human"):
        super().__init__(name=name)

    def _place_ship(self, ship: Ship) -> Coordinate:
        """
        Prompts user for a location and orientation to place ship
        """
        while True:
            coor = None
            inp = input(f"Place your {ship.name}. Enter [row col orientation(h/v)] (e.g.: A 1 v): ")
            try:
                x, y, o = inp.split(' ')
                x = x.upper()
                y = int(y)
                o = o.lower()
                coor = Coordinate(row=Coordinate.rows[x], col=y-1)
            except Exception as e:
                print(f"Move must be in the form [x y o] (no brackets) {e}")
                continue
            orient = -1
            if o == "v":
                orient = Orientation.VERTICAL
            elif o == "h":
                orient = Orientation.HORIZONTAL
            else:
                print("Must enter v or h for orientation")
                continue
            if ship.place(self.ships, orient, coor):
                break
            else:
                print("Cannot place ship there, try again")
        return ship

    def take_turn(self) -> Coordinate:
        """
        Prompts user for a cell to strike. Returns the input Coordinate.
        """
        while True:
            move = input("Your move, enter [x y] (no brackets): ")
            try:
                x, y = move.split(' ')
                x = x.upper()
                y = int(y)
                if not 0 < y <= BOARD_SIZE:
                    raise Exception("Invalid cell input (must be 0 < row <= 10")
                coor = Coordinate(row=Coordinate.rows[x], col=int(y)-1)
            except Exception as e:
                print(f"Move must be in the form [x y] (no brackets) {e}")
                continue
            break
        return coor

    def output(self, msg: str):
        print(msg)
