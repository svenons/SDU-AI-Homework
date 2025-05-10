import random
from typing import Self

from ga import Individual, genetic_algorithm


class NumberIndividual(Individual):
    def __init__(self, gene: tuple):
        self.gene = gene

    def get_fitness(self) -> float:
        """
        Computes the decimal value of the individual
        Return the fitness level of the individual

        Explanation:
        enumerate(list) returns a list of pairs (position, element):
        enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]
        enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
        """

        fitness = 0
        for i, bit in enumerate(reversed(self.gene)):
            contribution = bit * 2**i
            fitness += contribution
        return fitness
      
    def mutate(self) -> Self:
            '''
            Mutate an individual by randomly assigning one of its bits
            '''
            # index is point of mutation
            index = int(random.uniform(0, len(self.gene)))
            print("  Mutate: {} at {}".format(self.gene, index))
            new_bit = random.randint(0, 1)
            mutatedgene = tuple(self.gene[:index] + (new_bit,) + self.gene[index + 1:])
            mutation= NumberIndividual(mutatedgene)
            print("    Mutation: {}".format(mutation))
            
            return mutation
       
    def reproduce(self, other: Self) -> Self:
        """
        Reproduce this individual with another with single-point crossover
        Return the child individual
        """
        
        print("  Reproduce: {} with {}".format(self, other))
        c = random.randrange(len(self.gene))
        print("    Crossover at {}".format(c))
        gene = tuple(self.gene[:c] + other.gene[c:])
        child= NumberIndividual(gene)
         
        print("    Child: {}".format(child.gene))
        return child

    def __hash__(self):
        return hash(self.gene)

    @classmethod
    def create_random(cls, length_of_gene: int) -> Self:
        return cls(tuple(random.randint(0, 1) for _ in range(length_of_gene)))

    def __repr__(self) -> str:
        return f"Gene: {self.gene} - Fitness: {self.get_fitness()}"


def get_initial_population(n: int, count: int) -> set[NumberIndividual]:
    """
    Randomly generate count individuals of length n
    Note since it's a set it disregards duplicate elements.

    Be aware that since the individuals are generated randomly, but duplicates are not allowed.
    It can take a long time if you use large numbers of count and n together.
    """

    if count > 2 ** n:
        raise ValueError("Count must be less than 2^n, otherwise not enough unique individuals can be generated.")

    out: set[NumberIndividual] = set()

    while len(out) < count:
        out.add(NumberIndividual.create_random(n))

    return out


def main():
    minimal_fitness = 7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        NumberIndividual((1, 1, 0)),
        NumberIndividual((0, 0, 0)),
        NumberIndividual((0, 1, 0)),
        NumberIndividual((1, 0, 0))
    }
    
    #initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    main()
