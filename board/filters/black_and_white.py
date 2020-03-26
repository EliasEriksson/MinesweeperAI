from typing import *
from PIL import Image
from .errors import UnKnownDifficulty


WHITE = 255
BLACK = 0
EASY = 1
MEDIUM = 2
HARD = 3


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


def black_and_white(image: Image.Image,
                    difficulty: int
                    ) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    image: Image.Image = image.convert("1", dither=Image.NONE)

    if difficulty == EASY:
        board_width = 0
        board_height = 0
    elif difficulty == MEDIUM:
        board_width = 540
        board_height = 420
    elif difficulty == HARD:
        board_width = 0
        board_height = 0
    else:
        raise UnKnownDifficulty(f"difficulty={difficulty} is not valid. "
                                f"Must be EASY (1), MEDIUM (2) or HARD (3)")

    potential_starting_points = [
        ((x, y), corner)
        for x in range(image.width)
        for y in range(image.height)
        if image.getpixel((x, y)) == WHITE
        if (corner := _look_around(image, (x, y)))]

    return [(coordinate, corner)
            for coordinate, corner in potential_starting_points
            if corner[0] - coordinate[0] == board_width - 1 and corner[1] - coordinate[1] == board_height - 1]
