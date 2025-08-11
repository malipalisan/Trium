import pygame
from typing import List
from .constants import *

class Renderer:
    """Handles all drawing and visual rendering of the game"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def render(self, game_state, player):
        """Render the complete game"""
        self._clear_screen()
        self._draw_grid(game_state)
        self._draw_door(game_state)
        self._draw_player(game_state)
        self._draw_ui(game_state, player)
        self._draw_instructions()
        self._draw_legend()
        pygame.display.flip()
    
    def _clear_screen(self):
        """Clear the screen with white background"""
        self.screen.fill(WHITE)
    
    def _draw_grid(self, game_state):
        """Draw the game grid with all tiles using sprites"""
        for y in range(TILE_HEIGHT):
            for x in range(TILE_WIDTH):
                if (x, y) in game_state.sprites:
                    sprite = game_state.sprites[(x, y)]
                    sprite.draw(self.screen)
                else:
                    # Fallback drawing for tiles without sprites
                    rect = pygame.Rect(x * TILE_SIZE + GRID_X, y * TILE_SIZE + GRID_Y, TILE_SIZE, TILE_SIZE)
                    tile_type = game_state.grid[y][x]
                    color = self._get_tile_color(tile_type)
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)
    
    def _get_tile_color(self, tile_type: int) -> tuple:
        """Get color for tile type"""
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
    
    def _draw_door(self, game_state):
        """Draw the door using sprite"""
        if 'door' in game_state.sprites:
            door_sprite = game_state.sprites['door']
            door_sprite.draw(self.screen)
            
            # Draw door handle
            door_pos = game_state.door_pos
            handle_rect = pygame.Rect(
                door_pos[0] * TILE_SIZE + GRID_X + TILE_SIZE - 10,
                door_pos[1] * TILE_SIZE + GRID_Y + TILE_SIZE // 2 - 5,
                5, 10
            )
            pygame.draw.rect(self.screen, BLACK, handle_rect)
    
    def _draw_player(self, game_state):
        """Draw the player using sprite"""
        if 'player' in game_state.sprites:
            player_sprite = game_state.sprites['player']
            player_sprite.draw(self.screen)
    
    def _draw_ui(self, game_state, player):
        """Draw the user interface elements"""
        # Level info - top left, above the grid
        level_text = self.font.render(f"Level: {game_state.level}/{MAX_LEVELS}", True, BLACK)
        self.screen.blit(level_text, (20, 20))
        
        # Current rules - below level info
        rules_text = [
            "Rules:",
            "1. Player cannot step on red tiles",
            "2. Maximum 100 moves per level",
            f"3. {game_state.current_rule.value}"
        ]
        
        y_offset = 60
        for rule in rules_text:
            rule_text = self.small_font.render(rule, True, BLACK)
            self.screen.blit(rule_text, (20, y_offset))
            y_offset += 25
        
        # Moves counter - below rules
        moves_text = self.small_font.render(f"Moves: {game_state.moves}/{game_state.max_moves}", True, BLACK)
        self.screen.blit(moves_text, (20, y_offset + 10))
    
    def _draw_instructions(self):
        """Draw game instructions"""
        instructions = [
            "Use WASD or Arrow Keys to move",
            "Reach the brown door to complete the level",
            "Don't step on red tiles!",
            "Press R to restart level"
        ]
        
        y_offset = WINDOW_HEIGHT - 120
        for instruction in instructions:
            instruction_text = self.small_font.render(instruction, True, BLACK)
            self.screen.blit(instruction_text, (20, y_offset))
            y_offset += 25
    
    def _draw_legend(self):
        """Draw tile legend"""
        legend_items = [
            ("Player", BLUE),
            ("Door", BROWN),
            ("Wall", GRAY),
            ("Teleporter", PURPLE),
            ("Speed Boost", ORANGE),
            ("Red Tile", RED),
            ("Empty", WHITE)
        ]
        
        x_offset = WINDOW_WIDTH - 200
        y_offset = 20
        
        for item, color in legend_items:
            # Draw color box
            color_rect = pygame.Rect(x_offset, y_offset, 20, 20)
            pygame.draw.rect(self.screen, color, color_rect)
            pygame.draw.rect(self.screen, BLACK, color_rect, 1)
            
            # Draw label
            label_text = self.small_font.render(item, True, BLACK)
            self.screen.blit(label_text, (x_offset + 25, y_offset))
            y_offset += 25 