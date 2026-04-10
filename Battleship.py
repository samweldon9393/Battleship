#!/bin/env python3

from Board import Board
from Client import BattleshipClient
from ComputerPlayer import ComputerPlayer
from Displayer import Displayer, SimulationDisplayer
from GameManager import GameManager
from HumanPlayer import HumanPlayer
from Player import Player
from Server import ClientPlayer
from util import send_msg, Difficulty

import argparse

def single_player():
    difficulty      = _prompt_difficulty()
    name            = input("Enter your name: ")
    human           = HumanPlayer(name=name)
    computer        = ComputerPlayer(difficulty)
    displayer       = Displayer(
            opp_board=computer.guess_board,
            player_board=human.guess_board,
            ships=human.ships
    )
    gameManager     = GameManager(human, computer, displayer)

    gameManager.start()

def server_mode(port: int):
    name            = input("Enter your name: ")
    server_player   = HumanPlayer(name=name)
    server_displayer   = Displayer(
            player_board=server_player.guess_board,
            ships=server_player.ships,
    )

    client_player   = ClientPlayer(displayer=Displayer(), port=port)
    server_displayer.opp_board              = client_player.guess_board
    client_player.displayer.opp_board       = server_player.guess_board
    client_player.displayer.player_board    = client_player.guess_board
    client_player.displayer.ships           = client_player.ships
    client_player.displayer.print_fn        = lambda msg : send_msg(client_player.conn, msg+'\n')

    gameManager     = GameManager(server_player, client_player, server_displayer)
    gameManager.start()

def client_mode(ip: str = '127.0.0.1', port: int = 8888):
    clnt = BattleshipClient(ip, port)
    clnt.start()

def simulation_mode(diffs: str, display: bool):
    if len(diffs) != 2:
        print("Usage: Battleship.py -m XX (where x can be [E|M|H])")
        exit(1)
    p1_diff         = _get_difficulty(diffs[0].upper())
    p2_diff         = _get_difficulty(diffs[1].upper())
    if p1_diff == -1 or p2_diff == -1:
        print("Usage: Battleship.py -m XX (where x can be [E|M|H])")
        exit(1)
    p1              = ComputerPlayer(p1_diff)
    p2              = ComputerPlayer(p2_diff)
    if display:
        displayer   = Displayer(
                opp_board=p2.guess_board,
                player_board=p1.guess_board,
                ships=p1.ships
        )
    else:
        displayer   = SimulationDisplayer()
    gameManager     = GameManager(p1, p2, displayer)

    if gameManager.start() == p1:
        print(f"Player one won (on turn {gameManager.cur_turn})!")
    else:
        print(f"Player two won (on turn {gameManager.cur_turn})!")

def _get_difficulty(difficulty_str: str) -> Difficulty:
    match difficulty_str:
        case "E":
            return Difficulty.EASY
        case "M":
            return Difficulty.MEDIUM
        case "H":
            return Difficulty.HARD
        case _:
            return -1

def _prompt_difficulty() -> Difficulty:
    difficulty_str  = input("Enter difficulty level [E | M | H]: ").upper()
    difficulty      = _get_difficulty(difficulty_str)
    while difficulty == -1:
        difficulty_str = input("Must enter E | M | H: ").upper()
        _get_difficulty(difficulty_str)
    return difficulty

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
        help="Run in mutli-player server mode. "
        "Must enter port number to host on."
    )
    parser.add_argument(
        "-c", "--client", 
        action="store_true",
        help="Run in mutli-player client mode. "
        "Must enter ip address and port number to connect to."
    )
    parser.add_argument(
        "-m", "--simulation", 
        type=str,
        help="Run in simulation mode. "
        "Must enter difficulty level for both players."
    )
    # Optional with value
    parser.add_argument(
        "-p", "--port",
        type=int,
        help="Port number."
    )
    parser.add_argument(
        "-i", "--ip",
        type=str,
        help="Server IP address to connect to."
    )
    parser.add_argument(
        "--display",
        action="store_true",
        help="In simulation mode, display the game board"
    )

    args = parser.parse_args()

    # Can only run in one of default, server, and client modes
    
    if args.simulation:
        simulation_mode(args.simulation, args.display)
        exit(0)

    if args.default + args.server + args.client > 1:
        print("Can only enter one of -d, -s, -c, -m")
        parser.print_help()
        exit(1)

    if args.server and (not args.port or args.ip):
        print("Must enter a port number to host server on")
        parser.print_help()
        exit(1)

    if args.client and not (args.port and args.ip):
        print("Must enter an ip address and port number to connect to")
        parser.print_help()
        exit(1)

    if args.default or (args.server + args.client) == 0:
        single_player()

    elif args.server:
        server_mode(args.port)

    elif args.client:
        client_mode(args.ip, args.port)

if __name__ == '__main__':
    main()
