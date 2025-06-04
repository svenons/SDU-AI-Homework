from enum import Enum


class States(Enum):
    Argentina = 1
    Bolivia = 2
    Brazil = 3
    Chile = 4
    Colombia = 5
    Ecuador = 6
    FrenchGuiana = 7
    Guyana = 8
    Paraguay = 9
    Peru = 10
    Suriname = 11
    Uruguay = 12
    Venezuela = 13

    def __lt__(self, other):
        if type(other) != type(self):
            return False
        return self.value < other.value

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(repr(self))