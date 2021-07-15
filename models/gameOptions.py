import pygame as pg


class GameOptions:
    """The options of the ongoing game"""

    instance = None

    @staticmethod
    def getInstance():
        if GameOptions.instance is None:
            GameOptions()
        return GameOptions.instance

    def __init__(self):
        if GameOptions.instance is not None:
            raise RuntimeError("Trying to instanciate a second object of a singleton class")
        GameOptions.instance = self

        self.volume = 5
        self.difficulty = 5

    def changeDifficulty(self, value):
        """Changes the difficulty of the game from the given amount"""
        self.difficulty += value

    def changeVolume(self, value):
        self.volume += value

        pg.mixer.music.set_volume(self.volume / 10)
