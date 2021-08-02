import math

import pygame as pg

from models.screen import Screen

from src.utils.rotCenter import rot_center


class ProjectileDO:
    """Represents a projectile launched by a tower"""

    def __init__(self, data: dict, tower, target, time_before_impact):
        self.vitesse = data["speed"]

        image2rot = pg.image.load(data["image"]).convert_alpha()

        NewPosEnnemi_x = target.PosAbsolue[0] + target.vitesse * target.Dir_x * time_before_impact
        NewPosEnnemi_y = target.PosAbsolue[1] + target.vitesse * target.Dir_y * time_before_impact

        self.delta_x = NewPosEnnemi_x - tower.absolute_position[0] * 64
        self.delta_y = NewPosEnnemi_y - tower.absolute_position[1] * 64

        self.Dist = math.sqrt(self.delta_x ** 2 + self.delta_y ** 2)

        if self.delta_x != 0:
            Angle = -math.atan(self.delta_y / self.delta_x)
            if self.delta_x > 0:
                Angle -= math.pi
            Angle = Angle * 180 / math.pi
        else:
            if target.posy < tower.absolute_position[1]:
                Angle = -90
            else:
                Angle = 90

        self.image = rot_center(image2rot, Angle)

        self.Centre_d_x = (NewPosEnnemi_x + tower.absolute_position[0] * 64) / 2
        self.Centre_d_y = (NewPosEnnemi_y + tower.absolute_position[1] * 64) / 2

        self.degats = tower.damage

        self.Compteur = -1

        self.tower = tower

    def update(self, timeElapsed: float):
        pass

    def draw(self, screen: Screen):
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

        screen.blit(self.image, (x, y))

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
