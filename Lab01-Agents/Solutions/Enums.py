from enum import Enum, auto


class States(Enum):
    CLEAN = auto()
    DIRTY = auto()
    UNKNOWN = auto()

    def __repr__(self):
        cls_name = self.__class__.__name__
        # return f'{cls_name}.{self.name}'
        return self.name


class Action(Enum):
    SUCK = auto()
    RIGHT = auto()
    LEFT = auto()
    DOWN = auto()
    UP = auto()
    NO_OP = auto()

    def __repr__(self):
        cls_name = self.__class__.__name__
        # return f'{cls_name}.{self.name}'
        return self.name


class Location(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    UNKNOWN = auto()

    def allowed_moves(self) -> tuple[Action, ...]:
        always_allowed = Action.NO_OP, Action.SUCK  # Tuple
        if self == Location.A:
            return Action.RIGHT, *always_allowed  # * provides Tuple unpacking, which we directly pack back into a tuple alongside Action.RIGHT
        if self == Location.B:
            return Action.DOWN, *always_allowed
        if self == Location.C:
            return Action.LEFT, *always_allowed
        if self == Location.D:
            return Action.UP, *always_allowed
        return always_allowed

    def __repr__(self):
        cls_name = self.__class__.__name__
        # return f'{cls_name}.{self.name}'
        return self.name


type LocationState = tuple[Location, States]
