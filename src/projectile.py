import math

import pygame as pg

from models.screen import Screen
from models.ennemy import Ennemy

from src.utils.rotCenter import rot_center


class ProjectileDO:
    """Represents a projectile launched by a tower"""

    def __init__(self, data: dict, tower, time_before_impact):
        self.vitesse = data["speed"]
        self.curvature = data["curvature"]
        self.tower = tower
        self.target = tower.target
        self.zone_damage = data["zone"]

        image2rot = pg.image.load(data["image"]).convert_alpha()

        ennemy_final_position = (
            self.target.absolute_position[0] + self.target.speed * self.target.direction[0] * time_before_impact,
            self.target.absolute_position[1] + self.target.speed * self.target.direction[1] * time_before_impact
        )
        self.final_pos = ennemy_final_position

        self.delta_x = ennemy_final_position[0] - tower.absolute_position[0]
        self.delta_y = ennemy_final_position[1] - tower.absolute_position[1]

        self.Dist = math.sqrt(self.delta_x ** 2 + self.delta_y ** 2)

        if self.delta_x != 0:
            Angle = -math.atan(self.delta_y / self.delta_x)
            if self.delta_x > 0:
                Angle -= math.pi
            Angle = Angle * 180 / math.pi
        else:
            if self.target.position[1] < tower.absolute_position[1]:
                Angle = -90
            else:
                Angle = 90

        self.image = rot_center(image2rot, Angle)

        self.Centre_d_x = (ennemy_final_position[0] + tower.absolute_position[0]) / 2
        self.Centre_d_y = (ennemy_final_position[1] + tower.absolute_position[1]) / 2

        self.degats = self.tower.damage

        self.advancement = -1

        self.position: tuple = tower.absolute_position

    @property
    def hasHit(self):
        return self.advancement >= 1

    def _dealDamage(self):
        ennemy_list = Ennemy.getInstance().getEnnemyList()

        for ennemi in ennemy_list:
            dist = math.sqrt(
                ((self.position[0] - ennemi.absolute_position[0]) ** 2) + ((self.position[1] - ennemi.absolute_position[1]) ** 2)
            )
            if dist < 64:
                died = ennemi.hit(self.degats)
                if died:
                    self.tower.EnnemiKilled += 1
                self.tower.TotalDegats += self.degats
                if self.zone_damage is not True:
                    break

    def update(self, timeElapsed: float):
        self.advancement += timeElapsed * 64 * self.vitesse / self.Dist

        if self.advancement >= 1:
            self._dealDamage()

        x0 = self.Centre_d_x + self.advancement * (self.delta_x / 2)
        y0 = self.Centre_d_y + self.advancement * (self.delta_y / 2)

        height = (1 - self.advancement ** 2) * self.curvature * self.Dist

        self.position = (
            x0,
            y0 - height
        )

    def draw(self, screen: Screen):
        """Makes a projectile move"""
        screen.blit(self.image, self.position)
