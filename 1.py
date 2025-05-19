import tkinter as tk # Not used in this version, but kept as per original
import pygame
import os # Not used in this snippet directly, but often useful
import time # Used for blinking cursor effect
import random # For potential future use (e.g., NPC movement)

# --- Game Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32

# Viewport dimensions in tiles
DIALOGUE_BOX_HEIGHT = 120 # Height of the dialogue box in pixels
GAME_AREA_HEIGHT = SCREEN_HEIGHT - DIALOGUE_BOX_HEIGHT # Used for in-game viewport
VIEWPORT_WIDTH_TILES = SCREEN_WIDTH // TILE_SIZE
VIEWPORT_HEIGHT_TILES = GAME_AREA_HEIGHT // TILE_SIZE

FPS = 60 # Target 60 frames per second, similar to GBA refresh rates
MAX_PLAYER_NAME_LENGTH = 7 # Typical Pokemon name length

# --- Colors (Gen 3 Inspired - simplified) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
C_PATH_GRASS = (136, 192, 112)
C_GRASS_REGULAR = (104, 168, 88)
C_TALL_GRASS = (64, 128, 72)
C_TREE_TRUNK = (112, 80, 48)
C_TREE_LEAVES = (48, 96, 48)
C_WATER = (80, 128, 200)
C_FLOWER_RED = (208, 72, 48)
C_FLOWER_YELLOW = (248, 224, 96)
C_SAND = (216, 200, 160)
C_BUILDING_WALL_LIGHT = (200, 160, 120)
C_BUILDING_WALL_DARK = (160, 128, 96)
C_ROOF_RED = (192, 80, 48)
C_ROOF_BLUE = (80, 96, 160)
C_ROOF_GRAY = (128, 128, 128)
C_ROOF_MART = (60, 120, 180)
C_DOOR = (96, 64, 32)
C_SIGN = (144, 112, 80)
C_LEDGE = (120, 176, 104)
C_FENCE = (160, 144, 128)
C_PLAYER = (224, 80, 64) # Default Boy color
C_PLAYER_GIRL = (230, 120, 150) # Girl color
C_NPC = (80, 144, 224)
C_PROF = (100, 100, 180) # Professor color for intro
C_DIALOGUE_BG = (40, 40, 40)
C_DIALOGUE_TEXT = WHITE
C_DIALOGUE_BORDER = (100, 100, 100)
C_PC_WALL = (230, 190, 190)
C_MART_WALL = (180, 200, 230)
C_BUTTON = (70, 70, 150) # Button color for UI elements
C_BUTTON_HOVER = (100, 100, 180) # Button color when mouse hovers
C_BUTTON_TEXT = WHITE
C_TEXT_INPUT_BG = (60, 60, 60) # Background for name input field
C_TEXT_INPUT_BORDER = (120, 120, 120) # Border for name input field
C_CURSOR = (220, 220, 20) # Custom mouse cursor color

# --- Tile Types (Numeric identifiers for different map elements) ---
T_PATH_GRASS = 0
T_GRASS_REGULAR = 1
T_TALL_GRASS = 2
T_WATER = 3
T_TREE = 4
T_FLOWER_RED = 5
T_FLOWER_YELLOW = 6
T_SAND = 7
T_BUILDING_WALL = 10 # Generic building wall
T_PLAYER_HOUSE_WALL = 11
T_PLAYER_HOUSE_DOOR = 12
T_RIVAL_HOUSE_WALL = 13
T_RIVAL_HOUSE_DOOR = 14
T_LAB_WALL = 15
T_LAB_DOOR = 16
T_ROOF_PLAYER = 17
T_ROOF_RIVAL = 18
T_ROOF_LAB = 19
T_SIGN = 20
T_LEDGE_JUMP_DOWN = 21 # Tile for one-way ledges
T_FENCE = 22
T_PC_WALL = 23 # PokeCenter-like wall
T_PC_DOOR = 24 # PokeCenter-like door
T_MART_WALL = 25 # Mart-like wall
T_MART_DOOR = 26 # Mart-like door
T_ROOF_PC = 27
T_ROOF_MART = 28
T_NPC_SPAWN = 98 # Marker for NPC positions in map data
T_PLAYER_SPAWN = 99 # Marker for initial player start position

# --- Map IDs (String identifiers for different game maps) ---
MAP_LITTLEROOT = "littleroot_town"
MAP_ROUTE_101 = "route_101"
MAP_OLDALE = "oldale_town"

# --- Helper variables for map creation (shorthands for tile types) ---
PHW, PHD = T_PLAYER_HOUSE_WALL, T_PLAYER_HOUSE_DOOR
RHW, RHD = T_RIVAL_HOUSE_WALL, T_RIVAL_HOUSE_DOOR
LBW, LBD = T_LAB_WALL, T_LAB_DOOR
PCW, PCD = T_PC_WALL, T_PC_DOOR
MRW, MRD = T_MART_WALL, T_MART_DOOR
RPL, RRV, RLB, RPC, RMR = T_ROOF_PLAYER, T_ROOF_RIVAL, T_ROOF_LAB, T_ROOF_PC, T_ROOF_MART
TRE, PTH, SGN, FNC, WTR, TLG, FLR, FLY, LJD, NSP, PSP = \
    T_TREE, T_PATH_GRASS, T_SIGN, T_FENCE, T_WATER, T_TALL_GRASS, \
    T_FLOWER_RED, T_FLOWER_YELLOW, T_LEDGE_JUMP_DOWN, T_NPC_SPAWN, T_PLAYER_SPAWN
GRS = T_GRASS_REGULAR

