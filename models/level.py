import json
from copy import copy

import pygame as pg

import src.constantes as consts
from src.bastion import Bastion
from src.errors.invalidPositionException import InvalidPositionException
from src.gold import Gold
from src.tile import Tile


class Level:
    """The level class contains information and logic about the current level
    such as the list of gold anim objects and the number of ennemy killed
    """

    instance = None

    @staticmethod
    def getInstance():
        """Returns the model's instance, creating it if needed"""
        if Level.instance is None:
            Level()
        return Level.instance

    def __init__(self):
        if Level.instance is not None:
            raise RuntimeError("This class is a singleton")
        Level.instance = self

        self.tiles = {}

        images = [
            (("assets/images/tiles/straight.png", "assets/images/tiles/straight_edit.png"), "c1"),
            (("assets/images/tiles/turn.png", "assets/images/tiles/left_turn_edit.png"), "t2"),
            (("assets/images/tiles/turn.png", "assets/images/tiles/right_turn_edit.png"), "t1"),
            ("assets/images/tiles/cross.png", "x1"),
            (consts.poubelle, "p1"),
            ("assets/images/tiles/fort.png", "k1"),
            ((None, "assets/images/blocked_edit.png"), "v1"),
        ]

        for path, code in images:
            if isinstance(path, tuple):
                self.tiles[code] = Tile(
                    code, (
                        pg.image.load(path[0]).convert_alpha() if path[0] is not None else None,
                        pg.image.load(path[1]).convert_alpha() if path[0] is not None else None
                    )
                )
            elif isinstance(path, str):
                self.tiles[code] = Tile(
                    code, (
                        pg.image.load(path).convert_alpha(),
                        pg.image.load(path).convert_alpha()
                    )
                )

        # self.editorImage["QG", 0] = pg.image.load("img/QuestGiverF1.png").convert_alpha()

        self.bastions: list(Bastion) = []
        self.gold = 500
        self.killed_ennemies = 0
        self.background: pg.Surface = pg.image.load("assets/images/fond.png").convert_alpha()
        self.backgroundName = "fond1"
        self.size = [18, 11]

        self.gold_anim: [Gold] = []
        self.FondFenetre = None
        self.map = None
        self.initMap()

    @property
    def health(self):
        return sum([x.health for x in self.bastions])

    def initMap(self):
        """Empties the level"""
        self.map = []
        for x in range(self.size[0]):
            self.map.append([])
            for _ in range(self.size[1]):
                self.map[x].append(None)

    def save(self, nomfichier: str, thumbnail_path: str):
        """Saves the level

        Args:
            nomfichier (str): The name of the file to save the level in
            thumbnail_path (str): The path of the level's thumbnail
        """
        serializedMap = [[tile.toJson() if tile is not None else {} for tile in row] for row in self.map]
        level = {
            "background": self.backgroundName,
            "size": self.size,
            "map": serializedMap,
            "thumbnail": thumbnail_path,
        }

        with open(nomfichier, "w") as f:
            f.write(json.dumps(level))

    def build(self, nomfichier, editor=False):
        """Builds the level from a file

        Args:
            nomfichier ([type]): [description]
        """
        with open(nomfichier) as f:
            data = json.load(f)
            self.background = pg.image.load(data["background"])
            self.size = data["size"]
            self.initMap()

        self.background = pg.transform.scale(self.background, (1152, 704))
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                tile = data["map"][x][y]
                if len(tile.keys()) == 0:
                    continue

                tile_position = (int((x * 64)), int((y * 64)))
                self.map[x][y] = copy(self.tiles[tile["code"]])
                self.map[x][y].rotate(amount=tile["rotation"])
                self.map[x][y].move(tile_position)

                if not editor:
                    if self.map[x][y].code not in ("k1", "QG"):
                        self.map[x][y].draw(self.background)
                    elif self.map[x][y].code == "k1":
                        bastion = Bastion((x, y), initial_health=10000)
                        self.bastions.append(bastion)

    def placeTile(self, position: tuple, tile):
        """Places a tile at the given coordinates

        Args:
            position (tuple): the position to place the tile at
            tile ([type]): [description]
        """
        if position[0] not in list(range(self.size[0])) or position[1] not in list(range(self.size[1])):
            raise InvalidPositionException("Tile is outside of the map !")

        self.map[position[0]][position[1]] = tile

    def update(self, timeElapsed: float):
        for bastion in self.bastions:
            bastion.update(timeElapsed)
        for gold in self.gold_anim:
            if gold.update(timeElapsed):
                del self.gold_anim[self.gold_anim.index(gold)]

    def draw(self, screen, editor=False):
        """Draws the current level

        Args:
            screen (Screen): The screen to blit the level on
        """
        screen.blit(self.background, (0, 0))
        for bastion in self.bastions:
            bastion.draw(screen)

        if editor:
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    if self.map[x][y] is not None:
                        self.map[x][y].draw(screen, editor=editor)

        for gold in self.gold_anim:
            gold.draw(screen)

    def Set_Difficulty(self, Difficulte):
        """Changes variables relative to the diffculty information

        Args:
            Difficulte ([type]): [description]

        Returns:
            [type]: [description]
        """
        Level_Difficulty = 0

        Difficulty = 11 - Difficulte

        if self.killed_ennemies >= 0:
            Level_Difficulty = 10 * Difficulty
        if self.killed_ennemies >= 10:
            Level_Difficulty = 9 * Difficulty
        if self.killed_ennemies >= 25:
            Level_Difficulty = 8 * Difficulty
        if self.killed_ennemies >= 50:
            Level_Difficulty = 7 * Difficulty
        if self.killed_ennemies >= 100:
            Level_Difficulty = 6 * Difficulty
        if self.killed_ennemies >= 200:
            Level_Difficulty = 5 * Difficulty
        if self.killed_ennemies >= 400:
            Level_Difficulty = 4 * Difficulty
        if self.killed_ennemies >= 750:
            Level_Difficulty = 3 * Difficulty
        if self.killed_ennemies >= 1000:
            Level_Difficulty = 2 * Difficulty
        if self.killed_ennemies >= 2500:
            Level_Difficulty = 1 * Difficulty

        return Level_Difficulty

    def hitBastion(self, position: tuple, damage: int = 0) -> bool:
        """Hits the bastion at the given coordinate (if any) with the given amount of damage"""
        for bastion in self.bastions:
            if bastion.position == position:
                bastion.hit(damage)
                return True
        return False

    def addGold(self, amount, position):
        self.gold += amount
        self.gold_anim.append(
            Gold(
                position,
                amount
            )
        )

    def pay(self, amount: int):
        self.gold -= amount

    def canAfford(self, amount: int):
        return self.gold - amount > 0
