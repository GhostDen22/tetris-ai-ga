from core.game import Game
from ai.bot import Bot

def main():
    game = Game()
    bot = Bot()

    print("BOARD:")
    for row in game.get_board():
        print(row)

    print("\nSCORE:", game.get_score())
    print("LINES:", game.get_lines())
    print("SEED:", game.get_seed())

    print("\nFEATURES:")
    print(bot.get_features())


if __name__ == "__main__":
    main()