# --- Map Data (Defines the layout of each map using tile type constants) ---
# Littleroot Town Map Data
littleroot_town_map_data = [
    [TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, PTH, PTH, PTH, PTH, PTH, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE],
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, RLB, RLB, RLB, RLB, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, FLY, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, LBW, LBD, LBW, LBW, PTH, PTH, PTH, PTH, PTH, PTH, PTH, FLR, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, PTH, PTH, PTH, TRE, TRE, PTH, PTH, PTH, PTH, LBW, NSP, LBW, LBW, PTH, PTH, PTH, PTH, TRE, TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE], # Prof Birch NPC spawn
    [TRE, PTH, PTH, PTH, PTH, TRE, TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE, TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, PTH, SGN, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, SGN, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, FNC, FNC, FNC, FNC, FNC, PTH, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, PTH, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, PTH, TRE],
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, RPL, RPL, RPL, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, RRV, RRV, RRV, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, PHW, PHD, PHW, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, RHW, RHD, RHW, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, PHW, NSP, PHW, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, RHW, RHW, RHW, PTH, PTH, PTH, PTH, PTH, TRE], # Mom NPC spawn
    [TRE, PTH, PTH, PSP, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE], # Player initial spawn
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE, TRE, PTH, PTH, PTH, PTH, PTH, PTH, TRE, TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE, TRE, PTH, PTH, PTH, PTH, PTH, PTH, TRE, TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, LJD, LJD, LJD, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, TLG, TLG, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TLG, TLG, TLG, TRE],
    [TRE, TLG, TLG, PTH, PTH, PTH, PTH, WTR, WTR, WTR, PTH, PTH, PTH, PTH, PTH, PTH, WTR, WTR, WTR, PTH, PTH, PTH, PTH, PTH, PTH, TLG, TLG, TLG, TRE],
    [TRE, TRE, TRE, TRE, TRE, TRE, TRE, WTR, WTR, WTR, TRE, TRE, TRE, TRE, TRE, TRE, WTR, WTR, WTR, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE],
]
# Route 101 Map Data
route_101_map_data = [
    [TRE, TRE, TRE, TRE, TRE, PTH, PTH, PTH, PTH, PTH, TRE, TRE, TRE, TRE, TRE],
    [TRE, TLG, TLG, TLG, PTH, PTH, GRS, GRS, PTH, PTH, PTH, TLG, TLG, TLG, TRE],
    [TRE, TLG, GRS, TLG, PTH, GRS, GRS, NSP, GRS, GRS, PTH, TLG, GRS, TLG, TRE],
    [TRE, TLG, GRS, TLG, PTH, GRS, GRS, GRS, GRS, GRS, PTH, TLG, GRS, TLG, TRE],
    [TRE, TRE, GRS, TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE, GRS, TRE, TRE],
    [TRE, GRS, GRS, GRS, PTH, GRS, GRS, GRS, GRS, GRS, PTH, GRS, GRS, GRS, TRE],
    [TRE, GRS, TRE, GRS, PTH, GRS, TLG, TLG, TLG, GRS, PTH, GRS, TRE, GRS, TRE],
    [TRE, GRS, TRE, GRS, PTH, GRS, TLG, NSP, TLG, GRS, PTH, GRS, TRE, GRS, TRE],
    [TRE, GRS, TRE, GRS, PTH, GRS, TLG, TLG, TLG, GRS, PTH, GRS, TRE, GRS, TRE],
    [TRE, GRS, GRS, GRS, PTH, GRS, GRS, GRS, GRS, GRS, PTH, GRS, GRS, GRS, TRE],
    [TRE, TRE, TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE, TRE, TRE],
    [TRE, TLG, TLG, PTH, GRS, GRS, GRS, GRS, GRS, GRS, GRS, PTH, TLG, TLG, TRE],
    [TRE, GRS, TLG, PTH, GRS, TLG, TLG, TLG, TLG, TLG, GRS, PTH, TLG, GRS, TRE],
    [TRE, GRS, GRS, PTH, GRS, TLG, GRS, GRS, GRS, TLG, GRS, PTH, GRS, GRS, TRE],
    [TRE, GRS, GRS, PTH, GRS, TLG, GRS, NSP, GRS, TLG, GRS, PTH, GRS, GRS, TRE],
    [TRE, GRS, GRS, PTH, GRS, TLG, GRS, GRS, GRS, TLG, GRS, PTH, GRS, GRS, TRE],
    [TRE, TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE, TRE],
    [TRE, TLG, PTH, GRS, GRS, GRS, TLG, TLG, TLG, GRS, GRS, GRS, PTH, TLG, TRE],
    [TRE, TLG, PTH, GRS, TLG, TLG, TLG, GRS, TLG, TLG, TLG, GRS, PTH, TLG, TRE],
    [TRE, PTH, PTH, GRS, GRS, GRS, GRS, GRS, GRS, GRS, GRS, GRS, PTH, PTH, TRE],
    [TRE, PTH, GRS, GRS, TRE, TRE, TRE, NSP, TRE, TRE, TRE, GRS, GRS, PTH, TRE],
    [TRE, PTH, GRS, GRS, TRE, PTH, PTH, PTH, PTH, PTH, TRE, GRS, GRS, PTH, TRE],
    [TRE, PTH, PTH, PTH, TRE, PTH, GRS, GRS, GRS, PTH, TRE, PTH, PTH, PTH, TRE],
    [TRE, TRE, TRE, TRE, TRE, PTH, GRS, GRS, GRS, PTH, TRE, TRE, TRE, TRE, TRE],
    [TRE, TRE, TRE, TRE, TRE, PTH, PTH, PTH, PTH, PTH, TRE, TRE, TRE, TRE, TRE],
]
# Oldale Town Map Data
oldale_town_map_data = [
    [TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE],
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, GRS, GRS, RPC, RPC, RPC, PTH, GRS, GRS, RMR, RMR, RMR, PTH, PTH, SGN, PTH, GRS, GRS, GRS, GRS, GRS, GRS, PTH, TRE], 
    [TRE, PTH, GRS, GRS, PCW, PCD, PCW, PTH, GRS, GRS, MRW, MRD, MRW, PTH, NSP, PTH, PTH, GRS, GRS, GRS, GRS, GRS, GRS, PTH, TRE], 
    [TRE, PTH, GRS, GRS, PCW, NSP, PCW, PTH, GRS, GRS, MRW, MRW, MRW, PTH, PTH, PTH, PTH, GRS, GRS, FLY, GRS, FLR, GRS, PTH, TRE], 
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, GRS, GRS, GRS, GRS, GRS, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, GRS, GRS, GRS, GRS, GRS, GRS, PTH, TRE],
    [TRE, PTH, GRS, TRE, TRE, TRE, GRS, PTH, FNC, FNC, FNC, FNC, FNC, FNC, FNC, PTH, GRS, TRE, TRE, TRE, TRE, TRE, GRS, PTH, TRE],
    [TRE, PTH, GRS, TRE, NSP, TRE, GRS, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, GRS, TRE, NSP, TRE, GRS, TRE, GRS, PTH, TRE], 
    [TRE, PTH, GRS, TRE, TRE, TRE, GRS, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, GRS, TRE, TRE, TRE, GRS, TRE, GRS, PTH, TRE],
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, GRS, GRS, GRS, GRS, GRS, GRS, GRS, PTH, PTH, PTH, PTH, PTH, GRS, GRS, GRS, GRS, GRS, GRS, GRS, GRS, GRS, PTH, TRE],
    [TRE, PTH, GRS, TLG, TLG, GRS, GRS, GRS, GRS, PTH, SGN, PTH, PTH, PTH, GRS, TLG, TLG, GRS, GRS, FLR, GRS, FLY, GRS, PTH, TRE],
    [TRE, PTH, GRS, TLG, TLG, GRS, GRS, GRS, GRS, PTH, PTH, PTH, PTH, PTH, GRS, TLG, TLG, GRS, GRS, GRS, GRS, GRS, GRS, PTH, TRE],
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, PTH, TRE],
    [TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, PTH, PTH, PTH, PTH, PTH, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE],
    [TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, PTH, GRS, GRS, GRS, PTH, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE],
    [TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, PTH, GRS, GRS, GRS, PTH, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE],
    [TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, PTH, PTH, PTH, PTH, PTH, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE, TRE],
]

