import numpy as np
from numpy import ndarray

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a description of the number
of ice cream eaten by a boy in the summer.
"""


def main():
    np.set_printoptions(suppress=True)

    states = np.array(["initial", "hot", "cold", "final"])

    # To simulate starting from index 1, we add a dummy value at index 0
    # observation_sets = [
    #     [None, 3, 1, 3],
    #     [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
    #     [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    # ]
    observation_sets = [
        [None, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    ]

    # Markov transition matrix
    #
    # prob_of_next = transitions[current][next]
    # index 0 = start
    # index 1 = hot
    # index 2 = cold
    # index 3 = end      to:  S   h   c   e     from:
    transitions = np.array([[.0, .8, .2, .0],  # Initial state
                            [.0, .2, .6, .2],  # Hot state
                            [.0, .3, .5, .2],  # Cold state
                            [.0, .0, .0, .0],  # Final state
                            ])

    # P(v|q)
    # emission[state][observation]
    # probality_of_this_amount_of_icecreams_given_weather = emission[state (weather)][observation (number of icecreams)]
    #                      0    1   2   3
    emissions = np.array([[.0, .0, .0, .0],  # Initial state
                          [.0, .1, .15, .75],  # Hot state
                          [.0, .8, .1, .1],  # Cold state
                          [.0, .0, .0, .0],  # Final state
                          ])

    for observations in observation_sets:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))

        probability = compute_forward(states, observations, transitions, emissions)
        print("Probability: {}".format(probability))

        path = compute_viterbi(states, observations, transitions, emissions)
        print(f"Path: {convert_path_states_to_observations(path, states)}")

        print('')


def convert_path_states_to_observations(path: list[int], states: ndarray[str]) -> list[str]:
    return [states[p] for p in path]


def inclusive_range(a: int, b: int) -> range:
    return range(a, b + 1)


def compute_forward(states: ndarray, observations: list[int | None], a_transitions: ndarray,
                    b_emissions: ndarray[float]) -> float:
    # number of states - subtract two because "initial" and "final" doesn't count.
    big_n = len(states) - 2

    # number of observations - subtract one, because a dummy "None" is added on index 0.
    big_t = len(observations) - 1

    # final state
    qf: int = big_n + 1

    # probability matrix - all values initialized to 5, as 0 has meaning in the matrix
    # forward[state][time] will hold the total probability of being in `state` at time `t`,
    # having observed all previous emissions up to time `t`.
    forward: ndarray = np.ones((big_n + 2, big_t + 1)) * 5

    # ----------------------------------------
    # Step 1: Initialization (t = 1)
    # ----------------------------------------

    # Looping over the states - which are 1 or 2 in the states array
    for state in range(1, big_n + 1): 
        # a_transitions[0][state]: probability of transitioning from start to this state
        # b_emissions[state][observations[1]]: probability this state emits the first observed value (like 3 ice creams)
        # forward[state][1]: total probability of being in this state at time 1, after seeing the first observation
        forward[state][1] = a_transitions[0][state] * b_emissions[state][observations[1]]

    # ----------------------------------------
    # Step 2: Induction (t = 2 to T)
    # ----------------------------------------

    for t in range(2, big_t + 1):  # Loop over time steps
        for state in range(1, big_n + 1):  # Loop over current states
            # For each current state at time t:
            # Sum over all paths from previous states to this state
            # forward[prev_state][t - 1]: probability of being in prev_state at t-1
            # a_transitions[prev_state][state]: transition probability to current state
            # b_emissions[state][observations[t]]: emission probability of current observation
            forward[state][t] = sum(
                forward[prev_state][t - 1] *
                a_transitions[prev_state][state] *
                b_emissions[state][observations[t]]
                for prev_state in range(1, big_n + 1)
            )

    # ----------------------------------------
    # Step 3: Termination - sum probabilities ending in each real state
    # and transitioning into the final state
    # ----------------------------------------

    return sum(
        forward[state][big_t] * a_transitions[state][qf]
        for state in range(1, big_n + 1)
    )

def compute_viterbi(states: ndarray, observations: list[int | None], a_transitions: ndarray, b_emissions: ndarray):
    # ----------------------------------------
    # Setup: Get number of real states (HOT, COLD) and time steps (observations)
    # ----------------------------------------

    big_n = len(states) - 2       # Exclude "initial" and "final"
    big_t = len(observations) - 1 # Exclude dummy value at index 0

    qf = big_n + 1                # Index of the "final" state

    # ----------------------------------------
    # Initialize matrices for Viterbi values and backpointers
    # ----------------------------------------

    # viterbi[state][time]: highest probability of a path that ends at this state at this time
    viterbi = np.ones((big_n + 2, big_t + 1)) * 5  # Avoid using 0 as it's a valid probability

    # backpointers[state][time]: which previous state gave us the highest probability at this time
    backpointers = np.ones((big_n + 2, big_t + 1), dtype=int) * 5

    # ----------------------------------------
    # Step 1: Initialization (t = 1)
    # ----------------------------------------

    for state in range(1, big_n + 1):  # HOT = 1, COLD = 2
        # Transition from START (index 0) to this state
        # Multiply by emission probability of observing the first value from this state
        viterbi[state][1] = a_transitions[0][state] * b_emissions[state][observations[1]]

    # ----------------------------------------
    # Step 2: Recursion (t = 2 to T)
    # ----------------------------------------

    for t in range(2, big_t + 1):  # For each time step (from 2 to T)
        for s in range(1, big_n + 1):  # For each current state s (HOT or COLD)
            # Calculate max probability of reaching this state s from any previous state
            # viterbi[prev][t-1] = best path to prev state
            # a_transitions[prev][s] = transition from prev → current
            # b_emissions[s][obs] = emission of current observation from state s
            viterbi[s][t] = max(
                viterbi[prev_state][t - 1] *
                a_transitions[prev_state][s] *
                b_emissions[s][observations[t]]
                for prev_state in range(1, big_n + 1)
            )

            # Store which previous state gave us the max probability
            # This will help reconstruct the best path later
            backpointers[s][t] = argmax(
                (prev_state,
                 viterbi[prev_state][t - 1] * a_transitions[prev_state][s])
                for prev_state in range(1, big_n + 1)
            )

    # ----------------------------------------
    # Step 3: Termination - Find best last state
    # ----------------------------------------

    # At the final time step, consider the transition from each real state to the final state
    # Multiply viterbi[state][T] by a_transitions[state][final]
    last_probabilities = [
        (s, viterbi[s][big_t] * a_transitions[s][qf])
        for s in range(1, big_n + 1)
    ]

    # Choose the state with the highest final probability
    best_last_state = argmax(last_probabilities)

    # ----------------------------------------
    # Step 4: Backtrace - Reconstruct most likely path
    # ----------------------------------------

    # path[t] will hold the best state at time t
    path = [0] * (big_t + 1)  # Include index 0 for dummy alignment

    # Set the final state in the path
    path[big_t] = best_last_state

    # Follow backpointers from the last state to reconstruct the full path
    for t in range(big_t, 1, -1):
        # At time t, look back to where we came from
        path[t - 1] = backpointers[path[t]][t]

    # Return path starting from time 1 (skip index 0)
    return path[1:]

def argmax(sequence: list[tuple[float, float]]):
    '''
    This takes in a list, that provides its own keys as tuples.
    As such the following must hold true:
    sequence[i] = tuple(key, value)
    '''
    # I have rewritten this function slightly, to make it make better sense in my head
    return max(sequence, key=lambda x: x[1])[0]


if __name__ == '__main__':
    main()
