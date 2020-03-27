from typing import *
from PIL import Image
from .errors import UnKnownDifficulty


WHITE = 255
BLACK = 0

EASY_WIDTH = 450-1
EASY_HEIGHT = 360-1

MEDIUM_WIDTH = 540-1
MEDIUM_HEIGHT = 420-1

HARD_WIDTH = 600-1
HARD_HEIGHT = 500-1

WIDTHS = (EASY_WIDTH, MEDIUM_WIDTH, HARD_WIDTH)
HEIGHTS = (EASY_HEIGHT, MEDIUM_HEIGHT, HARD_HEIGHT)


def _look_down(image: Image.Image,
               coordinate: Tuple[int, int]
               ) -> Union[Tuple[int, int], Tuple[()]]:
    x, y = coordinate
    for y in range(y, image.height - 1):
        if image.getpixel((x, y)) == WHITE:
            if image.getpixel((x, y + 1)) == BLACK:
                if image.getpixel((x, y + 1)) == BLACK:
                    return x, y
        else:
            return ()
    return ()


def _look_right(image: Image.Image,
                coordinate: Tuple[int, int]
                ) -> Union[Tuple[int, int], Tuple[()]]:
    x, y = coordinate
    for x in range(x, image.width - 1):
        if image.getpixel((x, y)) == WHITE:
            if image.getpixel((x + 1, y)) == BLACK:
                if image.getpixel((x + 1, y)) == BLACK:
                    return x, y
        else:
            return ()
    return ()


def _look_around(image: Image.Image,
                 coordinate: Tuple[int, int]
                 ) -> Union[Tuple[int, int], Tuple[()]]:
    x, y = coordinate
    if image.getpixel((x - 1, y)) == BLACK:
        if image.getpixel((x + 1, y)) == WHITE:
            if image.getpixel((x, y - 1)) == BLACK:
                if image.getpixel((x, y + 1)) == WHITE:
                    if right := _look_right(image, coordinate):
                        if down := _look_down(image, coordinate):
                            if (corner := _look_right(image, down)) == _look_down(image, right) and corner:
                                return corner
    return ()


def black_and_white_filter(image: Image.Image,
                           ) -> List[Tuple[Tuple[int, int], Tuple[int, int], int]]:
    """
    analyzes the image as a binary black and white image in search for a game board

    the algorithm starts by finding a pixel that is
    1: white
    2: white pixel bellow
    3: white pixel to the right
    4: black pixel above
    5: black pixel to the left
    by walking right and down from the original pixel as well as down and right 2 pixels are found
    if the pixels coordinates are the same its assumed that a rectangle representing the playing field is found
    if the distance between each corner is found in the defined width and height constants.

    a list of the start and end coordinate as well as a difficulty (easy medium hard) that fits these requirements
    will be returned. Will most likely only be one value as the distancing between each pixel is rather precise

    :param image: PIL.Image.Image, image to be analyzed
    :return: List[Tuple[Tuple[int, int], Tuple[int, int], int]], list of start and end coordinate and difficulty
    """

    image: Image.Image = image.convert("1", dither=Image.NONE)

    potential_starting_points = [
        (start, end)
        for x in range(image.width)
        for y in range(image.height)
        if image.getpixel((start := (x, y))) == WHITE
        if (end := _look_around(image, start))]

    return [(start, end, 0) if dx == EASY_WIDTH else
            (start, end, 3) if dx == MEDIUM_WIDTH else
            (start, end, 4)
            for start, end in potential_starting_points
            if (dx := end[0] - start[0]) in WIDTHS and end[1] - start[1] in HEIGHTS]
