from models.screen import Screen

from UI.components.loading_bar import LoadingBar


class Bastion:
    """Represents a bastion the ennemies are trying to destroy"""

    def __init__(self, position: tuple, initial_health: int = 100):
        self.position = position

        self.initial_health = initial_health
        self.health = initial_health

        self.healthBar = LoadingBar(
            (self.position[0] - 10, self.position[1]),
            (64, 5),
            max_val=self.initial_health,
            initial_val=self.initial_health
        )

    def update(self, timeElapsed: float):
        """Updates the healthbar of the bastion"""
        self.healthBar.update(timeElapsed)

    def hit(self, damage: int):
        """Hits the bastion with the given amount of damage"""
        self.health -= damage
        self.healthBar.set_advancement(self.health)

    def draw(self, screen: Screen):
        """Draws the healthbar on the screen if the bastion is under attack"""
        if self.underAttack:
            self.healthBar.draw(screen)
