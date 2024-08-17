import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory / "sorting"))

from sorting.visualizer import main
from sorting.config import Config

import pygame

config = Config()

# bubble_sort, insertion_sort, selection_sort, merge_sort, quick_sort
config.DEMO_SORTING_ALGORITHMS = ["bubble_sort", "insertion_sort", "selection_sort", "merge_sort", "quick_sort"]

config.DEMO_LIST_NUM_RANGE = None  # leave as none to auto smooth generate range of numbers
# config.DEMO_LIST_NUM_RANGE = (0, 10000)

config.DEMO_LIST_LENGTHS = [10, 25, 100, 250, 500, 1000]
config.SPEEDS = []

config.SCREEN_WIDTH = 1000
config.SCREEN_HEIGHT = 600

config.BACKGROUND_COLOR = pygame.Color("black")
config.DEFAULT_BLOCK_COLOR = pygame.Color("white")

config.READ_BLOCK_COLOR = pygame.Color("grey")
config.PAST_WRITE_BLOCK_COLOR = pygame.Color("aquamarine2")
config.WRITE_BLOCK_COLOR = pygame.Color("green")

config.BLOCK_GAP = 1

config.TEXT_COLOR = pygame.Color(200, 200, 250)

config.DELAY_AFTER_COMPLETION = 0.5

main(config)
