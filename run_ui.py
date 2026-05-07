import pygame

from ai.bot import Bot
from core.game import Game
from ga.storage import load_genome
from ui.panels import InfoPanel
from ui.renderer import BoardRenderer


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 760
FPS = 60

DEFAULT_SEED = 42
MAX_MOVES = 500

BACKGROUND_COLOR = (14, 17, 23)

SPEED_OPTIONS = {
    "slow": 700,
    "normal": 400,
    "fast": 200,
}


def load_bot_weights():
    try:
        genome = load_genome()
        return genome["weights"], "trained genome"
    except FileNotFoundError:
        return Bot.DEFAULT_WEIGHTS, "default weights"


def parse_seed(seed_text):
    try:
        return int(seed_text)
    except ValueError:
        return DEFAULT_SEED


def create_game_and_bot(seed, weights):
    game = Game(seed=seed)
    bot = Bot(weights=weights)
    return game, bot


def get_current_piece_name(game):
    current_piece = game.get_current_piece()

    if current_piece is None:
        return "N/A"

    return getattr(current_piece, "name", str(current_piece))


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("TetrisGA Demo")

    clock = pygame.time.Clock()

    weights, weights_label = load_bot_weights()

    selected_seed = DEFAULT_SEED
    seed_text = str(DEFAULT_SEED)
    seed_input_active = False

    selected_speed = "normal"
    bot_move_delay_ms = SPEED_OPTIONS[selected_speed]

    selected_mode = "demo"
    is_playing = True

    game, bot = create_game_and_bot(selected_seed, weights)

    board_renderer = BoardRenderer(x=24, y=58, cell_size=26)
    info_panel = InfoPanel(x=332, y=34, width=920, height=690)

    moves_played = 0
    no_available_move = False
    last_placed_piece = "N/A"

    last_bot_step_time = pygame.time.get_ticks()
    clickable_rects = {}

    running = True

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                seed_input_active = False

                if (
                    clickable_rects.get("seed_input")
                    and clickable_rects["seed_input"].collidepoint(mouse_position)
                ):
                    seed_input_active = True

                elif (
                    clickable_rects.get("toggle_play")
                    and clickable_rects["toggle_play"].collidepoint(mouse_position)
                ):
                    if selected_mode == "demo":
                        is_playing = not is_playing

                elif (
                    clickable_rects.get("reset")
                    and clickable_rects["reset"].collidepoint(mouse_position)
                ):
                    selected_seed = parse_seed(seed_text)
                    game, bot = create_game_and_bot(selected_seed, weights)
                    moves_played = 0
                    no_available_move = False
                    last_placed_piece = "N/A"
                    is_playing = True
                    last_bot_step_time = pygame.time.get_ticks()

                elif (
                    clickable_rects.get("mode_demo")
                    and clickable_rects["mode_demo"].collidepoint(mouse_position)
                ):
                    selected_mode = "demo"
                    is_playing = True
                    last_bot_step_time = pygame.time.get_ticks()

                elif (
                    clickable_rects.get("mode_train")
                    and clickable_rects["mode_train"].collidepoint(mouse_position)
                ):
                    selected_mode = "train"
                    is_playing = False

                elif (
                    clickable_rects.get("speed_slow")
                    and clickable_rects["speed_slow"].collidepoint(mouse_position)
                ):
                    selected_speed = "slow"
                    bot_move_delay_ms = SPEED_OPTIONS[selected_speed]

                elif (
                    clickable_rects.get("speed_normal")
                    and clickable_rects["speed_normal"].collidepoint(mouse_position)
                ):
                    selected_speed = "normal"
                    bot_move_delay_ms = SPEED_OPTIONS[selected_speed]

                elif (
                    clickable_rects.get("speed_fast")
                    and clickable_rects["speed_fast"].collidepoint(mouse_position)
                ):
                    selected_speed = "fast"
                    bot_move_delay_ms = SPEED_OPTIONS[selected_speed]

            if event.type == pygame.KEYDOWN and seed_input_active:
                if event.key == pygame.K_BACKSPACE:
                    seed_text = seed_text[:-1]

                elif event.key == pygame.K_RETURN:
                    selected_seed = parse_seed(seed_text)
                    game, bot = create_game_and_bot(selected_seed, weights)
                    moves_played = 0
                    no_available_move = False
                    last_placed_piece = "N/A"
                    is_playing = True
                    seed_input_active = False
                    last_bot_step_time = pygame.time.get_ticks()

                elif event.unicode.isdigit() and len(seed_text) < 9:
                    seed_text += event.unicode

        demo_finished = (
            game.is_game_over()
            or moves_played >= MAX_MOVES
            or no_available_move
        )

        should_run_demo_step = (
            selected_mode == "demo"
            and is_playing
            and not demo_finished
            and current_time - last_bot_step_time >= bot_move_delay_ms
        )

        if should_run_demo_step:
            current_piece_name = get_current_piece_name(game)

            move = bot.find_best_move(
                game.board,
                game.get_current_piece(),
            )

            if move is None:
                no_available_move = True
            else:
                last_placed_piece = current_piece_name
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

        ui_state = {
            "selected_mode": selected_mode,
            "is_playing": is_playing,
            "weights_label": weights_label,
            "seed_text": seed_text,
            "seed_input_active": seed_input_active,
            "selected_speed": selected_speed,
            "bot_move_delay_ms": bot_move_delay_ms,
            "moves_played": moves_played,
            "max_moves": MAX_MOVES,
            "demo_finished": demo_finished,
            "no_available_move": no_available_move,
            "current_piece": get_current_piece_name(game),
            "last_placed_piece": last_placed_piece,
        }

        clickable_rects = info_panel.draw(
            surface=screen,
            game=game,
            bot=bot,
            ui_state=ui_state,
        )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()