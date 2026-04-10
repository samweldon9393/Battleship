from Displayer import Displayer
from HumanPlayer import HumanPlayer
from Ship import Ship
from util import BOARD_SIZE, Coordinate, Orientation, recv_msg, send_msg

import socket

"""
ClientPlayer: A HumanPlayer with networking added. The client side of the 
    TCP connection handles no game logic. Instead, the server side of the 
    connection handles the client's player object. This allows for a 
    single GameManager and minimal networking coordination.
"""
class ClientPlayer(HumanPlayer):
    def __init__(self,
                 displayer: Displayer,
                 port: int = 8888,
                 name: str = "Human"):
        super().__init__(name=name)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse port numbers
        s.bind(('', port))
        s.listen()
        self.conn, self.addr = s.accept()               # blocks until client connects
        self.displayer = displayer
        
        send_msg(self.conn, "Enter your name: ")
        self.name = recv_msg(self.conn)

    def place_ships(self):
        self.displayer.draw_boards_side_by_side()
        super().place_ships()

    def take_turn(self) -> Coordinate:
        """
        Prompts user for a cell to strike. Returns the input Coordinate.
        """
        self.displayer.display()
        while True:
            send_msg(self.conn, "Your move, enter [x y] (no brackets): ")
            move = recv_msg(self.conn)
            try:
                x, y = move.split(' ')
                x = x.upper()
                y = int(y)
                if not 0 < y <= BOARD_SIZE:
                    raise Exception("Invalid cell input (must be form [A <= row <= J, 1 <= col <= 10])")
                coor = Coordinate(row=Coordinate.rows[x], col=int(y)-1)
            except Exception as e:
                send_msg(self.conn, f"Move must be in the form [x y] (no brackets) {e}")
                continue
            if move in self.unguessed:
                self.unguessed.remove(move)
                break
            else:
                send_msg(self.conn, "Cannot repeat moves")
        return coor

    def output(self, msg: str):
        send_msg(self.conn, msg)

    def _place_ship(self, ship: Ship) -> Coordinate:
        """
        Prompts user for a location and orientation to place ship
        """
        while True:
            coor = None
            send_msg(self.conn, f"Place your {ship.name}. Enter [col row orientation(h/v)] (e.g.: A 1 v): ")
            inp  = recv_msg(self.conn)
            try:
                x, y, o = inp.split(' ')
                x = x.upper()
                y = int(y)
                o = o.lower()
                coor = Coordinate(row=Coordinate.rows[x], col=y-1)
            except Exception as e:
                send_msg(self.conn, f"Move must be in the form [x y o] (no brackets) {e}")
                continue
            orient = -1
            if o == "v":
                orient = Orientation.VERTICAL
            elif o == "h":
                orient = Orientation.HORIZONTAL
            else:
                send_msg(self.conn, "Must enter v or h for orientation: ")
                continue
            if ship.place(self.ships, orient, coor):
                break
            else:
                send_msg(self.conn, "Cannot place ship there, try again: ")
        return ship
