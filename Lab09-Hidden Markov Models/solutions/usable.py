import numpy as np
from typing import List, Dict

class HiddenMarkovModel:
    def __init__(self, states: List[str], observations: List[str], 
                 initial_probs: Dict[str, float],
                 transition_probs: Dict[str, Dict[str, float]],
                 emission_probs: Dict[str, Dict[str, float]]):
        self.states = states
        self.observations = observations
        self.initial_probs = initial_probs
        self.transition_probs = transition_probs
        self.emission_probs = emission_probs
        self.state_idx = {s: i for i, s in enumerate(states)}

    def forward(self, observed_sequence: List[str]) -> float:
        N = len(self.states)
        T = len(observed_sequence)
        fwd = np.zeros((N, T))

        # Initialize
        for s in self.states:
            i = self.state_idx[s]
            fwd[i][0] = self.initial_probs[s] * self.emission_probs[s][observed_sequence[0]]

        # Induction
        for t in range(1, T):
            for curr in self.states:
                j = self.state_idx[curr]
                fwd[j][t] = sum(
                    fwd[self.state_idx[prev]][t-1] *
                    self.transition_probs[prev][curr] *
                    self.emission_probs[curr][observed_sequence[t]]
                    for prev in self.states
                )

        return sum(fwd[self.state_idx[s]][T-1] for s in self.states)

    def viterbi(self, observed_sequence: List[str]) -> List[str]:
        N = len(self.states)
        T = len(observed_sequence)

        vit = np.zeros((N, T))
        back = np.zeros((N, T), dtype=int)

        # Initialize
        for s in self.states:
            i = self.state_idx[s]
            vit[i][0] = self.initial_probs[s] * self.emission_probs[s][observed_sequence[0]]

        # Recursion
        for t in range(1, T):
            for curr in self.states:
                j = self.state_idx[curr]
                max_prob, max_state = max(
                    (
                        vit[self.state_idx[prev]][t-1] * self.transition_probs[prev][curr],
                        self.state_idx[prev]
                    ) for prev in self.states
                )
                vit[j][t] = max_prob * self.emission_probs[curr][observed_sequence[t]]
                back[j][t] = max_state

        # Termination
        last_state = np.argmax(vit[:, T-1])
        path_idx = [0] * T
        path_idx[T-1] = last_state

        # Backtrace
        for t in range(T-1, 0, -1):
            path_idx[t-1] = back[path_idx[t]][t]

        # Convert to state names
        idx_to_state = {i: s for s, i in self.state_idx.items()}
        return [idx_to_state[i] for i in path_idx]

def run_robot_example():
    states = ["1", "2", "3", "4", "5", "6"]
    observations = ["Ice Cream", "No Movement"]

    initial_probs = {"A": 0.4, "B": 0.4, "C": 0.2}
    transition_probs = {
        "A": {"A": 0.5, "B": 0.25, "C": 0.25},
        "B": {"A": 0.25, "B": 0.5, "C": 0.25},
        "C": {"A": 0.25, "B": 0.25, "C": 0.5},
    }
    emission_probs = {
        "A": {"Movement": 0.9, "No Movement": 0.1},
        "B": {"Movement": 0.6, "No Movement": 0.4},
        "C": {"Movement": 0.2, "No Movement": 0.8},
    }

    observed_sequence = ["Movement", "Movement"]

    hmm = HiddenMarkovModel(states, observations, initial_probs, transition_probs, emission_probs)
    prob = hmm.forward(observed_sequence)
    path = hmm.viterbi(observed_sequence)

    print(f"Forward Probability: {prob:.5f}")
    print(f"Most Likely Path: {path}")

def run_ice_cream_example():
    # States (excluding "initial" and "final" — we model only real states)
    states = ["hot", "cold"]

    # Observations (possible number of ice creams eaten)
    observations = ["1", "2", "3"]

    # Initial probabilities (from "initial" row in original transition matrix)
    initial_probs = {
        "hot": 0.8,
        "cold": 0.2,
    }

    # Transition probabilities (slice from original matrix, skipping initial/final)
    transition_probs = {
        "hot": {"hot": 0.2, "cold": 0.6},
        "cold": {"hot": 0.3, "cold": 0.5},
    }

    # Emission probabilities for each state (from emission matrix)
    emission_probs = {
        "hot": {"1": 0.1, "2": 0.15, "3": 0.75},
        "cold": {"1": 0.8, "2": 0.1, "3": 0.1},
    }

    # Observation sequences (drop None and convert ints to strings)
    observation_sets = [
        ["1", "2", "1", "3", "2", "1"],
    ]

    # Create the HMM
    hmm = HiddenMarkovModel(states, observations, initial_probs, transition_probs, emission_probs)

    # Run each observation sequence
    for obs_seq in observation_sets:
        print(f"Observations: {' '.join(obs_seq)}")
        prob = hmm.forward(obs_seq)
        path = hmm.viterbi(obs_seq)
        print(f"Forward Probability: {prob:.5f}")
        print(f"Most Likely Path: {path}")
        print()

if __name__ == '__main__':
    #run_robot_example()
    run_ice_cream_example()