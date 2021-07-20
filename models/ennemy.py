import os
import glob
import json

import random
from src.ennemy import EnnemyDO

from models.gameOptions import GameOptions


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
        self.available_ennemies: {str: {}} = {}
        self.ennemies_weight: [int] = []
        self.load()

    def load(self):
        options = GameOptions.getInstance()
        for ennemyFile in glob.glob(options.fullPath("ennemies", "*.json")):
            with open(ennemyFile) as ennemyInfo:
                data = json.load(ennemyInfo)
                self.ennemies_weight.append(data["weight"])
                self.available_ennemies[os.path.splitext(os.path.split(ennemyFile)[1])[0]] = data

    def update(self):
        if self.level.Nombre_Ennemis_Tue >= 5000:
            double_invoque = True

        invoke = random.random() * Level_Difficulty
        if invoke <= 1:
            self.invoke()

    def invoke(self):
        invoque = random.randrange(10)
        if invoque == 0:
            ennemi = EnnemyDO("../Ennemis/Orc.json")
            ennemi.pose_ennemi(self.level.map)
            self.ennemies.append(ennemi)
        elif invoque in (1, 2):
            ennemi = EnnemyDO("../Ennemis/Goblin.json")
            ennemi.pose_ennemi(self.level.map)
            self.ennemies.append(ennemi)
        elif invoque == 3:
            ennemi = EnnemyDO("../Ennemis/Dwarf.json")
            ennemi.pose_ennemi(self.level.map)
            self.ennemies.append(ennemi)
        elif invoque == 4:
            ennemi = EnnemyDO("../Ennemis/Knight.json")
            ennemi.pose_ennemi(self.level.map)
            self.ennemies.append(ennemi)
        elif invoque == 5:
            ennemi = EnnemyDO("../Ennemis/Ghost.json")
            ennemi.pose_ennemi(self.level.map)
            self.ennemies.append(ennemi)
        elif invoque == 6:
            ennemi = EnnemyDO("../Ennemis/Golem.json")
            ennemi.pose_ennemi(self.level.map)
            self.ennemies.append(ennemi)
        elif invoque == 7:
            invoque = random.randrange(5)
            if invoque == 0:
                ennemi = EnnemyDO("../Ennemis/Dragon.json")
                ennemi.pose_ennemi(self.level.map)
                self.ennemies.append(ennemi)
        elif invoque in (8, 9, 10):
            ennemi = EnnemyDO("../Ennemis/Wolf.json")
            ennemi.pose_ennemi(self.level.map)
            self.ennemies.append(ennemi)
