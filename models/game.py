import glob
import random
import pygame

import src.constantes as constants
from UI.menus.main import MainMenu
from models.screen import Screen
from models.gameOptions import GameOptions


class Game:
    """The Game singleton object, used to start the game in itself"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the model's instance, creating it if needed"""
        if Game.instance is None:
            Game()
        return Game.instance

    def __init__(self):
        if Game.instance is not None:
            raise RuntimeError("This class is a Singleton!")
        Game.instance = self

        self.screen = Screen.getInstance((1152, 704), "StormTarys", constants.IconImg, False)

        GameOptions.getInstance().load()

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
