from enum import Enum
from dataclasses import dataclass
import random

BOARD_SIZE    = 10
MAX_SHIP_SIZE = 5
TOTAL_SHIPS   = 5

#=============================================================================#
#                               Game Utilities                                #
#=============================================================================#

@dataclass
class Coordinate:
    row: int
    col: int
    rows = { "A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9 }
    inds = { 0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J" }
    def is_valid(self) -> bool:
        return (0 <= self.row < BOARD_SIZE) and (0 <= self.col < BOARD_SIZE)
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

class Unguessed(object):
    """
    A simple container class that wraps a list and a set.
    Allows O(1) membership testing and fast random choices (as python
    sets don't implement random.choice)
    """
    def __init__(self):
        """
        All possible coordinates are generated
        """
        self._list = [Coordinate(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
        self._set  = set(self._list)

    def __contains__(self, c: Coordinate):
        return c in self._set

    def __len__(self):
        return len(self._list)

    def remove(self, c: Coordinate):
        if c not in self:
            raise KeyError(f"{c} not in Unguessed")
        self._list.remove(c)
        self._set.remove(c)

    def random(self):
        if len(self) == 0:
            raise IndexError("Empty Unguessed")
        return random.choice(self._list)

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
