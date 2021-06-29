import pygame
import src.constantes as const
from src.button import Button


class EditorUI:
    """The UI of the editor"""

    def __init__(self, level):
        self.right_panel = pygame.Surface((158, const.WINDOW_HEIGHT))
        self.vert_line = pygame.Surface((1, const.WINDOW_WIDTH))
        self.hori_line = pygame.Surface((const.WINDOW_WIDTH, 1))

        self.fond = pygame.image.load(const.fond).convert_alpha()
        self.QGImg = pygame.image.load("img/QuestGiverF1.png").convert_alpha()

        self.fond_Edit = None

        self.buttons = {}
        self.buttons["c1"] = Button((const.WINDOW_WIDTH + 10, 10), (64, 64), level.editorImage["c1", 0])
        self.buttons["t2"] = Button((const.WINDOW_WIDTH + 10, 74), (64, 64), level.editorImage["t2", 0])
        self.buttons["t1"] = Button((const.WINDOW_WIDTH + 10, 138), (64, 64), level.editorImage["t1", 0])
        self.buttons["x1"] = Button((const.WINDOW_WIDTH + 85, 10), (64, 64), level.editorImage["x1", 0])
        self.buttons["p1"] = Button((const.WINDOW_WIDTH + 85, 74), (64, 64), level.editorImage["p1", 0])
        self.buttons["v1"] = Button((const.WINDOW_WIDTH + 85, 138), (64, 64), level.editorImage["v1", 0])
        self.buttons["k1"] = Button((const.WINDOW_WIDTH + 5, 228), (192, 64), level.editorImage["k1", 0])
        self.buttons["QG"] = Button((const.WINDOW_WIDTH + 10, 292), (64, 64), level.editorImage["QG", 0])
        self.buttons["eraseButton"] = Button(
            (const.WINDOW_WIDTH + 10, const.WINDOW_HEIGHT - 40),
            (80, 30),
            pygame.image.load(const.efface).convert_alpha(),
        )
        self.buttons["changeBackgroundButton"] = Button(
            (const.WINDOW_WIDTH + 10, const.WINDOW_HEIGHT - 100),
            (72, 44),
            pygame.image.load(const.Mini_Fond).convert_alpha(),
        )
        self.buttons["saveButton"] = Button(
            (const.WINDOW_WIDTH + 100, const.WINDOW_HEIGHT - 40),
            (40, 40),
            pygame.image.load(const.sauve).convert_alpha(),
        )
        self.buttons["loadButton"] = Button(
            (const.WINDOW_WIDTH + 150, const.WINDOW_HEIGHT - 40),
            (40, 40),
            pygame.image.load(const.ouvrir).convert_alpha(),
        )

        self.right_panel.fill((189, 83, 64))
        self.vert_line.fill((0, 0, 0))
        self.hori_line.fill((0, 0, 0))

        self.QGPos = (0, 0)

    def draw(self, screen):
        for i in range(1, const.tabx):
            screen.blit(self.vert_line, (i * 64, 0))
            screen.blit(self.hori_line, (0, i * 64))
        screen.blit(self.right_panel, (const.WINDOW_WIDTH, 0))
        for button in self.buttons.values():
            button.draw(screen)

    def update(self, event):
        if event.button == 1:
            for key in self.buttons:
                self.buttons[key].click(event.pos)
