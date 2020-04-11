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
        sleep(0.1)

    def mark_as_mine(self, key: Tuple[int, int]) -> None:
        if key not in self.board.mines:
            self.mouse.position = (sum(pair) for pair in zip(self.board[key].middle, self.board_start))
            self.mouse.click(Button.right)
            self.board.mark_as_mine(key)
            sleep(0.1)

    def fields_nearby(self: "AI",
                      key: Tuple[int, int],
                      field: Type[fields.Field]
                      ) -> List[TypeVar("Field", bound=fields.Field)]:
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
              ) -> None:
        middle = round(self.board.size[0] / 2), round(self.board.size[1] / 2)
        self.click(middle)
        while self.board.green_field.difference(self.board.mines):
            # loops over all the numbers on the board and marks green fields as mines if its found to be a mine
            mines = {
                green_field.board_coordinate
                for number in self.board.numbers
                if (nearby_green_fields := self.fields_nearby(number, fields.GreenField))
                if len(nearby_green_fields) == self.board[number].number - len(self.fields_nearby(number, fields.Mine))  # TODO store Number in self.numbers instead
                for green_field in nearby_green_fields
            }
            [self.mark_as_mine(mine) for mine in mines]

            # loops over all of the marked mines on the board and find all nearby numbers
            # loops over all the found nearby numbers and checks how many mines are nearby
            # if there are as many nearby mines as the value of the number all
            # nearby green fields are located and are clicked
            [
                self.click(green_field.board_coordinate)
                for mine in self.board.mines
                if (numbers := self.fields_nearby(mine, fields.Number))
                for number in numbers
                if number.number == len(self.fields_nearby(number.board_coordinate, fields.Mine))
                for green_field in self.fields_nearby(number.board_coordinate, fields.GreenField)
            ]
            sleep(1)
            self.update()


