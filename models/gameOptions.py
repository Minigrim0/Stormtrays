import os
import glob
import json

import pygame as pg

from src.utils.bound import bound


class GameOptions:
    """The options of the ongoing game"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the model's instance, creating it if needed"""
        if GameOptions.instance is None:
            GameOptions()
        return GameOptions.instance

    def __init__(self):
        if GameOptions.instance is not None:
            raise RuntimeError("Trying to instanciate a second object of a singleton class")
        GameOptions.instance = self

        self.volume = 5
        self.difficulty = 5

        self.fonts = {}

    def __getitem__(self, category: str) -> dict:
        if category not in self.settings.keys():
            return None
        return self.settings[category]

    def load(self):
        """Loads the game's fonts"""
        for font in glob.glob("UI/assets/fonts/*/*.ttf"):
            filename = os.path.splitext(os.path.split(font)[1])[0]
            self.fonts[filename] = {}
            for size in [12, 14, 18, 25, 35, 40, 100]:
                self.fonts[filename][str(size)] = pg.font.Font(font, size)

        with open("assets/settings.json") as settings:
            self.settings = json.load(settings)

    def changeDifficulty(self, value):
        """Changes the difficulty of the game from the given amount (and makes sure it's in its bounds)"""
        self.difficulty += value
        self.difficulty = bound(1, 10, self.difficulty)

    def changeVolume(self, value):
        """Modifies the volume options, and updates it in pygame (and makes sure it's in its bounds)"""
        self.volume += value
        self.volume = bound(0, 10, self.volume)
        pg.mixer.music.set_volume(self.volume / 10)
