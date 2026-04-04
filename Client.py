from util import send_msg, recv_msg
import socket

class BattleshipClient(object):
    def __init__(self, ip: str = '127.0.0.1', port: int = 8888):
        s            = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        self.conn    = s

    def start(self):
        while True:
            msg      = "start loop"
            while msg[-2:] != ": ":
                msg  = recv_msg(self.conn)
                print(msg, end="")
                if len(msg) < 2:
                    msg += "  "
            response = input("")
            send_msg(self.conn, response)
