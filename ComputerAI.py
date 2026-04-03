from Displayer import Displayer
from Player import Player
from Ship import AttackResult, Carrier, Battleship, Destroyer, Submarine, PatrolBoat, Ship
from util import BOARD_SIZE, CellState, Coordinate, Difficulty, Orientation, Modes
import random

"""
ComputerAI: A class that contains the logic to play Battleship on 
    various difficulty levels:
        EASY    - Completely random guessing
        Medium  - Random guessing until hit, then search nearby

Strategy Source: http://www.datagenetics.com/blog/december32011/
"""
class ComputerAI(Player):
    def __init__(self, difficulty: Difficulty, name: str = "Hal"):
        super().__init__(name=name)
        self.difficulty = difficulty
        self.mode       = Modes.HUNT
        self.targets    = list()

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

    def turn_result(self, move: Coordinate, rslt: AttackResult):
        if not rslt.hit:
            return
        if rslt.sunk:
            self.targets.clear()
            self.mode = Modes.HUNT
            return
        else: # move was a hit, and the ship isn't sunk yet
            self.mode = Modes.TARGET
            if move.col < BOARD_SIZE - 1:
                coor = Coordinate(move.col + 1, move.row)
                if coor not in self.targets and self.board.get_cell(coor) == CellState.UNKNOWN:
                    self.targets.append(coor)
            if move.col > 0:
                coor = Coordinate(move.col - 1, move.row)
                if coor not in self.targets and self.board.get_cell(coor) == CellState.UNKNOWN:
                    self.targets.append(coor)
            if move.row < BOARD_SIZE - 1:
                coor = Coordinate(move.col, move.row + 1)
                if coor not in self.targets and self.board.get_cell(coor) == CellState.UNKNOWN:
                    self.targets.append(coor)
            if move.row > 0:
                coor = Coordinate(move.col, move.row - 1)
                if coor not in self.targets and self.board.get_cell(coor) == CellState.UNKNOWN:
                    self.targets.append(coor)

    def _easy_guess(self) -> Coordinate:
        row = random.choice([i for i in range(10)])
        col = random.choice([i for i in range(10)])
        while self.board.get_cell(Coordinate(row, col)) != CellState.UNKNOWN:
            row = random.choice([i for i in range(10)])
            col = random.choice([i for i in range(10)])
        return Coordinate(row, col)

    def _med_guess(self) -> Coordinate:
        if self.mode == Modes.HUNT:
            return self._easy_guess()
        else:
            print(f"self.targets: {self.targets}")
            return self.targets.pop() if len(self.targets) > 0 else self._easy_guess()
