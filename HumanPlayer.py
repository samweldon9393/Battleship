from Displayer import Displayer
from Player import Player
from Ship import AttackResult, Ship
from util import BOARD_SIZE, Coordinate, Orientation, Unguessed

"""
HumanPlayer: Maintain's game state for a player and handles I/O
"""
class HumanPlayer(Player):
    def __init__(self, name: str = "Human"):
        super().__init__(name=name)

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
                coor = Coordinate(row=Coordinate.rows[x], col=int(y)-1)
            except IndexError as e:
                print(f"Invalid entry: {e}")
            except Exception as e:
                print(f"Move must be in the form [x y] (no brackets) {e}")
                continue
            if move in self.unguessed:
                self.unguessed.remove(move)
                break
            else:
                print("Cannot repeat moves")
        return coor

    def output(self, msg: str):
        print(msg)

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
                if not coor.is_valid():
                    print(f"Coordinate must be [A <= row <= J, 1 <= col <= 10]")
                    continue
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
