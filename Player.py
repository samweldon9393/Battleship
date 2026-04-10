from Board import Board
from Displayer import Displayer
from abc import abstractmethod
from util import BOARD_SIZE, CellState, Coordinate, TOTAL_SHIPS, Unguessed
from Ship import AttackResult, AircraftCarrier, Battleship, Cruiser, Destroyer, Submarine, Ship

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
        self.ships.append(self._place_ship(AircraftCarrier()))
        self.ships.append(self._place_ship(Battleship()))
        self.ships.append(self._place_ship(Cruiser()))
        self.ships.append(self._place_ship(Destroyer()))
        self.ships.append(self._place_ship(Destroyer(1))) # Differentiate 2 Destroyers
        self.ships.append(self._place_ship(Submarine()))
        self.ships.append(self._place_ship(Submarine(1)))

    @abstractmethod
    def take_turn(self) -> Coordinate:
        """
        Make a guess.
        Basic game loop is p1.take_turn -> p2.take_hit -> p1.turn_result
        """
        pass

    def take_hit(self, coor: Coordinate) -> AttackResult:
        """
        Receive opponent's move. Return the results of the move.
        """
        for ship in self.ships:
            if ship.occupies(coor):
                return AttackResult(hit=True, sunk=ship.is_sunk(), ship=ship)
        return AttackResult(hit=False, sunk=False, ship=None)

    def turn_result(self, move: Coordinate, result: AttackResult):
        """
        Update internal data structures based on result of a turn
        """
        if result.sunk:
            self.guess_board.ship_sunk(result.ship)
        elif result.hit:
            self.guess_board.update(move, CellState.HIT)
        else:
            self.guess_board.update(move, CellState.MISS)

    @abstractmethod
    def output(self, msg: str):
        """
        Polymorphic output function that either prints to screen or sends
        output over network connection
        """
        pass

    @abstractmethod
    def _place_ship(self, ship: Ship) -> Coordinate:
        """
        Place a single ship, prompts human or random generation for computer
        """
        pass
