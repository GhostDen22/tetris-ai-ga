import pygame

from ai.bot import Bot
from audit.logger import AuditLogger
from core.game import Game
from ga.storage import load_genome
from ui.panels import InfoPanel
from ui.renderer import BoardRenderer


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 760
FPS = 60

DEFAULT_SEED = 42
MAX_MOVES = 500
MAX_RECENT_LOGS = 6

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


def format_score(value):
    if isinstance(value, float):
        return f"{value:.2f}"

    return str(value)


def add_recent_log(recent_logs, message):
    recent_logs.append(message)

    while len(recent_logs) > MAX_RECENT_LOGS:
        recent_logs.pop(0)


def log_ui_event(logger, event_name, data=None):
    if data is None:
        data = {}

    logger.log_event(
        "ui_event",
        {
            "name": event_name,
            **data,
        },
    )


def log_ui_decision(logger, bot, move, moves_played, seed, speed, mode):
    logger.log_decision(
        move=move,
        score=bot.get_last_score(),
        features=bot.get_features(),
        reasons=bot.get_last_reasons(),
    )

    logger.log_event(
        "ui_decision_context",
        {
            "moves_played": moves_played,
            "seed": seed,
            "speed": speed,
            "mode": mode,
        },
    )


def log_ui_game_result(logger, game, bot, moves_played, max_moves, seed, finish_reason):
    result = {
        "source": "ui",
        "seed": seed,
        "score": game.get_score(),
        "lines": game.get_lines(),
        "moves": moves_played,
        "max_moves": max_moves,
        "game_over": game.is_game_over(),
        "finish_reason": finish_reason,
        "last_features": bot.get_features(),
        "last_move": bot.get_last_move(),
        "last_score": bot.get_last_score(),
        "last_reasons": bot.get_last_reasons(),
    }

    logger.log_game_result(result)


