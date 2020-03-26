from typing import *
from PIL import Image
from pathlib import Path, PosixPath
import board.filters as filters


def find(image_path: Union[Path, PosixPath], difficulty):
    image: Image.Image = Image.open(image_path)
    potential_starting_points = filters.black_and_white(image, difficulty)
    return potential_starting_points



