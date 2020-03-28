from typing import *
from PIL import Image
from pathlib import Path, PosixPath
import board.filters as filters


def find(image_path: Union[Path, PosixPath]):
    """
    find the game board on the image



    :param image_path:
    :return:
    """
    image: Image.Image = Image.open(image_path)
    potential_starting_points = filters.black_and_white(image)
    potential_starting_points = filters.color(image, *potential_starting_points)
    return potential_starting_points



