"""
Consider two medical tests, A and B, for a virus. Test A is 95% effective at recognizing the 
virus when it is present, but has a 10% false positive rate (indicating that the virus is present, 
when it is not). Test B is 90% effective at recognizing the virus, but has a 5% false positive 
rate. The two tests use independent methods of identifying the virus. The virus is carried by 
1% of all people. Say that a person is tested for the virus using only one of the tests, and that 
test comes back positive for carrying the virus. Which test returning positive is more 
indicative of someone really carrying the virus? Justify your answer mathematically
"""

"""
Theorem formula:
P(Disease | Positive) = (P(Positive | Disease) * P(Disease)) / P(Positive)
"""

"""
First implementation:
def bayes_rule(prevalence, sensitivity, false_positive_rate):
    # P(Disease)
    p_disease = prevalence

    # P(No Disease)
    p_no_disease = 1 - p_disease

    # P(Positive | Disease)
    p_pos_given_disease = sensitivity

    # P(Positive | No Disease)
    p_pos_given_no_disease = false_positive_rate

    # Total probability of testing positive
    p_positive = (
        p_pos_given_disease * p_disease +
        p_pos_given_no_disease * p_no_disease
    )

    # Bayes' Theorem
    p_disease_given_positive = (
        p_pos_given_disease * p_disease
    ) / p_positive

    return 
    
# Test A: 95% sensitivity, 10% false positive
bayes_rule(0.01, 0.95, 0.10)

# Test B: 90% sensitivity, 5% false positive
bayes_rule(0.01, 0.90, 0.05)
"""

class Disease:
    def __init__(self, prevalence: float):
        self.prevalence = prevalence

class MedicalTest:
    def __init__(self, sensitivity: float, false_positive_rate: float):
        self.sensitivity = sensitivity  # True positive rate
        self.false_positive_rate = false_positive_rate  # False positive rate

    def bayes_theorem(self, disease: Disease) -> float:
        # P(Disease)
        p_disease = disease.prevalence

        # P(No Disease)
        p_no_disease = 1 - p_disease

        # P(Positive | Disease)
        p_pos_given_disease = self.sensitivity

        # P(Positive | No Disease)
        p_pos_given_no_disease = self.false_positive_rate

        # Total probability of testing positive
        p_positive = (
            p_pos_given_disease * p_disease +
            p_pos_given_no_disease * p_no_disease
        )

        # Bayes' Theorem: P(Disease | Positive)
        p_disease_given_positive = (
            p_pos_given_disease * p_disease
        ) / p_positive

        return p_disease_given_positive

if __name__ == "__main__":
    # Define disease with 1% prevalence
    disease = Disease(prevalence=0.01)

    # Define Test A and Test B
    test_A = MedicalTest(sensitivity=0.95, false_positive_rate=0.10)
    test_B = MedicalTest(sensitivity=0.90, false_positive_rate=0.05)

    # Compute post-test probabilities
    prob_A = test_A.bayes_theorem(disease)
    prob_B = test_B.bayes_theorem(disease)

    # Display results
    print(f"Probability of having the disease given a positive result:")
    print(f"Test A: {prob_A:.4f}")
    print(f"Test B: {prob_B:.4f}")

    # Considering the results, we can conclude:
    # Test B has a higher probability of indicating the presence of the disease when it returns positive.