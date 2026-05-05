from core.game import Game
from ai.bot import Bot


def print_board(board):
    for row in board:
        print(row)


def main():
    game = Game(seed=42)
    bot = Bot()

    for step in range(25):
        print(f"\nSTEP {step}")
        board = game.get_board()
        bot.update(board)

        print_board(board)
        print("Score:", game.get_score())
        print("Lines:", game.get_lines())
        print("Seed:", game.get_seed())
        print("Game over:", game.is_game_over())
        print("Features:", bot.get_features())

        game.step()


if __name__ == "__main__":
    main()