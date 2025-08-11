import random
from typing import List, Dict
from .constants import *
from .enums import RuleType
from .level_generator import LevelGenerator
from .level_loader import LevelLoader
from .sprite import Sprite

class GameState:
    """Manages the current game state and level progression"""
    
    def __init__(self):
        self.level = 1
        self.player_pos = [0, 0]
        self.door_pos = [0, 0]
        self.grid = []
        self.sprites = {}  # Dictionary to store all sprites
        self.current_rule = None
        self.teleporters = []
        self.speed_boosts = []
        self.red_tiles = []
        self.walls = []
        self.reverse_controls = False
        self.no_left_movement = False
        self.door_changes_position = False
        self.tiles_turn_red = False
        self.moves = 0
        self.max_moves = MAX_MOVES
        self.level_generator = LevelGenerator()
        self.level_loader = LevelLoader()
        self.stepped_tiles = set()  # Track tiles player has stepped on
        self.door_move_counter = 0  # Counter for door position changes
        
    def generate_level(self):
        """Generate a new level with the current rules"""
        # Try to load level from file first
        level_data = self.level_loader.load_level_from_file(self.level)

        
        if level_data:
            # Load level from file
            self._load_level_from_data(level_data)
        else:
            # Generate level procedurally
            self._generate_procedural_level()
        
        # Create sprites for all tiles
        self._create_sprites()
    
    def _load_level_from_data(self, level_data: Dict):
        """Load level from level data"""
        self.grid = level_data['grid']
        self.teleporters = level_data['teleporters']
        self.speed_boosts = level_data['speed_boosts']
        self.red_tiles = level_data['red_tiles']
        self.walls = level_data['walls']
        self.player_pos = level_data['player_pos']
        self.door_pos = level_data['door_pos']
        
        # Set the 3rd rule randomly for this level
        self.current_rule = self._get_rule_for_level(self.level)
        self._set_rule_flags()
        
        self.moves = 0
        self.stepped_tiles = set()
        self.door_move_counter = 0
    
    def _generate_procedural_level(self):
        """Generate level procedurally"""
        # Set player position (top-left)
        self.player_pos = [0, 0]
        
        # Generate level data first (this will create the grid with tiles)
        level_data = self.level_generator.generate_level(self.level, self.player_pos)
        
        # Update game state with level data
        self.grid = level_data['grid']
        self.teleporters = level_data['teleporters']
        self.speed_boosts = level_data['speed_boosts']
        self.red_tiles = level_data['red_tiles']
        self.walls = level_data['walls']
        self.current_rule = level_data['current_rule']
        
        # Now find a valid door position on an empty tile
        self.door_pos = self._find_valid_door_position()
        
        self._set_rule_flags()
        self.moves = 0
        self.stepped_tiles = set()
        self.door_move_counter = 0
    
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
    
    def _set_rule_flags(self):
        """Set rule flags based on current rule"""
        self.reverse_controls = (self.current_rule == RuleType.INVERTED_CONTROLS)
        self.no_left_movement = (self.current_rule == RuleType.NO_LEFT_MOVEMENT)
        self.door_changes_position = (self.current_rule == RuleType.DOOR_CHANGES_POSITION)
        self.tiles_turn_red = (self.current_rule == RuleType.TILES_TURN_RED)
    
    def _create_sprites(self):
        """Create sprite objects for all tiles, door, and player"""
        self.sprites = {}
        
        # Create sprites for all tiles
        for y in range(TILE_HEIGHT):
            for x in range(TILE_WIDTH):
                tile_type = self.grid[y][x]
                sprite_type = self._get_sprite_type(tile_type)
                color = self._get_tile_color(tile_type)
                
                sprite = Sprite(x, y, sprite_type, color)
                self.sprites[(x, y)] = sprite
        
        # Create door sprite
        door_sprite = Sprite(self.door_pos[0], self.door_pos[1], SPRITE_DOOR, BROWN, DOOR_SIZE)
        self.sprites['door'] = door_sprite
        
        # Create player sprite
        player_sprite = Sprite(self.player_pos[0], self.player_pos[1], SPRITE_PLAYER, BLUE, PLAYER_SIZE)
        self.sprites['player'] = player_sprite
    
    def _get_sprite_type(self, tile_type: int) -> str:
        """Get sprite type from tile type"""
        if tile_type == TILE_WALL:
            return SPRITE_WALL
        elif tile_type == TILE_TELEPORTER:
            return SPRITE_TELEPORTER
        elif tile_type == TILE_SPEED_BOOST:
            return SPRITE_SPEED_BOOST
        elif tile_type == TILE_RED:
            return SPRITE_RED
        else:
            return SPRITE_EMPTY
    
    def _get_tile_color(self, tile_type: int) -> tuple:
        """Get color from tile type"""
        if tile_type == TILE_WALL:
            return GRAY
        elif tile_type == TILE_TELEPORTER:
            return PURPLE
        elif tile_type == TILE_SPEED_BOOST:
            return ORANGE
        elif tile_type == TILE_RED:
            return RED
        else:
            return WHITE
    
    def next_level(self):
        """Advance to next level"""
        if self.level < MAX_LEVELS:
            self.level += 1
            self.generate_level()
        else:
            print("Congratulations! You've completed all levels!")
    
    def reset_level(self):
        """Reset current level"""
        self.generate_level()
    
    def is_game_over(self) -> bool:
        """Check if game is over (out of moves)"""
        return self.moves >= self.max_moves
    
    def is_level_complete(self) -> bool:
        """Check if current level is complete (player reached door)"""
        return self.player_pos == self.door_pos
    
    def update_player_position(self, new_pos: List[int]):
        """Update player position from player object"""
        self.player_pos = new_pos
        if 'player' in self.sprites:
            self.sprites['player'].set_position(new_pos[0], new_pos[1])
        
        # Handle tiles turning red after stepping on them
        if self.tiles_turn_red:
            pos_tuple = (new_pos[0], new_pos[1])
            if pos_tuple not in self.stepped_tiles and self.grid[new_pos[1]][new_pos[0]] == TILE_EMPTY:
                self.stepped_tiles.add(pos_tuple)
                self.grid[new_pos[1]][new_pos[0]] = TILE_RED
                # Update sprite
                if pos_tuple in self.sprites:
                    self.sprites[pos_tuple].color = RED
                    self.sprites[pos_tuple].sprite_type = SPRITE_RED
    
    def increment_moves(self):
        """Increment move counter and handle door position changes"""
        self.moves += 1
        
        # Handle door position changes after 10 moves
        if self.door_changes_position and self.moves % 10 == 0:
            self._change_door_position()
    
    def _change_door_position(self):
        """Change door position randomly to an empty tile"""
        old_pos = self.door_pos.copy()
        new_pos = self._find_valid_door_position()
        
        # Make sure the new position is different from the old one
        attempts = 0
        max_attempts = 50
        while new_pos == old_pos and attempts < max_attempts:
            new_pos = self._find_valid_door_position()
            attempts += 1
        
        self.door_pos = new_pos
        if 'door' in self.sprites:
            self.sprites['door'].set_position(new_pos[0], new_pos[1])
    
    def get_remaining_moves(self) -> int:
        """Get remaining moves"""
        return self.max_moves - self.moves
    
    def check_red_tile_collision(self) -> bool:
        """Check if player is on a red tile"""
        return self.grid[self.player_pos[1]][self.player_pos[0]] == TILE_RED 
    
    def _is_valid_door_position(self, pos: List[int]) -> bool:
        """Check if a position is valid for a door (must be an empty tile)"""
        x, y = pos
        # Check bounds
        if x < 0 or x >= TILE_WIDTH or y < 0 or y >= TILE_HEIGHT:
            return False
        # Check if it's not the player position
        if pos == self.player_pos:
            return False
        # Check if it's an empty tile
        if self.grid[y][x] != TILE_EMPTY:
            return False
        return True
    
    def _find_valid_door_position(self) -> List[int]:
        """Find a valid door position (empty tile)"""
        attempts = 0
        max_attempts = 100  # Prevent infinite loops
        
        while attempts < max_attempts:
            pos = [
                random.randint(DOOR_MIN_COORD, TILE_WIDTH-1), 
                random.randint(DOOR_MIN_COORD, TILE_HEIGHT-1)
            ]
            if self._is_valid_door_position(pos):
                return pos
            attempts += 1
        
        # If no valid position found, find the first empty tile
        for y in range(TILE_HEIGHT):
            for x in range(TILE_WIDTH):
                pos = [x, y]
                if self._is_valid_door_position(pos):
                    return pos
        
        # Fallback to a default position
        return [TILE_WIDTH-1, TILE_HEIGHT-1] 