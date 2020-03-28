from typing import *


class Field:
    def __init__(self, coordinate: Tuple[int, int]) -> None:
        self.coordinate = coordinate
        self.click_coordinate = ()

    def is_clickable(self) -> bool:
        return True if self.click_coordinate else False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self.coordinate}"


class GreenField(Field):
    def __init__(self, coordinate: Tuple[int, int], size: int):
        super(GreenField, self).__init__(coordinate)
        x, y = coordinate
        self.click_coordinate = (x + (p := round(size / 2)), y + p)


class BeigeField(Field):
    def __init__(self, coordinate: Tuple[int, int]):
        super(BeigeField, self).__init__(coordinate)


class Number(Field):
    def __init__(self, coordinate: Tuple[int, int], number: int) -> None:
        super(Number, self).__init__(coordinate)
        self.mines = number


class Mine(Field):
    def __init__(self, coordinate: Tuple[int, int]):
        super(Mine, self).__init__(coordinate)


if __name__ == '__main__':
    field = BeigeField((50, 250))