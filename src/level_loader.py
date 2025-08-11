import os
from typing import List, Dict, Optional
from .constants import *
from .sprite import Sprite

class LevelLoader:
    """Handles loading levels from .txt files"""
    
    def __init__(self):
        self.levels_dir = "levels"
        self._ensure_levels_directory()
    
    def _ensure_levels_directory(self):
        """Ensure the levels directory exists"""
        if not os.path.exists(self.levels_dir):
            os.makedirs(self.levels_dir)
    
    def load_level_from_file(self, level_number: int) -> Optional[Dict]:
        """Load a level from a .txt file"""
        filename = os.path.join(self.levels_dir, f"level_{level_number}.txt")
        
        if not os.path.exists(filename):
            return None
        
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
            
            # Parse level data
            level_data = self._parse_level_file(lines)
            return level_data
            
        except Exception as e:
            print(f"Error loading level {level_number}: {e}")
            return None
    
    def _parse_level_file(self, lines: List[str]) -> Dict:
        """Parse level data from file lines"""
        level_data = {
            'grid': [],
            'player_pos': [0, 0],
            'door_pos': [0, 0],
            'teleporters': [],
            'speed_boosts': [],
            'red_tiles': [],
            'walls': [],
            'current_rule': None
        }
        
        # Remove empty lines and strip whitespace
        lines = [line.strip() for line in lines if line.strip()]
        
        if len(lines) < TILE_HEIGHT + 2:  
            raise ValueError("Invalid level file format")
        
        # Parse grid (first TILE_HEIGHT lines)
        for y in range(TILE_HEIGHT):
            if y >= len(lines):
                break
            
            row = lines[y]
            grid_row = []
            
            for x in range(TILE_WIDTH):
                if x >= len(row):
                    grid_row.append(TILE_EMPTY)
                else:
                    tile_char = row[x]
                    tile_type = self._char_to_tile_type(tile_char)
                    grid_row.append(tile_type)
                    
                    # Track special tiles
                    if tile_type == TILE_WALL:
                        level_data['walls'].append([x, y])
                    elif tile_type == TILE_TELEPORTER:
                        # Teleporters will be paired later
                        pass
                    elif tile_type == TILE_SPEED_BOOST:
                        level_data['speed_boosts'].append([x, y])
                    elif tile_type == TILE_RED:
                        level_data['red_tiles'].append([x, y])
            
            level_data['grid'].append(grid_row)
        
        # Parse player position (line after grid)
        if len(lines) > TILE_HEIGHT:
            player_line = lines[TILE_HEIGHT]
            level_data['player_pos'] = self._parse_position(player_line)
        
        # Parse door position (line after player)
        if len(lines) > TILE_HEIGHT + 1:
            door_line = lines[TILE_HEIGHT + 1]
            door_pos = self._parse_position(door_line)
            # Validate door position to ensure it's on an empty tile
            level_data['door_pos'] = self._validate_door_position(door_pos, level_data['grid'], level_data['player_pos'])
        
        # Parse teleporters (remaining lines)
        teleporter_positions = []
        for y in range(TILE_HEIGHT):
            for x in range(TILE_WIDTH):
                if level_data['grid'][y][x] == TILE_TELEPORTER:
                    teleporter_positions.append([x, y])
        
        # Pair teleporters
        for i in range(0, len(teleporter_positions), 2):
            if i + 1 < len(teleporter_positions):
                level_data['teleporters'].append([
                    teleporter_positions[i],
                    teleporter_positions[i + 1]
                ])
        
        return level_data
    
    def _char_to_tile_type(self, char: str) -> int:
        """Convert character to tile type"""
        char = char.upper()
        if char == 'W':
            return TILE_WALL
        elif char == 'T':
            return TILE_TELEPORTER
        elif char == 'S':
            return TILE_SPEED_BOOST
        elif char == 'R':
            return TILE_RED
        elif char == 'D':
            return TILE_DOOR
        else:
            return TILE_EMPTY
    
    def _parse_position(self, line: str) -> List[int]:
        """Parse position from line (format: 'x,y')"""
        try:
            parts = line.split(',')
            if len(parts) >= 2:
                return [int(parts[0].strip()), int(parts[1].strip())]
        except Exception as e:
            print(f"Error parsing position '{line}': {e}")
        return [0, 0]
    
    def save_level_to_file(self, level_number: int, level_data: Dict):
        """Save a level to a .txt file"""
        filename = os.path.join(self.levels_dir, f"level_{level_number}.txt")
        
        try:
            with open(filename, 'w') as file:
                # Write grid
                for row in level_data['grid']:
                    row_str = ''
                    for tile in row:
                        row_str += self._tile_type_to_char(tile)
                    file.write(row_str + '\n')
                
                # Write player position
                player_pos = level_data['player_pos']
                file.write(f"{player_pos[0]},{player_pos[1]}\n")
                
                # Write door position
                door_pos = level_data['door_pos']
                file.write(f"{door_pos[0]},{door_pos[1]}\n")
                
        except Exception as e:
            print(f"Error saving level {level_number}: {e}")
    
    def _tile_type_to_char(self, tile_type: int) -> str:
        """Convert tile type to character"""
        if tile_type == TILE_WALL:
            return 'W'
        elif tile_type == TILE_TELEPORTER:
            return 'T'
        elif tile_type == TILE_SPEED_BOOST:
            return 'S'
        elif tile_type == TILE_RED:
            return 'R'
        elif tile_type == TILE_DOOR:
            return 'D'
        else:
            return '.' 

    def _validate_door_position(self, door_pos: List[int], grid: List[List[int]], player_pos: List[int]) -> List[int]:
        """Validate and potentially correct door position to ensure it's on an empty tile"""
        x, y = door_pos
        
        # Check bounds
        if x < 0 or x >= TILE_WIDTH or y < 0 or y >= TILE_HEIGHT:
            # Find first empty tile
            for y2 in range(TILE_HEIGHT):
                for x2 in range(TILE_WIDTH):
                    if grid[y2][x2] == TILE_EMPTY and [x2, y2] != player_pos:
                        return [x2, y2]
            return [0, 0]  # Fallback
        
        # Check if it's not the player position
        if door_pos == player_pos:
            # Find first empty tile
            for y2 in range(TILE_HEIGHT):
                for x2 in range(TILE_WIDTH):
                    if grid[y2][x2] == TILE_EMPTY and [x2, y2] != player_pos:
                        return [x2, y2]
            return [0, 0]  # Fallback
        
        # Check if it's an empty tile
        if grid[y][x] != TILE_EMPTY:
            # Find first empty tile
            for y2 in range(TILE_HEIGHT):
                for x2 in range(TILE_WIDTH):
                    if grid[y2][x2] == TILE_EMPTY and [x2, y2] != player_pos:
                        return [x2, y2]
            return [0, 0]  # Fallback
        

        return door_pos 
