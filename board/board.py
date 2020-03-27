from typing import *


class Field:
    def __init__(self, coordinate: Tuple[int, int]):
        self.coordinate = coordinate


class Grid:
    def __init__(self, grid: List[List[Any]]) -> None:
        self.grid = grid

    def __getitem__(self, coordinate: Tuple[int, int]):
        x, y = coordinate
        return self.grid[x][y]


class Board:
    def __init__(self: "Board",
                 start: Tuple[int, int],
                 end: Tuple[int, int],
                 difficulty: int
                 ) -> None:
        self.start = start
        self.end = end
        self.square_size = 25 + 5 * difficulty
        self.board_width = end[0] - start[0]
        self.board_height = end[1] - start[1]
        self.grid = Grid([
            [Field((x, y)) for x in range(0, self.board_width, self.square_size)]
            for y in range(0, self.board_height, self.square_size)
        ])



