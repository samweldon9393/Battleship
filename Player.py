from Board import Board
from Displayer import Displayer
from abc import abstractmethod
from util import BOARD_SIZE, CellState, Coordinate, TOTAL_SHIPS
from Ship import AttackResult, Carrier, Battleship, Destroyer, Submarine, PatrolBoat, Ship
import random

"""
Player: A base class that exposes a common API across different types of player
    (human, computer, remote client). Maintains game state from one player's
    perspective.
"""
class Player(object):
    def __init__(self, name: str = "Player"):
        self.name       = name
        self.board      = Board()
        self.ships      = list()
        self.ships_left = TOTAL_SHIPS
        self.unguessed  = Unguessed()

    def place_ships(self):
        """"
        Place all 5 ships with _place_ship abstractmethod that handles 
        getting client input or generating locations for ComputerPlayers.
        """
        self.ships.append(self._place_ship(Carrier()))
        self.ships.append(self._place_ship(Battleship()))
        self.ships.append(self._place_ship(Destroyer()))
        self.ships.append(self._place_ship(Submarine()))
        self.ships.append(self._place_ship(PatrolBoat()))

    @abstractmethod
    def _place_ship(self, ship: Ship) -> Coordinate:
        pass

    @abstractmethod
    def take_turn(self) -> Coordinate:
        pass

    @abstractmethod
    def turn_result(self, move: Coordinate, result: AttackResult) -> Coordinate:
        pass

    @abstractmethod
    def output(self, msg: str):
        pass

    def take_hit(self, coor: Coordinate) -> AttackResult:
        """
        Receive opponent's move. Return the results of the move.
        """
        for ship in self.ships:
            if ship.occupies(coor):
                self.board.update(coor, CellState.HIT)
                return AttackResult(hit=True, sunk=ship.is_sunk(), ship=ship)
        self.board.update(coor, CellState.MISS)
        return AttackResult(hit=False, sunk=False, ship=None)

    def save_move(self, move: Coordinate):
        """
        Tries to record's a player's move. If that player already made that 
        move, return False, else True. Taking a turn has polymorphic behavior
        based on derived player type, but handling repeat moves is same
        for humans and robots, so this is a function of the base class.
        """
        if move in self.unguessed:
            self.unguessed.remove(move)
            return True
        return False

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
        self._list.remove(c)
        self._set.remove(c)

    def random(self):
        return random.choice(self._list)
