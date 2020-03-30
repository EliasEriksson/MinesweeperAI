from typing import *
from PIL import Image
import board.fields as fields
import board.filters as filters
import pytesseract


"""
1: save the whole grid in a dict with x, y coordinates as keys in tuple
2: make sets with keys as well where union and intersect operations can be preformed to
       get intresting keys for the grid dict
3: iterate over returned keys and use on the dict
"""


# def identify_field(image: Image.Image, field: fields.Field) -> fields.Field:
#     if image.getpixel(field.lookup_point) == 0:
#         return field
#     else:
#         square = image.crop(field + field.size)
#         number = pytesseract.image_to_string(square, config='--psm 10')
#         if number:
#             return fields.Number.from_field(field, number)
#         else:
#             return fields.BeigeField.from_field(field)


class Board:
    def __init__(self: "Board",
                 start: Tuple[int, int],
                 end: Tuple[int, int],
                 difficulty: int
                 ) -> None:
        self.start = start
        self.end = end
        self.square_size = 45 - 5 * difficulty
        self.board_width = end[0] - start[0]
        self.board_height = end[1] - start[1]

        # TODO make sure board gets correct coordinates
        self.board = {
            (x, y): fields.GreenField((x, y), self.square_size)
            for y in range(0, int((self.board_height + 1) / self.square_size))
            for x in range(0, int((self.board_width + 1) / self.square_size))}  # will be redefined after every update
        self.keys = set(self.board.keys())  # will not change durring runtime
        self.numbers = set()
        self.beige_fields = set()
        self.mines = set()
        self.green_field = self.keys.copy()  # will get keys subtracted over time durring runtime

    def identify_field(self, image: Image.Image, field: fields.Field) -> fields.Field:
        if image.getpixel(field.lookup_point) == 0:
            return field
        else:
            square = image.crop(field + field.size)
            number = pytesseract.image_to_string(square, config='--psm 10')
            if number:
                self.numbers.add(self.board.pop(field.coordinate))
                return fields.Number.from_field(field, number)
            else:
                self.beige_fields.add(self.board.pop(field.coordinate))
                return fields.BeigeField.from_field(field)

    def is_mine(self, key: Tuple[int, int]) -> None:
        self.board[key] = fields.Mine.from_field(self.board[key])

    def update(self, image: Image.Image) -> None:
        image = filters.field(image)
        for key in self.green_field:
            field = self.board[key]
            self.board[key] = self.identify_field(image, field)

    def __getitem__(self: "Board", coordinate: Tuple[int, int]):
        return self.board[coordinate]

    def __repr__(self: "Board"):
        return (f"{self.__class__.__name__}(start={self.start}, end={self.end}, "
                f"width={self.board_width}, height={self.board_height})")
