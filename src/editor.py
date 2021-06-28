import os
from tkinter import filedialog
import pygame

from src.editorUI import EditorUI
from src.screen import Screen
from src.classes import Niveau

import src.constantes as consts


class Editor:
    """The editor class, that runs handles the displaying and update of the editor"""

    def __init__(self):
        self.level = Niveau()
        self.UI = EditorUI(self.level)
        self.UI.buttons["eraseButton"].callback = self.erase
        self.UI.buttons["changeBackgroundButton"].callback = self.changeBackground
        self.UI.buttons["loadButton"].callback = self.loadLevel
        self.UI.buttons["saveButton"].callback = self.save
        for buttonID in ["c1", "t2", "t1", "x1", "p1", "v1", "k1", "QG"]:
            self.UI.buttons[buttonID].callback = self.setChoice, buttonID

        self.running = True

        self.choice = None
        self.rot = 0
        self.mousePosition = (0, 0)

    def run(self, screen: Screen):
        """Shows the editor and handles the actions to create/save/load levels

        Args:
            screen (Screen): The screen object to blit images
        """
        while self.running:
            self.draw(screen)

            for event in screen.getEvent():
                self.handleEvent(screen, event)

    def handleEvent(self, screen: Screen, event: pygame.event.Event):
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.UI.update(event)

                if self.choice is not None:
                    x = event.pos[0] // 64
                    y = event.pos[1] // 64
                    if self.choice == "p1":
                        self.level.map[x, y] = "  ", 0
                    elif self.choice == "QG":
                        self.QGPos = (x * 64, y * 64)
                    else:
                        self.level.map[x, y] = self.choice, self.rot

            if event.button == 3 and self.choice != "  ":
                self.rot = (self.rot + 90) % 360

        if event.type == pygame.locals.MOUSEMOTION:
            self.mousePosition = (event.pos[0], event.pos[1])

            if event.buttons[0] == 1 and self.choice != "  ":
                x = event.pos[0] // 64
                y = event.pos[1] // 64
                if self.choice == "p1":
                    self.level.map[x, y] = "  ", 0
                else:
                    self.level.map[x, y] = self.choice, self.rot

    def draw(self, screen: Screen):
        """Draws the diffrent elements of the Editor on the screen

        Args:
            screen (Screen): The screen to blit the editor elements on
        """
        self.level.afficheE(screen, self.UI.fond)
        self.UI.draw(screen)

        if self.UI.QGPos:
            screen.blit(self.UI.QGImg, (self.UI.QGPos))

        if self.choice is not None:
            screen.blit(
                self.level.editorImage[self.choice, self.rot],
                ((self.mousePosition[0] // 64) * 64, (self.mousePosition[1] // 64) * 64),
            )

        screen.flip()

    def erase(self):
        """Empties the level, and resets the tile choice"""
        self.level.empty()
        self.choice = "  "

    def changeBackground(self):
        """Changes the level's background"""
        filename = filedialog.askopenfilename(initialdir="img/Fonds", defaultextension=".png")
        if filename:
            self.UI.fond_Edit = os.path.relpath(filename)
            self.UI.fond = pygame.image.load(self.UI.fond_Edit).convert_alpha()

        self.choice = "  "

    def loadLevel(self):
        """Loads an already created level to be modified/cloned"""
        filename = filedialog.askopenfilename(initialdir="level", defaultextension=".txt")
        if filename:
            self.level.construit(filename)
        self.choice = "  "

    def save(self):
        """Saves the current level"""
        filename = filedialog.asksaveasfilename(initialdir="level", defaultextension=".txt")
        if filename:
            self.level.sauve(filename)
            self.level.sauveF(filename, self.fond_Edit, self.QGPos)
            # self.niveau.affiche(screen, self.fond)
            pygame.display.flip()
            arect = pygame.Rect(0, 0, consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT)
            sub = screen.subsurface(arect)
            sub = pygame.transform.scale(sub, (39 * 5, 22 * 5))
            dirname, filename = os.path.split(filename)
            filename, ext = os.path.splitext(filename)
            pygame.image.save(sub, os.path.join(dirname, "mininiveau", filename + ".png"))

        self.choice = "  "

    def setChoice(self, choice):
        """Sets the holded tile to the given choice

        Args:
            choice (str): The choice to set the user to
        """
        self.choice = choice
