import pygame
import math

from models.screen import Screen

from src.projectile import Projectile

from UI.components.imageAnimation import ImageAnimation


class TowerDO:
    """Represents an in-game tower"""

    def __init__(self, tower_data, position: tuple = (0, 0)):

        self.data = tower_data
        self.animation = ImageAnimation(
            self.data["animation"],
            flippable=True,
            callback=self.shoot,
            speed=self.data["fire_rate"],
            bank_name=self.data["animation"]
        )

        self.placed: bool = False
        self.position: tuple = position

        # self.t0 = self.vitesse / 6
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

    @property
    def flipped(self):
        return self.animation.flipped

    @property
    def absolute_position(self):
        return (
            self.position[0] * 64,
            self.position[1] * 64,
        )

    def place(self):
        """Places a tower on the level"""
        self.position = (
            self.position[0] // 64,
            self.position[1] // 64
        )
        self.placed = True

        self.Rect = pygame.Rect((self.absolute_position[0] * 64, self.absolute_position[1] * 64), (64, 64))
        return True

    def draw(self, screen: Screen):
        """Draws the tower on the screen"""
        if self.placed:
            self.animation.draw(screen, self.absolute_position)
        else:
            print(self.position)
            self.animation.draw(screen, self.position)

    def update(self, timeElapsed: float):
        self.animation.update(timeElapsed)

    def shoot(self):
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
        delta_x = self.absolute_position[0] - ennemi.PosAbsolue[0]
        delta_y = self.absolute_position[1] - ennemi.PosAbsolue[1]
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

    def setPosition(self, position: tuple):
        self.position = position
        print(position)
