"""
Would it be rational for an agent to hold the three beliefs P(A)=0.4, P(B)=0.3, 
and P(A∨B)=0.7? What type of relationship holds between A and B? 
"""

from exercise3 import ProbabilityRelations

if __name__ == "__main__":
    p_A = 0.4
    p_B = 0.3
    p_or = 0.7

    rel = ProbabilityRelations(p_A, p_B)
    min_and, max_and = rel.range_for_and()
    min_or, max_or = rel.range_for_or()
    p_and = rel.compute_and_given_or(p_or)
    p_or_computed = rel.compute_or_given_and(p_and)

    print(f"Valid range for P(A ∧ B): [{min_and}, {max_and}]")
    print(f"Valid range for P(A ∨ B): [{min_or}, {max_or}]")
    print(f"P(A ∧ B) if P(A ∨ B) = {p_or}: {p_and}")
    print(f"P(A ∨ B) if P(A ∧ B) = {p_and}: {p_or_computed}")

    # Yes, the beliefs are rational.
    # A and B are mutually exclusive — they cannot occur at the same time.