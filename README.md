# Battleship

A command-line Battleship game written in Python, supporting single-player, multiplayer (over network), and simulation modes. No external dependencies — just Python 3.10+.

---

## Features

- **Single-player** — play against a computer opponent at Easy, Medium, or Hard difficulty
- **Multiplayer** — play against another human over a TCP connection, with one player hosting as the server and the other joining as the client
- **Simulation** — two computer players face off; useful for testing AI strategies
- **Three AI difficulty levels** — Easy (random), Medium (hunt/target), Hard (probability-density map)
- **AI Strategy Source** - http://www.datagenetics.com/blog/december32011/

---

## Requirements

- Python 3.10 or later
- No third-party packages required

---

## Running the Game

Make sure `Battleship.py` is executable, then run it directly:

```bash
chmod +x Battleship.py   # first time only
./Battleship.py [options]
```

Or invoke it with the interpreter explicitly:

```bash
python3 Battleship.py [options]
```

### Options

| Flag | Long form | Description |
|------|-----------|-------------|
| `-d` | `--default` | Single-player mode (human vs. computer) |
| `-s` | `--server` | Multiplayer — host a game |
| `-c` | `--client` | Multiplayer — join a hosted game |
| `-m` | `--simulation` | Simulation mode (computer vs. computer) |
| `-p PORT` | `--port PORT` | Port number to use (multiplayer) |
| `-i IP` | `--ip IP` | Server IP address to connect to (client mode) |
| `-h` | `--help` | Show usage message |

---

## Game Modes

### Single-player

Play against the computer. You will be prompted to choose a difficulty level (Easy, Medium, or Hard) and to place your ships before the game begins.

```bash
./Battleship.py -d  # explicitly pass default flag
# Or
./Battleship.py     # pass no flag
```

### Multiplayer

One player hosts as the server and the other connects as the client. Both players place their ships locally, then take turns guessing over the network. The server player goes first.

**On the hosting machine:**
```bash
./Battleship.py -s -p 6000
```

**On the joining machine:**
```bash
./Battleship.py -c -p 6000 -i 192.168.1.42
```

Replace `192.168.1.42` with the server's IP address (or just localhost).

To find your local IP address:
- **macOS / Linux:** `ifconfig` or `ip addr`
- **Windows:** `ipconfig`

### Simulation

Two computer players compete automatically. Useful for testing AI behaviour and comparing AI strategies.

```bash
./Battleship.py -m eh # Easy mode AI vs. Hard mode AI
./Battleship.py -m mm # Medium mode AI vs. Medium mode AI
```

---

## Ships

The fleet consists of seven ships (2x Destroyer & 2x Submarine):

| Ship | Size |
|------|------|
| Aircraft Carrier | 5 |
| Battleship | 4 |
| Cruiser | 3 |
| Destroyer | 2 |
| Submarine | 1 |

---

## How to Play

At the start of each game, you will be prompted to place each of your ships on a 10×10 grid. Rows are labeled A–J and columns are labeled 1–10.

During your turn, enter a coordinate to fire at (e.g. `B4`). The board will update after each shot:

| Symbol | Meaning |
|--------|---------|
| `S` | Sunk |
| `X` | Hit |
| `·` | Miss |
| ` ` | Unknown |

Both your board (showing incoming hits) and your opponent's board (showing your guesses) are displayed side by side each turn. Your ship status is shown below the boards, with `█` for healthy cells and `X` for hit cells.

A player wins when all five of their opponent's ships are sunk.

---

## AI Difficulty

**Easy** — fires at a random unguessed cell each turn.

**Medium** — fires randomly until a ship is hit, then switches to targeting adjacent cells until the ship is sunk (hunt/target strategy).

**Hard** — maintains a probability density map across all remaining possible ship placements and always fires at the highest-probability cell.

---

## Project Structure

```
Battleship.py        Entry point and argument parsing
GameManager.py       Main game loop
Player.py            Abstract Player base class
HumanPlayer.py       Human player (terminal input) and ClientPlayer (networked)
ComputerPlayer.py    AI player with Easy / Medium / Hard strategies
Board.py             Grid state and attack logic
Ship.py              Ship base class and derived ship types
Displayer.py         Terminal rendering (boards and ship status)
Server.py            Multiplayer server setup and connection handling
Client.py            Multiplayer client setup and connection handling
util.py              Shared data classes, enums, and constants
```
