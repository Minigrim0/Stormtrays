import json
import pygame as pg

from copy import copy

from models.gameOptions import GameOptions

import src.constantes as consts
from src.tile import Tile
from src.errors.invalidPositionException import InvalidPositionException


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
            (consts.chem1, "c1"),
            (consts.tour2, "t2"),
            (consts.tour1, "t1"),
            (consts.croix1, "x1"),
            (consts.poubelle, "p1"),
            (consts.fort1, "k1"),
            (consts.Vide1, "v1"),
        ]

        for path, code in images:
            self.tiles[code] = Tile(
                code, (pg.image.load(path[0]).convert_alpha(), pg.image.load(path[1]).convert_alpha())
            )

        # self.editorImage["QG", 0] = pg.image.load("img/QuestGiverF1.png").convert_alpha()

        self.gold = 500
        self.Vie_Chateau = 100
        self.Nombre_Ennemis_Tue = 0
        self.background: pg.Surface = pg.image.load("assets/images/fond.png").convert_alpha()
        self.backgroundName = "fond1"
        self.size = [18, 11]

        self.GoldTab = []
        self.pos_Chateau = None
        self.FondFenetre = None
        self.map = None
        self.initMap()

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
        options = GameOptions.getInstance()
        with open(nomfichier) as f:
            data = json.load(f)
            print("Loading", options.fullPath("images", f'Fond/{data["background"]}.png'))
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
                        self.background.blit(self.map[x][y].image[0], tile_position)
                    elif self.map[x][y].code == "k1":
                        self.background.blit(self.map[x][y].image[0], tile_position)
                        self.pos_Chateau = [x, y + 1]

    def placeTile(self, position: tuple, tile):
        """Places a tile at the given coordinates

        Args:
            position (tuple): the position to place the tile at
            tile ([type]): [description]
        """
        if position[0] not in list(range(self.size[0])) or position[1] not in list(range(self.size[1])):
            raise InvalidPositionException("Tile is outside of the map !")

        self.map[position[0]][position[1]] = tile

    def draw(self, screen, editor=False):
        """Draws the current level

        Args:
            screen (Screen): The screen to blit the level on
        """
        screen.blit(self.background, (0, 0))

        if editor:
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    if self.map[x][y] is not None:
                        self.map[x][y].draw(screen, editor=editor)

    def Set_Difficulty(self, Difficulte):
        """Changes variables relative to the diffculty information

        Args:
            Difficulte ([type]): [description]

        Returns:
            [type]: [description]
        """
        Level_Difficulty = 0

        Difficulty = 11 - Difficulte

        if self.Nombre_Ennemis_Tue >= 0:
            Level_Difficulty = 10 * Difficulty
        if self.Nombre_Ennemis_Tue >= 10:
            Level_Difficulty = 9 * Difficulty
        if self.Nombre_Ennemis_Tue >= 25:
            Level_Difficulty = 8 * Difficulty
        if self.Nombre_Ennemis_Tue >= 50:
            Level_Difficulty = 7 * Difficulty
        if self.Nombre_Ennemis_Tue >= 100:
            Level_Difficulty = 6 * Difficulty
        if self.Nombre_Ennemis_Tue >= 200:
            Level_Difficulty = 5 * Difficulty
        if self.Nombre_Ennemis_Tue >= 400:
            Level_Difficulty = 4 * Difficulty
        if self.Nombre_Ennemis_Tue >= 750:
            Level_Difficulty = 3 * Difficulty
        if self.Nombre_Ennemis_Tue >= 1000:
            Level_Difficulty = 2 * Difficulty
        if self.Nombre_Ennemis_Tue >= 2500:
            Level_Difficulty = 1 * Difficulty

        return Level_Difficulty
