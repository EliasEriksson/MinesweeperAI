from typing import *
from PIL import Image
import board.filters as filters
import board.errors as errors


def find(image: Image.Image) -> Tuple[Tuple[int, int], Tuple[int, int], int]:
    """
    find the game board on the image

    :param image:
    :return:
    """
    potential_starting_points = filters.black_and_white(image)
    potential_starting_points = filters.color(image, *potential_starting_points)
    if not potential_starting_points:
        raise errors.NoStartingPoint("No starting point was found in the image.")
    if len(potential_starting_points) > 1:
        raise errors.TooManyStartingPoints("Too many potential starting points in the image.")
    return potential_starting_points[0]



