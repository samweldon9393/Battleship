from Displayer import Displayer
from Player import Player
from Ship import AttackResult, AircraftCarrier, Battleship, Cruiser, Destroyer, Submarine, Ship
from util import BOARD_SIZE, CellState, Coordinate, Difficulty, MAX_SHIP_SIZE, Modes, Orientation, Unguessed, TOTAL_SHIPS

import random

"""
ComputerPlayer: A class that contains the logic to play Battleship on 
    various difficulty levels:
        EASY    - Completely random guessing
        Medium  - Random guessing until hit, then search nearby
        Hard    - Guess based on probability-density map until hit,
                    then search nearby

Strategy Source: http://www.datagenetics.com/blog/december32011/
"""
class ComputerPlayer(Player):
    def __init__(self, difficulty: Difficulty, name: str = "Hal"):
        super().__init__(name=name)
        self.difficulty = difficulty

        # Medium Difficulty additions
        self.mode       = Modes.HUNT
        self.targets    = list()
        self.hit_ships  = set() # We might hit a second ship while in TARGET mode

        # Hard Difficulty additions
        self.sunk_ships = set() # Keep track for prob_map
        self.prob_map   = self._init_prob_map()

    def take_turn(self) -> Coordinate:
        move = None
        match self.difficulty:
            case Difficulty.EASY:
                move = self._easy_guess()
            case Difficulty.MEDIUM:
                move = self._med_guess()
            case Difficulty.HARD:
                move = self._hard_guess()
        self.unguessed.remove(move)
        return move

    def turn_result(self, move: Coordinate, result: AttackResult):
        super().turn_result(move, result)
        match self.difficulty:
            case Difficulty.EASY:
                # Always random guessing so no need to track results
                return
            case Difficulty.MEDIUM:
                self._turn_result_med(move, result)
                return
            case Difficulty.HARD:
                self._turn_result_hard(move, result)
                return

    def _turn_result_med(self, move: Coordinate, result: AttackResult):
        """
        Update targets stack and current mode based on a turn result
        """
        if not result.hit:
            return
        if result.sunk:
            if result.ship in self.hit_ships:
                self.hit_ships.remove(result.ship)
                self.sunk_ships.add(result.ship)
            # If we hit multiple ships while in TARGET mode
            # Don't clear targets and switch to HUNT yet
            if len(self.hit_ships) > 0:
                return 
            self.targets.clear()
            self.mode = Modes.HUNT
            return
        else: # move was a hit, and the ship isn't sunk yet
            self.mode = Modes.TARGET
            self.hit_ships.add(result.ship)
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

    def _turn_result_hard(self, move: Coordinate, result: AttackResult):
        """
        Update probability map, target stack, and mode based on a turn result
        """
        for i in range(MAX_SHIP_SIZE):
            self._update_prob_map(Coordinate(col=move.row+i, row=move.col))
            if i == 0:
                continue # don't do the same thing 4 times
            self._update_prob_map(Coordinate(col=move.row-i, row=move.col))
            self._update_prob_map(Coordinate(col=move.row, row=move.col+i))
            self._update_prob_map(Coordinate(col=move.row, row=move.col-i))
        self._turn_result_med(move, result)

    def _update_prob_map(self, cell: Coordinate):
        if not cell.is_valid():
            return
        ships = [
                AircraftCarrier(),
                Battleship(),
                Cruiser(),
                Destroyer(),
                Destroyer(1),
                Submarine(),
                Submarine(1)
                ]
        for ship in ships:
            if (ship in self.sunk_ships 
                    or not self.guess_board.ship_can_occupy(ship, cell)):
                ships.remove(ship)
        self.prob_map[cell] = len(ships)

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
                # If there's no intersection between max_cells and unguessed
                if len(set(max_cells) & self.unguessed._set) == 0:
                    # Go down to the next highest probability-density
                    max_prob -= 1
                    if max_prob == 0:
                        # This should be unreachable
                        return self.unguessed.random()
                    max_cells = [k for k, v in self.prob_map.items() if v == max_prob]
                cell = random.choice(max_cells)
            return cell
        else:
            return self._med_guess()

    def _init_prob_map(self):
        """
        Initialize a dict of {Coordinate : Prossible Ships} where Prossible Ships is 
            the number of ships that can occupy a given cell
        """
        if self.difficulty != Difficulty.HARD:
            return None
        prob_map = dict()
        coords = [
                Coordinate(x, y)
                for x in range(BOARD_SIZE)
                for y in range(BOARD_SIZE)
                ]
        for c in coords:
            prob_map[c] = TOTAL_SHIPS
        return prob_map

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

