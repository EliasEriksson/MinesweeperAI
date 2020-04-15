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


class Board:
    def __init__(self: "Board",
                 start: Tuple[int, int],
                 end: Tuple[int, int],
                 difficulty: int
                 ) -> None:
        self.start = start
        self.end = end
        self.square_size = 45 - 5 * difficulty
        self.board_width = end[0] - start[0] + 1
        self.board_height = end[1] - start[1] + 1

        self.board = {
            (x, y): fields.GreenField((x, y), self.square_size)
            for y in range(0, int(self.board_height / self.square_size))
            for x in range(0, int(self.board_width / self.square_size))}  # will be redefined after every update
        self.green_field: Set[Tuple[int, int]] = set(self.board.keys())  # will get keys subtracted during runtime
        self.numbers: Set[Tuple[int, int]] = set()
        self.done_numbers: Set[Tuple[int, int]] = set()
        self.beige_fields: Set[Tuple[int, int]] = set()
        self.mines: Set[Tuple[int, int]] = set()
        self.size = max(self.board.keys())

    def update_field(self: "Board",
                     image: Image.Image,
                     field: fields.Field
                     ) -> fields.Field:

        # OBS image must be a cropped image that only holds the game board
        if image.getpixel(field.lookup_point) == 0:
            return field
        else:
            square = image.crop(field.lookup_area)
            number = pytesseract.image_to_string(square, config='--psm 10, -c tessedit_char_whitelist=12345678')
            if number:
                field: fields.Field = fields.Number.from_field(field, int(number))
                self.green_field.remove(field.board_coordinate)
                self.numbers.add(field.board_coordinate)
                return field
            else:
                field = fields.BeigeField.from_field(field)
                self.green_field.remove(field.board_coordinate)
                self.beige_fields.add(field.board_coordinate)
                return field

    def mark_as_mine(self: "Board",
                     key: Tuple[int, int]
                     ) -> None:

        field: fields.Mine = fields.Mine.from_field(self.board[key])
        self.mines.add(field.board_coordinate)
        self.board[key] = field

    def update(self: "Board",
               image: Image.Image
               ) -> None:

        image = filters.field(image)
        for key in self:
            field = self.board[key]
            self.board[key] = self.update_field(image, field)

    def __getitem__(self: "Board",
                    coordinate: Tuple[int, int]
                    ) -> TypeVar("Field", bound=fields.Field):

        return self.board[coordinate]

    def __repr__(self: "Board"
                 ) -> str:

        return (f"{self.__class__.__name__}(start={self.start}, end={self.end}, "
                f"width={self.board_width}, height={self.board_height})")

    def __iter__(self: "Board"
                 ) -> Iterable[Tuple[int, int]]:

        return iter(self.green_field.copy())
