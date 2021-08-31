import pygame

import src.constantes as const
from models.game_options import GameOptions
from UI.components.button import Button


class EditorUI:
    """The UI of the editor"""

    def __init__(self, level):
        self.right_panel = pygame.Surface((158, const.WINDOW_HEIGHT))
        self.vert_line = pygame.Surface((1, const.WINDOW_WIDTH))
        self.hori_line = pygame.Surface((const.WINDOW_WIDTH, 1))

        options = GameOptions.getInstance()
        self.QGImg = pygame.image.load(options.fullPath("images", "QuestGiverF1.png")).convert_alpha()

        self.fond_Edit = None

        self.buttons = {}
        self.QGPos = (0, 0)

        self._build(level)

    def _build(self, level):
        options = GameOptions.getInstance()
        self.buttons["c1"] = Button((const.WINDOW_WIDTH + 10, 10), (64, 64), image=level.tiles["c1"].editor_image)
        self.buttons["t2"] = Button((const.WINDOW_WIDTH + 10, 74), (64, 64), image=level.tiles["t2"].editor_image)
        self.buttons["t1"] = Button((const.WINDOW_WIDTH + 10, 138), (64, 64), image=level.tiles["t1"].editor_image)
        self.buttons["x1"] = Button((const.WINDOW_WIDTH + 85, 10), (64, 64), image=level.tiles["x1"].editor_image)
        self.buttons["p1"] = Button((const.WINDOW_WIDTH + 85, 74), (64, 64), image=level.tiles["p1"].editor_image)
        self.buttons["v1"] = Button((const.WINDOW_WIDTH + 85, 138), (64, 64), image=level.tiles["v1"].editor_image)
        self.buttons["k1"] = Button((const.WINDOW_WIDTH + 5, 228), (192, 64), image=level.tiles["k1"].editor_image)
        self.buttons["QG"] = Button((const.WINDOW_WIDTH + 10, 292), (64, 64), image=self.QGImg)
        self.buttons["eraseButton"] = Button(
            (const.WINDOW_WIDTH + 2, const.WINDOW_HEIGHT - 45),
            (80, 30),
            image=pygame.image.load(options.fullPath("images", "buttons/erase.png")).convert_alpha(),
        )
        self.buttons["changeBackgroundButton"] = Button(
            (const.WINDOW_WIDTH + 6, const.WINDOW_HEIGHT - 100),
            (72, 44),
            image=pygame.image.load(options.fullPath("images", "buttons/change_background.png")).convert_alpha(),
        )
        self.buttons["saveButton"] = Button(
            (const.WINDOW_WIDTH + 96, const.WINDOW_HEIGHT - 50),
            (40, 40),
            image=pygame.image.load(options.fullPath("images", "buttons/save.png")).convert_alpha(),
        )
        self.buttons["loadButton"] = Button(
            (const.WINDOW_WIDTH + 96, const.WINDOW_HEIGHT - 100),
            (40, 40),
            image=pygame.image.load(options.fullPath("images", "buttons/open.png")).convert_alpha(),
        )

        self.right_panel.fill((189, 83, 64))
        self.vert_line.fill((0, 0, 0))
        self.hori_line.fill((0, 0, 0))

    def draw(self, screen):
        """Draws the UI on the screen"""
        for i in range(1, const.tabx):
            screen.blit(self.vert_line, (i * 64, 0))
            screen.blit(self.hori_line, (0, i * 64))
        screen.blit(self.right_panel, (const.WINDOW_WIDTH, 0))
        for _name, button in self.buttons.items():
            print(_name)
            button.draw(screen)

    def update(self, event):
        """Handles click events"""
        if event.button == 1:
            for key in self.buttons:
                self.buttons[key].click(event.pos)
