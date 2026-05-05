from ga.population import create_initial_population


def main():
    population = create_initial_population(size=5, seed=123)

    print("INITIAL POPULATION")

    for index, genome in enumerate(population):
        print(f"\nGenome {index}")
        print(genome.get_weights())


if __name__ == "__main__":
    main()