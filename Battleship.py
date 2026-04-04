#!/bin/env python3

from GameManager import GameManager
from ComputerPlayer import ComputerPlayer
from Displayer import Displayer
from HumanPlayer import HumanPlayer
from Player import Player
from util import Difficulty

import argparse

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

def server_mode(port: int):
    pass

def client_mode(port: int, ip: str):
    pass

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
        help="Port number."
    )
    parser.add_argument(
        "-i", "--ip",
        type=str,
        help="Server IP address to connect to."
    )

    args = parser.parse_args()

    # Can only run in one of default, server, and client modes
    if args.default + args.server + args.client > 1:
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
        exit(0)

    elif args.client:
        client_mode(args.port, args.ip)


if __name__ == '__main__':
    main()
