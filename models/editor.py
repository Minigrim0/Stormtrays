import os
from copy import copy
from tkinter import filedialog

import pygame

import src.constantes as consts
from models.game_options import GameOptions
from models.level import Level
from models.screen import Screen
from src.errors.invalidPositionException import InvalidPositionException
from src.runnable import Runnable
from src.tile import Tile
from UI.menus.editor import EditorUI


class Editor(Runnable):
    """The editor class, that runs handles the displaying and update of the editor"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the model's instance, creating it if needed"""
        if Editor.instance is None:
            Editor()
        return Editor.instance

    def __init__(self, screen: Screen):
        if Editor.instance is not None:
            raise RuntimeError("Trying to instanciate a second object from a singleton")
        Editor.instance = self

        self.level: Level = Level.getInstance()
        self.UI: EditorUI = EditorUI(self.level)
        self.UI.buttons["eraseButton"].setCallback(self.erase)
        self.UI.buttons["changeBackgroundButton"].setCallback(self.changeBackground)
        self.UI.buttons["loadButton"].setCallback(self.loadLevel)
        self.UI.buttons["saveButton"].setCallback(self.save)
        for code in ["c1", "t2", "t1", "x1", "p1", "v1", "k1"]:
            self.UI.buttons[code].setCallback(self.setChoice, self.level.tiles[code])

        self.choice: Tile = None
        self.mousePosition = (0, 0)
        self.screen: Screen = screen

    def loop(self):
        """Shows the editor and handles the actions to create/save/load levels"""
        self.draw()
        self.handleEvent()

        self.screen.flip()

    def handleEvent(self):
        """Handles eventual events from the user"""
        for event in self.screen.getEvent():
            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.UI.update(event)
                    self.placeTile(event)

                if event.button == 3 and self.choice is not None:
                    self.choice.rotate()

            if event.type == pygame.locals.MOUSEMOTION:
                self.mousePosition = (event.pos[0], event.pos[1])
                if self.choice is not None:
                    self.choice.move(event.pos)
                if event.buttons[0] == 1 and self.choice != "  ":
                    self.placeTile(event)

    def placeTile(self, event):
        """Places a tile on the map according to the event

        Args:
            event (pygame.Event): The event that occured
        """
        if self.choice is not None:
            x = event.pos[0] // 64
            y = event.pos[1] // 64
            if self.choice.code != "p1":
                tile = copy(self.choice)
                tile.move((x * 64, y * 64))
            else:
                tile = None

            try:
                self.level.placeTile((x, y), tile)
            except InvalidPositionException:
                pass

        if self.choice == "QG":
            self.QGPos = (x * 64, y * 64)

    def draw(self):
        """Draws the diffrent elements of the Editor on the screen"""
        self.level.draw(self.screen, editor=True)
        self.UI.draw(self.screen)

        if self.UI.QGPos:
            self.screen.blit(self.UI.QGImg, (self.UI.QGPos))

        if self.choice is not None:
            self.choice.draw(self.screen, editor=True)

    def erase(self):
        """Empties the level, and resets the tile choice"""
        self.level.initMap()
        self.choice = None

    def changeBackground(self):
        """Changes the level's background"""
        options = GameOptions.getInstance()
        filename = filedialog.askopenfilename(initialdir=options.fullPath("images", "levels"), defaultextension=".png")
        if filename:
            self.level.backgroundName = os.path.relpath(filename)
            self.level.background = pygame.image.load(self.level.backgroundName).convert_alpha()

        self.choice = None

    def loadLevel(self):
        """Loads an already created level to be modified/cloned"""
        options = GameOptions.getInstance()
        filename = filedialog.askopenfilename(initialdir=options["paths"]["levels"], defaultextension=".json")
        if filename:
            self.level.build(filename, editor=True)
        self.choice = None

    def save(self):
        """Saves the current level"""
        options = GameOptions.getInstance()
        full_path = filedialog.asksaveasfilename(initialdir=options["paths"]["levels"], defaultextension=".json")
        if full_path:
            self.level.draw(self.screen)

            arect = pygame.Rect(0, 0, consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT)
            sub = self.screen.subsurface(arect)
            sub = pygame.transform.scale(sub, (39 * 5, 22 * 5))
            dirname, filename = os.path.split(full_path)
            filename, _ext = os.path.splitext(filename)

            thumbnail_path = os.path.join(options.fullPath("levels", "thumbnails"), filename + ".png")
            pygame.image.save(sub, thumbnail_path)

            self.level.save(full_path, thumbnail_path)

        self.choice = None

    def setChoice(self, choice):
        """Sets the holded tile to the given choice

        Args:
            choice (str): The choice to set the user to
        """
        self.choice = copy(choice)
        self.choice.move(self.mousePosition)
