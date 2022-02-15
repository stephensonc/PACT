from array import array
from typing import Tuple

from zeroconf import struct


class AlgorithmInterface:

    # Must return an array of tuples containing path coords
    def run(env_grid):
        pass



class DefaultAStar(AlgorithmInterface):

    def run(env_grid, dest_cell_coords: Tuple):
        pass

    def is_blocked(tile_value: int):
        return tile_value == 1

    def get_h_value(row, col, dest_cell_coords: Tuple):
        pass
    def return_path() -> None:
        pass