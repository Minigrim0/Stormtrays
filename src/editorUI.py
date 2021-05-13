import pygame
import src.constantes as const
from src.button import Button


class EditorUI(object):

    def __init__(self):
        self.right_panel = pygame.Surface((200, const.WINDOW_HEIGHT))
        self.vert_line = pygame.Surface((1, const.WINDOW_WIDTH))
        self.hori_line = pygame.Surface((const.WINDOW_WIDTH, 1))

        self.fond = pygame.image.load(const.fond).convert_alpha()
        self.QGImg = pygame.image.load("img/QuestGiverF1.png").convert_alpha()

        self.fond_Edit = None

        self.rect = {}
        self.rect["c1"] = pygame.Rect((const.WINDOW_WIDTH + 10, 0), (64, 64))
        self.rect["t2"] = pygame.Rect((const.WINDOW_WIDTH + 10, 64), (64, 64))
        self.rect["t1"] = pygame.Rect((const.WINDOW_WIDTH + 10, 128), (64, 64))
        self.rect["x1"] = pygame.Rect((const.WINDOW_WIDTH + 85, 0), (64, 64))
        self.rect["p1"] = pygame.Rect((const.WINDOW_WIDTH + 85, 64), (64, 64))
        self.rect["v1"] = pygame.Rect((const.WINDOW_WIDTH + 85, 128), (64, 64))
        self.rect["k1"] = pygame.Rect((const.WINDOW_WIDTH, 218), (192, 64))
        self.rect["QG"] = pygame.Rect((const.WINDOW_WIDTH + 10, 282), (64, 64))

        self.eraseButton = Button(
            (const.WINDOW_WIDTH + 10, const.WINDOW_HEIGHT - 40),
            (80, 30),
            pygame.image.load(const.efface).convert_alpha()
        )

        self.changeBackgroundButton = Button(
            (const.WINDOW_WIDTH + 10, const.WINDOW_HEIGHT - 100),
            (72, 44),
            pygame.image.load(const.Mini_Fond).convert_alpha()
        )

        self.saveButton = Button(
            (const.WINDOW_WIDTH + 100, const.WINDOW_HEIGHT - 40),
            (40, 40),
            pygame.image.load(const.sauve).convert_alpha()
        )

        self.loadButton = Button(
            (const.WINDOW_WIDTH + 150, const.WINDOW_HEIGHT - 40),
            (40, 40),
            pygame.image.load(const.ouvrir).convert_alpha()
        )

        self.right_panel.fill((189, 83, 64))
        self.vert_line.fill((0, 0, 0))
        self.hori_line.fill((0, 0, 0))

        self.QGPos = (0, 0)

    def draw(self, screen):
        for i in range(1, const.tabx):
            screen.blit(self.vert_line, (i*64, 0))
            screen.blit(self.hori_line, (0, i*64))
        screen.blit(self.right_panel, (const.WINDOW_WIDTH, 0))
        self.eraseButton.draw(screen)
        self.saveButton.draw(screen)
        self.loadButton.draw(screen)
        self.changeBackgroundButton.draw(screen)

    def update(self, screen, event, niveau, choix):
        if event.button == 1:
            for key in self.rect:
                if self.rect[key].collidepoint(event.pos):
                    choix = key

            self.eraseButton.click(event.pos)
            self.changeBackgroundButton.click(event.pos)
            self.loadButton.click(event.pos)
            self.saveButton.click(event.pos)

        return choix
