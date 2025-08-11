import pygame
from typing import Tuple, Optional
from .constants import *

class Sprite:
    """Base sprite class for all game objects"""
    
    def __init__(self, x: int, y: int, sprite_type: str, color: Tuple[int, int, int], size: int = TILE_SIZE):
        self.x = x
        self.y = y
        self.sprite_type = sprite_type
        self.color = color
        self.size = size
        self.rect = pygame.Rect(x * TILE_SIZE + GRID_X, y * TILE_SIZE + GRID_Y, size, size)
    
    def draw(self, screen: pygame.Surface):
        """Draw the sprite on the screen"""
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)
    
    def get_position(self) -> Tuple[int, int]:
        """Get the grid position of the sprite"""
        return (self.x, self.y)
    
    def set_position(self, x: int, y: int):
        """Set the grid position of the sprite"""
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x * TILE_SIZE + GRID_X, y * TILE_SIZE + GRID_Y, self.size, self.size)
    
    def get_type(self) -> str:
        """Get the sprite type"""
        return self.sprite_type 