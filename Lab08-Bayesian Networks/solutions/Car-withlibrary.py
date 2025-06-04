from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


def car_diagnosis_pgmpy():
    # Define the structure of the network
    model = BayesianNetwork([
        ('DT', 'V'),
        ('DT', 'SMS'),
        ('EM', 'SMS'),
        ('DT', 'HC'),
        ('FTL', 'HC'),
        ('EM', 'HC')
    ])

    # Prior probabilities
    cpd_dt = TabularCPD(variable='DT', variable_card=2, values=[[0.3], [0.7]])
    cpd_em = TabularCPD(variable='EM', variable_card=2, values=[[0.3], [0.7]])
    cpd_ftl = TabularCPD(variable='FTL', variable_card=2, values=[[0.2], [0.8]])

    # Conditional probabilities
    cpd_v = TabularCPD(variable='V', variable_card=2,
                       values=[[0.7, 0.1], [0.3, 0.9]],
                       evidence=['DT'], evidence_card=[2])

    cpd_sms = TabularCPD(variable='SMS', variable_card=2,
                         values=[
                             [0.05, 0.6, 0.3, 0.7],  # P(SMS=true)
                             [0.95, 0.4, 0.7, 0.3]   # P(SMS=false)
                         ],
                         evidence=['DT', 'EM'], evidence_card=[2, 2])

    cpd_hc = TabularCPD(variable='HC', variable_card=2,
                        values=[
                            [0.9, 0.8, 0.3, 0.2, 0.6, 0.5, 0.1, 0.01],   # P(HC=true)
                            [0.1, 0.2, 0.7, 0.8, 0.4, 0.5, 0.9, 0.99]   # P(HC=false)
                        ],
                        evidence=['DT', 'FTL', 'EM'],
                        evidence_card=[2, 2, 2])

    # Add CPDs to the model
    model.add_cpds(cpd_dt, cpd_em, cpd_ftl, cpd_v, cpd_sms, cpd_hc)

    # Verify the model is valid
    assert model.check_model()

    # Inference
    infer = VariableElimination(model)

    # Marginal probability
    print("Marginal P(HC=true):", infer.query(variables=['HC']).values[0])
    print("Marginal P(SMS=true):", infer.query(variables=['SMS']).values[0])

    # Joint probability example
    joint_prob = infer.query(variables=['V', 'SMS', 'HC'],
                             evidence={'DT': 0, 'EM': 0, 'FTL': 1})
    print("\nJoint probability P(V, SMS, HC | DT=T, EM=T, FTL=F):")
    print(joint_prob)

    # Conditional probability example
    cond_prob = infer.query(variables=['DT'], evidence={'V': 0, 'SMS': 1})
    print("\nP(DT=true | V=true, SMS=false):", cond_prob.values[0])


if __name__ == '__main__':
    car_diagnosis_pgmpy()