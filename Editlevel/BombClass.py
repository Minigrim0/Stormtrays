import pygame
import math


class Bomb (object):

    def __init__(self, Posx, Posy, time):

        self.Posx = Posx
        self.Posy = Posy
        self.Time = time
        self.i = 0
        self.TabImg = []
        self.Image = pygame.image.load(
            "../Img/Explosion/Bombe.png").convert_alpha()
        self.TabImg.append(
            pygame.image.load("../Img/Explosion/Bombe.png").convert_alpha())
        self.TabImg.append(
            pygame.image.load("../Img/Explosion/Bombe.png").convert_alpha())
        self.TabImg.append(
            pygame.image.load("../Img/Explosion/Frame1.png").convert_alpha())
        self.TabImg.append(
            pygame.image.load("../Img/Explosion/Frame2.png").convert_alpha())
        self.TabImg.append(
            pygame.image.load("../Img/Explosion/Frame3.png").convert_alpha())
        self.TabImg.append(
            pygame.image.load("../Img/Explosion/Frame4.png").convert_alpha())

    def Live(self, fenetre, TabEnnemi, niveau, coin, King, ListeBomb):
        self.i += 1
        if self.i == 6:
            self.i = 0
            self.Time -= 1

        if self.Time == 1:
            self.Image = self.TabImg[self.i]

        if self.Time <= 0:
            self.Explode(TabEnnemi, niveau, coin, King, ListeBomb)

        fenetre.blit(self.Image, (self.Posx, self.Posy))

    def Explode(self, TabEnnemi, niveau, coin, King, ListeBomb):
        for Ennemi in TabEnnemi:
            dist = math.sqrt(
                ((Ennemi.PosAbsolue[0] - self.Posx)**2)
                + ((Ennemi.PosAbsolue[1] - self.Posy)**2)
            )

            if dist <= 40:
                Ennemi.IsAttacked = True
                Ennemi.enleve_vie(20, TabEnnemi, Ennemi, niveau, coin, King)
        ListeBomb.remove(self)
