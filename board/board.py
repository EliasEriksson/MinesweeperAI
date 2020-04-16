from typing import *
from board.fields import GreenField, Mine, Number, Field
import board.filters as filters
import board.fields as fields
from PIL import Image
import pytesseract

# TODO make sure doc strings are up to date


class Board:
    def __init__(self: "Board",
                 start: Tuple[int, int],
                 end: Tuple[int, int],
                 difficulty: int
                 ) -> None:
        """
        :attr start: the top left corner of the game board on the screenshot in pixels
        :attr end: the bottom right corner of the game board on the screenshot in pixels
        :attr square_size: the width and height of the fields squares in pixels
        :attr board_width: the width of the game board on the screenshot in pixels
        :attr board_height: the height of the game board on the screenshot in pixels
        :param start: the top left corner of the game board on the screenshot in pixels
        :param end: the bottom right corner of the game board on the screenshot in pixels
        :param difficulty: the difficulty of the game board
        """
        self.start = start
        self.end = end
        self.square_size = 45 - 5 * difficulty
        self.board_width = end[0] - start[0] + 1
        self.board_height = end[1] - start[1] + 1

        self.board: Dict[Tuple[int, int], Field] = {
            (x, y): fields.GreenField((x, y), self.square_size)
            for y in range(0, int(self.board_height / self.square_size))
            for x in range(0, int(self.board_width / self.square_size))}

        self.green_fields: Set[GreenField] = {
            value for value in self.board.values()}

        self.numbers: Set[Number] = set()
        self.done_numbers: Set[Number] = set()
        self.mines: Set[Mine] = set()
        self.size: Tuple[int, int] = max(self.board.keys())

    def update_field(self: "Board",
                     image: Image.Image,
                     field: GreenField
                     ) -> None:
        """updates one field on the game board

        :param image: an image of only the game board
        :param field: a green field on the board
        :return: None
        """
        if image.getpixel(field.lookup_point) == 0:
            return
        else:
            square = image.crop(field.lookup_area)
            number = pytesseract.image_to_string(square, config='--psm 10, -c tessedit_char_whitelist=12345678')
            if number:
                self.green_fields.remove(field)
                field = fields.Number.from_field(field, int(number))
                self.numbers.add(field)
            else:
                self.green_fields.remove(field)
                field = fields.BeigeField.from_field(field)
        self.board[field.board_coordinate] = field

    def mark_as_mine(self: "Board",
                     field: GreenField
                     ) -> None:
        """marks a green field on the board as a mine

        :param field: a green field to be made a Mine instead
        :return: None
        """
        field: fields.Mine = fields.Mine.from_field(field)
        self.mines.add(field)
        self.board[field.board_coordinate] = field

    def update(self: "Board",
               image: Image.Image
               ) -> None:
        """updates all the GreenFields on the board

        :param image: a screenshot of the board
        :return: None
        """
        image = filters.field(image)
        for field in self.green_fields.copy():
            self.update_field(image, field)

    def __getitem__(self: "Board",
                    coordinate: Tuple[int, int]
                    ) -> TypeVar("Field", bound=fields.Field):
        return self.board[coordinate]

    def __repr__(self: "Board"
                 ) -> str:
        return (f"{self.__class__.__name__}(start={self.start}, end={self.end}, "
                f"width={self.board_width}, height={self.board_height})")
