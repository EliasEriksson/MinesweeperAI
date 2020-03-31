from typing import *
from PIL import Image


def line_is_color(image: Image.Image,
                  start: Tuple[int, int],
                  end: Tuple[int, int],
                  color: tuple,
                  ) -> bool:
    """
    checks weather a line is made of only one color

    in reality a rectangle is checked but will only be used for 1 pixel wide rectangles
    this allows the same function to be used for both vertical and horizontal lines

    :param image: PIL.Image.Image
    :param start: Tuple[int, int], start of the line
    :param end: Tuple[int, int], end of the line
    :param color: tuple, a tuple of some length (representing the colors of a pixel) depending on image format
    :return: bool, true if line is of same color else false
    """
    (x1, y1), (x2, y2) = start, end
    for x in range(x1, x2):
        for y in range(y1, y2 + 1):
            if not image.getpixel((x, y)) == color:
                return False
    return True


def outline_is_grid(image: Image.Image,
                    start: Tuple[int, int],
                    end: Tuple[int, int],
                    square_size: int,
                    ) -> bool:
    """
    checks weather the outline of the rectangle is in a grid pattern

    the grid is assumed be 2 colors (like a chessboard)
    the color of the first pixel of a square is selected and passed down to see if the
    squares outline is the same color using `line_is_color`
    then takes the color of the second square
    and does the same thing
    OBS only the first pixel of the first and second square in line are used to
    compare all squares outlines

    :param image: PIL.Image.Image, image to be analyzed
    :param start: Tuple[int, int], start of the rectangle
    :param end: Tuple[int, int], end of the rectangle
    :param square_size: the size of the squares on the grid
    :return: bool, true if its a grid pattern else false
    """
    (x1, y1), (x2, y2) = start, end

    for i, x in enumerate(range(x1, x2, square_size)):
        color = image.getpixel((x, y1)) if (even := i % 2 == 0) else image.getpixel((x + square_size - 1, y1))
        if not line_is_color(image, (x, y1), (x + square_size, y1), color):
            return False

        color = image.getpixel((x, y2)) if even else image.getpixel((x + square_size - 1, y2))
        if not line_is_color(image, (x, y2), (x + square_size, y2), color):
            return False

    for i, y in enumerate(range(y1, y2, square_size)):
        color = image.getpixel((x1, y)) if (even := i % 2 == 0) else image.getpixel((x1, y + square_size - 1))
        if not line_is_color(image, (x1, y), (x1, y + square_size), color):
            return False

        color = image.getpixel((x2, y)) if even else image.getpixel((x2, y + square_size - 1))
        if not line_is_color(image, (x2, y), (x2, y + square_size), color):
            return False

    return True


def color_filter(image: Image.Image,
                 *boards: Tuple[Tuple[int, int], Tuple[int, int], int],
                 ) -> List[Tuple[Tuple[int, int], Tuple[int, int], int]]:
    """
    filters given boards with google´s minesweeper defining colors patterns

    return the given boards who fill the following criteria
    1: if the outline of the board is in a grid pattern described in `outline_is_grid`
    2: the pixel line above the board is the same color confirming the game menu
    3: if the pixel left of the game menu is in a different color than the game menu
    4: if the pixel right of the game menu is in a different color than the game menu


    :param image: PIL.Image.Image, image to be analyzed
    :param boards: Tuple[Tuple[int, int], Tuple[int, int], int], game boards to be filtered
    :return: Tuple[Tuple[int, int], Tuple[int, int], int], game boards that complies to the above criteria
    """
    return [
        (start, end, difficulty)
        for (x1, y1), (x2, y2), difficulty in boards
        if outline_is_grid(image, (start := (x1, y1)), (end := (x2, y2)), 45 - 5 * difficulty)  # if grid pattern
        if line_is_color(image, (x1, y1 - 1), (x2, y1 - 1), image.getpixel((x1, y1 - 1)))  # if menu header
        if image.getpixel((x1, y1 - 1)) != image.getpixel((x1 - 1, y1 - 1))  # left of menu not same color as menu
        if image.getpixel((x2, y1 - 1)) != image.getpixel((x2 + 1, y1 - 1))  # right of menu not same color as menu
    ]


