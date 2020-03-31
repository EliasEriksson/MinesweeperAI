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
        self.image_coordinate = (x * size, y * size)
        self.board_coordinate = coordnate
        self.size = size
        self.lookup_point = (x * size + 4, y * size + 4)

    @classmethod
    def from_field(cls, field: "Field", *args):
        return cls(field.board_coordinate, field.size, args)

    def __add__(self, pixels: int):
        x, y = self.image_coordinate
        return x + pixels, y + pixels

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"board_coordinate={self.board_coordinate}), "
                f"image_coordinate={self.image_coordinate}")


class GreenField(Field):
    pass


class BeigeField(Field):
    pass


class Number(Field):
    def __init__(self: "Number",
                 coordinate: Tuple[int, int],
                 size: int,
                 number: int,) -> None:
        super(Number, self).__init__(coordinate, size)
        self.mines = number


class Mine(Field):
    pass


if __name__ == '__main__':
    pass
