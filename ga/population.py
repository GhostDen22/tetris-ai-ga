import random

from ga.genome import Genome


def create_initial_population(size=30, seed=123):
    rng = random.Random(seed)

    population = []

    for _ in range(size):
        genome = Genome.random_genome(rng)
        population.append(genome)

    return population