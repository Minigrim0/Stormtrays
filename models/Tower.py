import json
import glob

import pygame as pg

from models.gameOptions import GameOptions

from src.tower import TowerDO


class Tower:
    """Represents the tower manager"""

    instance = None

    @staticmethod
    def getInstance():
        if Tower.instance is None:
            Tower()
        return Tower.instance

    def __init__(self):
        if Tower.instance is not None:
            raise RuntimeError("Trying to instanciate a second object from a singleton class")
        Tower.instance = self

        self.towers: list(TowerDO) = []
        self.available_towers: list(dict) = []
        self._load()

    def _load(self):
        """Loads information about the available tower"""
        options = GameOptions.getInstance()
        for tower_file in glob.glob(options.fullPath("ennemies", "*.json")):
            with open(tower_file) as tower_info:
                data = json.load(tower_info)
                data["thumbnail"] = pg.image.load(data["img"]).convert_alpha()
                self.available_towers.append(data)

    def affichemenu(self, fenetre, num):
        """Shows the tower in the menu

        Args:
            fenetre ([type]): [description]
            num ([type]): [description]
        """
        fenetre.blit(self.image_menu, (18 + (60 * num) + (num * 10), (704) - (72)))
        fenetre.blit(self.prix_affiche, (18 + (60 * num) + (num * 10), (704) - (72)))
