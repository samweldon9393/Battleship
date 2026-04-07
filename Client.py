from util import send_msg, recv_msg
import socket

"""
BattleshipClient: A very simple TCP client that doesn't know it is
    playing a game of Battleship. Instead, it uses a very simple protocol
    to send and receive messages from a TCP server.

Protocol:
    Receive messages endlessly in a loop until receives a prompt or 
    server closes connection.
    Prompts are messages from the server where the last two characters
    are ": ".
    Upon receiving a prompt, get input from stdin and forward it to the
    server.
"""
class BattleshipClient(object):
    def __init__(self, ip: str = '127.0.0.1', port: int = 8888):
        s            = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        self.conn    = s

    def start(self):
        try:
            while True:
                msg      = "start"
                while msg[-2:] != ": ":
                    msg  = recv_msg(self.conn)
                    print(msg, end="")
                    if len(msg) < 2:
                        msg += "  "
                response = input("")
                send_msg(self.conn, response)
        except ConnectionError:
            print("Connection Terminated")
