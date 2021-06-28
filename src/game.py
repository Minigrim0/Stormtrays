import glob
import random
import pygame


class Game:
    def __init__(self):
        self.Tableau_Musique = []
        for Muse in glob.glob("../musique/Themes/*.wav"):
            self.Tableau_Musique.append(Muse)

    def playMusic(self):
        """Plays the next song if the current one is finished"""
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.Tableau_Musique[random.randrange(len(self.Tableau_Musique))])
            pygame.mixer.music.play()