# --- Game States (Manages different phases of the game, like intro, gameplay, menus, etc.) ---
STATE_INTRO_WELCOME = 0         # Initial welcome screen
STATE_INTRO_PROF_SPEECH = 1     # Professor's introductory dialogue
STATE_INTRO_GENDER_SELECT = 2   # Player chooses gender
STATE_INTRO_NAME_INPUT = 3      # Player inputs their name
STATE_GAMEPLAY = 4              # Main game exploration mode
STATE_TRANSITION_TO_GAME = 5    # Brief state for final message before gameplay

class DialogueBox:
    """Handles the display and interaction of dialogue messages."""
    def __init__(self, screen, font_size=28, alt_font_size=24):
        self.screen = screen
        self.font = pygame.font.Font(None, font_size) # Primary font for dialogue
        self.alt_font = pygame.font.Font(None, alt_font_size) # Alternative font (e.g., for UI hints)
        self.messages = [] # Queue of messages to be displayed
        self.active = False # Is a message currently being shown?
        # Position and dimensions of the dialogue box
        self.rect = pygame.Rect(10, SCREEN_HEIGHT - DIALOGUE_BOX_HEIGHT - 10, SCREEN_WIDTH - 20, DIALOGUE_BOX_HEIGHT)
        self.text_rect = self.rect.inflate(-40, -40) # Padding for text inside the box
        self.current_message_surfaces = [] # Surfaces for each line of the current wrapped message
        self.line_height = self.font.get_linesize()
        self.on_complete_callback = None # Optional function to call when all messages in queue are shown

    def show_message(self, text, callback=None):
        """Adds a message to the queue and starts displaying if not already active."""
        self.messages.append(text)
        self.on_complete_callback = callback # Store callback for when this batch of messages finishes
        if not self.active:
            self.next_message()

    def next_message(self):
        """Processes and displays the next message from the queue."""
        if self.messages:
            self.active = True
            current_text = self.messages.pop(0)
            self.current_message_surfaces = [] # Clear surfaces from previous message

            # Word wrapping logic
            words = current_text.split(' ')
            current_line_text = ""
            for word in words:
                # Check if adding the next word exceeds the width of the text area
                test_line = current_line_text + word + " "
                if self.font.size(test_line.strip())[0] <= self.text_rect.width:
                    current_line_text = test_line
                else:
                    # Render the completed line and start a new one
                    line_surf = self.font.render(current_line_text.strip(), True, C_DIALOGUE_TEXT)
                    self.current_message_surfaces.append(line_surf)
                    current_line_text = word + " "
            
            # Add the last remaining line
            if current_line_text.strip():
                line_surf = self.font.render(current_line_text.strip(), True, C_DIALOGUE_TEXT)
                self.current_message_surfaces.append(line_surf)
            
            # Truncate if message has too many lines for the box (basic handling)
            max_lines = self.text_rect.height // self.line_height
            if len(self.current_message_surfaces) > max_lines:
                self.current_message_surfaces = self.current_message_surfaces[:max_lines]
        else:
            # No more messages in the queue
            self.active = False
            self.current_message_surfaces = []
            if self.on_complete_callback:
                self.on_complete_callback() # Execute the callback
                self.on_complete_callback = None # Clear callback once executed

    def draw(self):
        """Draws the dialogue box and its current message if active."""
        if self.active and self.current_message_surfaces:
            # Draw the background and border of the dialogue box
            pygame.draw.rect(self.screen, C_DIALOGUE_BG, self.rect, border_radius=15)
            pygame.draw.rect(self.screen, C_DIALOGUE_BORDER, self.rect, 3, border_radius=15)
            
            # Draw each line of the current message
            current_y = self.text_rect.top
            for line_surf in self.current_message_surfaces:
                if current_y + self.line_height <= self.text_rect.bottom: # Ensure line fits
                    self.screen.blit(line_surf, (self.text_rect.left, current_y))
                    current_y += self.line_height
                else:
                    break # Stop if no more space

    def handle_input(self, event):
        """Handles input (e.g., key press) to advance to the next message."""
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_e:
                self.next_message()
                return True # Input was handled by the dialogue box
        return False

