import glob
import json
import os

import pygame as pg

from src.utils.bound import bound
import gettext


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
        self.game_speed = 1

        self.tile_size: int = 64
        self.map_size: tuple = (18, 11)

        self.window_size = (
            self.tile_size * self.map_size[0],
            self.tile_size * self.map_size[1]
        )

        self.fonts = {}

        self.lang = None

        self._load()

    def __getitem__(self, category: str) -> dict:
        if category not in self.settings.keys():
            return None
        return self.settings[category]

    def _load(self):
        """Loads the game's fonts"""
        for font in glob.glob("UI/assets/fonts/*/*.ttf"):
            filename = os.path.splitext(os.path.split(font)[1])[0]
            self.fonts[filename] = {}
            for size in [12, 14, 20, 25, 35, 40, 60, 100]:
                self.fonts[filename][str(size)] = pg.font.Font(font, size)

        with open("assets/settings.json") as settings:
            self.settings = json.load(settings)

        self._loadLang()

    def _loadLang(self):
        self.lang = gettext.translation('stormtrays', localedir='locales', languages=[self["Game"]["lang"]])
        self.lang.install()

    def fullPath(self, category, path):
        """Returns the concatenated full path for a category and a sub path"""
        return os.path.join(self["paths"][category], path)

    def changeDifficulty(self, value):
        """Changes the difficulty of the game from the given amount (and makes sure it's in its bounds)"""
        self.difficulty += value
        self.difficulty = bound(1, 10, self.difficulty)

    def changeVolume(self, value):
        """Modifies the volume options, and updates it in pygame (and makes sure it's in its bounds)"""
        self.volume += value
        self.volume = bound(0, 10, self.volume)
        pg.mixer.music.set_volume(self.volume / 10)

    def toggleGameSpeed(self):
        """Toggles the speed of the game between *4 et *1"""
        self.game_speed = 1 if self.game_speed == 4 else 4

    def setSpeed(self, speed: int):
        """Changes the speed of the game to the given speed"""
        self.game_speed = speed

    def setLang(self, lang):
        self.settings["Game"]["lang"] = lang

        with open("assets/settings.json", "w") as settings:
            json.dump(self.settings, settings)

        self._loadLang()

    def get_lang(self):
        return self.lang.gettext
