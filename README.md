# 2048 Game Project

Recently, I play games like 2048 on my phone, and I'm curious about how they work. In this project, I've implemented the game logic and AI algorithm from scratch.

However, the genertated grid only can be 2 or 4 in a tile while in my game, it can be 8 or 16 in a tile. Since the rate of 8 
This project is an implementation of the 2048 game with additional features such as exponential display and a Tkinter-based visual interface.

## Files

- **game.py**: Contains the core logic of the 2048 game, including tile merging and score calculation. The game algorithm evaluates the next three possible moves and selects the one with the highest score.

- **config.py**: Defines various configuration parameters for the game, including time-related parameters and color settings for display.

- **2048.py**: The original project file that can determine the next move based on a given 4x4 grid.

- **2048exp.py**: Displays the game using exponential notation. For example, the number 64 is displayed as 6, representing 2^6.

- **2048exp_2.0.py**: Uses the Tkinter library for a convenient graphical display and visual operations.

## Game Algorithm

The game's AI evaluates the next three possible moves and chooses the move with the highest score based on a scoring mechanism. The primary steps involved are:

1. **Tile Evaluation**: For each possible move direction ("U", "L", "R", "D"), the algorithm evaluates the resulting grid state after simulating the move.
2. **Score Calculation**: The AI calculates a score for each resulting grid state using a custom scoring function that takes into account the alignment and proximity of tiles.
3. **Best Move Selection**: The move that results in the highest minimum score across multiple random tile additions is selected as the best move.

### Scoring Mechanism

The scoring mechanism is based on the alignment and proximity of tiles. The AI has several helper functions to evaluate the score:

- **get_score(tiles)**: Calculates the score of a given grid state by evaluating tile alignment and proximity.
- **get_bj2__2(tiles), get_bj2__3(tiles), get_bj2__4(tiles)**: Helper functions that calculate a penalty based on the difference in values between adjacent tiles. These penalties are subtracted from the score to discourage configurations with large discrepancies between adjacent tiles.

### Example of AI Decision

Here is an example of how the AI makes a decision:

```python
initial_state_powers = np.array([
    [2, 0, 0, 1],
    [0, 1, 3, 1],
    [2, 5, 3, 10],
    [4, 6, 5, 4]
])

# Convert to actual tile values
initial_state = np.where(initial_state_powers == 0, 0, 2 ** initial_state_powers)

game = Game(4)
game.grid.tiles = initial_state
ai = Ai()
print("Initial state:")
printf(game.grid.tiles)

move, _ = ai.get_next(game.grid.tiles)
print(f"AI recommended move: {move}")

game.run(move)
print("State after move:")
printf(game.grid.tiles)
```

## Usage

1. **Running the game**: To run the 2048 game with AI, use the provided scripts. For example, to see the AI's recommended move and the resulting state, you can run the main block in `2048exp.py`.

2. **Configuration**: Adjust parameters in `config.py` to change time settings and display colors as needed.

3. **Visualization**: Use `2048exp_2.0.py` to launch a Tkinter-based graphical interface for easier interaction with the game.

Feel free to explore and modify the code to enhance the functionality or adjust the AI's decision-making process.
