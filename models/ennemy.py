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

        options = GameOptions.getInstance()
        self.ennemies: [EnnemyDO] = []
        self.available_ennemies: [str] = []
        self.ennemies_weight: [int] = []

        for ennemyFile in glob.glob(options.fullPath("ennemies", "*.json")):
            self.available_ennemies.append(os.path.splitext(os.path.split(ennemyFile)[1])[0])
            with open(ennemyFile) as ennemyInfo:
                self.ennemies_weight.append(json.load(ennemyInfo)["weight"])

    def update(self):
        if self.level.Nombre_Ennemis_Tue >= 5000:
            double_invoque = True

        invoke = random.random() * Level_Difficulty
        if invoke <= 1:
            self.invoke()

    def invoke(self):
        invoque = random.randrange(10)
        if invoque == 0:
            ennemi = Ennemi_IG("../Ennemis/Orc.json")
            ennemi.pose_ennemi(niveau.map)
            Liste_Mechants.append(ennemi)
        elif invoque in (1, 2):
            ennemi = Ennemi_IG("../Ennemis/Goblin.json")
            ennemi.pose_ennemi(niveau.map)
            Liste_Mechants.append(ennemi)
        elif invoque == 3:
            ennemi = Ennemi_IG("../Ennemis/Dwarf.json")
            ennemi.pose_ennemi(niveau.map)
            Liste_Mechants.append(ennemi)
        elif invoque == 4:
            ennemi = Ennemi_IG("../Ennemis/Knight.json")
            ennemi.pose_ennemi(niveau.map)
            Liste_Mechants.append(ennemi)
        elif invoque == 5:
            ennemi = Ennemi_IG("../Ennemis/Ghost.json")
            ennemi.pose_ennemi(niveau.map)
            Liste_Mechants.append(ennemi)
        elif invoque == 6:
            ennemi = Ennemi_IG("../Ennemis/Golem.json")
            ennemi.pose_ennemi(niveau.map)
            Liste_Mechants.append(ennemi)
        elif invoque == 7:
            invoque = random.randrange(5)
            if invoque == 0:
                ennemi = Ennemi_IG("../Ennemis/Dragon.json")
                ennemi.pose_ennemi(niveau.map)
                Liste_Mechants.append(ennemi)
        elif invoque in (8, 9, 10):
            ennemi = Ennemi_IG("../Ennemis/Wolf.json")
            ennemi.pose_ennemi(niveau.map)
            Liste_Mechants.append(ennemi)
