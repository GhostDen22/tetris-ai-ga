import pygame

from core.game import Game
from ai.bot import Bot
from ui.renderer import BoardRenderer
from ui.panels import InfoPanel


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 30

BACKGROUND_COLOR = (14, 17, 23)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("TetrisGA Demo")

    clock = pygame.time.Clock()

    game = Game()
    bot = Bot()

    board_renderer = BoardRenderer()
    info_panel = InfoPanel()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        board = game.get_board()

        board_renderer.draw(screen, board)
        info_panel.draw(screen, game, bot)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()