import pygame

import src.constantes as const
from models.game_options import GameOptions
from UI.components.button import Button
from UI.components.text import Text

SIDE_PANEL_WIDTH = 180


class EditorUI:
    """The UI of the editor"""

    def __init__(self, level):
        from models.editor import Editor

        self.editor = Editor.getInstance()
        self.buttons = {}

        self._build(level)

    def _build(self, level):
        """Builds the Editor's UI"""
        options = GameOptions.getInstance()
        for index, (key, tile) in enumerate(level.tiles.items()):
            self.buttons[key] = Button(
                (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 18) + (74 * (index % 2)), 10 + (74 * (index // 2))),
                (64, 64),
                image=tile.editor_image
            )

        self.buttons["eraseButton"] = Button(
            (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 2), const.WINDOW_HEIGHT - 45),
            (80, 30),
            image=pygame.image.load(options.fullPath("images", "buttons/erase.png")).convert_alpha(),
        )
        self.buttons["changeBackgroundButton"] = Button(
            (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 6), const.WINDOW_HEIGHT - 100),
            (72, 44),
            image=pygame.image.load(options.fullPath("images", "buttons/change_background.png")).convert_alpha(),
        )
        self.buttons["saveButton"] = Button(
            (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 96), const.WINDOW_HEIGHT - 50),
            (40, 40),
            image=pygame.image.load(options.fullPath("images", "buttons/save.png")).convert_alpha(),
        )
        self.buttons["loadButton"] = Button(
            (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 96), const.WINDOW_HEIGHT - 100),
            (40, 40),
            image=pygame.image.load(options.fullPath("images", "buttons/open.png")).convert_alpha(),
        )
        self.buttons["heightIncrease"] = Button(
            (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 120), const.WINDOW_HEIGHT - 140),
            (20, 20),
            image=pygame.image.load(options.fullPath("images", "buttons/increase.png")).convert_alpha(),
        )
        self.buttons["heightDecrease"] = Button(
            (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 70), const.WINDOW_HEIGHT - 140),
            (20, 20),
            image=pygame.image.load(options.fullPath("images", "buttons/decrease.png")).convert_alpha(),
        )
        self.buttons["widthIncrease"] = Button(
            (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 120), const.WINDOW_HEIGHT - 170),
            (20, 20),
            image=pygame.image.load(options.fullPath("images", "buttons/increase.png")).convert_alpha(),
        )
        self.buttons["widthDecrease"] = Button(
            (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 70), const.WINDOW_HEIGHT - 170),
            (20, 20),
            image=pygame.image.load(options.fullPath("images", "buttons/decrease.png")).convert_alpha(),
        )

        font = options.fonts["MedievalSharp-xOZ5"]["20"]
        self.texts = [
            Text(
                font.render("Map info :", 1, (255, 255, 255)),
                (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 30), const.WINDOW_HEIGHT - 195)
            ),
            Text(
                font.render("Width", 1, (255, 255, 255)),
                (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 2), const.WINDOW_HEIGHT - 172)
            ),
            Text(
                font.render("Height", 1, (255, 255, 255)),
                (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 2), const.WINDOW_HEIGHT - 142)
            ),
        ]

    def draw(self, screen):
        """Draws the UI on the screen"""
        tile_width, tile_height = self.editor.level.tile_size
        level_position_x, level_position_y = self.editor.level.position

        for i in range(1, self.editor.level.width - 1):
            pygame.draw.line(
                screen.fenetre,
                (0, 0, 0),
                (i * tile_width + level_position_x, level_position_y),
                (i * tile_width + level_position_x, level_position_y + const.WINDOW_HEIGHT)
            )

        for i in range(1, self.editor.level.height):
            pygame.draw.line(
                screen.fenetre,
                (0, 0, 0),
                (level_position_x, (i * tile_height) + level_position_y),
                (level_position_x + const.WINDOW_WIDTH, (i * tile_height) + level_position_y)
            )

        pygame.draw.rect(
            screen.fenetre,
            (128, 0, 0),
            pygame.Rect(
                (const.WINDOW_WIDTH - 180, 0),
                (const.WINDOW_WIDTH, const.WINDOW_HEIGHT)
            )
        )

        for _name, button in self.buttons.items():
            button.draw(screen)

        for text in self.texts:
            text.draw(screen)

        width, height = self.editor.map_info

        screen.blit(
            GameOptions.getInstance().fonts["MedievalSharp-xOZ5"]["20"].render(
                str(width), 0, (255, 255, 255)
            ),
            (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 95), const.WINDOW_HEIGHT - 172)
        )
        screen.blit(
            GameOptions.getInstance().fonts["MedievalSharp-xOZ5"]["20"].render(
                str(height), 0, (255, 255, 255)
            ),
            (const.WINDOW_WIDTH - (SIDE_PANEL_WIDTH - 95), const.WINDOW_HEIGHT - 142)
        )

    def update(self, event):
        """Handles click events"""
        if event.button == 1:
            for key in self.buttons:
                self.buttons[key].click(event.pos)