class Entity:
    """Base class for game objects like Player and NPCs."""
    def __init__(self, x, y, color, game, name="Entity"):
        self.x = x  # Tile x-coordinate in world space
        self.y = y  # Tile y-coordinate in world space
        self.color = color # Default color for the entity
        self.game = game # Reference to the main game object
        self.name = name

    def draw(self, surface, camera_x, camera_y):
        """Draws the entity on the screen, adjusted by camera position."""
        # Calculate screen coordinates based on world coordinates and camera
        screen_x = self.x * TILE_SIZE - camera_x
        screen_y = self.y * TILE_SIZE - camera_y

        # Basic culling: Only draw if entity is visible within the game area
        if screen_x + TILE_SIZE > 0 and screen_x < SCREEN_WIDTH and \
           screen_y + TILE_SIZE > 0 and screen_y < GAME_AREA_HEIGHT:
            rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            # Simple detail (e.g., eyes or a smaller inner square for basic representation)
            detail_size = TILE_SIZE // 3
            detail_offset = (TILE_SIZE - detail_size) // 2 # Center the detail
            detail_rect = pygame.Rect(screen_x + detail_offset, screen_y + detail_offset, detail_size, detail_size)
            pygame.draw.rect(surface, BLACK, detail_rect)

class NPC(Entity):
    """Non-Player Character class."""
    def __init__(self, x, y, game, name="NPC", dialogue="Hello there, traveler!"):
        super().__init__(x, y, C_NPC, game, name=name)
        self.dialogue = dialogue # Dialogue string for this NPC

    def interact(self, interactor): # Interactor is typically the player
        """Handles interaction with the NPC (e.g., shows dialogue)."""
        player_name = interactor.name if interactor else "Traveler" # Get player's name for dialogue
        # Replace placeholders in dialogue string
        formatted_dialogue = self.dialogue.replace("[PlayerName]", player_name)
        formatted_dialogue = formatted_dialogue.replace("[Rival]", self.game.rival_name if hasattr(self.game, 'rival_name') else "your Rival")
        self.game.dialogue_box.show_message(f"{self.name}: {formatted_dialogue}")

def is_walkable(tile_type):
    """Helper function to check if a given tile type is walkable."""
    walkable_tiles = [
        T_PATH_GRASS, T_GRASS_REGULAR, T_TALL_GRASS, T_FLOWER_RED, T_FLOWER_YELLOW, T_SAND,
    ]
    # Solid, non-walkable tiles
    non_walkable_tiles = [
        T_TREE, T_WATER, T_BUILDING_WALL, T_PLAYER_HOUSE_WALL,
        T_RIVAL_HOUSE_WALL, T_LAB_WALL, T_ROOF_PLAYER, T_ROOF_RIVAL,
        T_ROOF_LAB, T_FENCE, T_PC_WALL, T_MART_WALL, T_ROOF_PC, T_ROOF_MART
    ]
    if tile_type in walkable_tiles:
        return True
    if tile_type in non_walkable_tiles:
        return False
    # By default, tiles are not walkable unless specified. Doors, signs, ledges are handled specially.
    return False

