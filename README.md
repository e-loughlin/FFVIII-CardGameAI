# Final Fantasy VIII - Triple Triad Card Game AI

## Overview

This Python program provides recommendations for the "Best Move" in the Final Fantasy VIII Card Game, given a particular game state. It uses a simple Minimax algorithm to evaluate possible moves and determine the optimal one.

## Features

- **Game State Representation**: The game state is represented in a YAML file (`gamestate.yaml`) that specifies the 10 cards in the game, their owners, positions, and strength values.
- **Minimax Algorithm**: The program utilizes the Minimax algorithm to evaluate the game state and provide the best possible move for the current player.
- **Card Display**: The program visually represents the cards on the board and in the players' hands.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ffviii-card-game-ai.git
   cd ffviii-card-game-ai
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the program and get a move recommendation:

```bash
python main.py -f <path_to_gamestate.yaml> -d <max_tree_depth> -s <starting_player>
```

### Arguments:

- `-f <filepath>`: The file path to the `gamestate.yaml` file that defines the current game state.
- `-d <depth>`: The maximum depth for the Minimax algorithm. This determines how many moves ahead the AI will consider.
- `-s <starting_player>`: The player who is starting the game. Use `'P'` for Player or `'O'` for Opponent.

### Example:

```bash
python main.py -f gamestate.yaml -d 3 -s P
```

This command will load the game state from `gamestate.yaml`, evaluate the best possible move up to a depth of 3, and assume that the Player is starting.

## Game State File (gamestate.yaml)

The `gamestate.yaml` file should define the 10 cards in the game, their positions (either "Hand" or 1-9), and their strength values. An example structure is:

```yaml
Current_Player: P
Cards:
  1:
    symbol: Cactuar
    owner: P
    top: 1
    left: 4
    right: 3
    bottom: 2
    position: Hand
  2:
    symbol: Tonberry
    owner: O
    top: 2
    left: 2
    right: 6
    bottom: 7
    position: 5
  ...
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
