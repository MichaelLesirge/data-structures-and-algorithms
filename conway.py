
import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory / "conway"))

from conway.main import main
from conway.config import Config

Config.BORN = [3]  # A dead cell becomes alive if it has exactly 3 live neighbors
Config.SURVIVE = [2, 3]  # A live cell survives if it has 2 or 3 live neighbors, and dies if it does not

main(config)