import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory / "sorting"))

from sorting.visualizer import main
from sorting.config import Config

import pygame

config = Config()

# What sorting algorithms to display and in what order
# Options include bubble_sort, insertion_sort, selection_sort, merge_sort, quick_sort
config.DEMO_SORTING_ALGORITHMS = ["bubble_sort", "insertion_sort", "selection_sort", "merge_sort", "quick_sort"]

# Range of numbers to sort in demo.
# Leave as none to auto smooth generate range of numbers, or give [min, max] for random distribution
config.DEMO_LIST_NUM_RANGE = None 
# config.DEMO_LIST_NUM_RANGE = (0, 100)

# Lengths of list to sort
config.DEMO_LIST_LENGTHS = [10, 25, 100, 250, 500, 1000]

# Background color
config.BACKGROUND_COLOR = pygame.Color("black")

# Color of text
config.TEXT_COLOR = pygame.Color(200, 200, 250)

config.DEFAULT_BLOCK_COLOR = pygame.Color("white")  # Color of block
config.READ_BLOCK_COLOR = pygame.Color("grey")  # Color of block that was read
config.WRITE_BLOCK_COLOR = pygame.Color("green")   # Color of last block that was written to
config.PAST_WRITE_BLOCK_COLOR = pygame.Color("aquamarine2")   # Color of block that was written to one frame earlier

# Space between blocks, in pixels. 0 or 1 suggested.
config.BLOCK_GAP_PX = 1

# How long to wait after sorting is finished before moving on
config.DELAY_AFTER_COMPLETION = 0.5

main(config)
