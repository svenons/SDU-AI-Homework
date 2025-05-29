import random
from typing import Self

"""
Fitness utility: number of conflicting pairs (we minimize this, so fitness = -conflicts)
"""
def fitness_fn_negative(board_view: tuple[int, ...]) -> int:
    """
    Compute the number of conflicting queen pairs (negated).
    A perfect solution returns 0 conflicts (fitness = 0).
    """
    n = len(board_view)
    fitness = 0
    for column, row in enumerate(board_view):
        for other_column in range(column + 1, n):
            dx = abs(column - other_column)
            dy = abs(row - board_view[other_column])
            if dx == dy or dy == 0:
                fitness += 1
    return -fitness


"""
Abstract base class for individuals in a genetic algorithm
"""
class Individual:
    def get_fitness(self) -> float:
        """Return the fitness of the individual"""
        raise NotImplementedError

    def mutate(self) -> Self:
        """Return a mutated version of the individual"""
        raise NotImplementedError

    def reproduce(self, other: Self) -> Self:
        """Return a new individual from crossover with another"""
        raise NotImplementedError

    def __lt__(self, other: Self) -> bool:
        return self.get_fitness() < other.get_fitness()

    def __repr__(self):
        return f"Fitness: {self.get_fitness()}"


"""
A class representing an individual board in the N-Queens problem
Each individual stores a board as a tuple of row positions
"""
class Board(Individual):
    def __init__(self, board: tuple[int, ...]):
        self.board = board

    def get_fitness(self) -> float:
        """Use fitness function from queens_fitness to compute fitness"""
        return fitness_fn_negative(self.board)

    def mutate(self) -> Self:
        """
        Randomly change the row of one queen (one column)
        """
        board_list = list(self.board)
        index = random.randint(0, len(board_list) - 1)
        board_list[index] = random.randint(0, len(board_list) - 1)
        mutated = Board(tuple(board_list))
        print(f"  Mutate: {self.board} -> {mutated.board}")
        return mutated

    def reproduce(self, other: Self) -> Self:
        """
        Reproduce with another board using one-point crossover
        """
        crossover_point = random.randint(1, len(self.board) - 2)
        child_board = self.board[:crossover_point] + other.board[crossover_point:]
        child = Board(child_board)
        print(f"  Reproduce: {self.board} x {other.board} @ {crossover_point} -> {child.board}")
        return child

    def __hash__(self):
        return hash(self.board)

    def __repr__(self):
        return f"Board: {self.board}, Fitness: {self.get_fitness()}"


"""
Generate an initial population of random boards
"""
def get_initial_population(n: int, count: int) -> set[Board]:
    """
    Generate a set of unique board individuals with random queen placements
    """
    population: set[Board] = set()

    while len(population) < count:
        board = tuple(random.randint(0, n - 1) for _ in range(n))
        population.add(Board(board))

    return population


"""
Pick one individual using roulette wheel selection
"""
def pick_individual(totals: list[float], population: list[Individual]) -> Individual:
    r = random.uniform(0, 1)
    total_fitness = totals[-1]
    for i, individual in enumerate(population):
        if r < totals[i] / total_fitness:
            return individual
    return population[-1]  # fallback


"""
Select two individuals based on fitness proportionate selection
"""
def random_selection(population: set[Individual]) -> tuple[Individual, Individual]:
    ordered = list(population)
    totals = []
    total = 0

    for ind in ordered:
        fitness = ind.get_fitness()
        total += fitness
        totals.append(total)

    mother = pick_individual(totals, ordered)
    father = pick_individual(totals, ordered)
    return mother, father


"""
Get the fittest individual in a population
"""
def get_fittest_individual(population: set[Individual]) -> Individual:
    return max(population)


"""
Trim population to desired length (removes lowest fitness individuals)
"""
def trim_population(population: set[Individual], size: int) -> set[Individual]:
    if len(population) <= size:
        return population
    sorted_pop = sorted(population, reverse=True)
    return set(sorted_pop[:size])


"""
Print population or summarize it
"""
def print_population(population: set[Individual]):
    if len(population) > 10:
        print(f"Population too large to print ({len(population)}), best: {get_fittest_individual(population)}")
    else:
        for individual in population:
            print(individual)


"""
Genetic algorithm core logic
"""
def genetic_algorithm(population: set[Individual],
                      minimal_fitness: float,
                      num_of_generations: int = 100,
                      should_trim_population: bool = True,
                      p_mutation: float = 0.8,
                      max_population_size: int = 100) -> Individual | None:
    """
    Evolve population toward a minimal conflict state (maximized fitness = 0)
    """
    for generation in range(num_of_generations):
        print(f"\nGeneration {generation}")
        print_population(population)

        new_population = set()

        for _ in range(len(population)):
            mother, father = random_selection(population)
            child = mother.reproduce(father)

            if random.random() < p_mutation:
                child = child.mutate()

            new_population.add(child)

        population = population.union(new_population)

        if should_trim_population:
            population = trim_population(population, max_population_size)

        fittest = get_fittest_individual(population)
        if fittest.get_fitness() >= minimal_fitness:
            print("\nTerminating early — fitness target reached.")
            break

    print(f"\nFinal Generation {generation}")
    print_population(population)
    return get_fittest_individual(population)


"""
Main function to run the N-Queens GA using queens_fitness module
"""
def main():
    n = 8  # number of queens
    population_size = 50
    target_fitness = 0  # we want zero conflicts
    max_generations = 100

    initial_population = get_initial_population(n, population_size)

    fittest = genetic_algorithm(
        population=initial_population,
        minimal_fitness=target_fitness,
        num_of_generations=max_generations,
        should_trim_population=True,
        p_mutation=0.8,
        max_population_size=population_size
    )

    print("\nBest solution found:")
    print(fittest)


if __name__ == '__main__':
    main()