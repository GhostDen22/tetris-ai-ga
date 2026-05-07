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
    def __init__(self, x=365, y=50, width=735, height=640):
        self.rect = pygame.Rect(x, y, width, height)

        self.background_color = (20, 24, 32)
        self.card_color = (25, 30, 39)
        self.card_border_color = (72, 84, 105)

        self.title_color = (245, 247, 250)
        self.text_color = (214, 220, 230)
        self.muted_color = (150, 160, 175)
        self.good_color = (100, 220, 140)
        self.warning_color = (245, 190, 80)

        self.font_title = pygame.font.SysFont("arial", 30, bold=True)
        self.font_subtitle = pygame.font.SysFont("arial", 15)
        self.font_header = pygame.font.SysFont("arial", 19, bold=True)
        self.font_text = pygame.font.SysFont("arial", 16)
        self.font_small = pygame.font.SysFont("arial", 14)

    def draw_text(self, surface, text, x, y, font, color):
        rendered = font.render(str(text), True, color)
        surface.blit(rendered, (x, y))

    def format_value(self, value):
        if isinstance(value, float):
            return f"{value:.2f}"
        return value

    def draw_card(self, surface, x, y, width, height, title):
        rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(surface, self.card_color, rect, border_radius=12)
        pygame.draw.rect(surface, self.card_border_color, rect, 1, border_radius=12)

        self.draw_text(
            surface,
            title,
            x + 16,
            y + 14,
            self.font_header,
            self.title_color,
        )

        return x + 16, y + 46

    def draw_game_info(
        self,
        surface,
        game,
        mode_label,
        moves_played,
        max_moves,
        demo_finished,
        no_available_move,
        x,
        y,
        width,
        height,
    ):
        content_x, content_y = self.draw_card(
            surface,
            x,
            y,
            width,
            height,
            "Game info",
        )

        game_over = game.is_game_over()

        if demo_finished:
            if game_over:
                status = "Demo finished: game over"
            elif no_available_move:
                status = "Demo finished: no move"
            else:
                status = "Demo finished: max moves"

            status_color = self.warning_color
        else:
            status = "Running"
            status_color = self.good_color

        rows = [
            ("Mode", mode_label),
            ("Seed", game.get_seed()),
            ("Score", game.get_score()),
            ("Lines", game.get_lines()),
            ("Moves", moves_played),
            ("Max moves", max_moves),
            ("Game over", game_over),
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
            content_y += 23

        self.draw_text(
            surface,
            f"Status: {status}",
            content_x,
            content_y + 4,
            self.font_text,
            status_color,
        )

    def draw_last_move(self, surface, bot, x, y, width, height):
        content_x, content_y = self.draw_card(
            surface,
            x,
            y,
            width,
            height,
            "Last move",
        )

        move = bot.get_last_move()
        decision_score = bot.get_last_score()

        if move is None:
            self.draw_text(
                surface,
                "Waiting for first bot move...",
                content_x,
                content_y,
                self.font_text,
                self.muted_color,
            )
            return

        rows = [
            ("Piece", move.get("piece", "N/A")),
            ("Rotation", move.get("rotation_index", "N/A")),
            ("X", move.get("x", "N/A")),
            ("Decision score", self.format_value(decision_score)),
        ]

        for label, value in rows:
            self.draw_text(
                surface,
                f"{label}: {value}",
                content_x,
                content_y,
                self.font_text,
                self.text_color,
            )
            content_y += 24

    def draw_final_summary(
        self,
        surface,
        game,
        moves_played,
        demo_finished,
        x,
        y,
        width,
        height,
    ):
        content_x, content_y = self.draw_card(
            surface,
            x,
            y,
            width,
            height,
            "Final summary",
        )

        if not demo_finished:
            self.draw_text(
                surface,
                "Demo is still running.",
                content_x,
                content_y,
                self.font_text,
                self.muted_color,
            )
            return

        rows = [
            ("Final score", game.get_score()),
            ("Final lines", game.get_lines()),
            ("Moves played", moves_played),
        ]

        for label, value in rows:
            self.draw_text(
                surface,
                f"{label}: {value}",
                content_x,
                content_y,
                self.font_text,
                self.text_color,
            )
            content_y += 24

    def draw_features(self, surface, bot, x, y, width, height):
        content_x, content_y = self.draw_card(
            surface,
            x,
            y,
            width,
            height,
            "Features",
        )

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
            content_y += 21

    def draw_reasons(self, surface, bot, x, y, width, height):
        content_x, content_y = self.draw_card(
            surface,
            x,
            y,
            width,
            height,
            "Top 3 reasons",
        )

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
                self.text_color,
            )
            content_y += 20

            self.draw_text(
                surface,
                f"value={value}   weight={weight}",
                content_x + 14,
                content_y,
                self.font_small,
                self.muted_color,
            )
            content_y += 18

            self.draw_text(
                surface,
                f"contribution={contribution}",
                content_x + 14,
                content_y,
                self.font_small,
                self.muted_color,
            )
            content_y += 28

    def draw_footer(self, surface):
        line_y = self.rect.bottom - 42
        text_y = self.rect.bottom - 28

        pygame.draw.line(
            surface,
            self.card_border_color,
            (self.rect.x + 24, line_y),
            (self.rect.right - 24, line_y),
            1,
        )

        self.draw_text(
            surface,
            "UI displays backend data only. No AI, GA or Tetris logic is implemented here.",
            self.rect.x + 28,
            text_y,
            self.font_small,
            self.muted_color,
        )

    def draw(
        self,
        surface,
        game,
        bot,
        mode_label,
        moves_played,
        max_moves,
        demo_finished=False,
        no_available_move=False,
    ):
        pygame.draw.rect(surface, self.background_color, self.rect, border_radius=16)
        pygame.draw.rect(surface, self.card_border_color, self.rect, 2, border_radius=16)

        title_x = self.rect.x + 28
        title_y = self.rect.y + 22

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

        left_x = self.rect.x + 24
        right_x = self.rect.x + 388
        top_y = self.rect.y + 92

        left_width = 340
        right_width = 323

        self.draw_game_info(
            surface=surface,
            game=game,
            mode_label=mode_label,
            moves_played=moves_played,
            max_moves=max_moves,
            demo_finished=demo_finished,
            no_available_move=no_available_move,
            x=left_x,
            y=top_y,
            width=left_width,
            height=238,
        )

        self.draw_last_move(
            surface=surface,
            bot=bot,
            x=left_x,
            y=top_y + 252,
            width=left_width,
            height=150,
        )

        self.draw_final_summary(
            surface=surface,
            game=game,
            moves_played=moves_played,
            demo_finished=demo_finished,
            x=left_x,
            y=top_y + 416,
            width=left_width,
            height=92,
        )

        self.draw_features(
            surface=surface,
            bot=bot,
            x=right_x,
            y=top_y,
            width=right_width,
            height=238,
        )

        self.draw_reasons(
            surface=surface,
            bot=bot,
            x=right_x,
            y=top_y + 252,
            width=right_width,
            height=256,
        )

        self.draw_footer(surface)