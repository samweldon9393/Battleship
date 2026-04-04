#!/bin/env python3

from ComputerPlayer import ComputerPlayer
from Displayer import Displayer
from HumanPlayer import HumanPlayer
from Player import Player
from Ship import AttackResult
from util import Coordinate, Difficulty

import argparse

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
        self.p2.place_ships()
        self.displayer._draw_ships()
        while True:
            turn_result = self.turn(self.p1, self.p2)
            output = turn_result[1]
            if turn_result[0]:
                print(output)
                break
            turn_result = self.turn(self.p2, self.p1)
            output += turn_result[1]
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

def single_player():
    difficulty_str  = input("Select a difficulty level: E | M | H (coming soon): ")
    difficulty      = -1
    while True:
        difficulty_str = difficulty_str.upper()
        match difficulty_str:
            case "E":
                difficulty = Difficulty.EASY
                break
            case "M":
                difficulty = Difficulty.MEDIUM
                break
            case _:
                difficulty_str = input("Must enter E | M: ")
    name            = input("Enter your name: ")
    human           = HumanPlayer(name=name)
    computer        = ComputerPlayer(difficulty)
    displayer       = Displayer(computer.board, human.board, human.ships)
    gameManager     = GameManager(human, computer, displayer)

    gameManager.start()

def main():
    parser = argparse.ArgumentParser(description="A command line Battleship game.")

    # Optional flag (switch)
    parser.add_argument(
        "-d", "--default", 
        action="store_true",
        help="Run in single-player mode."
    )
    parser.add_argument(
        "-s", "--server", 
        action="store_true",
        help="Run in mutli-player server mode."
    )
    parser.add_argument(
        "-c", "--client", 
        action="store_true",
        help="Run in mutli-player client mode."
    )
    # Optional with value
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=8888,
        help="Port number."
    )
    parser.add_argument(
        "-i", "--ip",
        type=str,
        default="127.0.0.1",
        help="Server IP address to connect to."
    )

    args = parser.parse_args()

    if args.default + args.server + args.client > 1:
        parser.print_help()
        exit(1)

if __name__ == '__main__':
    main()
