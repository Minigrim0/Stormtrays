import pygame

import src.constantes as const
from models.game_options import GameOptions
from UI.components.button import Button
from UI.components.text import Text


class EditorUI:
    """The UI of the editor"""

    def __init__(self, level):
        self.right_panel = pygame.Surface((158, const.WINDOW_HEIGHT))
        self.vert_line = pygame.Surface((1, const.WINDOW_WIDTH))
        self.hori_line = pygame.Surface((const.WINDOW_WIDTH, 1))
        from models.editor import Editor

        self.editor = Editor.getInstance()
        self.buttons = {}

        self._build(level)

    def _build(self, level):
        """Builds the Editor's UI"""
        options = GameOptions.getInstance()
        for index, (key, tile) in enumerate(level.tiles.items()):
            self.buttons[key] = Button(
                (const.WINDOW_WIDTH + 10 + (74 * (index % 2)), 10 + (74 * (index // 2))),
                (64, 64),
                image=tile.editor_image
            )

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
        self.buttons["heightIncrease"] = Button(
            (const.WINDOW_WIDTH + 120, const.WINDOW_HEIGHT - 140),
            (20, 20),
            image=pygame.image.load(options.fullPath("images", "buttons/increase.png")).convert_alpha(),
        )
        self.buttons["heightDecrease"] = Button(
            (const.WINDOW_WIDTH + 70, const.WINDOW_HEIGHT - 140),
            (20, 20),
            image=pygame.image.load(options.fullPath("images", "buttons/decrease.png")).convert_alpha(),
        )
        self.buttons["widthIncrease"] = Button(
            (const.WINDOW_WIDTH + 120, const.WINDOW_HEIGHT - 170),
            (20, 20),
            image=pygame.image.load(options.fullPath("images", "buttons/increase.png")).convert_alpha(),
        )
        self.buttons["widthDecrease"] = Button(
            (const.WINDOW_WIDTH + 70, const.WINDOW_HEIGHT - 170),
            (20, 20),
            image=pygame.image.load(options.fullPath("images", "buttons/decrease.png")).convert_alpha(),
        )

        font = options.fonts["MedievalSharp-xOZ5"]["20"]
        self.texts = [
            Text(
                font.render("Map info :", 1, (255, 255, 255)),
                (const.WINDOW_WIDTH + 30, const.WINDOW_HEIGHT - 195)
            ),
            Text(
                font.render("Width", 1, (255, 255, 255)),
                (const.WINDOW_WIDTH + 2, const.WINDOW_HEIGHT - 172)
            ),
            Text(
                font.render("Height", 1, (255, 255, 255)),
                (const.WINDOW_WIDTH + 2, const.WINDOW_HEIGHT - 142)
            ),
        ]

        self.right_panel.fill((128, 0, 0))
        self.vert_line.fill((0, 0, 0))
        self.hori_line.fill((0, 0, 0))

    def draw(self, screen):
        """Draws the UI on the screen"""
        for i in range(1, const.tabx):
            screen.blit(self.vert_line, (i * 64, 0))
            screen.blit(self.hori_line, (0, i * 64))

        screen.blit(self.right_panel, (const.WINDOW_WIDTH, 0))
        for _name, button in self.buttons.items():
            button.draw(screen)

        for text in self.texts:
            text.draw(screen)

        width, height = self.editor.map_info

        screen.blit(
            GameOptions.getInstance().fonts["MedievalSharp-xOZ5"]["20"].render(
                str(width), 0, (255, 255, 255)
            ),
            (const.WINDOW_WIDTH + 95, const.WINDOW_HEIGHT - 172)
        )
        screen.blit(
            GameOptions.getInstance().fonts["MedievalSharp-xOZ5"]["20"].render(
                str(height), 0, (255, 255, 255)
            ),
            (const.WINDOW_WIDTH + 95, const.WINDOW_HEIGHT - 142)
        )

    def update(self, event):
        """Handles click events"""
        if event.button == 1:
            for key in self.buttons:
                self.buttons[key].click(event.pos)
