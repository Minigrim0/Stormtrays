import glob
import json

from models.game_options import GameOptions
from models.screen import Screen
from src.projectile import ProjectileDO


class Projectile:
    """The projectile model, handles the in game projectiles"""

    instance = None

    @staticmethod
    def getInstance():
        """Singleton pattern"""
        if Projectile.instance is None:
            Projectile()
        return Projectile.instance

    def __init__(self):
        if Projectile.instance is not None:
            raise RuntimeError("Trying to instanciate a second object from a singleton class")
        Projectile.instance = self

        self.available_projectiles: {{}} = {}
        self.projectiles: [ProjectileDO] = []

        self._load()

    def __getitem__(self, position):
        return self.available_projectiles[position]

    def _load(self):
        """Loads the available projectiles from the projectile folder"""
        options = GameOptions.getInstance()
        for projectile_file in glob.glob(options.fullPath("projectile", "*.json")):
            with open(projectile_file) as projectile_data:
                projectile = json.load(projectile_data)
                self.available_projectiles[projectile["name"]] = projectile

    def shootProjectile(self, name, tower, time_before_impact):
        """Shoots a projectile of the given name"""
        self.projectiles.append(
            ProjectileDO(
                self[name],
                tower,
                time_before_impact
            )
        )

    def update(self, elapsed_time: float):
        """Updates all in game projectiles"""
        for projectile in self.projectiles:
            projectile.update(elapsed_time)
            if projectile.hasHit:
                del self.projectiles[self.projectiles.index(projectile)]

    def draw(self, screen: Screen):
        """Draws all in-game projectiles"""
        for projectile in self.projectiles:
            projectile.draw(screen)
