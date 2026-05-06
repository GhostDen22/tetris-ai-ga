from ga.trainer import train_genetic_algorithm


def main():
    result = train_genetic_algorithm(
        population_size=30,
        generations=20,
        seed=123,
        max_moves=100,
        elitism_count=1,
        tournament_size=3,
        mutation_rate=0.2,
        mutation_strength=1.0,
    )

    print("\nTRAINING FINISHED")
    print("Best fitness:", result["best_fitness"])
    print("Best weights:", result["best_weights"])

    print("\nHistory:")
    for item in result["history"]:
        print(
            f"Generation {item['generation']}: "
            f"best_fitness={item['best_fitness']}"
        )


if __name__ == "__main__":
    main()