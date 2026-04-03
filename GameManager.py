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

def main():
    computerAI  = ComputerAI(Difficulty.EASY)
    human       = HumanPlayer()
    displayer   = Displayer()
    gameManager = GameManager(computerAI, human, displayer)


if __name__ == '__main__':
    main()
