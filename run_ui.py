import pygame

from ai.bot import Bot
from core.game import Game
from ga.storage import load_genome
from ui.panels import InfoPanel
from ui.renderer import BoardRenderer


WINDOW_WIDTH = 1140
WINDOW_HEIGHT = 740
FPS = 60

SEED = 42
MAX_MOVES = 500
BOT_MOVE_DELAY_MS = 400

BACKGROUND_COLOR = (14, 17, 23)


def load_bot_weights():
    try:
        genome = load_genome()
        return genome["weights"], "trained genome"
    except FileNotFoundError:
        return Bot.DEFAULT_WEIGHTS, "default weights"


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("TetrisGA Demo")

    clock = pygame.time.Clock()

    weights, mode_label = load_bot_weights()

    game = Game(seed=SEED)
    bot = Bot(weights=weights)

    board_renderer = BoardRenderer(x=25, y=50, cell_size=28)
    info_panel = InfoPanel(x=365, y=50, width=735, height=640)

    moves_played = 0
    no_available_move = False
    last_bot_step_time = pygame.time.get_ticks()

    running = True

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        demo_finished = (
            game.is_game_over()
            or moves_played >= MAX_MOVES
            or no_available_move
        )

        if (
            not demo_finished
            and current_time - last_bot_step_time >= BOT_MOVE_DELAY_MS
        ):
            move = bot.find_best_move(
                game.board,
                game.get_current_piece(),
            )

            if move is None:
                no_available_move = True
            else:
                game.apply_bot_move(move)
                moves_played += 1

            last_bot_step_time = current_time

        demo_finished = (
            game.is_game_over()
            or moves_played >= MAX_MOVES
            or no_available_move
        )

        screen.fill(BACKGROUND_COLOR)

        board = game.get_board()
        board_renderer.draw(screen, board)

        info_panel.draw(
            surface=screen,
            game=game,
            bot=bot,
            mode_label=mode_label,
            moves_played=moves_played,
            max_moves=MAX_MOVES,
            demo_finished=demo_finished,
            no_available_move=no_available_move,
        )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()