import json

import pygame as pg

from models.game_options import GameOptions
from models.screen import Screen


class Credits:
    """Represents the credit "image", built from a json file"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.elements: [{}] = []

        self._build()
        print(self.elements)

    @property
    def height(self):
        return sum([element["height"] + 10 for element in self.elements])

    def _build(self):
        with open(self.file_path) as credits_file:
            data = json.load(credits_file)
            for category in data["categories"]:
                self._buildCategory(category)

    def _buildCategory(self, category_data: dict):
        self._buildTitle(category_data["name"])

        for element in category_data["values"]:
            if isinstance(element, dict):
                self._buildElementFromDict(element)
            if isinstance(element, list):
                print("list", element)
            else:
                print("str", element)

    def _buildTitle(self, title: str):
        options: GameOptions = GameOptions.getInstance()
        title_font = options.fonts["MedievalSharp-xOZ5"]["100"]
        title = title_font.render(title, 1, (0, 0, 0))
        self.elements.append(
            {
                "image": title,
                "position_x": self._getElementXPosition(title.get_size()[0], "centered"),
                "height": title.get_size()[1]
            }
        )

    def _buildElementFromDict(self, element_dict):
        if "image" in element_dict.keys():
            image = pg.image.load(element_dict["image"]).convert_alpha()
            position = element_dict["position"] if "position" in element_dict.keys() else "centered"
            self.elements.append(
                {
                    "image": image,
                    "position_x": self._getElementXPosition(image.get_size()[0], position),
                    "height": image.get_size()[1]
                }
            )

    def _buildElementFromString(self, string: str):
        options: GameOptions = GameOptions.getInstance()
        element_font = options.fonts["MedievalSharp-xOZ5"]["40"]
        element = element_font.render(string, 1, (0, 0, 0))
        self.elements.append(
            {
                "image": element,
                "position_x": self._getElementXPosition(element.get_size[0], "centered"),
                "height": element.get_size[1]
            }
        )

    def _getElementXPosition(self, element_size: int, position: str, min_pos_x: int = 0, max_pos_x: int = 1152) -> int:
        if position == "centered":
            return (max_pos_x - element_size) / 2
        elif position == "left":
            return min_pos_x
        elif position == "right":
            return max_pos_x - element_size

    def draw(self, screen: Screen, y_offset: int):
        for element in self.elements:
            screen.blit(
                element["image"],
                (element["position_x"], y_offset)
            )
            y_offset += element["height"] + 10
