#!/usr/bin/env python3
"""
Puzzle Game - Main Entry Point

A grid-based puzzle game where you navigate from the top-left corner 
to a random exit door, with different rules changing every level.
"""

from src.game import PuzzleGame

def main():
    """Main entry point for the puzzle game"""
    try:
        game = PuzzleGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":

    main() 
