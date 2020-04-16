from typing import *
from board.fields import GreenField, Mine, Number, Field
import board
from pynput.mouse import Button, Controller
from PIL import ImageGrab
from PIL import Image
from time import sleep


def screenshot(start: Optional[Tuple[int, int]] = None,
               end: Optional[Tuple[int, int]] = None
               ) -> Image.Image:
    """takes a screenshot and crops it to start and end

    :param start: top left of the crop
    :param end: bottom right of the crop
    :return: Image.Image
    """
    if start and end:
        image: Image.Image = ImageGrab.grab((*start, *end))
    else:
        image: Image.Image = ImageGrab.grab()
    return image


class AI:
    def __init__(self: "AI"
                 ) -> None:
        """
        :attr start: the pixel position where the game board starts on screen.
        :attr end: the pixel position where the game board ends on screen.
        :attr click_delay: a safety delay to make sure the click occurs on the cursors position.
        :attr animation_delay: the animation of a clicked block being destroyed in to small particles.
        :attr board: instance of Board.
        :attr cursor_resting_point: a place for the cursor to be when a new screenshot is taken.
        :attr mouse: mouse controls.
        """
        screen = screenshot()
        start, end, difficulty = board.find(screen)
        self.start: Tuple[int, int] = start
        self.end: Tuple[int, int] = end
        self.click_delay = 0.005
        self.animation_delay = 1
        self.board = board.Board(start, end, difficulty)
        self.cursor_resting_point = round(start[0] + self.board.board_width * 0.75), start[1] - 20
        self.mouse = Controller()

    def update(self: "AI"
               ) -> None:
        """takes a new screenshot and updates the board

        with the given screenshot the board will get updated where the algorithm have not yet determined
        mine, beige field or a number
        :return: None
        """
        self.mouse.position = self.cursor_resting_point
        sleep(self.animation_delay)
        image = screenshot(self.start, self.end)
        self.board.update(image)

    def click(self: "AI",
              field: Field
              ) -> None:
        """clicks a coordinate on the board

        adds the starting point of the board and height/width of the board to determine where
        to place the mouse and then left click
        delay is in place to make sure the mouse doesnt slide when it is clicking

        :param field: game board field (not pixels)
        :return: None
        """
        self.mouse.position = (sum(pair) for pair in zip(field.middle, self.start))
        sleep(self.click_delay)
        self.mouse.click(Button.left)
        sleep(self.click_delay)

    def mark_as_mine(self: "AI",
                     field: GreenField
                     ) -> None:
        """marks a field on given coordinate to be a mine (flag it)

        this is only for visuals, all calls to this methods can be removed

        adds the starting point of the board and height/width of the board to determine where
        to place the mouse and then click

        :param field: a board coordinate (not pixels)
        :return: None
        """
        if field not in self.board.mines:
            self.mouse.position = (sum(pair) for pair in zip(field.middle, self.start))
            sleep(self.click_delay)
            self.mouse.click(Button.right)
            sleep(self.click_delay)
            self.board.mark_as_mine(field)

    def fields_nearby(self: "AI",
                      field: Field,
                      field_type: Type[Field]
                      ) -> Set[TypeVar("Field", bound=Field)]:
        """looks around given coordinate for fields matching `field`'s type

        length of returned list is in range 0-8 inclusive

        looks thru the internal board for types around the given coordinate in all "45 degree angles"
        for a field of the same type as the given field parameter

        :param field:
        :param field_type: type of field to compare
        :return: list of fields of same type as given field parameter
        """
        # TODO move this method to the Field class instead. board coordinate should nto be used outside of the class
        fields_ = set()
        x, y = field.board_coordinate
        if 0 < x:
            if 0 < y:
                field_ = self.board[(x - 1, y - 1)]
                if field_.same_name(field_type):
                    fields_.add(field_)
            field_ = self.board[(x - 1, y)]
            if field_.same_name(field_type):
                fields_.add(field_)

        if y < self.board.size[1]:
            if 0 < x:
                field_ = self.board[(x - 1, y + 1)]
                if field_.same_name(field_type):
                    fields_.add(field_)
            field_ = self.board[(x, y + 1)]
            if field_.same_name(field_type):
                fields_.add(field_)

        if x < self.board.size[0]:
            if y < self.board.size[1]:
                field_ = self.board[(x + 1, y + 1)]
                if field_.same_name(field_type):
                    fields_.add(field_)
            field_ = self.board[(x + 1, y)]
            if field_.same_name(field_type):
                fields_.add(field_)

        if 0 < y:
            if x < self.board.size[0]:
                field_ = self.board[(x + 1, y - 1)]
                if field_.same_name(field_type):
                    fields_.add(field_)
            field_ = self.board[(x, y - 1)]
            if field_.same_name(field_type):
                fields_.add(field_)
        return fields_

    def advanced_algorithm(self):
        """a more advanced algorithm that utilises 2 numbers with common green fields

        :return: None
        """
        fields_to_click = set()
        fields_to_mark = set()
        for number in self.board.numbers.copy():
            number_green_fields = self.fields_nearby(number, GreenField)
            if number_green_fields:
                numbers_mines = self.fields_nearby(number, Mine)
                adjacent_numbers = self.fields_nearby(number, Number)
                for adjacent_number in adjacent_numbers:
                    adjacent_number_green_fields = self.fields_nearby(adjacent_number, GreenField)
                    adjacent_number_mines = self.fields_nearby(adjacent_number, Mine)
                    common_green_fields = adjacent_number_green_fields.intersection(number_green_fields)
                    if common_green_fields:
                        if adjacent_number.value - len(adjacent_number_mines) == 1:
                            if number.value - 1 - len(numbers_mines) == 1:
                                if len(number_green_fields) - len(common_green_fields) == 1:
                                    to_mark = number_green_fields.difference(adjacent_number_green_fields)
                                    to_click = adjacent_number_green_fields.difference(number_green_fields)
                                    if to_click:
                                        fields_to_click.update(to_click)
                                    if to_mark:
                                        fields_to_mark.update(to_mark)
                    if common_green_fields == number_green_fields:
                        action_fields = adjacent_number_green_fields.difference(number_green_fields)
                        if action_fields:
                            if adjacent_number.value - len(adjacent_number_mines) == 1:
                                fields_to_click.update(action_fields)
                            elif len(action_fields) == 1:
                                fields_to_mark.update(action_fields)
            else:
                self.board.done_numbers.add(number)
                self.board.numbers.remove(number)

        for field_to_click in fields_to_click:
            self.click(field_to_click)
        for field_to_mark in fields_to_mark:
            self.mark_as_mine(field_to_mark)
        if fields_to_click or fields_to_mark:
            return True
        return False

    def solve(self: "AI"
              ) -> None:
        """entry point for solving the board

        initializes with clicking the middle of the board
        and update the internal board.

        finds guaranteed mines based on a single number and its neighbouring green fields,
        if a number is equal to green fields + already marked mines the remaining green fields are mines.
        eg: if 1 have 1 green field neighbouring it must be a mine.
        eg: if 2 have 1 green field and one mine neighbouring the green field must also be a mine.

        clicks guaranteed non mines based on a single mines neighbouring number, if a number is "full of mines"
        and have remaining green fields, the remaining green fields will be clicked.
        eg: if a 1 is neighbouring 1 mine and 2 green fields the green fields cant be mines.

        :return: None
        """
        middle = round(self.board.size[0] / 2), round(self.board.size[1] / 2)
        self.click(self.board[middle])

        while True:
            self.update()
            mines: Set[GreenField] = set()
            for number in self.board.numbers.copy():
                adjacent_green_fields = self.fields_nearby(number, GreenField)
                if adjacent_green_fields:
                    if len(adjacent_green_fields) == number.value - len(self.fields_nearby(number, Mine)):
                        mines.update(adjacent_green_fields)
                else:
                    self.board.done_numbers.add(number)
                    self.board.numbers.remove(number)

            for mine in mines:
                self.mark_as_mine(mine)

            fields_to_click: Set[GreenField] = set()
            for mine in self.board.mines:
                numbers = self.fields_nearby(mine, Number)
                for number in numbers:
                    if number.value == len(self.fields_nearby(number, Mine)):
                        fields_to_click.update(self.fields_nearby(number, GreenField))

            for field in fields_to_click:
                self.click(field)

            if not mines and not fields_to_click:
                if not self.advanced_algorithm():
                    break


if __name__ == '__main__':
    print(AI.__init__.__doc__)
