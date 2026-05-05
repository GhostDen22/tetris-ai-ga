from core.game import Game


def print_board(board):
    for row in board:
        print(row)


def main():
    game = Game(seed=42)

    for step in range(25):
        print(f"\nSTEP {step}")
        print_board(game.get_board())
        print("Score:", game.get_score())
        print("Lines:", game.get_lines())
        print("Seed:", game.get_seed())
        print("Game over:", game.is_game_over())

        game.step()


if __name__ == "__main__":
    main()