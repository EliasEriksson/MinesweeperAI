from typing import *
if TYPE_CHECKING:
    from board import Board

# TODO make sure docstrings are up to date


class Field:
    def __init__(self: "Field",
                 coordinate: Tuple[int, int],
                 size: int,
                 *args: Any
                 ) -> None:
        """
        :attr image_coordinate: the top left coordinate of the field on the screenshot
        :attr board_coordinate: the coordinate on the internal board
        :attr size: the with/height of the square in pixels
        :attr lookup_point: the image coordinate where the
        :attr lookup_area: the pixel on the screenshot that is  checked when the field is updated (after being clicked)
        :attr middle: the pixel to click to click the field
        :param coordinate: the coordinate on the board
        :param size: the with/height of the square in pixels
        :param args: additional arguments to support children
        """
        x, y = coordinate
        fix = 4 if size > 40 else 3
        self.image_coordinate = (x * size, y * size)
        self.board_coordinate = coordinate
        self.size = size
        self.lookup_point = (x * size + fix, y * size + fix)
        self.lookup_area = (*self.lookup_point, x * size + size - fix, y * size + size - fix)
        self.middle = (x * size + (length := round(size / 2)), y * size + length)

    def adjacent_fields(self: "Field",
                        board: "Board",
                        field_type: Type["Field"]
                        ) -> Set[TypeVar("Field", bound="Field")]:
        """looks around given coordinate for fields matching `field`'s type

        length of returned list is in range 0-8 inclusive

        looks thru the internal board for types around the given coordinate in all "45 degree angles"
        for a field of the same type as the given field parameter

        :param board:
        :param field_type: type of field to compare
        :return: list of fields of same type as given field parameter
        """
        fields: Set[Field] = set()
        x, y = self.board_coordinate
        if 0 < x:
            if 0 < y:
                field = board[(x - 1, y - 1)]
                if field.same_name(field_type):
                    fields.add(field)
            field = board[(x - 1, y)]
            if field.same_name(field_type):
                fields.add(field)

        if y < board.size[1]:
            if 0 < x:
                field = board[(x - 1, y + 1)]
                if field.same_name(field_type):
                    fields.add(field)
            field = board[(x, y + 1)]
            if field.same_name(field_type):
                fields.add(field)

        if x < board.size[0]:
            if y < board.size[1]:
                field = board[(x + 1, y + 1)]
                if field.same_name(field_type):
                    fields.add(field)
            field = board[(x + 1, y)]
            if field.same_name(field_type):
                fields.add(field)

        if 0 < y:
            if x < board.size[0]:
                field = board[(x + 1, y - 1)]
                if field.same_name(field_type):
                    fields.add(field)
            field = board[(x, y - 1)]
            if field.same_name(field_type):
                fields.add(field)
        return fields

    @classmethod
    def from_field(cls: Type["Field"],
                   field: "Field",
                   *args: Any
                   ) -> "Field":
        """constructs a new Field type from an already existing field

        :param field: the field to construct from
        :param args: additional arguments to support some children
        :return: Field
        """
        return cls(field.board_coordinate, field.size, *args)

    def same_name(self: "Field",
                  other: Type["Field"]
                  ) -> bool:
        """compares the instance class name with a class's class name

        :param other: some uninitiated class
        :return: bool
        """
        return self.__class__.__name__ == other.__name__

    def __eq__(self: "Field",
               other: "Field"
               ) -> bool:
        return self.board_coordinate == other.board_coordinate

    def __hash__(self: "Field"
                 ) -> int:
        """allows the object to be hashable

        mainly implemented to be used in sets
        :return: int
        """
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
                 number: int
                 ) -> None:
        super(Number, self).__init__(coordinate, size)
        self.value = number


class Mine(Field):
    pass


if __name__ == '__main__':
    pass
