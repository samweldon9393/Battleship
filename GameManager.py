from Displayer import Displayer
from Player import Player
from ComputerAI import ComputerAI
from HumanPlayer import HumanPlayer
from util import Difficulty

class GameManager(object):
    def __init__(self,
                 p1: Player,
                 p2: Player,
                 displayer: Displayer
                 ):
        self.p1 = p1
        self.p2 = p2
        self.displayer = displayer

    def start(self):
        self.p1.place_ships()
        while True:
            self.displayer.display()
            self.p1.take_turn()
            self.p2.take_turn()

def main():
    computerAI  = ComputerAI(Difficulty.EASY)
    human       = HumanPlayer()
    displayer   = Displayer(human.board)
    gameManager = GameManager(human, computerAI, displayer)

    gameManager.start()


if __name__ == '__main__':
    main()
