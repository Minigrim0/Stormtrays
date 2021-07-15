import os
import glob
import json

import pygame as pg

from menus.menu import Menu
from src.runnable import Runnable
import src.constantes as constants

from UI.components.card import Card
from UI.components.button import Button


class LevelSelectMenu(Menu, Runnable):
    def __init__(self, screen):
        super().__init__(screen)
        self.scrollAmount = 60

        self.background = pg.image.load(constants.fondm).convert_alpha()
        self.semiThing = pg.image.load(constants.sombre).convert_alpha()

        self.backButton = Button((654, 0), (500, 50), pg.image.load(constants.retour).convert_alpha())
        self.backButton.callback = self.back
        self.cards: [Card] = []
        self.load()

    def load(self):
        Compteur = 60
        for level in glob.glob("level/*.json"):
            with open(level) as f:
                data = json.load(f)

            try:
                img = pg.image.load(data["thumbnail"]).convert_alpha()
            except FileNotFoundError:
                img = pg.image.load("UI/assets/images/missing.png").convert_alpha()

            file = os.path.splitext(os.path.split(level)[1])[0]
            level = Card((1152 / 2 + 10, Compteur), (500, 110), img, "Level ?", "Level level !")
            level.callback = (self.runLevel, file)

            self.cards.append(level)
            Compteur += 120

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.semiThing, (0, 0))

        for card in self.cards:
            card.draw(self.screen)

        self.backButton.draw(self.screen)
        self.screen.flip()

    def loop(self):
        super().loop()
        self.draw()
        self.handleEvent()

    def handleEvent(self):
        for event in super().handleEvent():
            if event.type == pg.locals.KEYDOWN and event.key == pg.locals.K_ESCAPE:
                self.running = False

            if event.type == pg.locals.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.backButton.click(event.pos)

                    for levelcard in self.cards:
                        levelcard.click(event.pos)

                elif event.button == 5 and self.scrollAmount > -len(self.cards) * 120 + 704:
                    self.scroll(-50)
                elif event.button == 4 and self.scrollAmount < 60:
                    self.scroll(50)

    def scroll(self, amount):
        self.scrollAmount += amount
        for levelcard in self.cards:
            levelcard.move((0, amount))

    def runLevel(self, level):
        # jeu = True
        # lvl = level.File
        print("Running a level", level)
        self.running = False
        # break

    def back(self):
        self.running = False
