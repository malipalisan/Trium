from typing import List, Tuple
from .constants import *
from .enums import RuleType

class Player:
    """Handles player movement and interactions with special tiles"""
    
    def __init__(self):
        self.position = [0, 0]
        self.color = BLUE
    
    def reset(self):
        """Reset player to starting position"""
        self.position = [0, 0]
        self.color = BLUE
    
    def move(self, dx: int, dy: int, game_state) -> bool:
        """Move the player and handle special tile interactions"""
        # Check for movement restrictions
        if game_state.no_left_movement and dx < 0:
            return False
        
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        
        # Check bounds
        if new_x < 0 or new_x >= TILE_WIDTH or new_y < 0 or new_y >= TILE_HEIGHT:
            return False
        
        # Check walls
        if game_state.grid[new_y][new_x] == TILE_WALL:
            return False
        
        # Check red tiles (if player steps on red tile, level restarts)
        if game_state.grid[new_y][new_x] == TILE_RED:
            game_state.reset_level()
            self.reset()
            return False
        
        # Move player
        self.position = [new_x, new_y]
        game_state.update_player_position(self.position)
        game_state.increment_moves()
        
        # Handle special tiles
        tile_type = game_state.grid[new_y][new_x]
        
        if tile_type == TILE_TELEPORTER:
            self._handle_teleporter(game_state)
        elif tile_type == TILE_SPEED_BOOST:
            self._handle_speed_boost(dx, dy, game_state)
        
        return True
    
    def _handle_teleporter(self, game_state):
        """Handle teleporter mechanics"""
        current_pos = self.position.copy()
        for pair in game_state.teleporters:
            if current_pos == pair[0]:
                self.position = pair[1].copy()
                game_state.update_player_position(self.position)
                break
            elif current_pos == pair[1]:
                self.position = pair[0].copy()
                game_state.update_player_position(self.position)
                break
    
    def _handle_speed_boost(self, dx: int, dy: int, game_state):
        """Handle speed boost mechanics"""
        if dx != 0 or dy != 0:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            
            if (0 <= new_x < TILE_WIDTH and 0 <= new_y < TILE_HEIGHT and 
                game_state.grid[new_y][new_x] != TILE_WALL and
                game_state.grid[new_y][new_x] != TILE_RED):
                self.position = [new_x, new_y]
                game_state.update_player_position(self.position)
                game_state.increment_moves()
    
    def get_position(self) -> List[int]:
        """Get current player position"""
        return self.position.copy()
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get current player color"""

        return self.color 
