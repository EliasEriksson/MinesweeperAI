from typing import *
from PIL import Image
from .errors import UnKnownDifficulty


EASY = 1
MEDIUM = 2
HARD = 3


def check_line_same_color(image: Image.Image,
                          start: Tuple[int, int],
                          end: Tuple[int, int]
                          ) -> bool:
    (x1, y1), (x2, y2) = start, end
    color = image.getpixel((x1, y1))
    for x in range(x1, x2):
        for y in range(y1, y2):
            if not image.getpixel((x, y)) == color:
                return False
    return True


def board_features(image: Image.Image,
                   coordinates: List[Tuple[Tuple[int, int], Tuple[int, int]]],
                   difficulty: int
                   ) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    if difficulty == EASY:
        number_of_squares = 0
        square_length = 0
    elif difficulty == MEDIUM:
        number_of_squares = 18
        square_length = 30
    elif difficulty == HARD:
        number_of_squares = 0
        square_length = 0
    else:
        raise UnKnownDifficulty(f"difficulty={difficulty} is not valid. "
                                f"Must be EASY (1), MEDIUM (2) or HARD (3)")

    for rect in coordinates:
        start, end = rect
        (x1, y1), (x2, y2) = start, end
        if not image.getpixel((x1 - 1, y1)) == image.getpixel((x2, y2)):
            if not image.getpixel((x1, y2 - y1- 1)) == image.getpixel((x1 - 1, y2 - y1)):
                if check_line_same_color(image, start, end):
                    pass
