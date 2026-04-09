from Displayer import Displayer
from Player import Player
from Ship import AttackResult, AircraftCarrier, Battleship, Cruiser, Destroyer, Submarine, Ship
from util import BOARD_SIZE, CellState, Coordinate, Difficulty, Orientation, MAX_SHIP_SIZE, Modes
import random

"""
ComputerPlayer: A class that contains the logic to play Battleship on 
    various difficulty levels:
        EASY    - Completely random guessing
        Medium  - Random guessing until hit, then search nearby

Strategy Source: http://www.datagenetics.com/blog/december32011/
"""
class ComputerPlayer(Player):
    def __init__(self, difficulty: Difficulty, name: str = "Hal"):
        super().__init__(name=name)
        self.difficulty = difficulty
        self.mode       = Modes.HUNT
        self.targets    = list()
        self.hit_ships  = set() # We might hit a second ship while in TARGET mode
        self.prob_map   = dict()
        self._init_prob_map()

    def _place_ship(self, ship: Ship) -> Ship:
        """
        Place a ship in a random location.
        """
        while True:
            coor = Coordinate(
                    random.randint(0, BOARD_SIZE - 1),
                    random.randint(0, BOARD_SIZE - 1)
                    )
            orient = random.choice(
                    [Orientation.VERTICAL, Orientation.HORIZONTAL]
                    )
            if ship.place(self.ships, orient, coor):
                break
        return ship

    def take_turn(self) -> Coordinate:
        match self.difficulty:
            case Difficulty.EASY:
                return self._easy_guess()
            case Difficulty.MEDIUM:
                return self._med_guess()
            case Difficulty.HARD:
                return self._hard_guess()

    def turn_result(self, move: Coordinate, rslt: AttackResult):
        super().turn_result(move, rslt)
        match self.difficulty:
            case Difficulty.EASY:
                # Always random guessing so no need to track results
                return
            case Difficulty.MEDIUM:
                self._turn_result_med(move, rslt)
                return
            case Difficulty.HARD:
                self._turn_result_hard(move, rslt)
                return

    def _turn_result_med(self, move: Coordinate, rslt: AttackResult):
        if not rslt.hit:
            return
        if rslt.sunk:
            if rslt.ship in self.hit_ships:
                self.hit_ships.remove(rslt.ship)
            # If we hit multiple ships while in TARGET mode
            # Don't clear targets and switch to HUNT yet
            if len(self.hit_ships) > 0:
                return 
            self.targets.clear()
            self.mode = Modes.HUNT
            return
        else: # move was a hit, and the ship isn't sunk yet
            self.mode = Modes.TARGET
            self.hit_ships.add(rslt.ship)
            new_targets = [
                    Coordinate(i, j)
                    for i in range(move.row - 1, move.row + 2)
                    for j in range(move.col - 1, move.col + 2)
                    if 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE
                    ]
            for t in new_targets:
                # Check unguessed first since its O(1)
                if t in self.unguessed and t not in self.targets:
                    self.targets.append(t)

    def _turn_result_hard(self, move: Coordinate, rslt: AttackResult):
        for i in range(MAX_SHIP_SIZE):
            self._update_prob_map(Coordinate(col=move.row+1, row=move.col), rslt)
            if i == 0:
                continue # don't do the same thing 4 times
            self._update_prob_map(Coordinate(col=move.row-1, row=move.col), rslt)
            self._update_prob_map(Coordinate(col=move.row, row=move.col+1), rslt)
            self._update_prob_map(Coordinate(col=move.row, row=move.col-1), rslt)
        self._turn_result_med(move, rslt)

    def _update_prob_map(self, cell: Coordinate, rslt: AttackResult):
        num_ships = 0
        if self.guess_board.ship_can_occupy(Carrier(), cell):
            num_ships += 1
        if self.guess_board.ship_can_occupy(Battleship(), cell):
            num_ships += 1
        if self.guess_board.ship_can_occupy(Submarine(), cell):
            num_ships += 2 # Destroyer is same size
        if self.guess_board.ship_can_occupy(PatrolBoat(), cell):
            num_ships += 1
        self.prob_map[cell] = num_ships


    def _easy_guess(self) -> Coordinate:
        return self.unguessed.random()

    def _med_guess(self) -> Coordinate:
        if self.mode == Modes.TARGET and len(self.targets) > 0:
            return self.targets.pop() 
        # If self.mode == Modes.TARGET but self.targets is empty
        # Go back to HUNT mode, else we are already in HUNT mode
        self.mode = Modes.HUNT
        return self._easy_guess()

    def _hard_guess(self) -> Coordinate:
        if self.mode == Modes.HUNT:
            max_prob  = max(self.prob_map.values())
            max_cells = [k for k, v in self.prob_map.items() if v == max_prob]
            cell = random.choice(max_cells)
            while cell not in self.unguessed:
                cell = random.choice(max_cells)
            return cell
        else:
            return self._med_guess()

    def _init_prob_map(self):
        if self.difficulty != Difficulty.HARD:
            return
        coords = [Coordinate(x, y)
               for x in range(BOARD_SIZE)
               for y in range(BOARD_SIZE)]
        for c in coords:
            self.prob_map[c] = MAX_SHIP_SIZE
