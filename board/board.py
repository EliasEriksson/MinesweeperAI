from typing import *
from .field import Field


class Grid:
    def __init__(self, grid: List[List[Field]]) -> None:
        self.grid = grid

    def __getitem__(self, coordinate: Tuple[int, int]) -> Field:
        x, y = coordinate
        return self.grid[x][y]

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}([\n"
                f"{self[0, 0]},\t{self[1, 0]},\t...,\t\t\t\t...\n"
                f"{self[0, 1]},\t...,\t\t\t...,\t\t\t\t{self[-1, -2]}\n"
                f"...,\t\t\t...,\t\t\t{self[-2, -1]},\t{self[-1, -1]}\n"
                f"])")


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
            [Field((x, y), 45 - 5 * difficulty)
             for y in range(0, self.board_height, self.square_size)]
            for x in range(0, self.board_width, self.square_size)
        ])

    def __getitem__(self, coordinate: Tuple[int, int]):
        return self.grid[coordinate]

    def __repr__(self):
        return (f"{self.__class__.__name__}: start={self.start}, end={self.end}, "
                f"width={self.board_width}, height={self.board_height}")


if __name__ == '__main__':
    board = Board((1, 1), (450, 360), 0)
    print(len(board.grid.grid), len(board.grid.grid[0]))
    print(board)
    print(board[9, 7])
