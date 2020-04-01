from typing import *


class Field:
    def __init__(self: "Field",
                 coordnate: Tuple[int, int],
                 size: int,
                 *args) -> None:

        x, y = coordnate
        self.image_coordinate = (x * size, y * size)
        self.board_coordinate = coordnate
        self.size = size
        self.lookup_point = (x * size + 4, y * size + 4)
        self.lookup_area = (*self.lookup_point, x * size + size - 4, y * size + size - 4)
        self.middle = (x * size + (length := round(size / 2)), y * size + length)

    @staticmethod
    def is_green_field():
        return False

    @staticmethod
    def is_beige_field():
        return False

    @staticmethod
    def is_number():
        return False

    @staticmethod
    def is_mine():
        return False

    @classmethod
    def from_field(cls, field: "Field", *args):
        return cls(field.board_coordinate, field.size, args)

    def __eq__(self, other: Type[object]) -> bool:
        return self.__class__.__name__ == other.__name__

    def __hash__(self) -> int:
        return hash(self.board_coordinate)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"board_coordinate={self.board_coordinate}), "
                f"image_coordinate={self.image_coordinate}")


class GreenField(Field):
    @staticmethod
    def is_green_field():
        return True


class BeigeField(Field):
    @staticmethod
    def is_beige_field():
        return True


class Number(Field):
    def __init__(self: "Number",
                 coordinate: Tuple[int, int],
                 size: int,
                 number: int,) -> None:
        super(Number, self).__init__(coordinate, size)
        self.number = number

    @staticmethod
    def is_number():
        return True


class Mine(Field):
    @staticmethod
    def is_mine():
        return True


if __name__ == '__main__':
    pass
