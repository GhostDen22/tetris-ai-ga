from pathlib import Path

import pygame


FEATURE_NAMES = [
    "holes",
    "aggregate_height",
    "max_height",
    "bumpiness",
    "lines_cleared",
    "well_sums",
    "row_transitions",
    "column_transitions",
]


class InfoPanel:
    def __init__(self, x=332, y=34, width=920, height=690):
        self.rect = pygame.Rect(x, y, width, height)

        self.background_color = (28, 33, 44)
        self.card_color = (39, 45, 58)
        self.card_border_color = (90, 112, 148)

        self.button_color = (54, 65, 86)
        self.button_hover_color = (67, 81, 108)
        self.button_active_color = (67, 176, 235)
        self.button_warning_color = (242, 195, 87)

        self.input_color = (23, 27, 36)
        self.input_active_color = (36, 47, 65)

        self.title_color = (248, 250, 252)
        self.text_color = (236, 240, 246)
        self.muted_color = (180, 188, 201)
        self.good_color = (104, 232, 153)
        self.warning_color = (255, 205, 88)

        self.board_empty_color = (43, 49, 63)
        self.board_filled_color = (110, 203, 244)
        self.board_grid_color = (76, 91, 116)

        self.font_title = pygame.font.SysFont("arial", 31, bold=True)
        self.font_subtitle = pygame.font.SysFont("arial", 15)
        self.font_header = pygame.font.SysFont("arial", 20, bold=True)
        self.font_text = pygame.font.SysFont("arial", 16, bold=True)
        self.font_small = pygame.font.SysFont("arial", 14, bold=True)
        self.font_tiny = pygame.font.SysFont("arial", 12)
        self.font_button = pygame.font.SysFont("arial", 14, bold=True)
        self.font_logo_fallback = pygame.font.SysFont("arial", 18, bold=True)

        self.logo_surface = self.load_logo()

    def recolor_surface_to_white(self, surface):
        recolored = surface.copy()
        width, height = recolored.get_size()

        for px in range(width):
            for py in range(height):
                color = recolored.get_at((px, py))
                if color.a > 0:
                    recolored.set_at((px, py), pygame.Color(245, 248, 252, color.a))

        return recolored

    def load_logo(self):
        possible_paths = [
            Path("assets/UWB_logo.png"),
            Path("assets/UWB_logo.svg"),
        ]

        for path in possible_paths:
            if not path.exists():
                continue

            try:
                logo = pygame.image.load(str(path)).convert_alpha()
                logo = pygame.transform.smoothscale(logo, (112, 42))
                logo = self.recolor_surface_to_white(logo)
                return logo
            except pygame.error:
                continue

        return None

    def draw_text(self, surface, text, x, y, font, color):
        rendered = font.render(str(text), True, color)
        surface.blit(rendered, (x, y))

    def format_value(self, value):
        if isinstance(value, float):
            return f"{value:.2f}"
        return value

    def clip_text_to_width(self, text, font, max_width):
        text = str(text)

        if font.size(text)[0] <= max_width:
            return text

        ellipsis = "..."

        while text and font.size(text + ellipsis)[0] > max_width:
            text = text[:-1]

        return text + ellipsis

    def draw_card(self, surface, x, y, width, height, title):
        rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(surface, self.card_color, rect, border_radius=14)
        pygame.draw.rect(surface, self.card_border_color, rect, 1, border_radius=14)

        self.draw_text(
            surface,
            title,
            x + 16,
            y + 14,
            self.font_header,
            self.title_color,
        )

        return x + 16, y + 48

    def draw_logo(self, surface):
        logo_width = 128
        logo_height = 52
        logo_x = self.rect.right - logo_width - 24
        logo_y = self.rect.y + 14

        logo_rect = pygame.Rect(logo_x, logo_y, logo_width, logo_height)

        pygame.draw.rect(surface, self.card_color, logo_rect, border_radius=12)
        pygame.draw.rect(surface, self.card_border_color, logo_rect, 1, border_radius=12)

        if self.logo_surface is not None:
            logo_image_x = logo_x + (logo_width - self.logo_surface.get_width()) // 2
            logo_image_y = logo_y + (logo_height - self.logo_surface.get_height()) // 2
            surface.blit(self.logo_surface, (logo_image_x, logo_image_y))
        else:
            fallback_text = "UwB"
            fallback_surface = self.font_logo_fallback.render(
                fallback_text,
                True,
                self.title_color,
            )
            text_x = logo_x + (logo_width - fallback_surface.get_width()) // 2
            text_y = logo_y + (logo_height - fallback_surface.get_height()) // 2
            surface.blit(fallback_surface, (text_x, text_y))

    def draw_divider(self, surface, x, y, width):
        pygame.draw.line(
            surface,
            self.card_border_color,
            (x, y),
            (x + width, y),
            1,
        )

    def draw_button(self, surface, label, x, y, width, height, selected=False, warning=False):
        rect = pygame.Rect(x, y, width, height)

        mouse_position = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_position)

        if selected:
            color = self.button_active_color
        elif warning:
            color = self.button_warning_color
        elif hovered:
            color = self.button_hover_color
        else:
            color = self.button_color

        pygame.draw.rect(surface, color, rect, border_radius=9)

        text_surface = self.font_button.render(label, True, self.title_color)
        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (height - text_surface.get_height()) // 2

        surface.blit(text_surface, (text_x, text_y))
        return rect

    def draw_seed_input(self, surface, seed_text, is_active, x, y, width, height):
        rect = pygame.Rect(x, y, width, height)

        color = self.input_active_color if is_active else self.input_color

        pygame.draw.rect(surface, color, rect, border_radius=9)
        pygame.draw.rect(surface, self.card_border_color, rect, 1, border_radius=9)

        display_text = seed_text if seed_text else "42"
        suffix = "|" if is_active else ""

        self.draw_text(
            surface,
            f"{display_text}{suffix}",
            x + 12,
            y + 8,
            self.font_text,
            self.text_color,
        )

        return rect

    def draw_controls(self, surface, ui_state, x, y, width, height):
        content_x, content_y = self.draw_card(
            surface,
            x,
            y,
            width,
            height,
            "Controls",
        )

        rects = {}

        selected_mode = ui_state["selected_mode"]
        is_playing = ui_state["is_playing"]
        selected_speed = ui_state["selected_speed"]

        button_height = 32

        first_row_y = content_y - 8
        second_row_y = content_y + 32

        play_label = "Stop" if is_playing else "Start"

        rects["toggle_play"] = self.draw_button(
            surface,
            play_label,
            content_x,
            first_row_y,
            82,
            button_height,
            selected=is_playing,
        )

        rects["reset"] = self.draw_button(
            surface,
            "Reset",
            content_x + 94,
            first_row_y,
            82,
            button_height,
            warning=True,
        )

        self.draw_text(
            surface,
            "Seed",
            content_x + 196,
            first_row_y + 8,
            self.font_small,
            self.muted_color,
        )

        rects["seed_input"] = self.draw_seed_input(
            surface,
            ui_state["seed_text"],
            ui_state["seed_input_active"],
            content_x + 240,
            first_row_y,
            108,
            button_height,
        )

        self.draw_text(
            surface,
            "Press Enter or Reset to apply seed.",
            content_x + 366,
            first_row_y + 9,
            self.font_tiny,
            self.muted_color,
        )

        self.draw_text(
            surface,
            "Mode",
            content_x,
            second_row_y + 8,
            self.font_small,
            self.muted_color,
        )

        rects["mode_demo"] = self.draw_button(
            surface,
            "Demo",
            content_x + 52,
            second_row_y,
            72,
            button_height,
            selected=selected_mode == "demo",
        )

        rects["mode_train"] = self.draw_button(
            surface,
            "Train",
            content_x + 136,
            second_row_y,
            72,
            button_height,
            selected=selected_mode == "train",
        )

        self.draw_text(
            surface,
            "Speed",
            content_x + 238,
            second_row_y + 8,
            self.font_small,
            self.muted_color,
        )

        rects["speed_slow"] = self.draw_button(
            surface,
            "Slow",
            content_x + 296,
            second_row_y,
            64,
            button_height,
            selected=selected_speed == "slow",
        )

        rects["speed_normal"] = self.draw_button(
            surface,
            "Normal",
            content_x + 372,
            second_row_y,
            82,
            button_height,
            selected=selected_speed == "normal",
        )

        rects["speed_fast"] = self.draw_button(
            surface,
            "Fast",
            content_x + 466,
            second_row_y,
            64,
            button_height,
            selected=selected_speed == "fast",
        )

        return rects

    def get_status(self, game, ui_state):
        game_over = game.is_game_over()
        selected_mode = ui_state["selected_mode"]
        is_playing = ui_state["is_playing"]
        demo_finished = ui_state["demo_finished"]
        no_available_move = ui_state["no_available_move"]

        if selected_mode == "train":
            return "Train preview selected", self.warning_color

        if demo_finished:
            if game_over:
                return "Demo finished: game over", self.warning_color
            if no_available_move:
                return "Demo finished: no move", self.warning_color
            return "Demo finished: max moves", self.warning_color

        if is_playing:
            return "Running", self.good_color

        return "Stopped", self.warning_color

    def draw_game_info(self, surface, game, ui_state, x, y, width, height):
        content_x, content_y = self.draw_card(surface, x, y, width, height, "Game info")

        status, status_color = self.get_status(game, ui_state)

        rows = [
            ("Mode", ui_state["selected_mode"]),
            ("Weights", ui_state["weights_label"]),
            ("Seed", game.get_seed()),
            ("Score", game.get_score()),
            ("Lines", game.get_lines()),
            ("Moves", ui_state["moves_played"]),
            ("Max moves", ui_state["max_moves"]),
            ("Game over", game.is_game_over()),
        ]

        for label, value in rows:
            self.draw_text(
                surface,
                f"{label}: {self.format_value(value)}",
                content_x,
                content_y,
                self.font_text,
                self.text_color,
            )
            content_y += 18

        self.draw_text(
            surface,
            f"Status: {status}",
            content_x,
            content_y,
            self.font_text,
            status_color,
        )
        content_y += 28

        self.draw_divider(surface, content_x, content_y, width - 32)
        content_y += 14

        self.draw_text(
            surface,
            "Final summary",
            content_x,
            content_y,
            self.font_header,
            self.title_color,
        )
        content_y += 28

        if ui_state["demo_finished"]:
            final_rows = [
                ("Final score", game.get_score()),
                ("Final lines", game.get_lines()),
                ("Moves played", ui_state["moves_played"]),
            ]
        else:
            final_rows = [
                ("Final score", "not finished"),
                ("Final lines", "not finished"),
                ("Moves played", ui_state["moves_played"]),
            ]

        for label, value in final_rows:
            self.draw_text(
                surface,
                f"{label}: {self.format_value(value)}",
                content_x,
                content_y,
                self.font_text,
                self.text_color,
            )
            content_y += 18

    def draw_piece_info(self, surface, bot, ui_state, x, y, width, height):
        content_x, content_y = self.draw_card(
            surface,
            x,
            y,
            width,
            height,
            "Pieces and last decision",
        )

        move = bot.get_last_move()
        decision_score = bot.get_last_score()

        rows = [
            ("Current piece", ui_state["current_piece"]),
            ("Last placed", ui_state["last_placed_piece"]),
        ]

        if move is None:
            rows.extend(
                [
                    ("Last decision", "Waiting"),
                    ("Rotation", "N/A"),
                    ("X", "N/A"),
                    ("Decision score", "N/A"),
                ]
            )
        else:
            rows.extend(
                [
                    ("Last decision", move.get("piece", "N/A")),
                    ("Rotation", move.get("rotation_index", "N/A")),
                    ("X", move.get("x", "N/A")),
                    ("Decision score", self.format_value(decision_score)),
                ]
            )

        for label, value in rows:
            self.draw_text(
                surface,
                f"{label}: {value}",
                content_x,
                content_y,
                self.font_text,
                self.text_color,
            )
            content_y += 19

    def draw_features(self, surface, bot, x, y, width, height):
        content_x, content_y = self.draw_card(surface, x, y, width, height, "Features")

        features = bot.get_features()

        if not features:
            self.draw_text(
                surface,
                "Waiting for bot decision...",
                content_x,
                content_y,
                self.font_text,
                self.muted_color,
            )
            return

        for name in FEATURE_NAMES:
            value = self.format_value(features.get(name, "N/A"))
            self.draw_text(
                surface,
                f"{name}: {value}",
                content_x,
                content_y,
                self.font_small,
                self.text_color,
            )
            content_y += 17

    def draw_reasons(self, surface, bot, x, y, width, height):
        content_x, content_y = self.draw_card(surface, x, y, width, height, "Top 3 reasons")

        reasons = bot.get_last_reasons()

        if not reasons:
            self.draw_text(
                surface,
                "Waiting for first decision...",
                content_x,
                content_y,
                self.font_text,
                self.muted_color,
            )
            return

        for index, reason in enumerate(reasons[:3], start=1):
            feature = reason.get("feature", "N/A")
            value = self.format_value(reason.get("value", "N/A"))
            weight = self.format_value(reason.get("weight", "N/A"))
            contribution = self.format_value(reason.get("contribution", "N/A"))

            self.draw_text(
                surface,
                f"{index}. {feature}",
                content_x,
                content_y,
                self.font_text,
                self.title_color,
            )
            content_y += 18

            self.draw_text(
                surface,
                f"value = {value}",
                content_x + 12,
                content_y,
                self.font_small,
                self.text_color,
            )
            content_y += 16

            self.draw_text(
                surface,
                f"weight = {weight}",
                content_x + 12,
                content_y,
                self.font_small,
                self.text_color,
            )
            content_y += 16

            self.draw_text(
                surface,
                f"contribution = {contribution}",
                content_x + 12,
                content_y,
                self.font_small,
                self.text_color,
            )
            content_y += 24

    def draw_recent_logs(self, surface, recent_logs, x, y, width, height):
        content_x, content_y = self.draw_card(surface, x, y, width, height, "Recent logs")

        max_text_width = width - 34
        bottom_limit = y + height - 14

        if not recent_logs:
            self.draw_text(
                surface,
                "No UI logs yet.",
                content_x,
                content_y,
                self.font_text,
                self.muted_color,
            )
            return

        visible_logs = recent_logs[-3:]

        for log_line in visible_logs:
            if content_y + 18 > bottom_limit:
                break

            clipped_log = self.clip_text_to_width(
                f"- {log_line}",
                self.font_small,
                max_text_width,
            )

            self.draw_text(
                surface,
                clipped_log,
                content_x,
                content_y,
                self.font_small,
                self.text_color,
            )
            content_y += 19

    def draw_mini_board(self, surface, board, x, y, cell_size=3):
        rows = 20
        cols = 10

        for row in range(rows):
            for col in range(cols):
                value = 0

                if row < len(board) and col < len(board[row]):
                    value = board[row][col]

                cell_rect = pygame.Rect(
                    x + col * cell_size,
                    y + row * cell_size,
                    cell_size,
                    cell_size,
                )

                color = self.board_filled_color if value else self.board_empty_color

                pygame.draw.rect(surface, color, cell_rect)
                pygame.draw.rect(surface, self.board_grid_color, cell_rect, 1)

    def draw_train_preview_card(self, surface, preview, x, y, width, height):
        card_rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(surface, (33, 39, 51), card_rect, border_radius=10)
        pygame.draw.rect(surface, self.card_border_color, card_rect, 1, border_radius=10)

        board_x = x + 10
        board_y = y + 12

        self.draw_mini_board(
            surface=surface,
            board=preview["board"],
            x=board_x,
            y=board_y,
            cell_size=3,
        )

        text_x = board_x + 42
        text_y = y + 12

        rows = [
            f"Genome {preview['id']}",
            f"Seed: {preview['seed']}",
            f"Score: {preview['score']}",
            f"Lines: {preview['lines']}",
            f"Fit: {preview['fitness_hint']}",
        ]

        for index, line in enumerate(rows):
            font = self.font_small if index == 0 else self.font_tiny
            color = self.title_color if index == 0 else self.text_color

            clipped_line = self.clip_text_to_width(
                line,
                font,
                width - 58,
            )

            self.draw_text(
                surface,
                clipped_line,
                text_x,
                text_y,
                font,
                color,
            )

            text_y += 15

    def draw_train_previews(self, surface, previews, preview_moves, x, y, width, height):
        content_x, content_y = self.draw_card(
            surface,
            x,
            y,
            width,
            height,
            "Train mode preview",
        )

        self.draw_text(
            surface,
            f"Random generation preview, {preview_moves} moves per genome",
            content_x,
            content_y,
            self.font_tiny,
            self.muted_color,
        )

        content_y += 22

        if not previews:
            self.draw_text(
                surface,
                "No train preview data.",
                content_x,
                content_y,
                self.font_text,
                self.muted_color,
            )
            return

        gap = 8
        card_width = (width - 32 - gap) // 2
        card_height = 92

        for index, preview in enumerate(previews[:4]):
            col = index % 2
            row = index // 2

            card_x = content_x + col * (card_width + gap)
            card_y = content_y + row * (card_height + gap)

            self.draw_train_preview_card(
                surface=surface,
                preview=preview,
                x=card_x,
                y=card_y,
                width=card_width,
                height=card_height,
            )

    def draw(self, surface, game, bot, ui_state):
        clickable_rects = {}

        pygame.draw.rect(surface, self.background_color, self.rect, border_radius=18)
        pygame.draw.rect(surface, self.card_border_color, self.rect, 2, border_radius=18)

        title_x = self.rect.x + 24
        title_y = self.rect.y + 18

        self.draw_text(
            surface,
            "TetrisGA Demo",
            title_x,
            title_y,
            self.font_title,
            self.title_color,
        )

        self.draw_text(
            surface,
            "Autonomous Tetris bot dashboard",
            title_x,
            title_y + 34,
            self.font_subtitle,
            self.muted_color,
        )

        self.draw_logo(surface)

        panel_padding = 20
        column_gap = 14
        row_gap = 20

        controls_y = self.rect.y + 76
        controls_height = 120
        content_y = controls_y + controls_height + row_gap

        available_width = self.rect.width - panel_padding * 2 - column_gap * 2
        column_width = available_width // 3

        left_x = self.rect.x + panel_padding
        middle_x = left_x + column_width + column_gap
        right_x = middle_x + column_width + column_gap

        clickable_rects.update(
            self.draw_controls(
                surface=surface,
                ui_state=ui_state,
                x=left_x,
                y=controls_y,
                width=self.rect.width - panel_padding * 2,
                height=controls_height,
            )
        )

        self.draw_game_info(
            surface=surface,
            game=game,
            ui_state=ui_state,
            x=left_x,
            y=content_y,
            width=column_width,
            height=438,
        )

        if ui_state["selected_mode"] == "train":
            self.draw_train_previews(
                surface=surface,
                previews=ui_state.get("train_previews", []),
                preview_moves=ui_state.get("train_preview_moves", 0),
                x=middle_x,
                y=content_y,
                width=column_width * 2 + column_gap,
                height=438,
            )
        else:
            self.draw_piece_info(
                surface=surface,
                bot=bot,
                ui_state=ui_state,
                x=middle_x,
                y=content_y,
                width=column_width,
                height=180,
            )

            self.draw_features(
                surface=surface,
                bot=bot,
                x=middle_x,
                y=content_y + 196,
                width=column_width,
                height=242,
            )

            self.draw_reasons(
                surface=surface,
                bot=bot,
                x=right_x,
                y=content_y,
                width=column_width,
                height=300,
            )

            self.draw_recent_logs(
                surface=surface,
                recent_logs=ui_state.get("recent_logs", []),
                x=right_x,
                y=content_y + 316,
                width=column_width,
                height=122,
            )

        return clickable_rects