import random
from typing import List, Tuple
from .constants import *
from .enums import RuleType

class LevelGenerator:
    """Handles level generation and special tile placement"""
    
    def __init__(self):
        self.grid = []
        self.teleporters = []
        self.speed_boosts = []
        self.red_tiles = []
        self.walls = []
        
    def generate_level(self, level: int, player_pos: List[int], door_pos: List[int] = None) -> dict:
        """Generate a new level with the current rules"""
        self._reset_level()
        self._create_empty_grid()
        
        # Apply the 3rd rule based on level (randomly chosen from pool)
        current_rule = self._get_rule_for_level(level)
        
        # Add all required tiles (ignore door_pos for now since we'll find it later)
        self._add_walls(player_pos)
        self._add_teleporters(player_pos)
        self._add_speed_boosts(player_pos)
        self._add_red_tiles(player_pos)
        
        return {
            'grid': self.grid,
            'teleporters': self.teleporters,
            'speed_boosts': self.speed_boosts,
            'red_tiles': self.red_tiles,
            'walls': self.walls,
            'current_rule': current_rule
        }
    
    def _reset_level(self):
        """Reset all level data"""
        self.grid = []
        self.teleporters = []
        self.speed_boosts = []
        self.red_tiles = []
        self.walls = []
    
    def _create_empty_grid(self):
        """Create an empty grid"""
        self.grid = [[TILE_EMPTY for _ in range(TILE_WIDTH)] for _ in range(TILE_HEIGHT)]
    
    def _get_rule_for_level(self, level: int) -> RuleType:
        """Get the 3rd rule for the current level (randomly chosen from pool)"""
        rules = [
            RuleType.INVERTED_CONTROLS,
            RuleType.NO_LEFT_MOVEMENT,
            RuleType.DOOR_CHANGES_POSITION,
            RuleType.TILES_TURN_RED
        ]
        # Use level number as seed for consistent rule per level
        random.seed(level)
        return random.choice(rules)
    
    def _add_walls(self, player_pos: List[int]):
        """Add walls that block movement (10-15 tiles max)"""
        num_walls = random.randint(MIN_WALLS, MAX_WALLS)
        for _ in range(num_walls):
            x, y = random.randint(0, TILE_WIDTH-1), random.randint(0, TILE_HEIGHT-1)
            if [x, y] != player_pos and self.grid[y][x] == TILE_EMPTY:
                self.walls.append([x, y])
                self.grid[y][x] = TILE_WALL
    
    def _add_teleporters(self, player_pos: List[int]):
        """Add teleporter pairs (4-8 tiles max, must be even number)"""
        num_teleporters = random.randint(MIN_TELEPORTERS, MAX_TELEPORTERS)
        # Ensure even number
        if num_teleporters % 2 != 0:
            num_teleporters -= 1
        
        num_pairs = num_teleporters // 2
        for _ in range(num_pairs):
            # Find first teleporter position
            while True:
                x1, y1 = random.randint(0, TILE_WIDTH-1), random.randint(0, TILE_HEIGHT-1)
                if [x1, y1] != player_pos and self.grid[y1][x1] == TILE_EMPTY:
                    break
            
            # Find second teleporter position
            while True:
                x2, y2 = random.randint(0, TILE_WIDTH-1), random.randint(0, TILE_HEIGHT-1)
                if [x2, y2] != player_pos and [x2, y2] != [x1, y1] and self.grid[y2][x2] == TILE_EMPTY:
                    break
            
            self.teleporters.append([[x1, y1], [x2, y2]])
            self.grid[y1][x1] = TILE_TELEPORTER
            self.grid[y2][x2] = TILE_TELEPORTER
    
    def _add_speed_boosts(self, player_pos: List[int]):
        """Add speed boost tiles (5-7 tiles max)"""
        num_boosts = random.randint(MIN_SPEED_BOOSTS, MAX_SPEED_BOOSTS)
        for _ in range(num_boosts):
            x, y = random.randint(0, TILE_WIDTH-1), random.randint(0, TILE_HEIGHT-1)
            if [x, y] != player_pos and self.grid[y][x] == TILE_EMPTY:
                self.speed_boosts.append([x, y])
                self.grid[y][x] = TILE_SPEED_BOOST
    
    def _add_red_tiles(self, player_pos: List[int]):
        """Add red tiles (10-15 tiles max)"""
        num_red = random.randint(MIN_RED_TILES, MAX_RED_TILES)
        for _ in range(num_red):
            x, y = random.randint(0, TILE_WIDTH-1), random.randint(0, TILE_HEIGHT-1)
            if [x, y] != player_pos and self.grid[y][x] == TILE_EMPTY:
                self.red_tiles.append([x, y])
                self.grid[y][x] = TILE_RED 