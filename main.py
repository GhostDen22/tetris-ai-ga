from simulation.runner import run_bot_game


def main():
    result = run_bot_game(seed=42, max_moves=100)

    print("BOT GAME RESULT")
    print("Seed:", result["seed"])
    print("Score:", result["score"])
    print("Lines:", result["lines"])
    print("Moves:", result["moves"])
    print("Game over:", result["game_over"])
    print("Last move:", result["last_move"])
    print("Last features:", result["last_features"])
    print("Last reasons:", result["last_reasons"])


if __name__ == "__main__":
    main()