class Player(Entity):
    """Player character class."""
    def __init__(self, x, y, game, name="Player", gender="boy"):
        player_color = C_PLAYER if gender == "boy" else C_PLAYER_GIRL # Set color based on gender
        super().__init__(x, y, player_color, game, name=name)
        self.gender = gender

    def move(self, dx, dy):
        """Attempts to move the player by dx, dy tiles and handles interactions/collisions."""
        if self.game.dialogue_box.active:
            return "blocked_dialogue" # Cannot move if dialogue is active

        new_x, new_y = self.x + dx, self.y + dy # Calculate potential new position

        # --- Handle Map Transitions ---
        # (Order: Check for map transitions before checking boundaries of the current map)
        # From Littleroot to Route 101 (North Exit)
        if self.game.current_map_id == MAP_LITTLEROOT and new_y < 0 and 11 <= self.x <= 15:
            self.game.change_map(MAP_ROUTE_101, (self.x - 11) + 5, self.game.maps_data[MAP_ROUTE_101]['height'] - 1)
            return "map_changed"
        # From Route 101 to Littleroot (South Exit)
        elif self.game.current_map_id == MAP_ROUTE_101 and new_y >= self.game.current_map_height_tiles and 5 <= self.x <= 9:
            self.game.change_map(MAP_LITTLEROOT, (self.x - 5) + 11, 0)
            return "map_changed"
        # From Route 101 to Oldale (North Exit)
        elif self.game.current_map_id == MAP_ROUTE_101 and new_y < 0 and 5 <= self.x <= 9:
            self.game.change_map(MAP_OLDALE, (self.x - 5) + 9, self.game.maps_data[MAP_OLDALE]['height'] - 1)
            return "map_changed"
        # From Oldale to Route 101 (South Exit)
        elif self.game.current_map_id == MAP_OLDALE and new_y >= self.game.current_map_height_tiles and 9 <= self.x <= 13:
            self.game.change_map(MAP_ROUTE_101, (self.x - 9) + 5, 0)
            return "map_changed"

        # --- Standard Movement & Collision within current map ---
        # Check map boundaries for the new position
        if not (0 <= new_x < self.game.current_map_width_tiles and \
                0 <= new_y < self.game.current_map_height_tiles):
            return "blocked_boundary" # Tried to move off map where there's no connection

        target_tile_type = self.game.current_map_data[new_y][new_x]
        
        # Check for NPC at the target location (NPCs block movement)
        for npc in self.game.npcs:
            if npc.x == new_x and npc.y == new_y:
                npc.interact(self) # Player interacts with NPC
                return "interacted_npc" # Movement blocked by NPC

        # Tile-based interactions (Signs, Doors). These usually block movement onto the tile.
        interaction_message = None
        rival_name_display = self.game.rival_name if hasattr(self.game, 'rival_name') else '[Rival]'
        if target_tile_type == T_PLAYER_HOUSE_DOOR: interaction_message = f"{self.name}'s house. It's cozy inside!"
        elif target_tile_type == T_RIVAL_HOUSE_DOOR: interaction_message = f"This is {rival_name_display}'s house."
        elif target_tile_type == T_LAB_DOOR: interaction_message = "Professor Birch's Pokémon Lab."
        elif target_tile_type == T_PC_DOOR: interaction_message = "It's a Pokémon Center." # Placeholder
        elif target_tile_type == T_MART_DOOR: interaction_message = "It's a Poké Mart." # Placeholder
        elif target_tile_type == T_SIGN:
            if self.game.current_map_id == MAP_LITTLEROOT:
                if new_x == 3 and new_y == 6: interaction_message = "LITTLEROOT TOWN\nA town that can't be shaded any hue."
                elif new_x == 22 and new_y == 6: interaction_message = "ROUTE 101 ahead.\nTall grass! Wild Pokémon live there!"
            elif self.game.current_map_id == MAP_OLDALE:
                if new_x == 15 and new_y == 2 : interaction_message = "OLDALE TOWN\nWhere things get started."
                elif new_x == 10 and new_y == 12: interaction_message = "North: Route 103 (Not Implemented)\nWest: Petalburg Woods (Not Implemented)"
            else: interaction_message = "It's a wooden sign."
        
        if interaction_message:
            self.game.dialogue_box.show_message(interaction_message)
            return "interacted_tile" # Player interacted, movement blocked

        # Ledge Jumping Logic
        if target_tile_type == T_LEDGE_JUMP_DOWN:
            if dy == 1: # Moving downwards onto the ledge tile
                self.x = new_x
                self.y = new_y + 1 # Player lands one tile BELOW the ledge
                # Boundary check for landing spot
                if not (0 <= self.y < self.game.current_map_height_tiles):
                    self.y = new_y # Revert to ledge tile if landing out of bounds
                    return "blocked_ledge_fall_boundary"
                # Walkability check for landing spot
                landing_tile_type = self.game.current_map_data[self.y][self.x]
                if not is_walkable(landing_tile_type) and landing_tile_type != T_LEDGE_JUMP_DOWN:
                     self.x -= dx # Revert x
                     self.y = new_y -1 # Revert y to tile before ledge
                     return "blocked_ledge_landing"
                self.game.dialogue_box.show_message("Jumped down the ledge!")
                return "jumped_ledge"
            else: # Trying to move onto a ledge from sides, or upwards
                return "blocked_collision_ledge"

        # Standard walkable check for other tiles
        if is_walkable(target_tile_type):
            self.x = new_x
            self.y = new_y
            if target_tile_type == T_TALL_GRASS:
                # Future: Implement wild Pokémon encounter logic here
                return "moved_tall_grass"
            return "moved"
        else:
            # If not walkable and not any special interaction tile, it's a solid collision
            return "blocked_collision_solid"

