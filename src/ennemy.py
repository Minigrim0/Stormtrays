import random

import pygame

from models.level import Level
from src.utils.bound import bound
from UI.components.image_animation import ImageAnimation
from UI.components.loading_bar import LoadingBar


class EnnemyDO:
    """Represent an in game ennemy, keeps the health etc..."""

    def __init__(self, data):
        self.position = (0, 0)
        self.count = 0
        self.absolute_position = (0, 0)

        self.Returned = False
        self.under_attack = (False, 0)

        self.direction = (1, 0)
        self.Tics = 0

        self.place_ennemy()

        self.propriete = data

        self.name = self.propriete["name"]
        # self.meurt = pygame.mixer.Sound(self.propriete["DeathSound"])
        self.health = self.propriete["health"]
        self.max_health = self.propriete["health"]
        self.speed = self.propriete["speed"]
        self.height = self.propriete["height"]

        self.healthBar = LoadingBar(
            (0, 0),
            (self.height, 5),
            max_val=self.max_health, initial_val=self.max_health,
            animation_type="linear", speed=50
        )
        self.animation = ImageAnimation(
            self.propriete["animation"], flippable=True, loop=-1,
            speed=self.propriete["animation_speed"], image_size=(self.height, self.height),
            bank_name=self.name
        )
        self.animation.play()

        self.HitBox = None
        self.Vie_Rect = None

    @property
    def alive(self) -> bool:
        """Returns true if the ennemy is alive"""
        return self.health > 0

    @property
    def centeredPosition(self) -> (int, int):
        """Returns the centered position of the ennemy"""
        return (
            self.absolute_position[0] + self.height // 2,
            self.absolute_position[1] + self.height // 2,
        )

    def place_ennemy(self):
        """Adds an ennemy to the game"""
        level = Level.getInstance()
        spawn_point = random.choice(level.spawn_places)
        self.position = spawn_point

        tile = level.map[self.position[0]][self.position[1]]
        self.direction = tile.direction()

        self.absolute_position = (self.position[0] * level.tile_size[0], self.position[1] * level.tile_size[0])
        self.HitBox = pygame.Rect(self.absolute_position, (64, 64))

    def update(self, elapsed_time: float):
        """Makes the ennemy move and updates it's health bar"""
        self.animation.update(elapsed_time)
        self.healthBar.update(elapsed_time)

        level = Level.getInstance()

        if self.under_attack[0]:
            self.under_attack = (
                self.under_attack[0],
                self.under_attack[1] + elapsed_time
            )
        if self.under_attack[1] >= 5:
            self.under_attack = (False, 0)

        self.count += self.speed * 64 * elapsed_time
        if self.count >= 64:
            self.count = 0
            self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])

            if level.hitBastion(self.position, damage=(self.health / 2)):
                self.hit(2000)
            else:
                tile = level.map[self.position[0]][self.position[1]]
                new_dir = tile.direction()
                if new_dir is None:
                    self.place_ennemy()
                elif new_dir != (0, 0):
                    if new_dir[0] != self.direction[0]:
                        self.animation.flip()
                    self.direction = new_dir

        self.absolute_position = (
            self.position[0] * 64 + (self.count * self.direction[0]),
            self.position[1] * 64 + (self.count * self.direction[1]),
        )
        self.HitBox = pygame.Rect(self.absolute_position, (64, 64))

    def draw(self, screen):
        """Blits the ennemy and its health bar on the screen"""
        if self.under_attack[0]:
            self.healthBar.draw(screen, self.absolute_position)
        self.animation.draw(screen, self.absolute_position)

    def hit(self, damage: int):
        """Hits the ennemy with the given amount of damage"""
        self.health -= damage
        self.health = bound(0, self.max_health, self.health)
        self.under_attack = (True, 0)
        self.healthBar.set_advancement(self.health)

    def collide(self, position: tuple) -> bool:
        """Returns true if the given position collides with the ennemy"""
        return self.HitBox.collidepoint(position)
