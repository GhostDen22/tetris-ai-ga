from ga.trainer import train_genetic_algorithm
from audit.logger import AuditLogger
from ga.storage import save_genome


def main():
    logger = AuditLogger()

    result = train_genetic_algorithm(
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
        weights=result["best_weights"],
        fitness=result["best_fitness"],
    )

    print("\nTRAINING FINISHED")
    print("Best fitness:", result["best_fitness"])
    print("Audit saved to audit/audit_log.jsonl")


if __name__ == "__main__":
    main()