class GameMock:
    """Main class for the game engine, managing states, game loop, and rendering."""
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False) # Hide default system mouse cursor
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokémon Style RPG Engine")
        self.clock = pygame.time.Clock() # Pygame clock for controlling FPS
        
        # Fonts for different UI elements
        self.dialogue_font = pygame.font.Font(None, 32)
        self.ui_font = pygame.font.Font(None, 36)
        self.name_input_font = pygame.font.Font(None, 40)

        self.dialogue_box = DialogueBox(self.screen, font_size=30, alt_font_size=36)
        self.player = None # Player object, initialized after the intro sequence
        self.player_name_input = "" # Stores text during name input
        self.player_gender = "boy" # Default gender
        
        self.npcs = [] # List to store NPC objects for the current map
        # Visual representation for the professor in the intro
        self.prof_rect = pygame.Rect(SCREEN_WIDTH // 2 - TILE_SIZE * 1.5, SCREEN_HEIGHT // 2 - TILE_SIZE * 3, TILE_SIZE * 3, TILE_SIZE * 3)

        # Store all map data
        self.maps_data = {
            MAP_LITTLEROOT: {'data': littleroot_town_map_data, 'width': len(littleroot_town_map_data[0]), 'height': len(littleroot_town_map_data)},
            MAP_ROUTE_101: {'data': route_101_map_data, 'width': len(route_101_map_data[0]), 'height': len(route_101_map_data)},
            MAP_OLDALE: {'data': oldale_town_map_data, 'width': len(oldale_town_map_data[0]), 'height': len(oldale_town_map_data)},
        }
        # Current map properties (will be updated when map changes)
        self.current_map_id = MAP_LITTLEROOT
        self.current_map_data = self.maps_data[self.current_map_id]['data']
        self.current_map_width_tiles = self.maps_data[self.current_map_id]['width']
        self.current_map_height_tiles = self.maps_data[self.current_map_id]['height']
        
        self.rival_name = "May" # Example rival name, can be customized
        self.prof_name = "Prof. Birch" # Professor's name

        self.game_state = STATE_INTRO_WELCOME # Initial game state
        self.prof_speech_stage = 0 # Tracks progress through professor's speech

        # Rectangles for gender selection buttons
        self.boy_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25, 100, 50)
        self.girl_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 25, 100, 50)
        
        # Rectangle for name input field
        self.name_input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        
        self.camera_x, self.camera_y = 0,0 # Camera position for scrolling map
        
        self.start_intro() # Begin the game with the intro sequence

    def start_intro(self):
        """Initiates the introductory sequence of the game."""
        self.game_state = STATE_INTRO_WELCOME
        self.dialogue_box.show_message(f"Welcome to the world of Pokémon!", self.start_prof_speech)

    def start_prof_speech(self):
        """Starts the professor's speech part of the intro."""
        self.game_state = STATE_INTRO_PROF_SPEECH
        self.prof_speech_stage = 0
        self.advance_prof_speech()

    def advance_prof_speech(self):
        """Advances through the professor's pre-defined dialogue lines."""
        speeches = [
            f"{self.prof_name}: My name is {self.prof_name}. People call me the Pokémon Professor.",
            f"{self.prof_name}: This world is inhabited by creatures called Pokémon!",
            f"{self.prof_name}: For some people, Pokémon are pets. Others use them for fights. Myself...",
            f"{self.prof_name}: I study Pokémon as a profession.",
            f"{self.prof_name}: But first, tell me a little about yourself. Are you a boy, or are you a girl?"
        ]
        if self.prof_speech_stage < len(speeches):
            # Set callback to advance speech or transition to next state
            callback = self.advance_prof_speech if self.prof_speech_stage < len(speeches) -1 else self.transition_to_gender_select
            self.dialogue_box.show_message(speeches[self.prof_speech_stage], callback)
            self.prof_speech_stage += 1

    def transition_to_gender_select(self):
        """Transitions the game state to gender selection."""
        self.game_state = STATE_INTRO_GENDER_SELECT
        self.dialogue_box.active = False # Hide dialogue box to show UI elements

    def transition_to_name_input(self):
        """Transitions the game state to name input after gender is selected."""
        self.game_state = STATE_INTRO_NAME_INPUT
        self.dialogue_box.show_message(f"{self.prof_name}: I see! So, you're a {self.player_gender}. And what is your name?", None)

    def finalize_intro_and_start_game(self):
        """Finalizes intro, creates player object, and prepares to start gameplay."""
        self.game_state = STATE_TRANSITION_TO_GAME
        spawn_x, spawn_y = self.find_player_spawn_on_map(MAP_LITTLEROOT)
        self.player = Player(spawn_x, spawn_y, self, name=self.player_name_input, gender=self.player_gender)
        self.dialogue_box.show_message(f"{self.prof_name}: {self.player.name}, your very own Pokémon legend is about to unfold! A world of dreams and adventures with Pokémon awaits! Let's go!", self.actually_start_gameplay)

    def actually_start_gameplay(self):
        """Transitions to the main gameplay state and loads the starting map."""
        self.game_state = STATE_GAMEPLAY
        self.current_map_id = MAP_LITTLEROOT # Set the initial map for gameplay
        self.load_map(self.current_map_id, initial_load=True)

    def find_player_spawn_on_map(self, map_id):
        """Finds the T_PLAYER_SPAWN tile on a given map."""
        map_data = self.maps_data[map_id]['data']
        for r, row in enumerate(map_data):
            for c, tile in enumerate(row):
                if tile == T_PLAYER_SPAWN:
                    return c, r
        print(f"Warning: Player spawn (PSP) not found on map {map_id}. Defaulting.")
        return 5, 5 # Fallback spawn position

    def load_map(self, map_id, initial_load=False):
        """Loads map data, NPCs, and replaces spawn markers."""
        if map_id not in self.maps_data:
            print(f"Error: Map ID {map_id} not found.")
            return

        self.current_map_id = map_id
        map_info = self.maps_data[map_id]
        self.current_map_data = [row[:] for row in map_info['data']] # Deep copy for mutable map
        self.current_map_width_tiles = map_info['width']
        self.current_map_height_tiles = map_info['height']
        
        self.npcs = [] # Clear NPCs from previous map
        
        for r, row in enumerate(self.current_map_data):
            for c, tile in enumerate(row):
                if tile == T_PLAYER_SPAWN:
                    # Replace spawn marker with a walkable tile (e.g., path)
                    # This is important so the tile is walkable if player re-enters map at this point
                    # The actual player object creation/positioning is handled by intro or change_map
                    self.current_map_data[r][c] = T_PATH_GRASS 
                elif tile == T_NPC_SPAWN:
                    # Define NPCs based on map and location
                    npc_name = "Youngster" # Default NPC
                    npc_dialogue = "I like shorts! They're comfy and easy to wear!"
                    if map_id == MAP_LITTLEROOT and c == 12 and r == 3: # Prof Birch in Lab
                        npc_name = self.prof_name
                        npc_dialogue = "Ah, [PlayerName]! How is your Pokémon journey coming along?"
                    elif map_id == MAP_LITTLEROOT and c == 3 and r == 12: # Mom in Player's House
                        npc_name = "Mom"
                        npc_dialogue = "Be careful out there, [PlayerName]! And don't forget to change your underwear!"
                    
                    self.npcs.append(NPC(c, r, self, name=npc_name, dialogue=npc_dialogue))
                    self.current_map_data[r][c] = T_PATH_GRASS # Replace NPC spawn marker

    def change_map(self, new_map_id, player_new_x, player_new_y):
        """Handles changing maps and repositioning the player."""
        print(f"Changing map from {self.current_map_id} to {new_map_id}. Player to ({player_new_x}, {player_new_y})")
        
        # Update player's position for the new map
        self.player.x = player_new_x
        self.player.y = player_new_y
        
        self.load_map(new_map_id) # Load new map data and NPCs

    def handle_input(self):
        """Processes all user input based on the current game state."""
        mouse_pos = pygame.mouse.get_pos() # Get current mouse position

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False # Signal to quit the game loop

            # Dialogue input handling takes precedence if active
            if self.dialogue_box.active:
                if self.dialogue_box.handle_input(event):
                    continue # Dialogue handled input, skip other state-specific input

            # State-specific input handling
            if self.game_state == STATE_INTRO_GENDER_SELECT:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
                    if self.boy_button_rect.collidepoint(mouse_pos):
                        self.player_gender = "boy"
                        self.transition_to_name_input()
                    elif self.girl_button_rect.collidepoint(mouse_pos):
                        self.player_gender = "girl"
                        self.transition_to_name_input()
            elif self.game_state == STATE_INTRO_NAME_INPUT:
                if not self.dialogue_box.active: # Allow name input only after prof asks
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and len(self.player_name_input) > 0:
                            self.finalize_intro_and_start_game()
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name_input = self.player_name_input[:-1]
                        elif len(self.player_name_input) < MAX_PLAYER_NAME_LENGTH:
                            if event.unicode.isalnum(): # Allow alphanumeric characters
                                self.player_name_input += event.unicode.upper() # Uppercase for Pokémon names
            
            elif self.game_state == STATE_GAMEPLAY:
                if self.player and not self.dialogue_box.active and event.type == pygame.KEYDOWN:
                    action_result = ""
                    if event.key == pygame.K_LEFT: action_result = self.player.move(-1, 0)
                    elif event.key == pygame.K_RIGHT: action_result = self.player.move(1, 0)
                    elif event.key == pygame.K_UP: action_result = self.player.move(0, -1)
                    elif event.key == pygame.K_DOWN: action_result = self.player.move(0, 1)
                    if action_result: 
                        print(f"Player action: {action_result}, New Pos: ({self.player.x}, {self.player.y}) on {self.current_map_id}")
        return True # Signal to continue running

    def update(self):
        """Updates game logic, like camera movement."""
        if self.game_state == STATE_GAMEPLAY and self.player:
            # Camera follows player
            self.camera_x = self.player.x * TILE_SIZE - SCREEN_WIDTH // 2 + TILE_SIZE // 2
            self.camera_y = self.player.y * TILE_SIZE - GAME_AREA_HEIGHT // 2 + TILE_SIZE // 2
            # Clamp camera to map boundaries to prevent showing areas outside the map
            self.camera_x = max(0, min(self.camera_x, self.current_map_width_tiles * TILE_SIZE - SCREEN_WIDTH))
            self.camera_y = max(0, min(self.camera_y, self.current_map_height_tiles * TILE_SIZE - GAME_AREA_HEIGHT))

    def draw_mouse_cursor(self):
        """Draws a custom mouse cursor."""
        mouse_pos = pygame.mouse.get_pos()
        # Simple triangle cursor
        cursor_points = [
            mouse_pos,
            (mouse_pos[0] + 15, mouse_pos[1] + 10),
            (mouse_pos[0] + 10, mouse_pos[1] + 15),
        ]
        pygame.draw.polygon(self.screen, C_CURSOR, cursor_points)
        pygame.draw.polygon(self.screen, BLACK, cursor_points, 1) # Border for cursor

    def draw(self):
        """Handles all drawing operations based on the current game state."""
        self.screen.fill(BLACK) # Default background for intro/transition states

        # --- Drawing logic for INTRO states ---
        if self.game_state in [STATE_INTRO_WELCOME, STATE_INTRO_PROF_SPEECH, STATE_TRANSITION_TO_GAME]:
            # Draw Professor visual (simple representation)
            pygame.draw.rect(self.screen, C_PROF, self.prof_rect, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, self.prof_rect, 2, border_radius=10) 
            eye_y = self.prof_rect.centery - TILE_SIZE // 3 # Position eyes
            pygame.draw.circle(self.screen, WHITE, (self.prof_rect.centerx - TILE_SIZE//4, eye_y), TILE_SIZE//8)
            pygame.draw.circle(self.screen, WHITE, (self.prof_rect.centerx + TILE_SIZE//4, eye_y), TILE_SIZE//8)
            pygame.draw.circle(self.screen, BLACK, (self.prof_rect.centerx - TILE_SIZE//4, eye_y), TILE_SIZE//16) # Pupils
            pygame.draw.circle(self.screen, BLACK, (self.prof_rect.centerx + TILE_SIZE//4, eye_y), TILE_SIZE//16)
            pygame.draw.line(self.screen, BLACK, (self.prof_rect.centerx - TILE_SIZE//5, self.prof_rect.centery + TILE_SIZE//5), 
                                                (self.prof_rect.centerx + TILE_SIZE//5, self.prof_rect.centery + TILE_SIZE//5), 2) # Mouth

        elif self.game_state == STATE_INTRO_GENDER_SELECT:
            prompt_surf = self.ui_font.render("Are you a BOY or a GIRL?", True, WHITE)
            prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(prompt_surf, prompt_rect)

            mouse_pos = pygame.mouse.get_pos() # Get mouse pos for hover effect
            # Boy Button
            boy_hover = self.boy_button_rect.collidepoint(mouse_pos)
            pygame.draw.rect(self.screen, C_BUTTON_HOVER if boy_hover else C_BUTTON, self.boy_button_rect, border_radius=10)
            boy_text_surf = self.ui_font.render("BOY", True, C_BUTTON_TEXT)
            boy_text_rect = boy_text_surf.get_rect(center=self.boy_button_rect.center)
            self.screen.blit(boy_text_surf, boy_text_rect)
            # Girl Button
            girl_hover = self.girl_button_rect.collidepoint(mouse_pos)
            pygame.draw.rect(self.screen, C_BUTTON_HOVER if girl_hover else C_BUTTON, self.girl_button_rect, border_radius=10)
            girl_text_surf = self.ui_font.render("GIRL", True, C_BUTTON_TEXT)
            girl_text_rect = girl_text_surf.get_rect(center=self.girl_button_rect.center)
            self.screen.blit(girl_text_surf, girl_text_rect)
        
        elif self.game_state == STATE_INTRO_NAME_INPUT:
            pygame.draw.rect(self.screen, C_TEXT_INPUT_BG, self.name_input_rect, border_radius=5)
            pygame.draw.rect(self.screen, C_TEXT_INPUT_BORDER, self.name_input_rect, 2, border_radius=5)
            
            # Display typed name with a blinking cursor effect
            cursor_visible = int(time.time() * 2) % 2 == 0 # Blink underscore cursor
            name_display_text = self.player_name_input
            if cursor_visible and len(self.player_name_input) < MAX_PLAYER_NAME_LENGTH and not self.dialogue_box.active:
                name_display_text += "_"
            
            name_surf = self.name_input_font.render(name_display_text, True, WHITE)
            name_rect = name_surf.get_rect(midleft=(self.name_input_rect.left + 15, self.name_input_rect.centery))
            self.screen.blit(name_surf, name_rect)

            if not self.dialogue_box.active: # Show hint only when dialogue is not active
                hint_surf = self.dialogue_box.alt_font.render(f"Max {MAX_PLAYER_NAME_LENGTH} chars. Press Enter to confirm.", True, (180,180,180))
                hint_rect = hint_surf.get_rect(center=(SCREEN_WIDTH // 2, self.name_input_rect.bottom + 30))
                self.screen.blit(hint_surf, hint_rect)

        # --- Drawing logic for GAMEPLAY state ---
        elif self.game_state == STATE_GAMEPLAY:
            self.screen.fill(C_GRASS_REGULAR) # Default background for game area
            # Draw Tiles (visible portion of the map)
            for r_idx, row_val in enumerate(self.current_map_data):
                for c_idx, tile_val in enumerate(row_val):
                    tile_screen_x = c_idx * TILE_SIZE - self.camera_x
                    tile_screen_y = r_idx * TILE_SIZE - self.camera_y
                    # Cull tiles not on screen for efficiency
                    if tile_screen_x + TILE_SIZE < 0 or tile_screen_x > SCREEN_WIDTH or \
                       tile_screen_y + TILE_SIZE < 0 or tile_screen_y > GAME_AREA_HEIGHT:
                        continue
                    
                    # Determine color based on tile type
                    color = BLACK # Default for unknown/undefined tiles
                    if tile_val == T_PATH_GRASS: color = C_PATH_GRASS
                    elif tile_val == T_GRASS_REGULAR: color = C_GRASS_REGULAR
                    elif tile_val == T_TALL_GRASS: color = C_TALL_GRASS
                    elif tile_val == T_TREE: color = C_TREE_LEAVES
                    elif tile_val == T_WATER: color = C_WATER
                    elif tile_val == T_FLOWER_RED: color = C_FLOWER_RED
                    elif tile_val == T_FLOWER_YELLOW: color = C_FLOWER_YELLOW
                    elif tile_val == T_FENCE: color = C_FENCE
                    elif tile_val == T_LEDGE_JUMP_DOWN: color = C_LEDGE
                    elif tile_val in [T_PLAYER_HOUSE_WALL, T_RIVAL_HOUSE_WALL, T_LAB_WALL, T_PC_WALL, T_MART_WALL, T_BUILDING_WALL]:
                        color = C_BUILDING_WALL_LIGHT # Generic wall
                        if tile_val == T_PC_WALL: color = C_PC_WALL
                        if tile_val == T_MART_WALL: color = C_MART_WALL
                    elif tile_val in [T_PLAYER_HOUSE_DOOR, T_RIVAL_HOUSE_DOOR, T_LAB_DOOR, T_PC_DOOR, T_MART_DOOR]: color = C_DOOR
                    elif tile_val in [T_ROOF_PLAYER, T_ROOF_RIVAL, T_ROOF_LAB, T_ROOF_PC, T_ROOF_MART]:
                        color = C_ROOF_GRAY # Generic roof
                        if tile_val == T_ROOF_PLAYER or tile_val == T_ROOF_RIVAL : color = C_ROOF_RED
                        if tile_val == T_ROOF_PC: color = C_ROOF_GRAY # Specific roof for PC
                        if tile_val == T_ROOF_MART: color = C_ROOF_MART # Specific roof for Mart
                    elif tile_val == T_SIGN: color = C_SIGN
                    pygame.draw.rect(self.screen, color, (tile_screen_x, tile_screen_y, TILE_SIZE, TILE_SIZE))
            
            # Draw NPCs
            for npc in self.npcs:
                npc.draw(self.screen, self.camera_x, self.camera_y)
            # Draw Player
            if self.player:
                self.player.draw(self.screen, self.camera_x, self.camera_y)

        # Draw Dialogue Box on top of everything else (if active)
        self.dialogue_box.draw()
        
        # Draw custom mouse cursor for relevant states
        if self.game_state == STATE_INTRO_GENDER_SELECT or self.game_state == STATE_INTRO_NAME_INPUT:
            self.draw_mouse_cursor()

        pygame.display.flip() # Update the full screen

    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_input() # Process input
            if not running: break # Exit loop if handle_input signals quit
            
            self.update() # Update game logic
            self.draw()   # Render the current frame
            
            self.clock.tick(FPS) # Maintain target FPS
            
        pygame.quit() # Clean up Pygame resources

if __name__ == '__main__':
    game = GameMock()
    game.run()
