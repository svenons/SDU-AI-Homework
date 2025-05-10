"""
A∨B means A is true, or B is true, or both, so A∨B = 1 - P(A)P(B)
A∧B: Both A and B happen at the same time.
"""

class ProbabilityRelations:
    def __init__(self, p_A: float, p_B: float):
        self.p_A = p_A
        self.p_B = p_B

    def range_for_and(self):
        """
        Returns the valid range for P(A ∧ B) given P(A) and P(B).
        """
        min_and = max(0, self.p_A + self.p_B - 1)
        max_and = min(self.p_A, self.p_B)
        return min_and, max_and

    def range_for_or(self):
        """
        Returns the valid range for P(A ∨ B) given P(A) and P(B).
        """
        min_or = max(self.p_A, self.p_B)
        max_or = min(1, self.p_A + self.p_B)
        return min_or, max_or

    def compute_and_given_or(self, p_or: float):
        """
        Computes P(A ∧ B) if P(A ∨ B) is known.
        """
        return self.p_A + self.p_B - p_or

    def compute_or_given_and(self, p_and: float):
        """
        Computes P(A ∨ B) if P(A ∧ B) is known.
        """
        return self.p_A + self.p_B - p_and


if __name__ == "__main__":
    rel = ProbabilityRelations(p_A=0.4, p_B=0.3)

    print("Valid range for A ∧ B:", rel.range_for_and())
    print("Valid range for A ∨ B:", rel.range_for_or())

    print("P(A ∧ B) if P(A ∨ B) = 0.5:", rel.compute_and_given_or(0.5))
    print("P(A ∨ B) if P(A ∧ B) = 0.2:", rel.compute_or_given_and(0.2))

    # The output will show the valid ranges for P(A ∧ B) and P(A ∨ B), as well as the computed probabilities based on the given values.
    # So, from the output - yes, the agent is rational to hold those beliefs.