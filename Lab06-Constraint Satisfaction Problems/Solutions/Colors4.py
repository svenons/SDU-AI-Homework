from enum import Enum


class Color(Enum):
    Red = 1
    Green = 2
    Blue = 3
    Yellow = 4

    def __str__(self):
        return self.name