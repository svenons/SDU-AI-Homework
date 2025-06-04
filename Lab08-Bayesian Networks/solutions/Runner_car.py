import random
from pprint import pformat

from Variable import Variable
from bn import BayesianNetwork


def create_random_sample(network: BayesianNetwork) -> dict[str, str]:
    """ creates random sample for the given network.
        the distribution of the samples follows the joint probability function.
        assumes binary variables. """
    sample: dict[str, str] = {}
    for var in network.variables:

        samp = random.random()
        assignment1 = list(var.assignments.keys())[0]
        assignment2 = list(var.assignments.keys())[1]

        parents_values = network.sub_vals(var, sample)
        prob = var.get_probability(assignment1, parents_values)

        if samp <= prob:
            sample[var.name] = assignment1
        else:
            sample[var.name] = assignment2
    return sample


def pad(string: str, pad: int = 4) -> str:
    lines = string.split('\n')
    padded_lines = (' ' * pad + line for line in lines)
    return '\n'.join(padded_lines)


def print_conditional_probability(network: BayesianNetwork, conditionals_vars: dict[str, str],
                                  conditionals_evidents: dict[str, str]) -> None:
    print('Given')
    print(pad(pformat(conditionals_evidents)))
    print('conditional probability of')
    print(pad(pformat(conditionals_vars)))
    print("is {:f}".format(
        network.get_conditional_probability(
            conditionals_vars,
            conditionals_evidents
        )))
    print()


def print_joint_probability(network: BayesianNetwork, values: dict[str, str]) -> None:
    print('Joint probability of')
    print(pad(pformat(values)))
    print("is {:f}".format(network.get_joint_probability(values)))


def print_marginal_probabilities(network: BayesianNetwork) -> None:
    print("Marginal probabilities:")
    for variable in network.get_variables():
        print("    {}".format(variable.get_name()))
        for assignment in variable.get_assignments():
            print("        {}: {:f}".format(
                assignment,
                variable.get_marginal_probability(assignment))
            )


def car_diagnosis_network():
    # new network for Exercise 2

    dt_prob = {(): (0.3, 0.7)}
    em_prob = {(): (0.3, 0.7)}
    ftl_prob = {(): (0.2, 0.8)}

    v_prob = {
        ('true',): (0.7, 0.3),
        ('false',): (0.1, 0.9)
    }

    sms_prob = {
        ('true', 'true'): (0.05, 0.95),
        ('true', 'false'): (0.6, 0.4),
        ('false', 'true'): (0.3, 0.7),
        ('false', 'false'): (0.7, 0.3)
    }

    hc_prob = {
        ('true', 'true', 'true'): (0.9, 0.1),
        ('true', 'true', 'false'): (0.8, 0.2),
        ('true', 'false', 'true'): (0.3, 0.7),
        ('true', 'false', 'false'): (0.2, 0.8),
        ('false', 'true', 'true'): (0.6, 0.4),
        ('false', 'true', 'false'): (0.5, 0.5),
        ('false', 'false', 'true'): (0.1, 0.9),
        ('false', 'false', 'false'): (0.01, 0.99)
    }

    dt = Variable('DT', ('true', 'false'), dt_prob)
    em = Variable('EM', ('true', 'false'), em_prob)
    ftl = Variable('FTL', ('true', 'false'), ftl_prob)

    v = Variable('V', ('true', 'false'), v_prob, [dt])
    sms = Variable('SMS', ('true', 'false'), sms_prob, [dt, em])
    hc = Variable('HC', ('true', 'false'), hc_prob, [dt, ftl, em])

    variables = [dt, em, ftl, v, sms, hc]

    network = BayesianNetwork()
    network.set_variables(variables)
    network.calculate_marginal_probabilities()

    print_marginal_probabilities(network)

    print('')

    joint_values = {
        'DT': 'true',
        'EM': 'true',
        'FTL': 'false',
        'V': 'true',
        'SMS': 'false',
        'HC': 'true'
    }
    print_joint_probability(network, joint_values)

    print('')

    conditionals_vars = {'DT': 'true'}
    conditionals_evidents = {'V': 'true', 'SMS': 'false'}

    print_conditional_probability(network, conditionals_vars, conditionals_evidents)

    print('')

    sample = create_random_sample(network)
    print_joint_probability(network, sample)


if __name__ == '__main__':
    car_diagnosis_network()