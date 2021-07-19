import os
import glob
import json

import pygame as pg

from menus.menu import Menu
from src.runnable import Runnable
import src.constantes as constants

from UI.components.card import Card
from UI.components.button import Button

from animations.animation import Animation


class LevelSelectMenu(Menu, Runnable):
    """The level selection menu"""

    def __init__(self, screen):
        super().__init__(screen)
        self.scrollAmount = 60

        self.background = pg.image.load(constants.fondm).convert_alpha()
        self.semiThing = pg.image.load(constants.sombre).convert_alpha()

        self.buttons.append(Button((654, 0), (500, 50), pg.image.load(constants.retour).convert_alpha(), self.back))

        self.cards: [Card] = []
        self.load()

    def load(self):
        """Generates the levels' cards"""
        Compteur = 60
        for index, level in enumerate(glob.glob("levels/*.json")):
            with open(level) as f:
                data = json.load(f)

            try:
                img = pg.image.load(data["thumbnail"]).convert_alpha()
            except FileNotFoundError:
                img = pg.image.load("UI/assets/images/missing.png").convert_alpha()

            file = os.path.splitext(os.path.split(level)[1])[0]
            level = Card((1152 / 2 + 10, Compteur), (500, 110), img, file, f"Level {index + 1}")
            level.setCallback(self.runLevel, file)

            self.cards.append(level)
            Compteur += 120

    def loop(self):
        """The bit of code called at each iteration"""
        super().loop()

        self.draw()
        self.screen.flip()

        self.handleEvent()

    def draw(self):
        """Draws the buttons/images on screen and refreshes it"""
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.semiThing, (0, 0))
        super().draw()

        for card in self.cards:
            card.draw(self.screen)

    def handleEvent(self):
        """Handles the user inputs"""
        for event in super().handleEvent():
            if event.type == pg.locals.KEYDOWN and event.key == pg.locals.K_ESCAPE:
                self.back()

            if event.type == pg.locals.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for levelcard in self.cards:
                        levelcard.click(event.pos)

                elif event.button == 5 and self.scrollAmount > -len(self.cards) * 120 + 704:
                    self.scroll(-40)
                elif event.button == 4 and self.scrollAmount < 60:
                    self.scroll(40)

    def scroll(self, amount):
        """Moves the levelss cards up or down"""
        self.scrollAmount += amount
        for levelcard in self.cards:
            levelcard.move((0, amount))

    def runLevel(self, level):
        """Callback for the levels' cards, launches the selected level"""
        # jeu = True
        # lvl = level.File
        print("Running a level", level)
        self.running = False
        # break

    def back(self):
        """Callback for the back button, gets the user back to the main menu"""
        anim = Animation("animations/mainToSelect.json", self.screen)
        anim.invert()
        anim()
        self.running = False
