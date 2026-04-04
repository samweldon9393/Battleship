from Displayer import Displayer
from HumanPlayer import HumanPlayer
from Player import Player
from Ship import AttackResult
from util import Coordinate

class GameManager(object):
    def __init__(self,
                 p1: Player,
                 p2: Player,
                 displayer: Displayer
                 ):
        self.p1         = p1
        self.p2         = p2
        self.displayer  = displayer

    def start(self):
        self.displayer._draw_boards_side_by_side()
        self.p1.place_ships()
        self.p2.place_ships() #TODO concurrent?
        self.displayer._draw_ships()
        while True:
            turn_result = self.turn(self.p1, self.p2)
            output      = turn_result[1]
            if turn_result[0]:
                print(output)
                break
            turn_result = self.turn(self.p2, self.p1)
            output      += turn_result[1]
            if turn_result[0]:
                print(output)
                break
            self.displayer.display()
            print(output)

    def turn(self, player: Player, opp: Player) -> tuple[bool, str]:
        """
        Player makes a move, opp receives a hit
        Returns output to print and True if game over, else False
            Output is returned instead of printed to allow displaying board
            before output
        """

        # One player makes a guess (no repeats)
        move = player.take_turn()
        while not player.save_move(move): # Don't allow the same move twice
            if isinstance(player, HumanPlayer):
                print("Cannot repeat moves")
            move = player.take_turn()

        # That guess is sent to the other player, who replies with a result
        attk_rslt = opp.take_hit(move)

        # That result is then relayed to the first player to record
        player.turn_result(move, attk_rslt)

        output      = f"{player.name} guessed [{Coordinate.inds[move.col]}, {move.row + 1}]. "
        if attk_rslt.hit:
            if attk_rslt.sunk:
                output += f"{player.name} sunk {opp.name}'s {attk_rslt.ship.name}\n"
                # Update num ships left here as it makes formatting output easy
                opp.ships_left -= 1
                if opp.ships_left == 0:
                    output += f"{player.name} wins!\n"
                    return (True, output)
            else:
                output += f"{player.name} hit {opp.name}'s {attk_rslt.ship.name}\n"
        else:
            output += f"{player.name} miss\n"
        return (False, output)
