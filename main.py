from ga.trainer import train_genetic_algorithm
from audit.logger import AuditLogger
from ga.storage import save_genome
from ga.evaluation import evaluate_weights_on_seed_sets


def print_result(name, result):
    print(f"\n{name.upper()}")
    print("Fitness:", result["fitness"])
    print("Average score:", result["average_score"])
    print("Average lines:", result["average_lines"])
    print("Average moves:", result["average_moves"])
    print("Games:", len(result["games"]))


def main():
    logger = AuditLogger()

    training_result = train_genetic_algorithm(
        population_size=10,
        generations=5,
        seed=123,
        max_moves=100,
        elitism_count=1,
        tournament_size=3,
        mutation_rate=0.2,
        mutation_strength=1.0,
        audit_logger=logger,
    )

    save_genome(
        weights=training_result["best_weights"],
        fitness=training_result["best_fitness"],
    )

    evaluation = evaluate_weights_on_seed_sets(
        weights=training_result["best_weights"],
        max_moves=100,
    )

    print("\nTRAINING FINISHED")
    print("Best fitness:", training_result["best_fitness"])

    print_result("train", evaluation["train"])
    print_result("validation", evaluation["validation"])
    print_result("test", evaluation["test"])


if __name__ == "__main__":
    main()