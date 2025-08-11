from enum import Enum

class RuleType(Enum):
    """Enumeration of different game rule types for the 3rd rule of each level"""
    INVERTED_CONTROLS = "Inverted Controls"
    NO_LEFT_MOVEMENT = "Player Cannot Move Left"
    DOOR_CHANGES_POSITION = "Doors Change Position After 10 Moves"
    TILES_TURN_RED = "Tiles Turn Red After Stepping On Them" 