import pygame
import sys
from .constants import *
from .game_state import GameState
from .player import Player
from .input_handler import InputHandler
from .renderer import Renderer

class PuzzleGame:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Trium")
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.game_state = GameState()
        self.player = Player()
        self.input_handler = InputHandler()
        self.renderer = Renderer(self.screen)
        
        # Generate first level
        self.game_state.generate_level()
        self.player.reset()
    
    def run(self):
        running = True
        
        while running:
            # Handle events
            events = pygame.event.get()
            actions = self.input_handler.handle_events(events)
            
            if actions['quit']:
                running = False
            elif actions['restart']:
                self._restart_level()
            
            # Handle input and movement
            self._handle_movement(events)
            
            # Check game state
            self._check_game_state()
            
            # Render the game
            self.renderer.render(self.game_state, self.player)
            
            # Control frame rate
            self.clock.tick(FPS)
        
        self._cleanup()
    
    def _handle_movement(self, events):
        """Handle player movement based on input"""
        dx, dy = self.input_handler.get_single_movement(
            events, 
            self.game_state.reverse_controls,
            self.game_state.no_left_movement
        )
        
        if dx != 0 or dy != 0:
            self.player.move(dx, dy, self.game_state)
    
    def _check_game_state(self):
        """Check for win/lose conditions"""
        if self.game_state.is_level_complete():
            self._next_level()
        elif self.game_state.is_game_over():
            self._game_over()
    
    def _next_level(self):
        """Advance to next level"""
        if self.game_state.level < MAX_LEVELS:
            self.game_state.next_level()
            self.player.reset()
        else:
            print("Congratulations! You've completed all levels!")
            self._cleanup()
            sys.exit()
    
    def _restart_level(self):
        """Restart current level"""
        self.game_state.reset_level()
        self.player.reset()
    
    def _game_over(self):
        """Handle game over"""
        print(f"Game Over! You reached level {self.game_state.level}")
        self._cleanup()
        sys.exit()
    
    def _cleanup(self):
        """Clean up pygame resources"""
        pygame.quit()

        sys.exit() 
