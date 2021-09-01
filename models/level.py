import logging
import json
from copy import copy

import pygame as pg

from models.game_options import GameOptions
from models.screen import Screen
from src.bastion import Bastion
from src.coin import Coin
from src.errors.invalidPositionException import InvalidPositionException
from src.errors.invalidPathException import InvalidPathException
from src.tile import Tile


class Level:
    """The level class contains information and logic about the current level
    such as the list of coins and the number of ennemy killed
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

        self.counters = {
            "tower_kills": 0,
            "player_kills": 0
        }

        self.bastions: list(Bastion) = []
        self.spawn_places = []
        self.gold = 500

        self.background: pg.Surface = None
        self.background_path = "assets/images/levels/fond1.png"
        self.size = [18, 11]

        self.coins: [Coin] = []
        self.map = None
        self.initMap()
        self._preload()

    @property
    def killed_ennemies(self) -> int:
        """Returns the total amount of ennemies killed"""
        return self.counters["player_kills"] + self.counters["tower_kills"]

    @property
    def health(self):
        """Returns the sum of all the bastions health"""
        return sum([x.health for x in self.bastions])

    @property
    def tile_size(self):
        """Returns the size of a tile in pixels"""
        screen: Screen = Screen.getInstance()
        return (
            screen.initial_size[0] / self.size[0],
            screen.initial_size[1] / self.size[1],
        )

    @property
    def spawn_rate(self):
        """Returns the spawn rate of the ennemies, based on the difficulty and the amount of killed ennemies"""
        options = GameOptions.getInstance()

        return (0.2 * options.difficulty) * (0.1 * self.killed_ennemies) + 1

    @property
    def valid(self) -> bool:
        for start_pos in self.spawn_places:
            try:
                self.findLinkedBastion(start_pos)
            except InvalidPathException:
                return False
        return len(self.spawn_places) > 0

    def _preload(self):
        """Loads the diffrent tiles"""
        images = [
            (("assets/images/tiles/straight.png", "assets/images/tiles/start_edit.png"), "s1"),
            (("assets/images/tiles/straight.png", "assets/images/tiles/straight_edit.png"), "c1"),
            (("assets/images/tiles/turn.png", "assets/images/tiles/left_turn_edit.png"), "t2"),
            (("assets/images/tiles/turn.png", "assets/images/tiles/right_turn_edit.png"), "t1"),
            ("assets/images/tiles/cross.png", "x1"),
            ("assets/images/tiles/fort.png", "k1"),
            ("assets/images/poubelle.png", "p1"),
            ((None, "assets/images/tiles/blocked_edit.png"), "v1"),
        ]

        for path, code in images:
            if isinstance(path, tuple):
                self.tiles[code] = Tile(
                    code, (
                        pg.image.load(path[0]).convert_alpha() if path[0] is not None else None,
                        pg.image.load(path[1]).convert_alpha() if path[1] is not None else None
                    )
                )
            elif isinstance(path, str):
                self.tiles[code] = Tile(
                    code, (
                        pg.image.load(path).convert_alpha(),
                        pg.image.load(path).convert_alpha()
                    )
                )

    def _build(self, filename, editor=False):
        """Builds the level from a file"""
        with open(filename) as f:
            data = json.load(f)
            self.setBackground(data["background"])
            self.size = data["size"]
            self.initMap()

        self.spawn_places = []
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
                        if self.map[x][y].code == "s1":
                            self.spawn_places.append((x, y))
                        self.map[x][y].draw(self.background)
                    elif self.map[x][y].code == "k1":
                        bastion = Bastion((x, y), initial_health=100)
                        self.bastions.append(bastion)

    def findLinkedBastion(self, start_pos: tuple) -> (int, int):
        """Follows a path to find the bastion at the end of the path"""
        logging.info(f"checking starting_position {start_pos}")
        x, y = start_pos
        while self.map[x][y] is not None and self.map[x][y].code != "k1":
            logging.info(f"{x}-{y}")
            direction_x, direction_y = self.map[x][y].direction()
            x += direction_x
            y += direction_y

        if self.map[x][y] is None:
            raise InvalidPathException(f"The path starting on {start_pos} does not lead to a bastion")
        return x, y

    def setBackground(self, background_path: str):
        """Sets the background of the level"""
        self.background_path = background_path
        self.background = pg.image.load(background_path)
        self.background = pg.transform.scale(self.background, (1152, 704))

    def reset(self):
        """Resets the map, the counters, the gold etc..."""
        self.counters = {
            "tower_kills": 0,
            "player_kills": 0
        }

        self.bastions: list(Bastion) = []
        self.gold = 500

        self.coins: [Coin] = []

    def initMap(self):
        """Empties the level"""
        self.map = []
        for x in range(self.size[0]):
            self.map.append([])
            for _ in range(self.size[1]):
                self.map[x].append(None)

    def load(self, filename, editor=False):
        """Loads a level (for either the editor or the game)"""
        self.reset()
        self._build(filename, editor)

    def save(self, filename: str, thumbnail_path: str):
        """Saves the current level"""
        serializedMap = [[tile.toJson() if tile is not None else {} for tile in row] for row in self.map]
        level = {
            "background": self.background_path,
            "size": self.size,
            "map": serializedMap,
            "thumbnail": thumbnail_path,
        }

        with open(filename, "w") as f:
            f.write(json.dumps(level))

    def placeTile(self, position: tuple, tile):
        """Places a tile at the given coordinates"""
        if position[0] not in list(range(self.size[0])) or position[1] not in list(range(self.size[1])):
            raise InvalidPositionException("Tile is outside of the map !")

        self.map[position[0]][position[1]] = tile
        if tile is not None and tile.code == "s1":
            self.spawn_places.append(position)

    def update(self, elapsed_time: float):
        """Updates the bastions and the floating coins"""
        for bastion in self.bastions:
            bastion.update(elapsed_time)
        for coin in self.coins:
            if coin.update(elapsed_time):
                del self.coins[self.coins.index(coin)]

    def draw(self, screen, editor=False, force_tile_rendering=False):
        """Draws the current level"""
        screen.blit(self.background, (0, 0))
        for bastion in self.bastions:
            bastion.draw(screen)

        if editor or force_tile_rendering:
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    if self.map[x][y] is not None:
                        self.map[x][y].draw(screen, editor=editor)

        for gold in self.coins:
            gold.draw(screen)

    def hitBastion(self, position: tuple, damage: int = 0) -> bool:
        """Hits the bastion at the given coordinate (if any) with the given amount of damage"""
        for bastion in self.bastions:
            if bastion.position == position:
                bastion.hit(damage)
                if not bastion.alive:
                    logging.info("Bastion dead, deleting spawn place")
                    for start_pos in self.spawn_places:
                        if self.findLinkedBastion(start_pos) == bastion.position:
                            logging.info(f"Spawn place is {start_pos}, deleting")
                            del self.spawn_places[self.spawn_places.index(start_pos)]
                return True
        return False

    def addGold(self, amount, position):
        """Adds the given amount of gold to the user's stash and spawns a coin"""
        self.gold += amount
        self.coins.append(
            Coin(position, amount)
        )

    def pay(self, amount: int):
        """Pays the given amount from the user's stash"""
        self.gold -= amount

    def canAfford(self, amount: int):
        """Returns whether the player can afford the given amount"""
        return self.gold - amount > 0

    def add_count(self, counter: str, amount: int):
        """Adds the given value to the given counter"""
        self.counters[counter] += amount

    def isFree(self, position: tuple) -> bool:
        """Returns whether the tile at the given position is free or not"""
        return self.map[position[0]][position[1]] is None
