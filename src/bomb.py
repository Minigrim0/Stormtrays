from models.ennemy import Ennemy
from UI.components.image_animation import ImageAnimation
from src.utils.distance_between import distance_between


class Bomb:
    """A bomb for the user to place on the map"""

    def __init__(self, position: tuple, time: int):
        self.position: tuple = position
        self.lifespan: float = time
        self.radius: int = 40
        self.animation = ImageAnimation(
            "assets/images/animations/bomb", callback=self.explode, speed=5, bank_name="bomb")
        self.alive: bool = True

    def _die(self):
        self.alive = False

    def update(self, elapsed_time: float):
        """Update the bomb lifetime and displays it to the screen"""
        if self.lifespan <= 0:
            self.animation.play()
            self.animation.update(elapsed_time)
        else:
            self.lifespan -= elapsed_time

    def draw(self, screen):
        """Draws the bomb on screen"""
        self.animation.draw(screen, self.position)

    def explode(self):
        """Deals damage to the surrouding ennemies"""
        ennemies = Ennemy.getInstance().getEnnemyList()
        for ennemy in ennemies:
            if distance_between(ennemy.centeredPosition, self.position) <= self.radius:
                ennemy.hit(20)
        self._die()
