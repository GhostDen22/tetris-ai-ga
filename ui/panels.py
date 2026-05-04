import pygame


class InfoPanel:
    def __init__(self, x=410, y=90, width=520, height=560):
        self.rect = pygame.Rect(x, y, width, height)

        self.background_color = (24, 28, 36)
        self.border_color = (70, 80, 100)
        self.title_color = (240, 240, 245)
        self.text_color = (210, 215, 225)
        self.muted_color = (150, 160, 175)

        self.font_title = pygame.font.SysFont("arial", 30, bold=True)
        self.font_header = pygame.font.SysFont("arial", 24, bold=True)
        self.font_text = pygame.font.SysFont("arial", 22)

    def draw_text(self, surface, text, x, y, font, color):
        rendered = font.render(str(text), True, color)
        surface.blit(rendered, (x, y))

    def draw(self, surface, game, bot):
        pygame.draw.rect(surface, self.background_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=10)

        x = self.rect.x + 30
        y = self.rect.y + 25

        self.draw_text(surface, "TetrisGA Demo", x, y, self.font_title, self.title_color)
        y += 55

        self.draw_text(surface, "Game info", x, y, self.font_header, self.title_color)
        y += 40

        score = game.get_score()
        lines = game.get_lines()
        seed = game.get_seed()

        self.draw_text(surface, f"Score: {score}", x, y, self.font_text, self.text_color)
        y += 32
        self.draw_text(surface, f"Lines: {lines}", x, y, self.font_text, self.text_color)
        y += 32
        self.draw_text(surface, f"Seed: {seed}", x, y, self.font_text, self.text_color)

        y += 60

        self.draw_text(surface, "Features", x, y, self.font_header, self.title_color)
        y += 40

        features = bot.get_features()

        feature_names = [
            "holes",
            "aggregate_height",
            "bumpiness",
            "lines_cleared",
        ]

        for name in feature_names:
            value = features.get(name, "N/A")
            self.draw_text(
                surface,
                f"{name}: {value}",
                x,
                y,
                self.font_text,
                self.text_color,
            )
            y += 32

        y += 40
        self.draw_text(
            surface,
            "UI only displays backend data.",
            x,
            y,
            self.font_text,
            self.muted_color,
        )
        y += 28
        self.draw_text(
            surface,
            "No game or AI logic here.",
            x,
            y,
            self.font_text,
            self.muted_color,
        )