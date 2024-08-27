# Final Fantasy VIII - Triple Triad Card Game AI

## Overview

This Python program provides recommendations for the "Best Move" in the Final Fantasy VIII Card Game, given a particular game state. It uses a simple Minimax algorithm to evaluate possible moves and determine the optimal one.

## How It Works

Take a look here for my explanation on the Minimax Algorithm: https://e-loughlin.github.io/final-fantasy-viii-triple-triad-solver/

## Features

- **Game State Representation**: The game state is represented in a YAML file (`gamestate.yaml`) that specifies the 10 cards in the game, their owners, positions, and strength values.
- **Minimax Algorithm**: The program utilizes the Minimax algorithm to evaluate the game state and provide the best possible move for the current player.
- **Card Display**: The program visually represents the cards on the board and in the players' hands.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/e-loughlin/ffviii-card-game-ai.git
   cd ffviii-card-game-ai
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the program and get a move recommendation:

```bash
python main.py --gamestate <path_to_gamestate.yaml> --depth <max_tree_depth> [--debug]
```

### Arguments:

- `--gamestate <filepath>`: The file path to the `gamestate.yaml` file that defines the current game state.
- `--depth <depth>`: The maximum depth for the Minimax algorithm. This determines how many moves ahead the AI will consider. Default is 3.
- `--debug`: Enable debug mode.

### Example:

```bash
python main.py --gamestate gamestate.yaml --depth 3 --debug
```

This command will load the game state from `gamestate.yaml`, evaluate the best possible move up to a depth of 3, and enable debug mode.

## Game State File (gamestate.yaml)

The `gamestate.yaml` file should define the 10 cards in the game, their positions (either "Hand" or 1-9), and their strength values. An example structure is:

```yaml
Current_Player: P
Cards:
  1:
    symbol: A
    owner: P
    top: 1
    left: 4
    right: 3
    bottom: 2
    position: Hand
  2:
    symbol: B 
    owner: O
    top: 2
    left: 2
    right: 6
    bottom: 7
    position: 5
  ...
```

## Example of Script Usage

