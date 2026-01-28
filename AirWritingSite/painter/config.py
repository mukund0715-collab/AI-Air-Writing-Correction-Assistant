############## Display Attributes ###############
W_WIDTH, W_HEIGHT = 1280, 720
HEADER_HEIGHT = 100  # Slightly taller for better spacing
TEXT_Y_START = 20
TEXT_LINE_HEIGHT = 20

############## Modern Color Palette (BGR Format) ###############
# Base Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)     # Soft Black
GRAY_LIGHT = (200, 200, 200)
GRAY_DARK = (50, 50, 50)

# UI Colors (Neon/Glass Theme)
UI_BG_OVERLAY = (30, 30, 35)     # Dark Blue-Grey for header
UI_BORDER = (100, 100, 100)      # Subtle border
UI_TEXT = (240, 240, 240)
UI_TEXT_MUTED = (150, 150, 150)

# Status Colors
NEON_GREEN = (100, 255, 100)     # Success / Alpha
NEON_BLUE = (255, 200, 50)       # Info / Numbers (Blueish)
NEON_RED = (100, 100, 255)       # Warning / Off
NEON_YELLOW = (50, 255, 255)     # Highlight

BACKGROUND = (255, 255, 255)
BORDER = (0, 255, 0)
BOUNDRYINC = 5

# Drawing Colors (The "Ink")
COLOR_OPTIONS = {
    "MAGENTA": (255, 0, 255),
    "CYAN": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "WHITE": (255, 255, 255),
    "ERASER": (0, 0, 0) 
}
COLOR_NAMES = list(COLOR_OPTIONS.keys())

############## Menu Attributes ###############
MENU_PADDING = 15
BUTTON_WIDTH = 110
BUTTON_HEIGHT = 50
BUTTON_SPACING = 15
START_X = 20
START_Y = 20

############## Predication Model Attributes ###############
MODEL_ALPHA_PATH = "bModel.h5"
MODEL_NUM_PATH = "bestmodel.h5"
MIN_BOX_SIZE = 30 

AlphaLABELS = { 0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j',
    10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't',
    20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z', 26: ''}
    
NumLABELS = {0:'0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5',
    6: '6', 7: '7', 8: '8', 9: '9'}

############## HandDetection Attributes ###############
DETECTION_CONFIDENCE = 0.85
BRUSH_THICKNESS = 15
ERASER_THICKNESS = 40
FIST_DURATION = 1.5  

############## Smoothing Filter Attributes ###############
SMOOTHING_WINDOW = 5