# Trium

A grid-based puzzle game built with Pygame where you navigate from the top-left corner to a random exit door, with different rules changing every level.


## Game Rules 

The game has 12 levels that the player must beat in order to successfully finish the game.
For each level, there are two constant rules:
1. Stepping on red tile restarts the level
2. Player has a maximum of 100 moves to finish the level

Third rule for each level is randomly chosen from pool of different rules.


## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. **Controls:**
   - **WASD** or **Arrow Keys**: Move the character
   - **R**: Restart current level
   - **ESC**: Quit game

3. **Objective:**
   - Move your character (colored square) from the top-left corner to the brown door
   - Complete each level within the move limit (100 moves)
   

4. **Game Elements:**
   - **Blue Square**: Your character
   - **Brown Door**: Exit/Goal
   - **Purple**: Teleporters
   - **Red**: Fail the level 
   - **Gray**: Walls (block movement)
   - **Orange**: Speed boosts

