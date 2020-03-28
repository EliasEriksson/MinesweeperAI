from typing import *


class Field:
    def __init__(self, coordinate: Tuple[int, int], size: int) -> None:
        self.coordinate = coordinate
        self.click_coordinate = ((p := round(size / 2)), p)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self.coordinate}"


class Number(Field):
    def __init__(self, coordinate: Tuple[int, int], size: int, number: int) -> None:
        super(Number, self).__init__(coordinate, size)
        self.number = number


class Flag(Field):
    pass
