from ga.population import create_initial_population, evaluate_population, get_best_genome


def main():
    population = create_initial_population(size=5, seed=123)

    evaluate_population(population, max_moves=100)

    best = get_best_genome(population)

    print("\nBEST GENOME")
    print("Fitness:", best.get_fitness())
    print("Weights:", best.get_weights())


if __name__ == "__main__":
    main()