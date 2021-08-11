import math

import pygame as pg

from models.ennemy import Ennemy
from models.level import Level
from models.screen import Screen
from src.ennemy import EnnemyDO
from src.utils.distance_between import distance_between
from src.utils.find_angle import findAngle
from UI.components.image_animation import ImageAnimation


class Character:
    """Reprensents the user's character"""

    instance = None

    @staticmethod
    def getInstance():
        """Singleton pattern"""
        if Character.instance is None:
            Character()
        return Character.instance

    def __init__(self):
        if Character.instance is not None:
            raise RuntimeError("Trying to instanciate a second object of a singleton class")
        Character.instance = self

        self.target = (576, 352)  # Either a position or an ennemy

        self.posx = 0
        self.posy = 0

        self.XpToAdd = 0
        self.xp = 0
        self.objectif = 10
        self.level = 1
        self.damage = 3
        self.speed = 5

        self.kills = 0

        self.Is_Returned = False
        self.capacite1 = False
        self.capacite2 = False

        from UI.menus.game_ui import GameUI
        self.ui = GameUI.getInstance()

        self.animations = {
            "idle": ImageAnimation("assets/images/animations/character/idle/", loop=-1, flippable=True),
            "walk": ImageAnimation("assets/images/animations/character/walk/", loop=-1, flippable=True, speed=8),
            "attack": ImageAnimation(
                "assets/images/animations/character/attack/", flippable=True, speed=9, loop=2, callback=self.hit),
            "invoke": ImageAnimation("assets/images/animations/character/invoke/", flippable=True, speed=5)
        }
        self.current_animation = "idle"

    def getCurrentAnimation(self) -> ImageAnimation:
        """Returns the currently playing animation"""
        return self.animations[self.current_animation]

    def level_up(self):
        """Upgrades the character skills"""
        self.level += 1

        self.damage = self.level * 0.5 + 3
        self.speed = self.level * 0.25 + 5

    def setAnimation(self, animation: str, direction: bool = None):
        """Sets the character animation to the given one, keeping track of the direction unless forced

        Args:
            animation (str): The name of the animation to play
            direction (bool, optional): The direction of the animation. None means "keep current". Defaults to None.
        """
        if animation != self.current_animation:
            direction = not self.getCurrentAnimation().flipped if direction is None else direction
            self.current_animation = animation
            animation = self.getCurrentAnimation()
            animation.reset()
        self.getCurrentAnimation().setDirection(direction)
        self.getCurrentAnimation().play()

    def hit(self):
        """Hits the character's target, automatically called after attack animation"""
        if isinstance(self.target, EnnemyDO):
            self.target.hit(self.damage)
            if not self.target.alive:
                self.kills += 1
                Level.getInstance().add_count("player_kills", 1)
                self.ui.add_xp(self.target.max_health)
                self.target = (self.posx, self.posy)
        self.setAnimation("idle")

    def update(self, elapsed_time: float):
        """Updates the character, makes him move"""
        # if self.capacite1:
        #     Icapacite1 += 1
        #     if Icapacite1 == 160:
        #         Icapacite1 = 0
        #         King.capacite1 = False
        # if CooldownInvoc > 0:
        #     CooldownInvoc -= 1
        # TpsCoolDown = CooldownInvoc // 24

        if isinstance(self.target, EnnemyDO) and not self.target.alive:
            self.target = (self.posx, self.posy)
        self.move(elapsed_time)
        self.getCurrentAnimation().update(elapsed_time)

    def handleEvent(self, event: pg.event):
        """Handles user events"""
        if self.current_animation == "attack":
            return

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            ennemy = Ennemy.getInstance().getEnnemy(event.pos)
            self.target = ennemy if ennemy is not None else event.pos

    def draw(self, screen: Screen):
        """Draws the character on screen"""
        self.getCurrentAnimation().draw(screen, (self.posx, self.posy), centered=True)

    @property
    def real_speed(self) -> float:
        """Returns the speed in pixel/sec instead of tiles/sec"""
        return self.speed * 64

    def move(self, elapsed_time: float):
        """Updates the status of the character"""
        if self.current_animation == "attack":
            return

        if isinstance(self.target, EnnemyDO):
            if distance_between(self.target.centeredPosition, (self.posx, self.posy)) > 10:
                delta_x = self.target.centeredPosition[0] - self.posx
                delta_y = self.target.centeredPosition[1] - self.posy

                angle = findAngle(delta_x, delta_y)

                movement_x = math.cos(angle) * self.real_speed * elapsed_time
                movement_y = math.sin(angle) * self.real_speed * elapsed_time

                self.posx += movement_x
                self.posy += movement_y

                self.setAnimation("walk", direction=(movement_x > 0))
            else:
                self.setAnimation("attack")
        else:
            if distance_between(self.target, (self.posx, self.posy)) > 10:
                delta_x = self.target[0] - self.posx
                delta_y = self.target[1] - self.posy

                angle = findAngle(delta_x, delta_y)

                movement_x = math.cos(angle) * self.real_speed * elapsed_time
                movement_y = math.sin(angle) * self.real_speed * elapsed_time

                self.posx += movement_x
                self.posy += movement_y

                self.setAnimation("walk", direction=(movement_x > 0))
            else:
                self.setAnimation("idle")

    def reset(self):
        """Resets all charachter's stats"""
        self.target = (576, 352)

        self.posx = 0
        self.posy = 0

        self.XpToAdd = 0
        self.xp = 0
        self.objectif = 10
        self.level = 1
        self.damage = 3
        self.speed = 5

        self.kills = 0

        self.Is_Returned = False
        self.capacite1 = False
        self.capacite2 = False
        self.current_animation = "idle"
