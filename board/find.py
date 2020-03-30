from typing import *
from PIL import Image
from pathlib import Path, PosixPath
import board.filters as filters
from .board import Board
import board.errors as errors


def find(image_path: Union[Path, PosixPath]):
    """
    find the game board on the image

    :param image_path:
    :return:
    """
    image: Image.Image = Image.open(image_path)
    potential_starting_points = filters.black_and_white(image)
    potential_starting_points = filters.color(image, *potential_starting_points)
    if not potential_starting_points:
        raise errors.NoStartingPoint("No starting point was found in the image.")
    if len(potential_starting_points) > 1:
        raise errors.TooManyStartingPoints("Too many potential starting points in the image.")

    return Board(*potential_starting_points[0])



