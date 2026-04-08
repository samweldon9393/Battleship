from enum import Enum
from dataclasses import dataclass

MAX_SHIP_SIZE   = 5
TOTAL_SHIPS     = 5
BOARD_SIZE      = 10

#=============================================================================#
#                               Game Utilities                                #
#=============================================================================#

@dataclass
class Coordinate:
    col: int
    row: int
    cols = { "A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9 }
    inds = { 0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J" }
    def __hash__(self):
        tup = (self.col, self.row)
        return hash(tup)

class CellState(Enum):
    UNKNOWN = 0
    MISS    = 1
    HIT     = 2
    SUNK    = 3
    INVALID = 4

class Orientation(Enum):
    HORIZONTAL  = 0
    VERTICAL    = 1

class Difficulty(Enum):
    EASY    = 0
    MEDIUM  = 1
    HARD    = 2

class Modes(Enum):
    HUNT    = 0
    TARGET  = 1

ShipTypes = [
        "Carrier",
        "Battleship",
        "Destroyer",
        "Submarine",
        "Patrol Boat"
        ]

#=============================================================================#
#                           Networking Utilities                              #
#=============================================================================#

def recv_all(conn, length):
    data = b""
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed mid-receive")
        data += chunk
    return data 

import struct

def send_msg(conn, msg: str):
    encoded = msg.encode('utf-8')
    header = struct.pack('>I', len(encoded))   # 4-byte big-endian length
    conn.send(header + encoded)

def recv_msg(conn) -> str:
    header = recv_all(conn, 4)
    length = struct.unpack('>I', header)[0]
    return recv_all(conn, length).decode('utf-8')
