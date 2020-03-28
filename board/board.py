from typing import *
from .field import Field, GreenField
from PIL import Image

"""
1: save the whole grid in a dict with x, y coordinates as keys in tuple
2: make sets with keys as well where union and intersect operations can be preformed to
       get intresting keys for the grid dict
3: iterate over returned keys and use on the dict
"""




class Grid:
    def __init__(self: "Grid", grid: List[List[Field]]) -> None:
        self.grid = grid

    def __getitem__(self: "Grid", coordinate: Tuple[int, int]) -> Field:
        x, y = coordinate
        return self.grid[x][y]

    def __repr__(self: "Grid") -> str:
        return f"{self.__class__.__name__}({self.grid})"


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
        self.grid = Grid([
            [GreenField((x, y), 45 - 5 * difficulty)
             for y in range(0, self.board_height, self.square_size)]
            for x in range(0, self.board_width, self.square_size)
        ])
        self.numbers = []
        self.beige_fields = []
        self.mines = []

    def update_grid(self, image: Image.Image, clicked: Tuple[int, int]) -> None:
        # clicked is not pixels
        pass

    def __getitem__(self: "Board", coordinate: Tuple[int, int]):
        return self.grid[coordinate]

    def __repr__(self: "Board"):
        return (f"{self.__class__.__name__}: start={self.start}, end={self.end}, "
                f"width={self.board_width}, height={self.board_height}")


if __name__ == '__main__':
    board = Board((1, 1), (450, 360), 0)
    print(len(board.grid.grid), len(board.grid.grid[0]))
    print(board)
    print(board[9, 7])
