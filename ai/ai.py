from typing import *
import board
from PIL import Image
# noinspection PyPep8Naming
import pyscreenshot as ImageGrab
from pynput.mouse import Button, Controller


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

    def solve(self: "AI"
              ):
        while self.board.green_field:
            for key in self.board:
                pass

    def click(self: "AI",
              key: Tuple[int, int]
              ) -> None:
        # TODO implemend field.__add__ to deal with this
        self.mouse.position = self.board[key].middle + self.board_start
        self.mouse.click(Button.left)
