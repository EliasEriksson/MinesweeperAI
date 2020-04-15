from typing import *


class Field:
    def __init__(self: "Field",
                 coordnate: Tuple[int, int],
                 size: int,
                 *args) -> None:

        x, y = coordnate
        fix = 4 if size > 40 else 3
        self.image_coordinate = (x * size, y * size)
        self.board_coordinate = coordnate
        self.size = size
        self.lookup_point = (x * size + fix, y * size + fix)
        self.lookup_area = (*self.lookup_point, x * size + size - fix, y * size + size - fix)
        self.middle = (x * size + (length := round(size / 2)), y * size + length)

    @classmethod
    def from_field(cls: Type["Field"],
                   field: "Field",
                   *args: Any
                   ) -> "Field":

        return cls(field.board_coordinate, field.size, *args)

    def same_name(self, other: Type["Field"]) -> bool:
        return self.__class__.__name__ == other.__name__

    def __eq__(self: "Field",
               other: "Field"
               ) -> bool:
        return self.board_coordinate == other.board_coordinate

    def __hash__(self: "Field"
                 ) -> int:

        return hash(self.board_coordinate)

    def __repr__(self: "Field"
                 ) -> str:

        return f"{self.__class__.__name__}(board_coordinate={self.board_coordinate})"


class GreenField(Field):
    pass


class BeigeField(Field):
    pass


class Number(Field):
    def __init__(self: "Number",
                 coordinate: Tuple[int, int],
                 size: int,
                 number: Tuple[int, ...]
                 ) -> None:

        super(Number, self).__init__(coordinate, size)
        self.number = number


class Mine(Field):
    pass


if __name__ == '__main__':
    pass
