from Player import Player
import util
import random

class ComputerAI(Player):
    def __init__(self, difficulty: Difficulty):
        super().__init__()
        self.difficulty = difficulty

    def place_ships(self):
        # TODO
        pass

    def take_turn(self):
        match self.difficulty:
            case EASY:
                self._easy_guess()
            case MEDIUM:
                self._med_guess()
            case HARD:
                self._hard_guess()

    def _easy_guess(self):
