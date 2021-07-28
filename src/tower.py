import pygame
import math
import glob

import src.utils as utils


class TowerDO:
    """Represents an in-game tower"""

    def __init__(self, Type_Tour, ImgsDir):

        self.vitesse_Projectile = Type_Tour.VitesseProject
        self.Projectile_Image = Type_Tour.Project_Image
        self.RoundTraj = Type_Tour.RoundTrajec
        self.vitesse = Type_Tour.vitesse
        self.degats = Type_Tour.degats
        self.portee = Type_Tour.portee
        self.prix = Type_Tour.prix
        self.Zone_Degats = Type_Tour.Zone
        self.nom = Type_Tour.nom
        self.t0 = self.vitesse / 6
        self.Position_IG = [0, 0]
        self.Tab_Image = []
        self.EnnemiKilled = 0
        self.TotalDegats = 0
        self.tps = 0
        self.i = 0
        self.Has_Ennemi2Attack = False
        self.Is_Returned = False
        self.frappe = False
        self.projectile = None
        self.Ennemi2Attack = None
        self.position_Absolue = None
        self.Rect = None

        for Img2Load in glob.glob(ImgsDir):
            Img = pygame.image.load(Img2Load).convert_alpha()
            self.Tab_Image.append(Img)
        self.Tab_ImageRet = [pygame.transform.flip(c, True, False) for c in self.Tab_Image]
        self.image = self.Tab_Image[0]

    def bougetoursouris(self, possouris, fenetre):
        """Moves the selected tower according to the tower move

        Args:
            possouris ([type]): [description]
            fenetre ([type]): [description]
        """
        if possouris[0] < 1152 and possouris[0] >= 0 and possouris[1] < 704 and possouris[1] >= 0:
            fenetre.blit(self.image, (possouris[0] - 32, possouris[1] - 32))

    def placetour(self, position_souris, fenetre, niveau):
        """Places a tower on the level

        Args:
            position_souris ([type]): [description]
            fenetre ([type]): [description]
            tableau ([type]): [description]
            Liste ([type]): [description]
            niveau ([type]): [description]
        """
        self.Position_IG[0] = (position_souris[0]) // (64)
        self.Position_IG[1] = (position_souris[1]) // (64)

        niveau.tableau[self.Position_IG[0], self.Position_IG[1]] = ("v1", 0)

        fenetre.blit(self.image, ((self.Position_IG[0] * 64), (self.Position_IG[1] * 64)))
        self.Rect = pygame.Rect((self.Position_IG[0] * 64, self.Position_IG[1] * 64), (64, 64))

        self.position_Absolue = [self.Position_IG[0] * 64, self.Position_IG[1] * 64]

    def affiche_jeu(self, fenetre):
        """Draws a tower in game

        Args:
            fenetre ([type]): [description]
        """
        if self.Is_Returned:
            self.image = self.Tab_ImageRet[self.i // (self.vitesse // 6)]
            fenetre.blit(self.image, ((self.Position_IG[0] * 64), (self.Position_IG[1] * 64)))
        else:
            self.image = self.Tab_Image[self.i // (self.vitesse // 6)]
            fenetre.blit(self.image, ((self.Position_IG[0] * 64), (self.Position_IG[1] * 64)))

    def attaque(self, Liste_Mechants, Tab_Projectile):
        """Attacks the first ennemy in its sight

        Args:
            pos_tour ([type]): [description]
            Liste_Mechants ([type]): [description]
            Tab_Projectile ([type]): [description]
        """
        if self.i == self.vitesse - 1:
            self.i = 0

        elif self.i > 0:
            if self.i == self.t0:
                Tab_Projectile.append(self.projectile)

            self.i += 1

        elif self.i == 0:
            for ennemi in Liste_Mechants:
                t = self.Time2Impact(ennemi)
                if (t - self.t0) * self.vitesse_Projectile <= self.portee * 64:
                    self.Ennemi2Attack = ennemi
                    self.i = 1
                    self.projectile = Projectile(t, self, ennemi)

                    if self.projectile.delta_x > 0:
                        self.Is_Returned = True
                    else:
                        self.Is_Returned = False

                    break

    def Time2Impact(self, ennemi):
        """Calculates the time until impact

        Args:
            ennemi ([type]): [description]

        Returns:
            [type]: [description]
        """
        delta_x = self.position_Absolue[0] - ennemi.PosAbsolue[0]
        delta_y = self.position_Absolue[1] - ennemi.PosAbsolue[1]
        Dist2 = delta_x ** 2 + delta_y ** 2

        # Cos Angle Tour|Dir Ennemi
        Cos_Beta = ennemi.Dir_x * delta_x + ennemi.Dir_y * delta_y

        # Triangle Tour/Ennemi/Impact
        # B^2 = A^2 + C^2 - 2AC cos(Beta)
        # A = Distance Ennemi|Impact = Vitesse Ennemi * temps
        # B = Distance Tour|Impact = Vitesse Projectile * (temps - tempsTir)
        # C = Distance Tour|Ennemi
        # Equation second ° pour T : a * t^2 + b * t + c = 0
        a = self.vitesse_Projectile ** 2 - ennemi.vitesse ** 2
        b = (2 * ennemi.vitesse * Cos_Beta) - (2 * self.vitesse_Projectile ** 2 * self.t0)
        c = (self.vitesse_Projectile ** 2 * self.t0 ** 2) - Dist2

        Ro = b ** 2 - 4 * a * c

        t = (-b + math.sqrt(Ro)) / (2 * a)

        return t


class Projectile:
    """Represents a projectile launched by a tower"""

    def __init__(self, t, tower, ennemi):
        self.vitesse = tower.vitesse_Projectile

        image2rot = pygame.image.load(tower.Projectile_Image).convert_alpha()

        NewPosEnnemi_x = ennemi.PosAbsolue[0] + ennemi.vitesse * ennemi.Dir_x * t
        NewPosEnnemi_y = ennemi.PosAbsolue[1] + ennemi.vitesse * ennemi.Dir_y * t

        self.delta_x = NewPosEnnemi_x - tower.Position_IG[0] * 64
        self.delta_y = NewPosEnnemi_y - tower.Position_IG[1] * 64

        self.Dist = math.sqrt(self.delta_x ** 2 + self.delta_y ** 2)

        if self.delta_x != 0:
            Angle = -math.atan(self.delta_y / self.delta_x)
            if self.delta_x > 0:
                Angle -= math.pi
            Angle = Angle * 180 / math.pi
        else:
            if ennemi.posy < tower.Position_IG[1]:
                Angle = -90
            else:
                Angle = 90

        self.image = utils.rot_center(image2rot, Angle)

        self.Centre_d_x = (NewPosEnnemi_x + tower.Position_IG[0] * 64) / 2
        self.Centre_d_y = (NewPosEnnemi_y + tower.Position_IG[1] * 64) / 2

        self.degats = tower.degats

        self.Compteur = -1

        self.tower = tower

    def Avance(self, fenetre, ListeEnnemis, niveau, Tab_Projectile, King):
        """Makes a projectile move

        Args:
            fenetre ([type]): [description]
            ListeEnnemis ([type]): [description]
            niveau ([type]): [description]
            Tab_Projectile ([type]): [description]
            King ([type]): [description]
        """
        self.Compteur += 2 * self.vitesse / self.Dist

        x0 = self.Centre_d_x + self.Compteur * (self.delta_x / 2)
        y0 = self.Centre_d_y + self.Compteur * (self.delta_y / 2)

        h = (1 - self.Compteur ** 2) * self.tower.RoundTraj * self.Dist

        x = x0
        y = y0 - h

        fenetre.blit(self.image, (x, y))

        if self.Compteur >= 1:
            for ennemi in ListeEnnemis:
                dist = math.sqrt(((x - ennemi.PosAbsolue[0]) ** 2) + ((y - ennemi.PosAbsolue[1]) ** 2))
                if dist < 64:
                    died = ennemi.enleve_vie(self.degats, ListeEnnemis, ennemi, niveau, King)
                    if died:
                        self.tower.EnnemiKilled += 1
                    self.tower.TotalDegats += self.degats
                    if self.tower.Zone_Degats != "Y":
                        break
            Tab_Projectile.remove(self)
