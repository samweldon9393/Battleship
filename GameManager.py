#!/bin/env python3

from Displayer import Displayer
from Player import Player
from ComputerPlayer import ComputerPlayer
from HumanPlayer import HumanPlayer
from Ship import AttackResult
from util import Coordinate, Difficulty

# TODO remove
import time

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
        move = player.take_turn()
        while not player.save_move(move): # Don't allow the same move twice
            if isinstance(player, HumanPlayer):
                print("Cannot repeat moves")
            move    = player.take_turn()
        attk_rslt   = opp.take_hit(move)
        player.turn_result(move, attk_rslt)
        output      = f"{player.name} guessed [{Coordinate.inds[move.col]}, {move.row + 1}]. "
        if attk_rslt.hit:
            if attk_rslt.sunk:
                output += f"{player.name} sunk {opp.name}'s {attk_rslt.ship.name}\n"
                opp.ships_left -= 1
                if opp.ships_left == 0:
                    output += f"{player.name} wins!\n"
                    return (True, output)
            else:
                output += f"{player.name} hit {opp.name}'s {attk_rslt.ship.name}\n"
        else:
            output += f"{player.name} miss\n"
        return (False, output)

def main():
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


if __name__ == '__main__':
    main()
