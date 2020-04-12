from typing import *
import board.fields as fields
import board
from PIL import Image
from PIL import ImageGrab
from pynput.mouse import Button, Controller
from time import sleep


def screenshot(start: Optional[Tuple[int, int]] = None,
               end: Optional[Tuple[int, int]] = None
               ) -> Image.Image:
    if start and end:
        image: Image.Image = ImageGrab.grab((*start, *end))
    else:
        image: Image.Image = ImageGrab.grab()
    return image


class AI:
    def __init__(self: "AI"
                 ) -> None:
        screen = screenshot()
        start, end, difficulty = board.find(screen)
        self.board_start: Tuple[int, int] = start
        self.board_end: Tuple[int, int] = end
        self.click_delay = 0.001
        self.animation_delay = 1

        self.board = board.Board(start, end, difficulty)

        self.cursor_resting_point = round(start[0] + self.board.board_width * 0.75), start[1] - 20
        self.mouse = Controller()

    def update(self: "AI"
               ) -> None:
        self.mouse.position = self.cursor_resting_point
        sleep(self.animation_delay)
        image = screenshot(self.board_start, self.board_end)
        self.board.update(image)

    def click(self: "AI",
              key: Tuple[int, int]
              ) -> None:
        self.mouse.position = (sum(pair) for pair in zip(self.board[key].middle, self.board_start))
        sleep(self.click_delay)
        self.mouse.click(Button.left)
        sleep(self.click_delay)

    def mark_as_mine(self, key: Tuple[int, int]) -> None:
        if key not in self.board.mines:
            self.mouse.position = (sum(pair) for pair in zip(self.board[key].middle, self.board_start))
            sleep(self.click_delay)
            self.mouse.click(Button.right)
            sleep(self.click_delay)
            self.board.mark_as_mine(key)

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
        while True:
            # loops over all the numbers on the board and marks green fields as mines if its found to be a mine
            self.update()
            mines = {
                green_field.board_coordinate
                for number in self.board.numbers
                if (nearby_green_fields := self.fields_nearby(number, fields.GreenField))
                if len(nearby_green_fields) == self.board[number].number - len(self.fields_nearby(number, fields.Mine))
                for green_field in nearby_green_fields
            }
            for mine in mines:
                self.mark_as_mine(mine)

            # loops over all of the marked mines on the board and find all nearby numbers
            # loops over all the found nearby numbers and checks how many mines are nearby
            # if there are as many nearby mines as the value of the number all
            # nearby green fields are located and are clicked
            fields_to_click = {
                green_field.board_coordinate
                for mine in self.board.mines
                if (numbers := self.fields_nearby(mine, fields.Number))
                for number in numbers
                if number.number == len(self.fields_nearby(number.board_coordinate, fields.Mine))
                for green_field in self.fields_nearby(number.board_coordinate, fields.GreenField)
            }
            for field in fields_to_click:
                self.click(field)

            if not mines and not fields_to_click:
                break
