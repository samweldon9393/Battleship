from Displayer import Displayer
from HumanPlayer import HumanPlayer
from Player import Player
from Server import ClientPlayer
from Ship import AttackResult
from util import Coordinate

import threading

"""
GameManager: Entry point into the Battleship game, handles the main loop.
"""
class GameManager(object):
    def __init__(self,
                 p1: Player,
                 p2: Player,
                 ):
        self.p1         = p1
        self.p2         = p2
        self.cur_turn   = 1

    def start(self) -> Player:
        """
        Main game loop
        """
        self.p1.displayer.draw_boards_side_by_side()
        self.p2.displayer.draw_boards_side_by_side()
        self._place_both_players_ships()
        self.p1.displayer.draw_ships()
        self.p2.displayer.draw_ships()
        winner = None
        while True:
            game_over, output = self.turn(self.p1, self.p2)
            if game_over:
                self.p1.output(output)
                self.p2.output(output)
                winner = self.p1
                break
            game_over, output = self.turn(self.p2, self.p1)
            if game_over:
                self.p1.output(output)
                self.p2.output(output)
                winner = self.p2
                break
            self.p1.displayer.display()
            self.p2.displayer.display()
            self.p1.output(output)
            self.p2.output(output)
            self.cur_turn += 1
        return winner

    def turn(self, player: Player, opp: Player) -> tuple[bool, str]:
        """
        Player makes a move, opp receives a hit
        Returns output to print and True if game over, else False
            Output is returned instead of printed to allow displaying board
            before output
        """

        # One player makes a guess (no repeats)
        move = player.take_turn()

        # That guess is sent to the other player, who replies with a result
        attk_result = opp.take_hit(move)

        # That result is then relayed to the first player to record
        player.turn_result(move, attk_result)

        output = f"{player.name} guessed [{Coordinate.inds[move.row]}, {move.col + 1}]. "
        if attk_result.hit:
            if attk_result.sunk:
                output += f"{player.name} sunk {opp.name}'s {attk_result.ship.name}\n"
                # Update num ships left here as it makes formatting output easy
                opp.ships_left -= 1
                if opp.ships_left == 0:
                    output += f"{player.name} wins (on turn {self.cur_turn})!\n"
                    return (True, output)
            else:
                output += f"{player.name} hit {opp.name}'s {attk_result.ship.name}\n"
        else:
            output += f"{player.name} miss\n"
        return (False, output)

    def _place_both_players_ships(self):
        """
        Place all ships for both players concurrently
        """
        t1 = threading.Thread(target=self.p1.place_ships)
        t2 = threading.Thread(target=self.p2.place_ships)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

