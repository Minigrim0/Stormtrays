import pygame

from src.utils.bound import bound

from models.level import Level

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

        self.pose_ennemi()

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
            max_val=self.max_health, initial_val=self.max_health
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

    def pose_ennemi(self):
        """Adds an ennemy to the game

        Args:
            tableau ([type]): [description]
        """
        self.position = (0, 0)
        level = Level.getInstance()
        self.direction = (1, 0)

        x = 0
        for y in range(11):
            tile = level.map[x][y]
            if tile is not None and (tile.code, tile.rotation) == ("c1", 0):
                self.position = (0, y)
                self.absolute_position = (0, y * 64)
                self.HitBox = pygame.Rect((0, y), (64, 64))

    def update(self, timeElapsed: float):
        """Makes the ennemy move"""
        self.animation.update(timeElapsed)
        self.healthBar.update(timeElapsed)

        level = Level.getInstance()

        if self.under_attack[0]:
            self.under_attack = (
                self.under_attack[0],
                self.under_attack[1] + timeElapsed
            )
        if self.under_attack[1] >= 5:
            self.under_attack = (False, 0)

        self.count += self.speed * 64 * timeElapsed
        if self.count >= 64:
            self.count = 0
            self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])

            if level.hitBastion(self.position, damage=(self.health / 2)):
                self.hit(2000)
            else:
                tile = level.map[self.position[0]][self.position[1]]
                new_dir = tile.direction()
                if new_dir is None:
                    self.pose_ennemi()
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
        """Blits the ennemy on the screen

        Args:
            screen ([type]): [description]
        """
        if self.under_attack[0]:
            self.healthBar.draw(screen, self.absolute_position)
        self.animation.draw(screen, self.absolute_position)

    def hit(self, damage: int):
        """Hits the ennemy with the given amount of damage

        Args:
            damage (int): The amount of damage to deal
        """
        self.health -= damage
        self.health = bound(0, self.max_health, self.health)
        self.under_attack = (True, 0)
        self.healthBar.set_advancement(self.health)

    def collide(self, position: tuple) -> bool:
        """Returns true if the given position collides with the ennemy"""
        return self.HitBox.collidepoint(position)
