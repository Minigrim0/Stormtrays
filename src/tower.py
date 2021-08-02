import pygame
import math

from models.screen import Screen
from models.ennemy import Ennemy
from models.projectile import Projectile

from src.ennemy import EnnemyDO

from UI.components.imageAnimation import ImageAnimation


class TowerDO:
    """Represents an in-game tower"""

    def __init__(self, tower_data, position: tuple = (0, 0)):
        self.placed: bool = False
        self.position: tuple = position
        self.range = tower_data["range"]

        self.target: EnnemyDO = None

        self.t0 = tower_data["fire_rate"] / 6

        self.EnnemiKilled = 0
        self.TotalDegats = 0

        self.projectile_model = Projectile.getInstance()[tower_data["projectile"]]
        self.Rect = None

        self.animation = ImageAnimation(
            tower_data["animation"],
            flippable=True,
            callback=self.shoot,
            speed=tower_data["fire_rate"],
            bank_name=tower_data["animation"]
        )

    @property
    def flipped(self):
        return self.animation.flipped

    @property
    def absolute_position(self):
        return (
            self.position[0] * 64,
            self.position[1] * 64,
        )

    def _targetInRange(self, target: EnnemyDO = None):
        target = target if target is not None else self.target

        t = self.Time2Impact(target)
        return (t - self.t0) * self.projectile_model["speed"] <= self.range * 64

    def _acquireTarget(self):
        for ennemy in Ennemy.getInstance().getEnnemyList():
            if self._targetInRange(ennemy):
                self.target = ennemy
                if self.target.position[0] > self.position[0]:
                    self.animation.flip()
                break

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
            self.animation.draw(screen, self.position)

    def update(self, timeElapsed: float):
        if self.placed:
            if self.target is not None:
                if self._targetInRange():
                    self.animation.play()
                else:
                    self.animation.reset()
            else:
                self._acquireTarget()

            self.animation.update(timeElapsed)

    def shoot(self):
        """Attacks the first ennemy in its sight

        Args:
            pos_tour ([type]): [description]
            Liste_Mechants ([type]): [description]
            Tab_Projectile ([type]): [description]
        """
        print("Shooting projectile")
        # Tab_Projectile.append(self.projectile)

    def Time2Impact(self, ennemi):
        """Calculates the time until impact

        Args:
            ennemi ([type]): [description]

        Returns:
            [type]: [description]
        """
        delta_x = self.absolute_position[0] - ennemi.absolute_position[0]
        delta_y = self.absolute_position[1] - ennemi.absolute_position[1]
        Dist2 = delta_x ** 2 + delta_y ** 2

        # Cos Angle Tour|Dir Ennemi
        Cos_Beta = ennemi.direction[0] * delta_x + ennemi.direction[1] * delta_y

        # Triangle Tour/Ennemi/Impact
        # B^2 = A^2 + C^2 - 2AC cos(Beta)
        # A = Distance Ennemi|Impact = Vitesse Ennemi * temps
        # B = Distance Tour|Impact = Vitesse Projectile * (temps - tempsTir)
        # C = Distance Tour|Ennemi
        # Equation second ° pour T : a * t^2 + b * t + c = 0
        print(self.projectile_model)
        a = self.projectile_model["speed"] ** 2 - ennemi.speed ** 2
        b = (2 * ennemi.speed * Cos_Beta) - (2 * self.projectile_model["speed"] ** 2 * self.t0)
        c = (self.projectile_model["speed"] ** 2 * self.t0 ** 2) - Dist2

        Ro = b ** 2 - 4 * a * c

        t = (-b + math.sqrt(Ro)) / (2 * a)

        return t

    def setPosition(self, position: tuple):
        self.position = position
