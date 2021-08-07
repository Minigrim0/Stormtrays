import glob
import json

from models.game_options import GameOptions
from models.screen import Screen
from src.projectile import ProjectileDO


class Projectile:

    instance = None

    @staticmethod
    def getInstance():
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
        self.projectiles.append(
            ProjectileDO(
                self[name],
                tower,
                time_before_impact
            )
        )

    def update(self, timeElapsed: float):
        for projectile in self.projectiles:
            projectile.update(timeElapsed)
            if projectile.hasHit:
                del self.projectiles[self.projectiles.index(projectile)]

    def draw(self, screen: Screen):
        for projectile in self.projectiles:
            projectile.draw(screen)
