import glob
import json
import random

from models.game_options import GameOptions
from models.level import Level
from src.ennemy import EnnemyDO


class Ennemy:
    """Represents the logic behind ennemy spawn and updates"""

    instance = None

    @staticmethod
    def getInstance():
        """Singleton pattern"""
        if Ennemy.instance is None:
            Ennemy()
        return Ennemy.instance

    def __init__(self):
        if Ennemy.instance is not None:
            raise RuntimeError("Trying to instanciate a second object from a singleton class")
        Ennemy.instance = self

        self.ennemies: [EnnemyDO] = []
        self.available_ennemies: [{}] = []
        self.ennemies_weights: list(int) = []
        self.load()

    def load(self):
        """Loads available ennemies"""
        options = GameOptions.getInstance()
        for ennemyFile in glob.glob(options.fullPath("ennemies", "*.json")):
            with open(ennemyFile) as ennemyInfo:
                data = json.load(ennemyInfo)
                self.available_ennemies.append(data)
                self.ennemies_weights.append(data["weight"])

    def update(self, elapsed_time: float):
        """Updates living ennemies + tries to spawn more"""
        options = GameOptions.getInstance()
        invoke = (random.random() * (1000/options.game_speed))/Level.getInstance().spawn_rate
        if invoke <= 1:  # We start with once in a thousand tries
            self.invoke()

        for ennemy in self.ennemies:
            if not ennemy.alive:
                Level.getInstance().addGold(
                    ennemy.max_health,
                    (
                        ennemy.absolute_position[0] + (ennemy.height // 2),
                        ennemy.absolute_position[1] + (ennemy.height // 2)
                    )
                )
                del self.ennemies[self.ennemies.index(ennemy)]
            ennemy.update(elapsed_time)

    def draw(self, screen):
        """Draws ennemies on screen"""
        for ennemy in self.ennemies:
            ennemy.draw(screen)

    def getEnnemy(self, position: tuple) -> EnnemyDO:
        """Returns the first ennemy at the given position or None"""
        for ennemy in self.ennemies:
            if ennemy.collide(position):
                return ennemy

    def invoke(self):
        """Invokes an ennemy, by choosing randomly in the weighted ennemy list"""
        ennemy = random.choices(self.available_ennemies, weights=self.ennemies_weights)[0]

        ennemi = EnnemyDO(ennemy)
        self.ennemies.append(ennemi)

    def getEnnemyList(self):
        return self.ennemies
