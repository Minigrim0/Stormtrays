import glob
import random
import pygame


class Game:
    instance = None

    @staticmethod
    def getInstance():
        """Singleton Pattern, returns the instance of the class if
            the class does have an instance, creates it otherwise

        Returns:
            [type]: [description]
        """
        if Game.instance is None:
            Game()
        return Game.instance

    def __init__(self):
        if Game.instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            Game.instance = self

        self.songList = []
        for song in glob.glob("../musique/Themes/*.wav"):
            self.songList.append(song)

    def playMusic(self):
        """Plays the next song if the current one is finished"""
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.songList[random.randrange(len(self.songList))])
            pygame.mixer.music.play()
