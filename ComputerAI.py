from Displayer import Displayer
from Player import Player
from Ship import Carrier, Battleship, Destroyer, Submarine, PatrolBoat, Ship
from util import CellState, Coordinate, Difficulty, Orientation
import random

class ComputerAI(Player):
    def __init__(self, difficulty: Difficulty, name: str = "Hal"):
        super().__init__(name=name)
        self.difficulty = difficulty

    def place_ships(self):
        self.ships.append(self._place_ship(Carrier()))
        self.ships.append(self._place_ship(Battleship()))
        self.ships.append(self._place_ship(Destroyer()))
        self.ships.append(self._place_ship(Submarine()))
        self.ships.append(self._place_ship(PatrolBoat()))

    def _place_ship(self, ship: Ship) -> Coordinate:
        while True:
            coor = Coordinate(random.randint(0, 9), random.randint(0, 9))
            orient = random.choice([Orientation.VERTICAL, Orientation.HORIZONTAL])
            if ship.place(self.ships, orient, coor):
                break
        return ship

    def take_turn(self) -> Coordinate:
        match self.difficulty:
            case Difficulty.EASY:
                return self._easy_guess()
            case Difficulty.MEDIUM:
                return self._med_guess()
            case Difficulty.HARD:
                return self._hard_guess()

    def _easy_guess(self) -> Coordinate:
        row = random.choice([i for i in range(10)])
        col = random.choice([i for i in range(10)])
        while self.board.get_cell(Coordinate(row, col)) != CellState.UNKNOWN:
            row = random.choice([i for i in range(10)])
            col = random.choice([i for i in range(10)])
        return Coordinate(row, col)
