from Player import Player
from util import Coordinate

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

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

