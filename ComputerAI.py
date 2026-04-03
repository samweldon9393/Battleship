from Player import Player
from util import CellState, Coordinate, Difficulty
import random

class ComputerAI(Player):
    def __init__(self, difficulty: Difficulty):
        super().__init__()
        self.difficulty = difficulty

    def place_ships(self):
        # TODO
        pass

    def take_turn(self) -> Coordinate:
        match self.difficulty:
            case Difficulty.EASY:
                self._easy_guess()
            case Difficulty.MEDIUM:
                self._med_guess()
            case Difficulty.HARD:
                self._hard_guess()

    def _easy_guess(self) -> Coordinate:
        row = random.choice([i for i in range(10)])
        col = random.choice([i for i in range(10)])
        while self.board.cell_grid[row][col] != CellState.UNKNOWN:
            row = random.choice([i for i in range(10)])
            col = random.choice([i for i in range(10)])
        return Coordinate(row, col)
