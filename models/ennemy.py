import os
import glob
import json

import random
from src.ennemy import EnnemyDO

from models.gameOptions import GameOptions
from models.level import Level


class Ennemy:
    """Represents the logic behind ennemy spawn and updates"""

    instance = None

    @staticmethod
    def getInstance():
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
        options = GameOptions.getInstance()
        for ennemyFile in glob.glob(options.fullPath("ennemies", "*.json")):
            with open(ennemyFile) as ennemyInfo:
                data = json.load(ennemyInfo)
                self.available_ennemies.append(data)
                self.ennemies_weights.append(data["weight"])

    def update(self, timeElapsed: float):
        invoke = random.random() * 100
        if invoke <= 1:
            self.invoke()

        for ennemy in self.ennemies:
            ennemy.update(timeElapsed)

    def draw(self, screen):
        for ennemy in self.ennemies:
            ennemy.draw(screen)

    def invoke(self):
        ennemy = random.choices(self.available_ennemies, weights=self.ennemies_weights)[0]

        ennemi = EnnemyDO(ennemy)
        ennemi.pose_ennemi()
        self.ennemies.append(ennemi)
