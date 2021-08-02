import math

import pygame as pg

from models.screen import Screen
from models.ennemy import Ennemy

from src.utils.rot_center import rotCenter
from src.utils.distance_between import distance_between
from src.ennemy import EnnemyDO


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

        self.image = rotCenter(image2rot, Angle)

        self.trajectory_top = (
            (ennemy_final_position[0] + tower.absolute_position[0]) / 2,
            (ennemy_final_position[1] + tower.absolute_position[1]) / 2
        )

        self.degats = self.tower.damage

        self.advancement = -1

        self.position: tuple = tower.absolute_position

    @property
    def hasHit(self) -> bool:
        """Returns an indication on whether the projectile has hit its target or not"""
        return self.advancement >= 1

    def _dealDamage(self):
        """Deals damage to one or multiple ennemies in a small range around the impact"""
        ennemy_list: [EnnemyDO] = Ennemy.getInstance().getEnnemyList()

        for ennemy in ennemy_list:
            if distance_between(self.position, ennemy.absolute_position) < 64:
                if ennemy.hit(self.degats):
                    self.tower.add_count("kills", 1)
                self.tower.add_count("damage", self.degats)

                if self.zone_damage is not True:
                    return

    def update(self, timeElapsed: float):
        """Updates the position of the projectile according to its speed"""
        self.advancement += timeElapsed * 64 * self.vitesse / self.Dist

        if self.advancement >= 1:
            self._dealDamage()

        x0 = self.trajectory_top[0] + self.advancement * (self.delta_x / 2)
        y0 = self.trajectory_top[1] + self.advancement * (self.delta_y / 2)

        height = (1 - self.advancement ** 2) * self.curvature * self.Dist

        self.position = (
            x0,
            y0 - height
        )

    def draw(self, screen: Screen):
        """Draws the projectile on screen"""
        screen.blit(self.image, self.position)
