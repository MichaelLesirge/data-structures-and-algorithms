import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory / "sorting"))

from sorting.visualizer import main
from sorting.config import Config

import pygame

Config.SORTING_ALGORITHMS = ["bubble_sort", "insertion_sort", "selection_sort", "merge_sort", "quick_sort"]

Config.SCREEN_WIDTH = 1000
Config.SCREEN_HEIGHT = 600

Config.BASE_FPS = 60

Config.DEMO_LIST_NUM_RANGE = None
Config.DEMO_LIST_LENGTHS = [10, 25, 100, 250, 500, 1000]
Config.SPEEDS = []

Config.WAIT_AT_END = 0.5

Config.BACKGROUND_COLOR = pygame.Color("black")
Config.DEFAULT_BLOCK_COLOR = pygame.Color("white")

Config.READ_BLOCK_COLOR = pygame.Color("grey")
Config.PAST_WRITE_BLOCK_COLOR = pygame.Color("aquamarine2")
Config.WRITE_BLOCK_COLOR = pygame.Color("green")

Config.TEXT_COLOR = pygame.Color(200, 200, 250)

main()