import pygame as pg

from models.screen import Screen
from UI.components.loading_bar import LoadingBar


class Bastion:
    """Represents a bastion the ennemies are trying to destroy"""

    def __init__(self, position: tuple, initial_health: int = 100):
        self.position = position

        self.initial_health = initial_health
        self.health = initial_health
        self.image = pg.image.load("assets/images/tiles/fort.png").convert_alpha()

        # Whether the bastion is under attack and how long since last attack
        self.underAttack: tuple(bool, int) = (False, 0)

        self.healthBar = LoadingBar(
            self._blit_position,
            (64, 5),
            max_val=self.initial_health,
            initial_val=self.initial_health
        )

    def update(self, elapsed_time: float):
        """Updates the healthbar of the bastion"""
        self.healthBar.update(elapsed_time)
        if self.underAttack[0]:
            self.underAttack = (True, self.underAttack[1] + (1 * elapsed_time))

            if self.underAttack[1] > 5:
                self.underAttack = (False, 0)

    def hit(self, damage: int):
        """Hits the bastion with the given amount of damage"""
        self.health -= damage
        self.healthBar.set_advancement(self.health)
        self.underAttack = (True, 0)

    @property
    def _blit_position(self) -> tuple:
        """Returns the real position to blit the bastion to"""
        return (self.position[0] * 64, self.position[1] * 64)

    def draw(self, screen: Screen):
        """Draws the healthbar on the screen if the bastion is under attack"""
        screen.blit(self.image, self._blit_position)
        if self.underAttack[0]:
            self.healthBar.draw(screen)
