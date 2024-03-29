import glob
import json

import pygame as pg

from models.game_options import GameOptions
from models.level import Level
from models.screen import Screen
from src.tower import TowerDO
from UI.components.button import Button
from UI.components.grid import Grid
from UI.components.popup import Popup


class Tower:
    """Represents the tower manager"""

    instance = None

    @staticmethod
    def getInstance():
        """Singleton pattern"""
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
            button_image=pg.image.load("assets/images/buttons/tower_button.png").convert_alpha()
        )

        self.towers: list(TowerDO) = []  # In game Towers
        self.available_towers: list(dict) = []  # Available towers to draw in the menu

        options = GameOptions.getInstance()
        self.font = options.fonts["MedievalSharp-xOZ5"]["25"]
        self.hovered_tower: TowerDO = None
        self.hovered_tower_name: pg.Surface = None
        self.missing_funds: pg.Surface = self.font.render("Vous n'avez pas assez d'argent", 1, (200, 100, 100))
        self.grid: pg.Surface = None

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
        self.available_towers = sorted(self.available_towers, key=lambda x: x["price"])

    def _build(self):
        """Build the buttons of the tower menu"""
        for index, tower in enumerate(self.available_towers):
            self.popup.addButton(
                Button(
                    (20 + (70 * index), 615),
                    (64, 64),
                    image=tower["thumbnail"],
                    callback=self.selectTower,
                    tower_data=tower
                )
            )

        level: Level = Level.getInstance()
        self.grid = Grid(level.size, level.tile_size)

    def _setTowerHover(self, tower_data: dict):
        """Builds the rendered name of the currently hovered tower"""
        self.hovered_tower_name = self.font.render(tower_data["name"], 1, (0, 0, 0))
        self.hovered_tower = tower_data

    def update(self, elapsed_time: float):
        """Updates the state of the in game towers"""
        for tower in self.towers:
            tower.update(elapsed_time)

    def draw(self, screen: Screen):
        """Draws the in game towers and the tower menu on the screen"""
        for tower in self.towers:
            tower.draw(screen)

        self.popup.draw(screen)

        if self.popup.opened:
            if self.hovered_tower_name is not None:
                screen.blit(self.hovered_tower_name, (10, 10))
                if not Level.getInstance().canAfford(self.hovered_tower["price"]):
                    screen.blit(self.missing_funds, (10, 40))
        elif self.selectedTower is not None:
            self.grid.draw(screen, (0, 0))
            self.selectedTower.draw(screen)

    def handleEvent(self, event):
        """Handles the user's events, selecting towers, opening/closing the tower menu, ..."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.selectedTower is not None:
                    position = (
                        self.selectedTower.position[0] // 64,
                        self.selectedTower.position[1] // 64
                    )
                    if Level.getInstance().isFree(position) and self.isFree(position) and self.selectedTower.place():
                        self.towers.append(self.selectedTower)
                        Level.getInstance().pay(self.selectedTower.price)
                        self.selectedTower = None
                else:
                    self.popup.handleEvent(event)
                    for tower in self.towers:
                        tower.click(event.pos)

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
                for button in self.popup.buttons:
                    if button.collide(event.pos):
                        self._setTowerHover(tower_data=button.ckwargs["tower_data"])
                        break
                    self.hovered_tower_name = None

    def selectTower(self, tower_data: dict):
        """Callback for the tower buttons"""
        if Level.getInstance().canAfford(tower_data["price"]):
            self.selectedTower = TowerDO(tower_data)
            self.popup.close()

    def reset(self):
        """Removes all towers currently in game and empties player's hand"""
        self.towers = []  # In game Towers
        self.hovered_tower_name = None
        self.selectedTower: TowerDO = None

    def isFree(self, position: tuple) -> bool:
        """Returns true if there is no tower at the given position"""
        for tower in self.towers:
            if tower.position == position:
                return False
        return True

    def delTower(self, tower: TowerDO):
        """Removes a tower from the map"""
        if tower in self.towers:
            del self.towers[self.towers.index(tower)]
