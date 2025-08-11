import pygame
from .constants import *

class InputHandler:
    """Handles keyboard input and player controls"""
    
    def __init__(self):
        self.keys = {
            'left': [pygame.K_LEFT, pygame.K_a],
            'right': [pygame.K_RIGHT, pygame.K_d],
            'up': [pygame.K_UP, pygame.K_w],
            'down': [pygame.K_DOWN, pygame.K_s],
            'restart': pygame.K_r,
            'quit': pygame.K_ESCAPE
        }
    
    def get_movement(self, reverse_controls: bool = False, no_left_movement: bool = False) -> tuple[int, int]:
        """Get movement direction from keyboard input"""
        keys_pressed = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        # Handle left/right movement
        if any(keys_pressed[key] for key in self.keys['left']) and not no_left_movement:
            dx = -1 if not reverse_controls else 1
        elif any(keys_pressed[key] for key in self.keys['right']):
            dx = 1 if not reverse_controls else -1
        
        # Handle up/down movement
        if any(keys_pressed[key] for key in self.keys['up']):
            dy = -1 if not reverse_controls else 1
        elif any(keys_pressed[key] for key in self.keys['down']):
            dy = 1 if not reverse_controls else -1
        
        return dx, dy
    
    def get_single_movement(self, events, reverse_controls: bool = False, no_left_movement: bool = False) -> tuple[int, int]:
        """Get movement direction from single key press events"""
        dx, dy = 0, 0
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.keys['left'] and not no_left_movement:
                    dx = -1 if not reverse_controls else 1
                elif event.key in self.keys['right']:
                    dx = 1 if not reverse_controls else -1
                elif event.key in self.keys['up']:
                    dy = -1 if not reverse_controls else 1
                elif event.key in self.keys['down']:
                    dy = 1 if not reverse_controls else -1
        
        return dx, dy
    
    def handle_events(self, events) -> dict:
        """Handle pygame events and return action dictionary"""
        actions = {
            'restart': False,
            'quit': False
        }
        
        for event in events:
            if event.type == pygame.QUIT:
                actions['quit'] = True
            elif event.type == pygame.KEYDOWN:
                if event.key == self.keys['restart']:
                    actions['restart'] = True
                elif event.key == self.keys['quit']:
                    actions['quit'] = True
        
        return actions 