def get_finish_reason(game, moves_played, max_moves, no_available_move):
    if game.is_game_over():
        return "game_over"

    if no_available_move:
        return "no_available_move"

    if moves_played >= max_moves:
        return "max_moves"

    return "running"


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("TetrisGA Demo")

    clock = pygame.time.Clock()

    audit_logger = AuditLogger()

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
    final_result_logged = False

    recent_logs = []
    add_recent_log(recent_logs, f"UI started: seed={selected_seed}, mode={selected_mode}")
    add_recent_log(recent_logs, f"Weights: {weights_label}")

    last_bot_step_time = pygame.time.get_ticks()
    clickable_rects = {}

    log_ui_event(
        audit_logger,
        "ui_demo_started",
        {
            "seed": selected_seed,
            "mode": selected_mode,
            "speed": selected_speed,
            "weights": weights_label,
            "max_moves": MAX_MOVES,
        },
    )

    running = True

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_ui_event(
                    audit_logger,
                    "ui_window_closed",
                    {
                        "seed": selected_seed,
                        "mode": selected_mode,
                        "moves_played": moves_played,
                        "score": game.get_score(),
                        "lines": game.get_lines(),
                    },
                )

                add_recent_log(
                    recent_logs,
                    f"Window closed after {moves_played} moves",
                )

                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                seed_input_active = False

                if (
                    clickable_rects.get("seed_input")
                    and clickable_rects["seed_input"].collidepoint(mouse_position)
                ):
                    seed_input_active = True

                    log_ui_event(
                        audit_logger,
                        "seed_input_focused",
                        {
                            "current_seed_text": seed_text,
                        },
                    )

                    add_recent_log(recent_logs, "Seed input focused")

                elif (
                    clickable_rects.get("toggle_play")
                    and clickable_rects["toggle_play"].collidepoint(mouse_position)
                ):
                    if selected_mode == "demo":
                        is_playing = not is_playing

                        log_ui_event(
                            audit_logger,
                            "playback_toggled",
                            {
                                "is_playing": is_playing,
                                "moves_played": moves_played,
                                "score": game.get_score(),
                                "lines": game.get_lines(),
                            },
                        )

                        if is_playing:
                            add_recent_log(recent_logs, "Playback started")
                        else:
                            add_recent_log(recent_logs, "Playback stopped")

                elif (
                    clickable_rects.get("reset")
                    and clickable_rects["reset"].collidepoint(mouse_position)
                ):
                    selected_seed = parse_seed(seed_text)
                    game, bot = create_game_and_bot(selected_seed, weights)

                    moves_played = 0
                    no_available_move = False
                    last_placed_piece = "N/A"
                    final_result_logged = False

                    is_playing = True
                    last_bot_step_time = pygame.time.get_ticks()

                    log_ui_event(
                        audit_logger,
                        "demo_reset",
                        {
                            "seed": selected_seed,
                            "mode": selected_mode,
                            "speed": selected_speed,
                            "weights": weights_label,
                            "max_moves": MAX_MOVES,
                        },
                    )

                    add_recent_log(
                        recent_logs,
                        f"Reset demo: seed={selected_seed}",
                    )

                elif (
                    clickable_rects.get("mode_demo")
                    and clickable_rects["mode_demo"].collidepoint(mouse_position)
                ):
                    selected_mode = "demo"
                    is_playing = True
                    last_bot_step_time = pygame.time.get_ticks()

                    log_ui_event(
                        audit_logger,
                        "mode_changed",
                        {
                            "mode": selected_mode,
                        },
                    )

                    add_recent_log(recent_logs, "Mode changed: demo")

                elif (
                    clickable_rects.get("mode_train")
                    and clickable_rects["mode_train"].collidepoint(mouse_position)
                ):
                    selected_mode = "train"
                    is_playing = False

                    log_ui_event(
                        audit_logger,
                        "mode_changed",
                        {
                            "mode": selected_mode,
                        },
                    )

                    add_recent_log(recent_logs, "Mode changed: train")

                elif (
                    clickable_rects.get("speed_slow")
                    and clickable_rects["speed_slow"].collidepoint(mouse_position)
                ):
                    selected_speed = "slow"
                    bot_move_delay_ms = SPEED_OPTIONS[selected_speed]

                    log_ui_event(
                        audit_logger,
                        "speed_changed",
                        {
                            "speed": selected_speed,
                            "delay_ms": bot_move_delay_ms,
                        },
                    )

                    add_recent_log(recent_logs, "Speed changed: slow")

                elif (
                    clickable_rects.get("speed_normal")
                    and clickable_rects["speed_normal"].collidepoint(mouse_position)
                ):
                    selected_speed = "normal"
                    bot_move_delay_ms = SPEED_OPTIONS[selected_speed]

                    log_ui_event(
                        audit_logger,
                        "speed_changed",
                        {
                            "speed": selected_speed,
                            "delay_ms": bot_move_delay_ms,
                        },
                    )

                    add_recent_log(recent_logs, "Speed changed: normal")

                elif (
                    clickable_rects.get("speed_fast")
                    and clickable_rects["speed_fast"].collidepoint(mouse_position)
                ):
                    selected_speed = "fast"
                    bot_move_delay_ms = SPEED_OPTIONS[selected_speed]

                    log_ui_event(
                        audit_logger,
                        "speed_changed",
                        {
                            "speed": selected_speed,
                            "delay_ms": bot_move_delay_ms,
                        },
                    )

                    add_recent_log(recent_logs, "Speed changed: fast")

            if event.type == pygame.KEYDOWN and seed_input_active:
                if event.key == pygame.K_BACKSPACE:
                    seed_text = seed_text[:-1]

                elif event.key == pygame.K_RETURN:
                    selected_seed = parse_seed(seed_text)
                    game, bot = create_game_and_bot(selected_seed, weights)

                    moves_played = 0
                    no_available_move = False
                    last_placed_piece = "N/A"
                    final_result_logged = False

                    is_playing = True
                    seed_input_active = False
                    last_bot_step_time = pygame.time.get_ticks()

                    log_ui_event(
                        audit_logger,
                        "seed_applied",
                        {
                            "seed": selected_seed,
                            "mode": selected_mode,
                            "speed": selected_speed,
                            "weights": weights_label,
                            "max_moves": MAX_MOVES,
                        },
                    )

                    add_recent_log(
                        recent_logs,
                        f"Seed applied: {selected_seed}",
                    )

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

                log_ui_event(
                    audit_logger,
                    "no_available_move",
                    {
                        "moves_played": moves_played,
                        "seed": selected_seed,
                        "score": game.get_score(),
                        "lines": game.get_lines(),
                    },
                )

                add_recent_log(
                    recent_logs,
                    f"No available move after {moves_played} moves",
                )
            else:
                last_move = bot.get_last_move()
                decision_score = bot.get_last_score()

                log_ui_decision(
                    logger=audit_logger,
                    bot=bot,
                    move=last_move,
                    moves_played=moves_played + 1,
                    seed=selected_seed,
                    speed=selected_speed,
                    mode=selected_mode,
                )

                last_placed_piece = current_piece_name
                game.apply_bot_move(move)
                moves_played += 1

                move_piece = last_move.get("piece", "N/A")
                move_rotation = last_move.get("rotation_index", "N/A")
                move_x = last_move.get("x", "N/A")

                add_recent_log(
                    recent_logs,
                    (
                        f"Move {moves_played}: "
                        f"{move_piece} rot={move_rotation} "
                        f"x={move_x} score={format_score(decision_score)}"
                    ),
                )

            last_bot_step_time = current_time

        demo_finished = (
            game.is_game_over()
            or moves_played >= MAX_MOVES
            or no_available_move
        )

        if demo_finished and not final_result_logged:
            finish_reason = get_finish_reason(
                game=game,
                moves_played=moves_played,
                max_moves=MAX_MOVES,
                no_available_move=no_available_move,
            )

            log_ui_game_result(
                logger=audit_logger,
                game=game,
                bot=bot,
                moves_played=moves_played,
                max_moves=MAX_MOVES,
                seed=selected_seed,
                finish_reason=finish_reason,
            )

            add_recent_log(
                recent_logs,
                (
                    f"Demo finished: {finish_reason}, "
                    f"score={game.get_score()}, lines={game.get_lines()}"
                ),
            )

            final_result_logged = True

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
            "recent_logs": recent_logs,
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