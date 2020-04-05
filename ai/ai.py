from typing import *
import board.fields as fields
import board
from PIL import Image
# noinspection PyPep8Naming
import pyscreenshot as ImageGrab
from pynput.mouse import Button, Controller
from time import sleep


def screenshot(start: Optional[Tuple[int, int]] = None,
               end: Optional[Tuple[int, int]] = None
               ) -> Image.Image:
    if start and end:
        image: Image.Image = ImageGrab.grab((*start, *end), backend="scrot")
    else:
        image: Image.Image = ImageGrab.grab(backend="scrot")
    return image


class AI:
    def __init__(self: "AI"
                 ) -> None:
        screen = screenshot()
        start, end, difficulty = board.find(screen)
        self.board_start: Tuple[int, int] = start
        self.board_end: Tuple[int, int] = end

        self.board = board.Board(start, end, difficulty)

        self.mouse = Controller()

    def update(self: "AI"
               ) -> None:
        image = screenshot(self.board_start, self.board_end)
        self.board.update(image)

    def click(self: "AI",
              key: Tuple[int, int]
              ) -> None:
        # TODO implemend field.__add__ to deal with this
        self.mouse.position = (sum(pair) for pair in zip(self.board[key].middle, self.board_start))
        self.mouse.click(Button.left)
        sleep(0.6)
        self.update()

    def fields_nearby(self: "AI",
                      key: Tuple[int, int],
                      field: Type[fields.Field]
                      ) -> List[fields.Field]:
        fields_ = []
        x, y = key
        if 0 < x:
            if 0 < y:
                if (field_ := self.board[(x - 1, y - 1)]) == field:
                    fields_.append(field_)
            if (field_ := self.board[(x - 1, y)]) == field:
                fields_.append(field_)
        if y < self.board.size[1]:
            if 0 < x:
                if (field_ := self.board[(x - 1, y + 1)]) == field:
                    fields_.append(field_)
            if (field_ := self.board[(x, y + 1)]) == field:
                fields_.append(field_)
        if x < self.board.size[0]:
            if y < self.board.size[1]:
                if (field_ := self.board[(x + 1, y + 1)]) == field:
                    fields_.append(field_)
            if (field_ := self.board[(x + 1, y)]) == field:
                fields_.append(field_)
        if 0 < y:
            if x < self.board.size[0]:
                if (field_ := self.board[(x + 1, y - 1)]) == field:
                    fields_.append(field_)
            if (field_ := self.board[(x, y - 1)]) == field:
                fields_.append(field_)
        return fields_

    def solve(self: "AI"
              ):

        middle = round(self.board.size[0] / 2), round(self.board.size[1] / 2)
        self.click(middle)
        while self.board.green_field:
            # noinspection PyTypeChecker
            hungry_numbers: Set[fields.Number] = set(
                nearby_number
                for key in self.board  # keys to green fields
                if (nearby_numbers := self.fields_nearby(key, fields.Number))
                for nearby_number in nearby_numbers
            )
            fields_to_click: Set[fields.GreenField] = {
                green_field
                for number in hungry_numbers
                if (nearby_green_fields := self.fields_nearby(number.board_coordinate, fields.GreenField))
                if len(nearby_green_fields) == number.number
                for green_field in nearby_green_fields
            }
            for green_field in fields_to_click:
                self.click(green_field.middle)


