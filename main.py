from ga.trainer import train_genetic_algorithm
from ga.storage import save_genome, load_genome


def main():
    result = train_genetic_algorithm(
        population_size=10,
        generations=5,
        seed=123,
        max_moves=100,
        elitism_count=1,
        tournament_size=3,
        mutation_rate=0.2,
        mutation_strength=1.0,
    )

    print("\nTRAINING FINISHED")
    print("Best fitness:", result["best_fitness"])

    save_genome(
        weights=result["best_weights"],
        fitness=result["best_fitness"],
    )

    loaded = load_genome()

    print("\nLOADED GENOME")
    print(loaded)


if __name__ == "__main__":
    main()