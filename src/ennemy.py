import pygame
import src.constantes as constantes
from src.gold import GoldAnim

import glob


class EnnemyDO:
    """Represent an in game ennemy, keeps the health etc..."""

    def __init__(self, data):
        self.posx = 0
        self.posy = 0
        self.count = 0
        self.PosAbsolue = (0, 0)
        self.i = 0
        self.Returned = False
        self.IsAttacked = False
        self.BlitLife = False
        self.tab = []
        self.tab_ret = []
        self.Dir_x = 0
        self.Dir_y = 0
        self.Tics = 0

        self.propriete = data

        self.Name = self.propriete["Name"]
        self.image2Scale = pygame.image.load(self.propriete["Img"]).convert_alpha()
        # self.meurt = pygame.mixer.Sound(self.propriete["DeathSound"])
        self.vie = self.propriete["LifePts"]
        self.vie_bas = self.propriete["LifePts"]
        self.vitesse = self.propriete["Speed"]
        self.Height = self.propriete["Height"]
        self.image = pygame.transform.scale(self.image2Scale, (self.Height, self.Height))
        self.Vie_Rect_Arriere = pygame.Surface((self.vie * (60 / self.vie), 3))
        self.Vie_Rect_Arriere.fill((255, 0, 0))

        for filename in glob.glob(self.propriete["ImgFolder"]):
            Img2Scale = pygame.image.load(filename).convert_alpha()
            Img = pygame.transform.scale(Img2Scale, (self.Height, self.Height))
            self.tab.append(Img)

        for filename in glob.glob(self.propriete["ImgFolderRet"]):
            ImgR2Scale = pygame.image.load(filename).convert_alpha()
            ImgR = pygame.transform.scale(ImgR2Scale, (self.Height, self.Height))
            self.tab_ret.append(ImgR)

        self.HitBox = None
        self.Vie_Rect = None

    def pose_ennemi(self, tableau):
        """Adds an ennemy to the game

        Args:
            tableau ([type]): [description]
        """
        self.posx = 0
        self.posy = 0

        x = 0
        for y in range(11):
            position = tableau[x][y]
            if position == ("c1", 0):
                self.posy = y
                self.PosAbsolue = (0, y * 64)
                self.HitBox = pygame.Rect((0, y), (64, 64))

    def draw(self, screen):
        """Blits the ennemy on the screen

        Args:
            screen ([type]): [description]
        """
        screen.blit(self.image, (self.PosAbsolue))

    def bouge(self, tableau, fenetre, niveau, Liste_Mechants, King):
        """Makes the ennemy move

        Args:
            tableau ([type]): [description]
            fenetre ([type]): [description]
            niveau ([type]): [description]
            Liste_Mechants ([type]): [description]
            coin ([type]): [description]
            King ([type]): [description]
        """
        try:
            self.Vie_Rect = pygame.Surface((self.vie * (60 / self.vie_bas), 3))
        except ZeroDivisionError as e:
            print("Warning :", e)
        self.Vie_Rect.fill((0, 255, 0))

        if self.IsAttacked:
            self.Tics += 1
            self.BlitLife = True

        if self.Tics == 50:
            self.IsAttacked = False
            self.BlitLife = False
            self.Tics = 0

        position = tableau[self.posx, self.posy]

        self.count += 1

        # PLUS EN X  (->)
        if position in (("c1", 0), ("t1", 180), ("t2", 270)):
            self.Dir_x = 1
            self.Dir_y = 0
            self.Returned = False

        # MOINS EN Y (^)
        elif position in (("c1", 90), ("t1", 270), ("t2", 0)):
            self.Dir_x = 0
            self.Dir_y = -1
            self.Returned = False

        # MOINS EN X (<-)
        elif position in (("c1", 180), ("t1", 0), ("t2", 90)):
            self.Dir_x = -1
            self.Dir_y = 0
            self.Returned = True

        # PLUS EN Y (v)
        elif position in (("c1", 270), ("t1", 90), ("t2", 180)):
            self.Dir_x = 0
            self.Dir_y = 1
            self.Returned = True

        elif position[0] == "x1":
            self.Dir_x = self.Dir_x
            self.Dir_y = self.Dir_y
            self.Returned = self.Returned

        else:
            print("Position erronée")
            self.pose_ennemi(tableau)

        if self.count == round(64 / self.vitesse):

            self.count = 0

            self.posx += self.Dir_x
            self.posy += self.Dir_y

            if self.BlitLife:
                fenetre.blit(self.Vie_Rect_Arriere, (self.posx * 64, self.posy * 64))
                fenetre.blit(self.Vie_Rect, (self.posx * 64, self.posy * 64))
            fenetre.blit(self.image, (self.posx * 64, self.posy * 64))

        else:

            self.PosAbsolue = (
                self.posx * 64 + (self.count * self.vitesse * self.Dir_x),
                self.posy * 64 + (self.count * self.vitesse * self.Dir_y),
            )
            if self.BlitLife:
                fenetre.blit(self.Vie_Rect_Arriere, self.PosAbsolue)
                fenetre.blit(self.Vie_Rect, self.PosAbsolue)

            fenetre.blit(self.image, self.PosAbsolue)
            self.HitBox = pygame.Rect(self.PosAbsolue, (64, 64))
            self.anim()

        if self.posx == niveau.pos_Chateau[0] and self.posy == niveau.pos_Chateau[1]:
            niveau.Vie_Chateau -= self.vie // 1.5
            self.enleve_vie(2000, Liste_Mechants, self, niveau, King)

    def enleve_vie(self, viemoins, liste_mech, ennemi, niveau, King):
        """Makes the ennemy loose life

        Args:
            viemoins ([type]): [description]
            liste_mech ([type]): [description]
            ennemi ([type]): [description]
            niveau ([type]): [description]
            King ([type]): [description]

        Returns:
            [type]: [description]
        """
        self.vie -= viemoins
        self.IsAttacked = True
        self.Tics = 0

        if self.vie <= 0:
            constantes.DicoEnnemisKilled[self.Name] += 1
            liste_mech.remove(ennemi)
            # self.meurt.play()
            if King.capacite1 is True:
                FlyingGold = GoldAnim(
                    (self.PosAbsolue[0] + self.Height // 2, self.PosAbsolue[1] + self.Height // 2), self.vie_bas
                )
                constantes.GoldGained[0] += self.vie_bas
                niveau.GoldTab.append(FlyingGold)
                niveau.gold += self.vie_bas

            else:
                FlyingGold = GoldAnim((self.PosAbsolue[0] + 32, self.PosAbsolue[1] + 32), self.vie_bas // 2)
                constantes.GoldGained[0] += self.vie_bas // 2
                niveau.GoldTab.append(FlyingGold)
                niveau.gold += self.vie_bas // 2

            niveau.Nombre_Ennemis_Tue += 1
            return True
        return False

    def anim(self):
        """Animates the ennemy"""
        self.i += 1
        if self.i == 12:
            self.i = 0
        if self.Returned:
            self.image = self.tab_ret[self.i // 2]
        else:
            self.image = self.tab[self.i // 2]
