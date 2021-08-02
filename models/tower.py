import json
import glob
import copy

import pygame as pg

from models.screen import Screen
from models.gameOptions import GameOptions

from src.tower import TowerDO

from UI.components.button import Button
from UI.components.popup import Popup


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

        self.popup = Popup(
            position=(15, 610),
            background=pg.image.load("assets/images/overlays/tower_menu.png"),
            button_position=(32, 654),
            button_size=(45, 45),
            button_image=pg.image.load("assets/images/Boutons/tower_button.png").convert_alpha()
        )

        self.towers: list(TowerDO) = []  # In game Towers
        self.available_towers: list(dict) = []  # Available towers to draw in the menu
        self.tower_buttons: [Button] = []

        self.selectedTower: TowerDO = None
        self._load()
        self._build()

    def _load(self):
        """Loads information about the available tower"""
        options = GameOptions.getInstance()
        for tower_file in glob.glob(options.fullPath("ennemies", "*.json")):
            with open(tower_file) as tower_info:
                data = json.load(tower_info)
                data["thumbnail"] = pg.image.load(data["img"]).convert_alpha()
                self.available_towers.append(data)

    def _build(self):
        font = GameOptions.getInstance().fonts["MedievalSharp-xOZ5"]["14"]

        for index, tower in enumerate(self.available_towers):
            image = copy(tower["thumbnail"])
            price = font.render(tower["price"], 1, (0, 0, 0))
            image.blit(price, (0, 0))

            self.tower_buttons.append(
                Button(
                    (18 + (70 * index), 632),
                    (64, 64),
                    image=image,
                    callback=self.selectTower,
                    tower_data=tower
                )
            )

    def update(self, timeElapsed: float):
        """Updates the state of the in game towers"""
        for tower in self.towers:
            tower.update(timeElapsed)

    def draw(self, screen: Screen):
        """Draws the in game towers and the tower menu on the screen"""
        self.popup.draw(screen)
        for tower in self.towers:
            tower.draw(screen)

    def handleEvent(self, event):
        self.popup.handleEvent(event)

    def toggleTowerMenu(self):
        self.show_towers = not self.show_towers

    def selectTower(self, tower_data: dict):
        self.selectedTower = TowerDO(tower_data)
