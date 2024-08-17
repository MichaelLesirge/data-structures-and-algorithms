import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory / "binary_search_tree"))

from binary_search_tree.main import main
from binary_search_tree.config import Config

config = Config()

config.NODE_RADIUS = 25
config.SPRINGINESS = 0.1
config.DAMPING = 0.85
config.CHILD_MOVE_FACTOR = 0.2

config.LEVEL_SPACING = 80

config.STARTING_NODES = [10]

main(config)