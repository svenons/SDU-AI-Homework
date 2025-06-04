from typing import List, Dict
from Colors4 import Color
from collections.abc import Callable
from StatesSA import States

# This is a CSP solver adapted for map coloring.
# The variables represent regions (now countries in South America).
# The goal is to color the map such that no neighboring regions have the same color.

type contraintFunction = Callable[[States, Color, States, Color], bool]
type Assignment = dict[States, Color]

class CSP:
    def __init__(self, variables: list[States], domains: dict[States, list[Color]],
                 neighbours: dict[States, list[States]], constraints: dict[States, contraintFunction]):
        self.variables: List[States] = variables
        self.domains: Dict[States, List[Color]] = domains
        self.neighbours: Dict[States, List[States]] = neighbours
        self.constraints: Dict[States, contraintFunction] = constraints

    def backtracking_search(self) -> dict[States, Color] | None:
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment: Assignment) -> Dict[States, Color]:
        if self.is_complete(assignment):
            return assignment
        
        variable = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(variable, assignment):
            if self.is_consistent(variable, value, assignment):
                assignment[variable] = value
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                del assignment[variable]

        return None

    def select_unassigned_variable(self, assignment: Assignment) -> States:
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment: Assignment) -> bool:
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable: States, assignment: Assignment) -> list[Color]:
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable: States, value: Color, assignment: Assignment) -> bool:
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_south_america_csp() -> CSP:
    # South American countries as variables
    variables = [
        States.Argentina, States.Bolivia, States.Brazil, States.Chile, States.Colombia,
        States.Ecuador, States.FrenchGuiana, States.Guyana, States.Paraguay, States.Peru,
        States.Suriname, States.Uruguay, States.Venezuela
    ]

    # 4-color palette
    values = [Color.Red, Color.Green, Color.Blue, Color.Yellow]

    domains = {state: values[:] for state in variables}

    # Neighboring countries
    neighbours = {
        States.Argentina: [States.Bolivia, States.Brazil, States.Chile, States.Paraguay, States.Uruguay],
        States.Bolivia: [States.Argentina, States.Brazil, States.Chile, States.Paraguay, States.Peru],
        States.Brazil: [States.Argentina, States.Bolivia, States.Colombia, States.FrenchGuiana,
                        States.Guyana, States.Paraguay, States.Peru, States.Suriname, States.Uruguay, States.Venezuela],
        States.Chile: [States.Argentina, States.Bolivia, States.Peru],
        States.Colombia: [States.Brazil, States.Ecuador, States.Peru, States.Venezuela],
        States.Ecuador: [States.Colombia, States.Peru],
        States.FrenchGuiana: [States.Brazil, States.Suriname],
        States.Guyana: [States.Brazil, States.Suriname, States.Venezuela],
        States.Paraguay: [States.Argentina, States.Bolivia, States.Brazil],
        States.Peru: [States.Bolivia, States.Brazil, States.Chile, States.Colombia, States.Ecuador],
        States.Suriname: [States.Brazil, States.FrenchGuiana, States.Guyana],
        States.Uruguay: [States.Argentina, States.Brazil],
        States.Venezuela: [States.Brazil, States.Colombia, States.Guyana],
    }

    def constraint_function(first_variable: States, first_value: Color, second_variable: States, second_value: Color) -> bool:
        """Returns true if neighboring variables have different values."""
        return first_value != second_value or first_variable == second_variable

    constraints = {state: constraint_function for state in variables}

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    south_america = create_south_america_csp()
    result = south_america.backtracking_search()
    for area, color in sorted(result.items(), key=lambda x: x[0].name):
        print("{}: {}".format(area, color))

    # Check at https://mapchart.net/america-south.html