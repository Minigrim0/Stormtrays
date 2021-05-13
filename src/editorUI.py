import pygame
import src.constantes as const
from src.button import Button

from tkinter import filedialog
import os


class EditorUI(object):

    def __init__(self):
        # Images
        self.right_panel = pygame.Surface((200, const.WINDOW_HEIGHT))
        self.vert_line = pygame.Surface((1, const.WINDOW_WIDTH))
        self.hori_line = pygame.Surface((const.WINDOW_WIDTH, 1))

        self.MicroFond = pygame.image.load(const.Mini_Fond).convert_alpha()
        self.fond = pygame.image.load(const.fond).convert_alpha()
        self.efface = pygame.image.load(const.efface).convert_alpha()
        self.sauve = pygame.image.load(const.sauve).convert_alpha()
        self.ouvre = pygame.image.load(const.ouvrir).convert_alpha()
        self.QGImg = pygame.image.load("img/QuestGiverF1.png").convert_alpha()

        self.fond_Edit = None

        # (Collide)Rects
        self.rect = {}
        self.rect["c1"] = pygame.Rect((const.WINDOW_WIDTH + 10, 0), (64, 64))
        self.rect["t2"] = pygame.Rect((const.WINDOW_WIDTH + 10, 64), (64, 64))
        self.rect["t1"] = pygame.Rect((const.WINDOW_WIDTH + 10, 128), (64, 64))
        self.rect["x1"] = pygame.Rect((const.WINDOW_WIDTH + 85, 0), (64, 64))
        self.rect["p1"] = pygame.Rect((const.WINDOW_WIDTH + 85, 64), (64, 64))
        self.rect["v1"] = pygame.Rect((const.WINDOW_WIDTH + 85, 128), (64, 64))
        self.rect["k1"] = pygame.Rect((const.WINDOW_WIDTH, 218), (192, 64))
        self.rect["QG"] = pygame.Rect((const.WINDOW_WIDTH + 10, 282), (64, 64))

        self.changeBackgroundRect = pygame.Rect(
            (const.WINDOW_WIDTH + 10, const.WINDOW_HEIGHT - 100), (72, 44))
        self.eraseRect = pygame.Rect(
            (const.WINDOW_WIDTH + 10, const.WINDOW_HEIGHT - 40), (80, 30))
        self.saveRect = pygame.Rect(
            (const.WINDOW_WIDTH + 100, const.WINDOW_HEIGHT - 40), (40, 40))
        self.loadRect = pygame.Rect(
            (const.WINDOW_WIDTH + 150, const.WINDOW_HEIGHT - 40), (40, 40))

        self.eraseButton = Button((0, 0), (0, 0), self.efface)

        self.right_panel.fill((189, 83, 64))
        self.vert_line.fill((0, 0, 0))
        self.hori_line.fill((0, 0, 0))

        self.QGPos = (0, 0)

    def draw(self, screen):
        for i in range(1, const.tabx):
            screen.blit(self.vert_line, (i*64, 0))
            screen.blit(self.hori_line, (0, i*64))
        screen.blit(self.right_panel, (const.WINDOW_WIDTH, 0))
        screen.blit(self.efface, (self.eraseRect.x, self.eraseRect.y))
        screen.blit(self.sauve, (self.saveRect.x,   self.saveRect.y))
        screen.blit(self.ouvre, (self.loadRect.x, self.loadRect.y))
        screen.blit(
            self.MicroFond,
            (self.changeBackgroundRect.x, self.changeBackgroundRect.y)
        )

    def save(self, niveau, screen):
        filename = filedialog.asksaveasfilename(
            initialdir="level", defaultextension=".txt")
        if filename:
            niveau.sauve(filename)
            niveau.sauveF(filename, self.fond_Edit, self.QGPos)
            niveau.affiche(screen, self.fond)
            pygame.display.flip()
            arect = pygame.Rect(
                0, 0, const.WINDOW_WIDTH, const.WINDOW_HEIGHT)
            sub = screen.subsurface(arect)
            sub = pygame.transform.scale(sub, (39*5, 22*5))
            dirname, filename = os.path.split(filename)
            filename, ext = os.path.splitext(filename)
            pygame.image.save(
                sub, os.path.join(
                    dirname, "mininiveau", filename+".png"
                )
            )

    def load(self, niveau):
        filename = filedialog.askopenfilename(
            initialdir="level", defaultextension=".txt")
        if filename:
            niveau.construit(filename)

    def changeBackground(self):
        filename = filedialog.askopenfilename(
            initialdir="img/Fonds", defaultextension=".png")
        if filename:
            self.fond_Edit = os.path.relpath(filename)
            self.fond = pygame.image.load(self.fond_Edit).convert_alpha()

    def update(self, screen, event, niveau, choix, rot, possouris):
        if event.button == 1:
            for key in self.rect:
                if self.rect[key].collidepoint(event.pos):
                    choix = key
                    rot = 0

                if self.eraseRect.collidepoint(event.pos):
                    niveau.videtab()
                    choix = "  "

                elif self.changeBackgroundRect.collidepoint(event.pos):
                    self.changeBackground()
                    choix = "  "

                elif self.loadRect.collidepoint(event.pos):
                    self.load(niveau)
                    choix = "  "

                elif self.saveRect.collidepoint(event.pos):
                    self.save(niveau, screen)
                    choix = "  "

            if choix != "  ":
                x = event.pos[0]//64
                y = event.pos[1]//64
                if choix == "p1":
                    niveau.tableau[x, y] = "  ", 0
                elif choix == "QG":
                    self.QGPos = (x*64, y*64)
                else:
                    niveau.tableau[x, y] = choix, rot

        elif event.button == 3 and choix != "  ":
            rot = (rot + 90) % 360

        return possouris, rot, choix