```txt


Player (P) Cards:
  A-P    B-P    C-P    D-P    E-P  
 | 4 |  | 6 |  | 6 |  | 3 |  | 8 | 
 |2 4|  |6 3|  |3 6|  |1 5|  |4 8| 
 | 5 |  | 1 |  | 2 |  | 2 |  | 4 | 


Opponent (O) Cards:
  V-O    W-O    X-O    Y-O    Z-O  
 | 1 |  | 6 |  | 7 |  | 3 |  | 3 | 
 |3 8|  |6 3|  |3 5|  |4 6|  |3 2| 
 | 8 |  | 1 |  | 1 |  | 4 |  | 4 | 


Board:
-------------------------------------------
Current Player: P  |  Points: P = 0, O = 0
                     
 |   |  |   |  |   | 
 |   |  |   |  |   | 
 |   |  |   |  |   | 

                     
 |   |  |   |  |   | 
 |   |  |   |  |   | 
 |   |  |   |  |   | 

                     
 |   |  |   |  |   | 
 |   |  |   |  |   | 
 |   |  |   |  |   | 


Determining best move...
* Best Move = (('A', 1), Score = 0)
Player P: Make a move:
Choose a card to place (Available = ['A', 'B', 'C', 'D', 'E'].A
Choose a position: (Available = [1, 2, 3, 4, 5, 6, 7, 8, 9])1
Player (P) Cards:
  B-P    C-P    D-P    E-P  
 | 6 |  | 6 |  | 3 |  | 8 | 
 |6 3|  |3 6|  |1 5|  |4 8| 
 | 1 |  | 2 |  | 2 |  | 4 | 


Opponent (O) Cards:
  V-O    W-O    X-O    Y-O    Z-O  
 | 1 |  | 6 |  | 7 |  | 3 |  | 3 | 
 |3 8|  |6 3|  |3 5|  |4 6|  |3 2| 
 | 8 |  | 1 |  | 1 |  | 4 |  | 4 | 


Board:
-------------------------------------------
Current Player: O  |  Points: P = 1, O = 0
                     
 |   |  |   |  |   | 
 |   |  |   |  |   | 
 |   |  |   |  |   | 

                     
 |   |  |   |  |   | 
 |   |  |   |  |   | 
 |   |  |   |  |   | 

  A-P                
 | 4 |  |   |  |   | 
 |2 4|  |   |  |   | 
 | 5 |  |   |  |   | 


Player O: Make a move:
Choose a card to place (Available = ['V', 'W', 'X', 'Y', 'Z'].W
Choose a position: (Available = [2, 3, 4, 5, 6, 7, 8, 9])2
Player (P) Cards:
  B-P    C-P    D-P    E-P  
 | 6 |  | 6 |  | 3 |  | 8 | 
 |6 3|  |3 6|  |1 5|  |4 8| 
 | 1 |  | 2 |  | 2 |  | 4 | 


Opponent (O) Cards:
  V-O    X-O    Y-O    Z-O  
 | 1 |  | 7 |  | 3 |  | 3 | 
 |3 8|  |3 5|  |4 6|  |3 2| 
 | 8 |  | 1 |  | 4 |  | 4 | 


Board:
-------------------------------------------
Current Player: P  |  Points: P = 0, O = 2
                     
 |   |  |   |  |   | 
 |   |  |   |  |   | 
 |   |  |   |  |   | 

                     
 |   |  |   |  |   | 
 |   |  |   |  |   | 
 |   |  |   |  |   | 

  A-O    W-O         
 | 4 |  | 6 |  |   | 
 |2 4|  |6 3|  |   | 
 | 5 |  | 1 |  |   | 


Determining best move...
* Best Move = (('B', 3), Score = 0)
Player P: Make a move:
Choose a card to place (Available = ['B', 'C', 'D', 'E'].B 
Choose a position: (Available = [3, 4, 5, 6, 7, 8, 9])3
Player (P) Cards:
  C-P    D-P    E-P  
 | 6 |  | 3 |  | 8 | 
 |3 6|  |1 5|  |4 8| 
 | 2 |  | 2 |  | 4 | 


Opponent (O) Cards:
  V-O    X-O    Y-O    Z-O  
 | 1 |  | 7 |  | 3 |  | 3 | 
 |3 8|  |3 5|  |4 6|  |3 2| 
 | 8 |  | 1 |  | 4 |  | 4 | 


Board:
-------------------------------------------
Current Player: O  |  Points: P = 2, O = 1
                     
 |   |  |   |  |   | 
 |   |  |   |  |   | 
 |   |  |   |  |   | 

                     
 |   |  |   |  |   | 
 |   |  |   |  |   | 
 |   |  |   |  |   | 

  A-O    W-P    B-P  
 | 4 |  | 6 |  | 6 | 
 |2 4|  |6 3|  |6 3| 
 | 5 |  | 1 |  | 1 | 


Player O: Make a move:
Choose a card to place (Available = ['V', 'X', 'Y', 'Z'].V
Choose a position: (Available = [4, 5, 6, 7, 8, 9])7
Player (P) Cards:
  C-P    D-P    E-P  
 | 6 |  | 3 |  | 8 | 
 |3 6|  |1 5|  |4 8| 
 | 2 |  | 2 |  | 4 | 


Opponent (O) Cards:
  X-O    Y-O    Z-O  
 | 7 |  | 3 |  | 3 | 
 |3 5|  |4 6|  |3 2| 
 | 1 |  | 4 |  | 4 | 


Board:
-------------------------------------------
Current Player: P  |  Points: P = 2, O = 2
  V-O                
 | 1 |  |   |  |   | 
 |3 8|  |   |  |   | 
 | 8 |  |   |  |   | 

                     
 |   |  |   |  |   | 
 |   |  |   |  |   | 
 |   |  |   |  |   | 

  A-O    W-P    B-P  
 | 4 |  | 6 |  | 6 | 
 |2 4|  |6 3|  |6 3| 
 | 5 |  | 1 |  | 1 | 


Determining best move...
* Best Move = (('C', 4), Score = 0)
Player P: Make a move:
Choose a card to place (Available = ['C', 'D', 'E'].C
Choose a position: (Available = [4, 5, 6, 8, 9])4
Player (P) Cards:
  D-P    E-P  
 | 3 |  | 8 | 
 |1 5|  |4 8| 
 | 2 |  | 4 | 


Opponent (O) Cards:
  X-O    Y-O    Z-O  
 | 7 |  | 3 |  | 3 | 
 |3 5|  |4 6|  |3 2| 
 | 1 |  | 4 |  | 4 | 


Board:
-------------------------------------------
Current Player: O  |  Points: P = 3, O = 2
  V-O                
 | 1 |  |   |  |   | 
 |3 8|  |   |  |   | 
 | 8 |  |   |  |   | 

  C-P                
 | 6 |  |   |  |   | 
 |3 6|  |   |  |   | 
 | 2 |  |   |  |   | 

  A-O    W-P    B-P  
 | 4 |  | 6 |  | 6 | 
 |2 4|  |6 3|  |6 3| 
 | 5 |  | 1 |  | 1 | 


Player O: Make a move:
Choose a card to place (Available = ['X', 'Y', 'Z'].X
Choose a position: (Available = [5, 6, 8, 9])5
Player (P) Cards:
  D-P    E-P  
 | 3 |  | 8 | 
 |1 5|  |4 8| 
 | 2 |  | 4 | 


Opponent (O) Cards:
  Y-O    Z-O  
 | 3 |  | 3 | 
 |4 6|  |3 2| 
 | 4 |  | 4 | 


Board:
-------------------------------------------
Current Player: P  |  Points: P = 3, O = 3
  V-O                
 | 1 |  |   |  |   | 
 |3 8|  |   |  |   | 
 | 8 |  |   |  |   | 

  C-P    X-O         
 | 6 |  | 7 |  |   | 
 |3 6|  |3 5|  |   | 
 | 2 |  | 1 |  |   | 

  A-O    W-P    B-P  
 | 4 |  | 6 |  | 6 | 
 |2 4|  |6 3|  |6 3| 
 | 5 |  | 1 |  | 1 | 


Determining best move...
* Best Move = (('D', 6), Score = 0)
Player P: Make a move:
Choose a card to place (Available = ['D', 'E'].D
Choose a position: (Available = [6, 8, 9])6
Player (P) Cards:
  E-P  
 | 8 | 
 |4 8| 
 | 4 | 


Opponent (O) Cards:
  Y-O    Z-O  
 | 3 |  | 3 | 
 |4 6|  |3 2| 
 | 4 |  | 4 | 


Board:
-------------------------------------------
Current Player: O  |  Points: P = 4, O = 3
  V-O                
 | 1 |  |   |  |   | 
 |3 8|  |   |  |   | 
 | 8 |  |   |  |   | 

  C-P    X-O    D-P  
 | 6 |  | 7 |  | 3 | 
 |3 6|  |3 5|  |1 5| 
 | 2 |  | 1 |  | 2 | 

  A-O    W-P    B-P  
 | 4 |  | 6 |  | 6 | 
 |2 4|  |6 3|  |6 3| 
 | 5 |  | 1 |  | 1 | 


Player O: Make a move:
Choose a card to place (Available = ['Y', 'Z'].Y
Choose a position: (Available = [8, 9])8
Player (P) Cards:
  E-P  
 | 8 | 
 |4 8| 
 | 4 | 


Opponent (O) Cards:
  Z-O  
 | 3 | 
 |3 2| 
 | 4 | 


Board:
-------------------------------------------
Current Player: P  |  Points: P = 4, O = 4
  V-O    Y-O         
 | 1 |  | 3 |  |   | 
 |3 8|  |4 6|  |   | 
 | 8 |  | 4 |  |   | 

  C-P    X-O    D-P  
 | 6 |  | 7 |  | 3 | 
 |3 6|  |3 5|  |1 5| 
 | 2 |  | 1 |  | 2 | 

  A-O    W-P    B-P  
 | 4 |  | 6 |  | 6 | 
 |2 4|  |6 3|  |6 3| 
 | 5 |  | 1 |  | 1 | 


Determining best move...
* Best Move = (('E', 9), Score = 0)
Player P: Make a move:
Choose a card to place (Available = ['E'].E
Choose a position: (Available = [9])9
Player (P) Cards:






Opponent (O) Cards:
  Z-O  
 | 3 | 
 |3 2| 
 | 4 | 


Board:
-------------------------------------------
Current Player: O  |  Points: P = 5, O = 4
  V-O    Y-O    E-P  
 | 1 |  | 3 |  | 8 | 
 |3 8|  |4 6|  |4 8| 
 | 8 |  | 4 |  | 4 | 

  C-P    X-O    D-P  
 | 6 |  | 7 |  | 3 | 
 |3 6|  |3 5|  |1 5| 
 | 2 |  | 1 |  | 2 | 

  A-O    W-P    B-P  
 | 4 |  | 6 |  | 6 | 
 |2 4|  |6 3|  |6 3| 
 | 5 |  | 1 |  | 1 | 


Winner is P. Final score: {'P': 5, 'O': 4}

```
## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
