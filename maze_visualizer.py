import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory / "maze_solver"))

from maze_solver.main import main
from maze_solver.config import Config

config = Config()

config.BACKGROUND = "#F0E7D8"  # Soft cream
config.WALL = "#2C3E50"        # Dark blue-gray
config.EMPTY = "#ECF0F1"       # Light gray

config.PATH = "#E67E22"        # Vibrant orange

config.START = "#27AE60"       # Emerald green
config.END = "#C0392B"         # Deep red

# 2 for corridor, 1 for wall
config.CORRIDOR_WIDTH = 2 + 1

config.SOLVER_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]       # down, right, up left
# config.SOLVER_DIRECTIONS += [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Add Diagonals

main(config)