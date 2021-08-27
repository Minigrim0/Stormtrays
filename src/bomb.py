import math

from models.ennemy import Ennemy
from UI.components.image_animation import ImageAnimation


class Bomb:
    """A bomb for the user to place on the map"""

    def __init__(self, position: tuple, time: int):
        self.position: tuple = position
        self.lifespan: float = time
        self.radius: int = 40
        self.animation = ImageAnimation("assets/images/animations/bomb", callback=self.explode, speed=5)

    def update(self, time_elapsed: float):
        """Update the bomb lifetime and displays it to the screen"""
        if self.lifespan <= 0:
            self.animation.play()
            self.animation.update(time_elapsed)
        else:
            self.lifespan -= time_elapsed

    def draw(self, screen):
        self.animation.draw(screen, self.position)

    def explode(self):
        """Deals damage to the surrouding ennemies"""

        ennemies = Ennemy.getInstance().getEnnemyList
        for ennemy in ennemies:
            dist = math.sqrt(((ennemy.PosAbsolue[0] - self.Posx) ** 2) + ((ennemy.PosAbsolue[1] - self.Posy) ** 2))

            if dist <= self.radius:
                ennemy.hit(20)
