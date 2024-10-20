import pygame

class Config:
    # Colors
    BACKGROUND = "#000000"  # Black
    CELL_ALIVE = "#FFFFFF"  # White
    CELL_DEAD = "#000000"   # Black
    BUTTON_COLOR = "#4CAF50"  # Green
    BUTTON_HOVER_COLOR = "#45a049"  # Darker Green
    BUTTON_TEXT_COLOR = "#FFFFFF"  # White
    SLIDER_COLOR = "#2196F3"  # Blue
    SLIDER_HANDLE_COLOR = "#FFFFFF"  # White
    TIMER_COLOR = "#FFFFFF"  # White

    # Grid settings
    GRID_WIDTH = 80
    GRID_HEIGHT = 60
    CELL_SIZE = 10

    # Game settings
    FPS_MIN = 1
    FPS_MAX = 60
    FPS_DEFAULT = 10

    # UI settings
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 40
    SLIDER_WIDTH = 200
    SLIDER_HEIGHT = 20

    # Conway's Game of Life rules
    BORN = [3]  # A dead cell becomes alive if it has exactly 3 live neighbors
    SURVIVE = [2, 3]  # A live cell survives if it has 2 or 3 live neighbors
    

    # Fonts
    FONT = None
    TIMER_FONT = None

    @classmethod
    def init_fonts(cls):
        pygame.font.init()
        cls.FONT = pygame.font.Font(None, 32)
        cls.TIMER_FONT = pygame.font.Font(None, 24)