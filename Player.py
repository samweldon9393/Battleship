from Board import Board
from Displayer import Displayer
from abc import abstractmethod
from util import BOARD_SIZE, CellState, Coordinate, TOTAL_SHIPS
from Ship import AttackResult, AircraftCarrier, Battleship, Cruiser, Destroyer, Submarine, Ship
import random

"""
Player: A base class that exposes a common API across different types of player
    (human, computer, remote client). Maintains game state from one player's
    perspective.
"""
class Player(object):
    def __init__(self, name: str = "Player"):
        self.name        = name
        self.guess_board = Board()       # Opp's board from the player's POV
        self.ships       = list()        # Player's own ships
        self.ships_left  = TOTAL_SHIPS
        self.unguessed   = Unguessed()

    def place_ships(self):
        """"
        Place all 5 ships with _place_ship abstractmethod that handles 
        getting client input or generating locations for ComputerPlayers.
        """
        self.ships.append(self._place_ship(AircraftCarrier(1)))
        self.ships.append(self._place_ship(Battleship(2)))
        self.ships.append(self._place_ship(Cruiser(3)))
        self.ships.append(self._place_ship(Destroyer(4)))
        self.ships.append(self._place_ship(Destroyer(5)))
        self.ships.append(self._place_ship(Submarine(6)))
        self.ships.append(self._place_ship(Submarine(7)))

    @abstractmethod
    def take_turn(self) -> Coordinate:
        pass

    def turn_result(self, move: Coordinate, result: AttackResult):
        if result.sunk:
            self.guess_board.ship_sunk(result.ship)
        elif result.hit:
            self.guess_board.update(move, CellState.HIT)
        else:
            self.guess_board.update(move, CellState.MISS)

    @abstractmethod
    def output(self, msg: str):
        pass

    def take_hit(self, coor: Coordinate) -> AttackResult:
        """
        Receive opponent's move. Return the results of the move.
        """
        for ship in self.ships:
            if ship.occupies(coor):
                return AttackResult(hit=True, sunk=ship.is_sunk(), ship=ship)
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

    @abstractmethod
    def _place_ship(self, ship: Ship) -> Coordinate:
        pass


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
