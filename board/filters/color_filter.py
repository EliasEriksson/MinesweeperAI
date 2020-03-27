from typing import *
from PIL import Image


def line_is_color(image: Image.Image,
                  start: Tuple[int, int],
                  end: Tuple[int, int],
                  color: tuple,
                  ) -> bool:
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
    (x1, y1), (x2, y2) = start, end

    for i, x in enumerate(range(x1, x2, square_size)):
        color = image.getpixel((x, y1)) if i % 2 == 0 else image.getpixel((x + square_size - 1, y1))
        if not line_is_color(image, (x, y1), (x + square_size, y1), color):
            return False

        color = image.getpixel((x, y2)) if i % 2 == 0 else image.getpixel((x + square_size - 1, y2))
        if not line_is_color(image, (x, y2), (x + square_size, y2), color):
            return False

    for i, y in enumerate(range(y1, y2, square_size)):
        color = image.getpixel((x1, y)) if i % 2 == 0 else image.getpixel((x1, y + square_size - 1))
        if not line_is_color(image, (x1, y), (x1, y + square_size), color):
            return False

        color = image.getpixel((x2, y)) if i % 2 == 0 else image.getpixel((x2, y + square_size - 1))
        if not line_is_color(image, (x2, y), (x2, y + square_size), color):
            return False

    return True


def color_filter(image: Image.Image,
                 *boards: Tuple[Tuple[int, int], Tuple[int, int], int],
                 ) -> List[Tuple[Tuple[int, int], Tuple[int, int], int]]:
    return [
        (start, end, difficulty)
        for (x1, y1), (x2, y2), difficulty in boards
        if outline_is_grid(image, (start := (x1, y1)), (end := (x2, y2)), 45 - 5 * difficulty)  # if grid pattern
        if line_is_color(image, (x1, y1 - 1), (x2, y1 - 1), image.getpixel((x1, y1 - 1)))  # if menu header
        if image.getpixel((x1, y1 - 1)) != image.getpixel((x1 - 1, y1 - 1))  # left of menu not same color as menu
        if image.getpixel((x2, y1 - 1)) != image.getpixel((x2 + 1, y1 - 1))  # right of menu not same color as menu
    ]


