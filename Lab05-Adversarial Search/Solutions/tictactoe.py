from enum import Enum
from typing import Self


class Symbols(Enum):
    X = "X"
    O = "O"
    UNPLACED = "i"

    def __str__(self):
        return self.value

    @classmethod
    def placed(cls) -> tuple[Self, Self]:
        return cls.X, cls.O


type Board = list[Symbols]


def minmax_decision(state: Board) -> int:
    """
    returns the minimax decision of the opponent
    :param state: State of the checkerboard. Ex: [Unplaced; Unplaced; Unplaced; Unplaced; X; Unplaced; Unplaced; Unplaced; Unplaced]
    :return: int
    """
    def max_value(state_option: Board) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        expected_value = -infinity
        for (a, s) in successors_of(state_option):
            expected_value = max(expected_value, min_value(s))
        return expected_value

    def min_value(state_option: Board) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        expected_value = infinity
        for (a, s) in successors_of(state_option):
            expected_value = min(expected_value, max_value(s))
        return expected_value

    infinity = float('inf')
    action, state = max(successors_of(state), key=lambda a: min_value(a[1]))
    return action
 

def is_terminal(state: Board) -> bool:
    """
    returns True if the state is either a win or a tie (board full)
    :param state: State of the checkerboard. Ex: [Unplaced; Unplaced; Unplaced; Unplaced; X; Unplaced; Unplaced; Unplaced; Unplaced]
    :return: True/False
    """
    return winner_of(state) is not None or is_full_board(state)

def is_full_board(state: Board):
    for i in range(9):
        if state[i] == Symbols.UNPLACED: #not in [Symbols.O, Symbols.X]:
            return False
    return True

def utility_of(state: Board) -> int:
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard. Ex: [Unplaced; Unplaced; Unplaced; Unplaced; X; Unplaced; Unplaced; Unplaced; Unplaced]
    """
    # For this function it might be beneficial to create helper functions to check different aspects of the board.
    # This can help to avoid making this function overly complicated.
    if winner_of(state) == Symbols.X:
        return +1
    elif winner_of(state) == Symbols.O:
        return -1
    else:
        return 0
    
def winner_of(state: Board):
    '''
    Returns 'X' if the first player won the game, 'O' if the second player won
    the game, or None if the game has not finished yet or if it is a tie.
    '''
    # Checks horizontally
    for c in [0, 3, 6]:
        if state[c + 0] == state[c + 1] and state[c + 0] == state[c + 2] and state[c + 0]!=Symbols.UNPLACED:
            return state[c + 0]
    # Checks vertically
    for c in [0, 1, 2]:
        if state[c + 0] == state[c + 3] and state[c + 0] == state[c + 6] and state[c + 0]!=Symbols.UNPLACED:
            return state[c+0]
    # Checks diagonally [\]
    if state[0] == state[4] and state[0] == state[8] and state[0]!=Symbols.UNPLACED:
        return state[4]
    # Checks diagonally [/]
    if state[2] == state[4] and state[2] == state[6] and state[2]!=Symbols.UNPLACED: 
        return state[4]
    return None


def successors_of(state: Board) -> list[tuple[int, Board]]:
    """
    returns a list of tuples (move, state) as shown in the exercise slides
    :param state: State of the checkerboard. Ex: [Unplaced; Unplaced; Unplaced; Unplaced; X; Unplaced; Unplaced; Unplaced; Unplaced]
    :return: [(move, state),...]  
    """
    successors = []
    open = 0
    # How many open spots there are
    for move in range(9):
        if state[move] == Symbols.UNPLACED:
            open += 1
    # Decides which player's turn it is
    if open % 2 == 1:
        player = Symbols.X  # X makes odd numbered moves
    else:
        player = Symbols.O
    # Creates a successor for each available move
    for move in range(9):
        if state[move] == Symbols.UNPLACED:  
            successor = state[:]  # Copy list
            successor[move] = player  # Place the player
            successors.append((move, successor))
    return successors


def display(state: list[Symbols]) -> None:
    print("-----")
    for i in range(0, 3):
        for c in range(i * 3, i * 3 + 3):
            print("|", end="")
            symbol = c if state[c] == Symbols.UNPLACED else state[c]
            print(symbol, end="")
        print("|")


def main():
    board = [Symbols.UNPLACED] * 9
    while not is_terminal(board):
        board[minmax_decision(board)] = Symbols.X
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = Symbols.O   
    display(board) 
    #print("Game is over")  

    result = winner_of(board)
    if result is None:
        print("Game is over. No winner")
    else:
        print("Game is over. The winner is:", result)


if __name__ == '__main__':
    main()
