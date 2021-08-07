import math

import pygame

from models.ennemy import Ennemy
from models.projectile import Projectile
from models.screen import Screen
from src.ennemy import EnnemyDO
from UI.components.image_animation import ImageAnimation


class TowerDO:
    """Represents an in-game tower"""

    def __init__(self, tower_data, position: tuple = (0, 0)):
        self.placed: bool = False
        self.position: tuple = position
        self.range = tower_data["range"]
        self.damage = tower_data["damage"]
        self.fire_rate = tower_data["fire_rate"]
        self.price = tower_data["price"]

        self.target: EnnemyDO = None

        self.EnnemiKilled = 0
        self.TotalDegats = 0

        self.projectile_model = Projectile.getInstance()[tower_data["projectile"]]
        self.Rect = None

        callback_on = tower_data["shoot_on"] if "shoot_on" in tower_data.keys() else [-1]

        self.animation = ImageAnimation(
            tower_data["animation"],
            flippable=True,
            callback=self.shoot,
            speed=tower_data["fire_rate"],
            bank_name=tower_data["animation"],
            callback_on=callback_on
        )

        self.counters: dict = {
            "kills": 0,
            "damage": 0
        }

    @property
    def flipped(self) -> bool:
        """Returns a boolean indicating whether the tower is flipped or not"""
        return not self.animation.flipped

    @property
    def absolute_position(self) -> tuple:
        """Returns the position on screen"""
        return (
            self.position[0] * 64,
            self.position[1] * 64,
        )

    def _targetInRange(self, target: EnnemyDO = None):
        """Check if the given or the current target is in range of the tower"""
        target = target if target is not None else self.target

        t = self.timeToImpact(target)
        return target.alive and (t - (1 / self.fire_rate)) * self.projectile_model["speed"] <= self.range * 64

    def _acquireTarget(self):
        """Finds the first in-range ennemy to target it"""
        for ennemy in Ennemy.getInstance().getEnnemyList():
            if self._targetInRange(ennemy):
                self.target = ennemy
                self.animation.setDirection(self.target.position[0] < self.position[0])
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
        """Updates the in-game towers and the tower menu"""
        if self.placed:
            if self.target is not None and not self.animation.playing and self._targetInRange():
                self.animation.play()
            else:
                self._acquireTarget()

            self.animation.update(timeElapsed)

    def shoot(self):
        """Attacks the first ennemy in its sight"""
        Projectile.getInstance().shootProjectile(
            self.projectile_model["name"],
            self,
            self.timeToImpact(self.target)
        )

    def timeToImpact(self, target) -> float:
        """
        Returns the time until impact for an hypothetic projectile

        Triangle tower/ennemy/impact
        b² = a²c² - 2ac*cos(ß)
        a = distance ennemy|impact = ennemy_speed * time
        b = distance tower |impact = projectile_speed * (time - shot_time)
        c = distance tower |ennemy

        cos(ß) = angle tower | ennemy_direction

        => a * t² + b * t + c = 0
        """
        delta_x = self.absolute_position[0] - target.absolute_position[0]
        delta_y = self.absolute_position[1] - target.absolute_position[1]
        Dist2 = delta_x ** 2 + delta_y ** 2

        Cos_Beta = target.direction[0] * delta_x + target.direction[1] * delta_y

        a = (self.projectile_model["speed"] ** 2) - target.speed ** 2
        b = (2 * target.speed * Cos_Beta) - (2 * (self.projectile_model["speed"] ** 2) * (1 / self.fire_rate))
        c = (self.projectile_model["speed"] ** 2) * ((1 / self.fire_rate) ** 2) - Dist2

        Ro = (b ** 2) - (4 * a * c)

        t = (-b + math.sqrt(Ro)) / (2 * a)

        return t

    def setPosition(self, position: tuple):
        """Sets the position of the tower (used when the tower is in the "hand" of the player)"""
        self.position = position

    def add_count(self, name: str, amount: float):
        """Adds the given value to the given counter"""
        if name in self.counters.keys():
            self.counters[name] += amount
        else:
            self.counters[name] = amount
