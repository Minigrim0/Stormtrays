import os
from tkinter import filedialog
import pygame

from src.editorUI import EditorUI
from src.screen import Screen
from src.classes import Niveau

import src.constantes as consts


class Editor:
    def __init__(self):
        self.UI = EditorUI()
        self.UI.eraseButton.callback = self.erase
        self.UI.changeBackgroundButton.callback = self.changeBackground
        self.UI.loadButton.callback = self.loadLevel
        self.UI.saveButton.callback = self.save

        self.running = True

        self.choix = "  "
        self.rot = 0
        self.niveau = Niveau()
        self.possouris = (0, 0)

    def run(self, screen: Screen):
        while self.running:
            self.draw(screen)

            for event in screen.getEvent():
                self.handleEvent(screen, event)

    def handleEvent(self, screen: Screen, event: pygame.event.Event):
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.choix = self.UI.update(screen, event, self.niveau, self.choix)

                    x = event.pos[0] // 64
                    y = event.pos[1] // 64
                    else:
                        self.niveau.tableau[x, y] = self.choix, self.rot

            if event.button == 3 and self.choix != "  ":
                self.rot = (self.rot + 90) % 360

        if event.type == pygame.locals.MOUSEMOTION:
            self.possouris = (event.pos[0], event.pos[1])

                x = event.pos[0] // 64
                y = event.pos[1] // 64
                        self.niveau.tableau[x, y] = self.choix, self.rot

    def draw(self, screen):
        self.niveau.afficheE(screen, self.UI.fond)
        self.UI.draw(screen)

        if self.UI.QGPos:
            screen.blit(self.UI.QGImg, (self.UI.QGPos))

        if self.choix != "  ":
            screen.blit(
                self.niveau.imgE[self.choix, self.rot],
                ((self.possouris[0] // 64) * 64, (self.possouris[1] // 64) * 64)
            )

        for v in self.UI.rect:
            screen.blit(
                self.niveau.imgE[v, 0], (self.UI.rect[v].x, self.UI.rect[v].y))

        screen.flip()

    def erase(self):
        self.niveau.videtab()
        self.choix = "  "

    def changeBackground(self):
        filename = filedialog.askopenfilename(
            initialdir="img/Fonds", defaultextension=".png")
        if filename:
            self.UI.fond_Edit = os.path.relpath(filename)
            self.UI.fond = pygame.image.load(self.UI.fond_Edit).convert_alpha()

        self.choix = "  "

    def loadLevel(self):
        filename = filedialog.askopenfilename(
            initialdir="level", defaultextension=".txt")
        if filename:
            self.niveau.construit(filename)
        self.choix = "  "

    def save(self):
        filename = filedialog.asksaveasfilename(
            initialdir="level", defaultextension=".txt")
        if filename:
            self.niveau.sauve(filename)
            self.niveau.sauveF(filename, self.fond_Edit, self.QGPos)
            # self.niveau.affiche(screen, self.fond)
            pygame.display.flip()
            arect = pygame.Rect(
                0, 0, consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT)
            sub = screen.subsurface(arect)
            sub = pygame.transform.scale(sub, (39*5, 22*5))
            dirname, filename = os.path.split(filename)
            filename, ext = os.path.splitext(filename)
            pygame.image.save(
                sub, os.path.join(
                    dirname, "mininiveau", filename+".png"
                )
            )

        self.choix = "  "
