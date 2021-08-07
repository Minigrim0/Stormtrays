import glob
import random

import pygame

from models.game_options import GameOptions
from models.screen import Screen
from UI.menus.main import MainMenu


class Stormtrays:
    """The Game singleton object, used to start the game in itself"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the model's instance, creating it if needed"""
        if Stormtrays.instance is None:
            Stormtrays()
        return Stormtrays.instance

    def __init__(self):
        if Stormtrays.instance is not None:
            raise RuntimeError("This class is a Singleton!")
        Stormtrays.instance = self

        self.screen = Screen.getInstance((1152, 704), "Stormtrays", "UI/assets/images/icon.png", False)

        GameOptions.getInstance()

        self.songList = []
        for song in glob.glob("../musique/Themes/*.wav"):
            self.songList.append(song)

        self.mainMenu = MainMenu(self.screen)

    def playMusic(self):
        """Plays the next song if the current one is finished"""
        if not pygame.mixer.music.get_busy() and len(self.songList) > 0:
            pygame.mixer.music.load(self.songList[random.randrange(len(self.songList))])
            pygame.mixer.music.play()

    def run(self):
        """Run the game by launching the main menu"""
        self.mainMenu()
