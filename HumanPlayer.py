from Player import Player
from Ship import Carrier, Battleship, Destroyer, Submarine, PatrolBoat, Ship
from util import Coordinate, Orientation, ShipTypes

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def place_ships(self) -> bool:
        self.ships.append(self._place_ship(Carrier()))
        self.ships.append(self._place_ship(Battleship()))
        self.ships.append(self._place_ship(Destroyer()))
        self.ships.append(self._place_ship(Submarine()))
        self.ships.append(self._place_ship(PatrolBoat()))

    def _place_ship(self, ship: Ship) -> Coordinate:
        while True:
            coor = None
            inp = input(f"Place your {ship.name}. Enter [x, y] (no brackets): ")
            try:
                x, y = inp.split(',')
                coor = Coordinate(int(x), int(y))
            except Exception as e:
                print(f"Move must be in the form [x, y] (no brackets) {e}")
                continue
            orient = -1
            inp = input(f"Place your {ship.name} vertically (v) or horizontally (h)? ")
            if inp == "v":
                orient = Orientation.VERTICAL
            elif inp == "h":
                orient = Orientation.HORIZONTAL
            else:
                print("Must enter v or h only")
                continue
            if ship.place(self.ships, orient, coor):
                break
            else:
                print("Cannot place ship there, try again")
        return ship

    def take_turn(self) -> Coordinate:
        while True:
            move = input("Your move, enter [x, y] (no brackets): ")
            try:
                x, y = move.split(',')
                coor = Coordinate(int(x), int(y))
            except Exception as e:
                print(f"Move must be in the form [x, y] (no brackets) {e}")
                continue
            break
        return coor

