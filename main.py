import random

from ga.population import (
    create_initial_population,
    evaluate_population,
    get_best_genome,
)

from ga.operators import (
    tournament_selection,
    crossover,
    mutate,
)


def main():
    rng = random.Random(123)

    population = create_initial_population(
        size=10,
        seed=123
    )

    evaluate_population(population, max_moves=100)

    parent_a = tournament_selection(population, rng=rng)
    parent_b = tournament_selection(population, rng=rng)

    child = crossover(parent_a, parent_b, rng=rng)

    mutated_child = mutate(
        child,
        mutation_rate=0.3,
        mutation_strength=1.5,
        rng=rng
    )

    print("\nPARENT A")
    print(parent_a.get_weights())

    print("\nPARENT B")
    print(parent_b.get_weights())

    print("\nCHILD")
    print(child.get_weights())

    print("\nMUTATED CHILD")
    print(mutated_child.get_weights())

    best = get_best_genome(population)

    print("\nBEST GENOME")
    print("Fitness:", best.get_fitness())


if __name__ == "__main__":
    main()