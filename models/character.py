import json
import math

import logging

import pygame as pg

from models.ennemy import Ennemy
from models.level import Level
from models.screen import Screen
from src.ennemy import EnnemyDO
from src.bomb import Bomb
from src.errors.missingAnimationException import MissingAnimationException
from src.utils.distance_between import distance_between
from src.utils.find_angle import findAngle
from UI.components.image_animation import ImageAnimation
from UI.components.power_bar.power_bar import PowerBar


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

        self.posx: int = 0
        self.posy: int = 0
        self.XpToAdd: int = 0
        self.xp: int = 0
        self.objectif: int = 10
        self.level: int = 1
        self.damage: int = 0
        self.speed: int = 0
        self.kills: int = 0

        self.Is_Returned: bool = False
        self.capacite1: bool = False
        self.capacite2: bool = False

        self.animations: dict = {}
        self.current_animation: str = "idle"

        self.power_bar = PowerBar(box_size=48)
        self.power_bar.addBox(
            icon=ImageAnimation("assets/images/animations/bomb", bank_name="bomb").getFrame(),
            name="Bomb", cooldown=5, callback=self._placeBomb
        )

        self.bombs: [Bomb] = []

        from UI.components.gui.game_ui import GameUI
        self.ui = GameUI.getInstance()

    @property
    def real_speed(self) -> float:
        """Returns the speed in pixel/sec instead of tiles/sec"""
        return self.speed * 64

    def _load(self, data):
        """Loads informations about the character from a parsed json file"""
        self.speed = data["speed"]
        self.damage = data["damage"]

        self.animations = {name: ImageAnimation(initial_data=state) for name, state in data["states"].items()}

        self.animations["attack"].setCallback(self.hit)

        logging.info("Ensuring the presence of required animatons")
        for animation in ["idle", "walk", "attack"]:
            if "idle" not in self.animations.keys():
                raise MissingAnimationException(f"Missing animation {animation} in Character model")
        logging.info("ok")

    def _placeBomb(self) -> bool:
        """Callback for the placing bomb power"""
        if Level.getInstance().canAfford(150):
            self.bombs.append(
                Bomb((self.posx, self.posy), 3)
            )
            Level.getInstance().pay(150)
            return True
        return False

    def setStyle(self, style: str):
        """Sets the style of the character, based on the available characters in assets/characters"""
        path = style.lower().replace(" ", "-")
        with open(f"assets/character/{path}/setup.json") as character_style:
            data = json.load(character_style)
            self._load(data)

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
        if isinstance(self.target, EnnemyDO) and not self.target.alive:
            self.target = (self.posx, self.posy)
        self.move(elapsed_time)
        self.getCurrentAnimation().update(elapsed_time)

        self.power_bar.update(elapsed_time)

        for bomb in self.bombs:
            bomb.update(elapsed_time)
            if not bomb.alive:
                del self.bombs[self.bombs.index(bomb)]

    def handleEvent(self, event: pg.event):
        """Handles user events"""
        if self.current_animation == "attack":
            return

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            ennemy = Ennemy.getInstance().getEnnemy(event.pos)
            self.target = ennemy if ennemy is not None else event.pos

        self.power_bar.handleEvent(event)

    def draw(self, screen: Screen):
        """Draws the character on screen"""
        self.getCurrentAnimation().draw(screen, (self.posx, self.posy), centered=True)
        for bomb in self.bombs:
            bomb.draw(screen)
        self.power_bar.draw(screen)

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
        self.bombs = []
