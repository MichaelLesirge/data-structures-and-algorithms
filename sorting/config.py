import pygame

class Config:
    DEMO_SORTING_ALGORITHMS = ["bubble_sort", "insertion_sort", "selection_sort", "merge_sort", "quick_sort"]
    
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    
    BASE_FPS = 60
    
    DEMO_LIST_LENGTHS = [10, 25, 100, 250, 500, 1000]
    DEMO_LIST_NUM_RANGE = None
    
    SPEEDS = []

    DELAY_AFTER_COMPLETION = 0.5
    
    BACKGROUND_COLOR = pygame.Color(0, 0, 0)
    DEFAULT_BLOCK_COLOR = pygame.Color(255, 255, 255)
    
    READ_BLOCK_COLOR = pygame.Color("grey")
    PAST_WRITE_BLOCK_COLOR = pygame.Color("aquamarine2")
    WRITE_BLOCK_COLOR = pygame.Color("green")

    BLOCK_GAP_PX = 1

    MIN_HEIGHT_PERCENT = 0
    MAX_HEIGHT_PERCENT = 1
    
    TEXT_COLOR = (200, 200, 250)
    
    FPS_CHANGE = 0.5

    FONT_PATH = 'sorting/font.ttf'
    FONT_SIZE = 16

    PLAY_SOUNDS = True
