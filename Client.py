from util import send_msg, recv_msg
import socket

class BattleshipClient(object):
    def __init__(self, ip: str = '127.0.0.1', port: int = 8888):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket()
        s.connect((ip, port))                       # connect()
        self.conn = s

    def start(self):
        while True:
            prompt   = recv_msg(self.conn)
            response = input(prompt)
            send_msg(self.conn, response)
