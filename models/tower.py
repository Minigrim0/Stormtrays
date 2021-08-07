import glob
import json

import pygame as pg

from models.game_options import GameOptions
from models.level import Level
from models.screen import Screen
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

        options = GameOptions.getInstance()
        self.font = options.fonts["MedievalSharp-xOZ5"]["25"]
        self.hovered_tower_name: pg.Surface = None
        self.missing_funds: pg.Surface = self.font.render("Vous n'avez pas assez d'argent", 1, (200, 100, 100))

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

    def _setTowerHover(self, tower_data: dict):
        self.hovered_tower_name = self.font.render(tower_data["name"], 1, (0, 0, 0))
        self.hovered_tower = tower_data

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
            if self.hovered_tower_name is not None:
                screen.blit(self.hovered_tower_name, (10, 10))
                if Level.getInstance().canAfford(self.hovered_tower["price"]):
                    screen.blit(self.missing_funds, (10, 40))
        elif self.selectedTower is not None:
            self.selectedTower.draw(screen)

    def handleEvent(self, event):
        """Handles the user's events, selecting towers, opening/closing the tower menu, ..."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.selectedTower is not None and self.selectedTower.place():
                    self.towers.append(self.selectedTower)
                    Level.getInstance().pay(self.selectedTower.price)
                    self.selectedTower = None

                elif self.popup.opened:
                    for tower_button in self.tower_buttons:
                        tower_button.click(event.pos)

                if self.selectedTower is None:
                    self.popup.handleEvent(event)

            elif event.button == 3:
                self.selectedTower = None
                self.popup.close()
                self.hovered_tower = None
                self.hovered_tower_name = None

        elif event.type == pg.MOUSEMOTION:
            if self.selectedTower is not None:
                self.selectedTower.setPosition(
                    (
                        event.pos[0] - 32,
                        event.pos[1] - 32
                    )
                )
            elif self.popup.opened:
                for button in self.tower_buttons:
                    if button.collide(event.pos):
                        self._setTowerHover(tower_data=button.ckwargs["tower_data"])
                        break
                    self.hovered_tower_name = None

    def selectTower(self, tower_data: dict):
        if Level.getInstance().canAfford(tower_data["price"]):
            self.selectedTower = TowerDO(tower_data)
            self.popup.close()
