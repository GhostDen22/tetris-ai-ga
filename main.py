from ai.bot import Bot
from ga.fitness import calculate_fitness


def main():
    result = calculate_fitness(
        weights=Bot.DEFAULT_WEIGHTS,
        max_moves=200
    )

    print("FITNESS RESULT")
    print("Fitness:", result["fitness"])
    print("Average score:", result["average_score"])
    print("Average lines:", result["average_lines"])
    print("Average moves:", result["average_moves"])
    print("Games tested:", len(result["games"]))


if __name__ == "__main__":
    main()