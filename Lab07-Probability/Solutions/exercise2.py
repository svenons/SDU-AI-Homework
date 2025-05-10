from exercise1 import Disease, MedicalTest

if __name__ == "__main__":
    # Define the disease with a prevalence of 1 in 10,000
    disease = Disease(1/10000)

    # Define the medical test with 99% sensitivity and 1% false positive rate
    test = MedicalTest(0.99, 0.01)

    # Calculate the probability of having the disease given a positive test result
    probability = test.bayes_theorem(disease)

    print(f"Probability of having the disease given a positive test result: {probability:.6f}")
    
    # From the results we can gather that the probability of having the disease given a positive test result is 0.009804, which is approximately 1%.
    # Therefore, after a positive test, only ~1 in 100 people actually have the disease, despite the test's high sensitivity and low false positive rate.