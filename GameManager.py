from Displayer import Displayer
from Player import Player
from ComputerAI import ComputerAI
from HumanPlayer import HumanPlayer
from Ship import AttackResult
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
        self.p2.place_ships()
        self.p1.place_ships()
        while True:
            self.displayer.display()
            if self.turn(self.p1, self.p2):
                break
            if self.turn(self.p2, self.p1):
                break

    def turn(self, player: Player, opp: Player) -> bool:
        """
        Player makes a move, opp receives a hit
        Returns True if game over, else False
        """
        move        = player.take_turn()
        attk_rslt   = opp.take_hit(move)
        if attk_rslt.hit:
            if attk_rslt.sunk:
                print(f"{player.name} sunk Player 2's {attk_rslt.ship.name}")
                p2.ships_left -= 1
                if p2.ships_left == 0:
                    print(f"{player.name} wins!")
                    return True
            else:
                print(f"{player.name} hit {opp.name}'s {attk_rslt.ship.name}")
        else:
            print(f"{player.name} miss")
        return False

def main():
    computerAI  = ComputerAI(Difficulty.EASY)
    name        = input("Enter your name: ")
    human       = HumanPlayer(name=name)
    displayer   = Displayer(human.board)
    gameManager = GameManager(human, computerAI, displayer)

    gameManager.start()


if __name__ == '__main__':
    main()
