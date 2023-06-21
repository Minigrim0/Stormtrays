import os
import json
from typing import Optional

import pygame as pg


class Tileset:
    def __init__(self, path):
        self.file = os.path.basename(path)
        self.path = path
        self.data = {}
        self.images: dict = {}

        self._build()

    def _build(self):
        image = pg.image.load(
            f"{os.path.splitext(self.path)[0]}.png"
        )

        with open(self.path) as json_file:
            data = json.load(json_file)
            for key, value in data["tiles"].items():
                self.data[key.replace(".png", "")] = image.subsurface(
                    pg.Rect(value[0], value[1], data["size"][0], data["size"][1])
                )

    def __getitem__(self, name: str) -> Optional[pg.Surface]:
        if name in self.data.keys():
            return self.data[name]
        return None
