from typing import *


class Field:
    def __init__(self: "Field",
                 coordnate: Tuple[int, int],
                 size: int,
                 *args) -> None:
        """

        :param coordnate: coordinate on the image
        :param size:
        :param args:
        """
        x, y = coordnate
        self.coordinate = coordnate
        self.size = size
        self.lookup_point = (x + 2, y + 2)

    @classmethod
    def from_field(cls, field: "Field", *args):
        cls(field.coordinate, field.size, args)

    def __add__(self, pixels: int):
        x, y = self.coordinate
        return x + pixels, y + pixels

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self.coordinate}"


class GreenField(Field):
    def __init__(self: "GreenField",
                 coordinate: Tuple[int, int],
                 size: int):
        super(GreenField, self).__init__(coordinate, size)


class BeigeField(Field):
    def __init__(self: "BeigeField",
                 coordinate: Tuple[int, int],
                 size: int) -> None:
        super(BeigeField, self).__init__(coordinate, size)


class Number(Field):
    def __init__(self: "Number",
                 coordinate: Tuple[int, int],
                 size: int,
                 number: int,) -> None:
        super(Number, self).__init__(coordinate, size)
        self.mines = number


class Mine(Field):
    def __init__(self: "Mine",
                 coordinate: Tuple[int, int],
                 size: int) -> None:
        super(Mine, self).__init__(coordinate, size)


if __name__ == '__main__':
    pass
