import json
import glob
import copy

import pygame as pg

from models.screen import Screen
from models.game_options import GameOptions

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

        font = options.fonts["MedievalSharp-xOZ5"]["14"]

        for tower_file in glob.glob(options.fullPath("towers", "*.json")):
            with open(tower_file) as tower_info:
                data = json.load(tower_info)
                data["thumbnail"] = pg.image.load(data["thumbnail"])
                price = font.render(str(data["price"]), 1, (0, 0, 0))
                data["thumbnail"].blit(price, (0, 0))
                self.available_towers.append(data)

    def _build(self):
        """Build the buttons of the tower menu"""
        for index, tower in enumerate(self.available_towers):
            self.tower_buttons.append(
                Button(
                    (20 + (70 * index), 615),
                    (64, 64),
                    image=tower["thumbnail"],
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

        if self.popup.opened:
            for tower_button in self.tower_buttons:
                tower_button.draw(screen)
        elif self.selectedTower is not None:
            self.selectedTower.draw(screen)

    def handleEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.selectedTower is not None and self.selectedTower.place():
                self.towers.append(self.selectedTower)
                self.selectedTower = None

            elif self.popup.opened:
                for tower_button in self.tower_buttons:
                    tower_button.click(event.pos)
            else:
                self.popup.handleEvent(event)

        elif event.type == pg.MOUSEMOTION and self.selectedTower is not None:
            self.selectedTower.setPosition(
                (
                    event.pos[0] - 32,
                    event.pos[1] - 32
                )
            )

    def selectTower(self, tower_data: dict):
        self.selectedTower = TowerDO(tower_data)
        self.popup.close()
