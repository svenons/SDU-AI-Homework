from collections.abc import Iterable
from typing import Callable

# This is based on the game Nim, where each player must in turn select a pile to split.
# The result of the split must be 2 piles of different sizes
# I dont like this Nim variant, the actual Nim is better.

type Piles = list[int]


def alpha_beta_decision(state: Piles) -> list[int]:
    infinity = float('inf')

    def max_value(state_option: Piles, alpha: float, beta: float) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        expected_value = -infinity
        for successor in successors_of(state_option):
            expected_value = max(expected_value, min_value(successor, alpha, beta))
            if expected_value >= beta:
                return expected_value
            alpha = max(alpha, expected_value)
        return expected_value

    def min_value(state_option: Piles, alpha: float, beta: float) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        expected_value = infinity
        for successor in successors_of(state_option):
            expected_value = min(expected_value, max_value(successor, alpha, beta))
            if expected_value <= alpha:
                return expected_value
            beta = min(beta, expected_value)
        return expected_value

    # Return the state resulting from the best move for MAX
    best_successor = argmax(
        successors_of(state),
        lambda a: min_value(a, -infinity, infinity)
    )
    return best_successor


def is_terminal(state: Piles) -> bool:
    """
    A state is terminal if all piles are of size 1 or 2.
    """
    return all(pile <= 2 for pile in state)


def utility_of(state: Piles) -> int:
    """
    Returns +1 if MIN wins, -1 if MAX wins.
    The player (MIN) moves first.
    If the game ends on MAX's turn, MIN wins (+1).
    If the game ends on MIN's turn, MAX wins (-1).
    """
    # Count of moves made from initial state to now determines whose turn it would have been
    total_moves = count_moves_to_terminal(state)
    if total_moves % 2 == 0:
        return -1  # MAX just played — MIN would have no move
    else:
        return +1  # MIN just played — MAX would have no move


def count_moves_to_terminal(state: Piles) -> int:
    """
    Helper to simulate the game path back to initial move count.
    Total number of splits = number of piles - 1
    """
    return len(state) - 1


def successors_of(state: Piles) -> list[Piles]:
    """
    Given a state, returns all possible successor states (valid splits).
    """
    result = []
    for i, pile in enumerate(state):
        if pile > 2:
            for split in split_pile_options(pile):
                new_state = state[:i] + split + state[i + 1:]
                result.append(new_state)
    return result


def split_pile_options(pile: int) -> list[Piles]:
    """
    Returns all valid 2-part splits of a pile (must be unequal and both > 0).
    """
    options = []
    for i in range(1, pile):
        j = pile - i
        if i != j:
            options.append([i, j])
    return options


def argmax(iterable: Iterable, func: Callable[[Piles], int]):
    return max(iterable, key=func)


def computer_select_pile(state: Piles) -> Piles:
    return alpha_beta_decision(state)


def user_select_pile(list_of_piles: Piles) -> Piles:
    """
    Given a list of piles, asks the user to select a pile and then a split.
    Then returns the new list of piles.
    """
    print("\n    Current piles: {}".format(list_of_piles))

    i = -1
    while i < 0 or i >= len(list_of_piles) or list_of_piles[i] < 3:
        print("What is the number of the pile you want to split?")
        print("The pile must have more than 2 stones")
        print(f"Choose a number between 1 and {len(list_of_piles)}")
        i = -1 + int(input())

    print("Selected pile {}".format(list_of_piles[i]))

    max_split = list_of_piles[i] - 1

    j = 0
    while j < 1 or j > max_split or j == list_of_piles[i] - j:
        print_str = f"Where should the first split be (from 1 to {max_split}"
        if list_of_piles[i] % 2 == 0:
            print_str += f", but not {list_of_piles[i] // 2}"
        print_str += ")?"
        print(print_str)

        j = int(input())

    k = list_of_piles[i] - j

    new_list_of_piles = list_of_piles[:i] + [j, k] + list_of_piles[i + 1:]

    print("    New piles: {}".format(new_list_of_piles))

    return new_list_of_piles


def main():
    # Test with pile size of 15
    print("=== Starting with pile [15] ===")
    play_nim([15])
    print("\n=== Starting with pile [20] ===")
    play_nim([20])


def play_nim(initial_state: Piles):
    state = initial_state

    while not is_terminal(state):
        state = user_select_pile(state)
        if not is_terminal(state):
            state = computer_select_pile(state)
            print("The computer has split a pile")

    print("    Final state is {}".format(state))
    print("    Result: " + ("MIN wins (+1)" if utility_of(state) == 1 else "MAX wins (-1)"))


if __name__ == '__main__':
    main()