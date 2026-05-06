import sys

from ai.bot import Bot
from simulation.runner import run_bot_game
from ga.trainer import train_genetic_algorithm
from ga.evaluation import evaluate_weights_on_seed_sets
from ga.storage import save_genome, load_genome
from audit.logger import AuditLogger


def print_evaluation_result(name, result):
    print(f"\n{name.upper()}")
    print("Fitness:", result["fitness"])
    print("Average score:", result["average_score"])
    print("Average lines:", result["average_lines"])
    print("Average moves:", result["average_moves"])
    print("Games:", len(result["games"]))


def run_demo():
    result = run_bot_game(
        seed=42,
        weights=Bot.DEFAULT_WEIGHTS,
        max_moves=100
    )

    print("DEMO RESULT")
    print("Score:", result["score"])
    print("Lines:", result["lines"])
    print("Moves:", result["moves"])
    print("Game over:", result["game_over"])
    print("Last move:", result["last_move"])
    print("Last features:", result["last_features"])
    print("Last reasons:", result["last_reasons"])


def run_training():
    logger = AuditLogger()

    result = train_genetic_algorithm(
        population_size=30,
        generations=20,
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
    print("Best weights:", result["best_weights"])


def run_evaluation():
    genome = load_genome()
    weights = genome["weights"]

    evaluation = evaluate_weights_on_seed_sets(
        weights=weights,
        max_moves=100,
    )

    print("LOADED GENOME FITNESS:", genome["fitness"])

    print_evaluation_result("train", evaluation["train"])
    print_evaluation_result("validation", evaluation["validation"])
    print_evaluation_result("test", evaluation["test"])


def print_help():
    print("Usage:")
    print("  python main.py demo   - run default heuristic bot")
    print("  python main.py train  - train GA and save best genome")
    print("  python main.py eval   - evaluate saved best genome")
    print("  python main.py help   - show this help")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "help"

    if mode == "demo":
        run_demo()
    elif mode == "train":
        run_training()
    elif mode == "eval":
        run_evaluation()
    elif mode == "help":
        print_help()
    else:
        print(f"Unknown mode: {mode}")
        print_help()


if __name__ == "__main__":
    main()