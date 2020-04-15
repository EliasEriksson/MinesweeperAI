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
        """

        :var self.start: the pixel position where the game board starts on screen.
        :var self.end: the pixel position where the game board ends on screen.
        :var self.click_delay: a safety delay to make sure the click occurs on the cursors position.
        :var self.animation_delay: the animation of a clicked block being destroyed in to small particles.
        :var self.board: instance of Board.
        :var self.cursor_resting_point: a place for the cursor to be when a new screenshot is taken.
        :var self.mouse: mouse controls.
        """
        screen = screenshot()
        start, end, difficulty = board.find(screen)
        self.start: Tuple[int, int] = start
        self.end: Tuple[int, int] = end
        # a safety delay to make sure the click occurs on the cursors position
        self.click_delay = 0.005
        # the animation of a clicked block being destroyed in to small particles. screws with the image processing
        self.animation_delay = 1

        self.board = board.Board(start, end, difficulty)

        self.cursor_resting_point = round(start[0] + self.board.board_width * 0.75), start[1] - 20
        self.mouse = Controller()

    def update(self: "AI"
               ) -> None:
        """
        takes a new screenshot and updates the board

        with the given screenshot the board will get updated where the algorithm have not yet determined
        mine, beige field or a number
        :return: None
        """
        self.mouse.position = self.cursor_resting_point
        sleep(self.animation_delay)
        image = screenshot(self.start, self.end)
        self.board.update(image)

    def click(self: "AI",
              key: Tuple[int, int]
              ) -> None:
        """
        clicks a coordinate on the board

        adds the starting point of the board and height/width of the board to determine where
        to place the mouse and then left click
        delay is in place to make sure the mouse doesnt slide when it is clicking

        :param key: a board coordinate (not pixels)
        :return: None
        """
        self.mouse.position = (sum(pair) for pair in zip(self.board[key].middle, self.start))
        sleep(self.click_delay)
        self.mouse.click(Button.left)
        sleep(self.click_delay)

    def mark_as_mine(self: "AI",
                     key: Tuple[int, int]
                     ) -> None:
        """
        marks a field on given coordinate to be a mine (flag it)

        this is only for visuals, all calls to this methods can be removed

        adds the starting point of the board and height/width of the board to determine where
        to place the mouse and then click

        :param key: a board coordinate (not pixels)
        :return: None
        """
        if key not in self.board.mines:
            self.mouse.position = (sum(pair) for pair in zip(self.board[key].middle, self.start))
            sleep(self.click_delay)
            self.mouse.click(Button.right)
            sleep(self.click_delay)
            self.board.mark_as_mine(key)

    def fields_nearby(self: "AI",
                      key: Tuple[int, int],
                      field: Type[fields.Field]
                      ) -> Set[TypeVar("Field", bound=fields.Field)]:
        """
        looks around given coordinate for fields matching `field`'s type

        length of returned list is in range 0-8 inclusive

        looks thru the internal board for types around the given coordinate in all "45 degree angles"
        for a field of the same type as the given field parameter

        :param key: board coordinate
        :param field: field class to compare with
        :return: list of fields of same type as given field parameter
        """
        fields_ = set()
        x, y = key
        if 0 < x:
            if 0 < y:
                field_ = self.board[(x - 1, y - 1)]
                if field_.same_name(field):
                    fields_.add(field_)
            field_ = self.board[(x - 1, y)]
            if field_.same_name(field):
                fields_.add(field_)

        if y < self.board.size[1]:
            if 0 < x:
                field_ = self.board[(x - 1, y + 1)]
                if field_.same_name(field):
                    fields_.add(field_)
            field_ = self.board[(x, y + 1)]
            if field_.same_name(field):
                fields_.add(field_)

        if x < self.board.size[0]:
            if y < self.board.size[1]:
                field_ = self.board[(x + 1, y + 1)]
                if field_.same_name(field):
                    fields_.add(field_)
            field_ = self.board[(x + 1, y)]
            if field_.same_name(field):
                fields_.add(field_)

        if 0 < y:
            if x < self.board.size[0]:
                field_ = self.board[(x + 1, y - 1)]
                if field_.same_name(field):
                    fields_.add(field_)
            field_ = self.board[(x, y - 1)]
            if field_.same_name(field):
                fields_.add(field_)
        return fields_

    def advanced_algorithm(self):
        fields_to_click = set()
        fields_to_mark = set()
        for number in self.board.numbers:
            number = self.board[number]
            number_green_fields = self.fields_nearby(number.board_coordinate, fields.GreenField)
            if number_green_fields:
                numbers_mines = self.fields_nearby(number.board_coordinate, fields.Mine)
                adjacent_numbers = self.fields_nearby(number.board_coordinate, fields.Number)
                for adjacent_number in adjacent_numbers:
                    adjacent_number_green_fields = self.fields_nearby(adjacent_number.board_coordinate, fields.GreenField)
                    adjacent_number_mines = self.fields_nearby(adjacent_number.board_coordinate, fields.Mine)
                    common_greenfields = adjacent_number_green_fields.intersection(number_green_fields)
                    if common_greenfields:
                        if adjacent_number.number - len(adjacent_number_mines) == 1:
                            if number.number - 1 - len(numbers_mines) == 1:
                                if len(number_green_fields) - len(common_greenfields) == 1:
                                    to_mark = number_green_fields.difference(adjacent_number_green_fields)
                                    to_click = adjacent_number_green_fields.difference(number_green_fields)
                                    if to_click:
                                        fields_to_click.update(to_click)
                                    if to_mark:
                                        fields_to_mark.update(to_mark)
                    if common_greenfields == number_green_fields:
                        action_fields = adjacent_number_green_fields.difference(number_green_fields)
                        if action_fields:
                            if adjacent_number.number - len(adjacent_number_mines) == 1:
                                fields_to_click.update(action_fields)
                            elif len(action_fields) == 1:
                                fields_to_mark.update(action_fields)
        for field_to_click in fields_to_click:
            self.click(field_to_click.board_coordinate)
        for field_to_mark in fields_to_mark:
            self.mark_as_mine(field_to_mark.board_coordinate)
        if fields_to_click or fields_to_mark:
            return True
        return False

    def solve(self: "AI"
              ) -> None:
        """
        entry point for solving the board

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
        self.click(middle)
        while True:
            # updates the screen from previous moves
            self.update()
            # loops over all the numbers on the board
            # marks green fields as mines if its found to be a mine described in function doc string
            mines = {
                green_field.board_coordinate
                for number in self.board.numbers
                if (nearby_green_fields := self.fields_nearby(number, fields.GreenField))
                if len(nearby_green_fields) == self.board[number].number - len(self.fields_nearby(number, fields.Mine))
                for green_field in nearby_green_fields
            }

            # mark the mines visually with a flag (can be removed sadly)
            for mine in mines:
                self.mark_as_mine(mine)

            # loops over all of the marked mines on the board and find all nearby numbers
            # loops over all the found nearby numbers and checks how many mines are nearby
            # if there are as many nearby mines as the value of the number all
            fields_to_click = {
                green_field.board_coordinate
                for mine in self.board.mines
                if (numbers := self.fields_nearby(mine, fields.Number))
                for number in numbers
                if number.number == len(self.fields_nearby(number.board_coordinate, fields.Mine))
                for green_field in self.fields_nearby(number.board_coordinate, fields.GreenField)
            }

            # nearby green fields are located and are clicked
            for field in fields_to_click:
                self.click(field)

            # if no mines were found nor there were anywhere to click there wont be any change in next
            # iteration and might as well exit as the algorithm will not find anything more
            if not mines and not fields_to_click:
                if not self.advanced_algorithm():
                    break


if __name__ == '__main__':
    print(AI.__init__.__doc__)
