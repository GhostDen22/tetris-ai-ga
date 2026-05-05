from core.game import Game
from ai.bot import Bot


def print_board(board):
    for row in board:
        print(row)


def main():
    game = Game(seed=42)
    bot = Bot()

    for turn in range(10):
        if game.is_game_over():
            break

        move = bot.find_best_move(
            game.board,
            game.get_current_piece()
        )

        game.apply_bot_move(move)

        print(f"\nTURN {turn}")
        print("Move:", bot.get_last_move())
        print("Move score:", bot.get_last_score())
        print("Features:", bot.get_features())
        print("Game score:", game.get_score())
        print("Lines:", game.get_lines())
        print("Game over:", game.is_game_over())
        print_board(game.get_board())


if __name__ == "__main__":
    main()