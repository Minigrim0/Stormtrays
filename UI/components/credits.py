import json
import logging

import pygame as pg

from models.game_options import GameOptions
from models.screen import Screen


class Credits:
    """Represents the credit "image", built from a json file"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.elements: [{}] = []

        self._build()

    @property
    def height(self) -> int:
        """Returns the total height of the credits"""
        return sum([element["height"] + 10 for element in self.elements])

    def _build(self):
        """Builds the credits from a file"""
        with open(self.file_path) as credits_file:
            data = json.load(credits_file)
            for category in data["categories"]:
                self._buildCategory(category)

                # Add spacer between categories
                self.elements.append(
                    {
                        "image": None,
                        "position_x": 0,
                        "height": 40
                    }
                )

    def _buildCategory(self, category_data: dict):
        """Builds a category of credits"""
        self._buildTitle(category_data["name"])

        for element in category_data["values"]:
            if isinstance(element, dict):
                self._buildElementFromDict(element)
            elif isinstance(element, list):
                self._buildElementFromList(element)
            elif isinstance(element, str):
                self._buildElementFromString(element)
            else:
                logging.warning(f"Unhandled {type(element)}")

    def _buildTitle(self, title: str):
        """Builds the title of a caegory"""
        options: GameOptions = GameOptions.getInstance()
        title_font = options.fonts["MedievalSharp-xOZ5"]["60"]
        title = title_font.render(title, 1, (0, 0, 0))
        self.elements.append(
            {
                "image": title,
                "position_x": self._getElementXPosition(title.get_size()[0], "centered"),
                "height": title.get_size()[1]
            }
        )

    def _buildElementFromDict(self, element_dict):
        """Builds an element from a dict"""
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
        """Builds an element from a string with default parameters"""
        options: GameOptions = GameOptions.getInstance()
        element_font = options.fonts["MedievalSharp-xOZ5"]["40"]
        element = element_font.render(string, 1, (0, 0, 0))
        self.elements.append(
            {
                "image": element,
                "position_x": self._getElementXPosition(element.get_size()[0], "centered"),
                "height": element.get_size()[1]
            }
        )

    def _buildElementFromList(self, element_list: list):
        """Builds elements from a list"""
        options: GameOptions = GameOptions.getInstance()
        element_font = options.fonts["MedievalSharp-xOZ5"]
        images = []
        for element in element_list:
            if isinstance(element, dict):
                if "image" in element.keys():
                    images.append(
                        pg.image.load(element["image"])
                    )
                elif "text" in element.keys():
                    font_size = str(element["size"]) if "size" in element.keys() else "40"
                    images.append(
                        element_font[font_size].render(element["text"], 1, (0, 0, 0))
                    )
            elif isinstance(element, str):
                images.append(
                    element_font["40"].render(element, 1, (0, 0, 0))
                )
        final_image = self._mergeImages(images)
        self.elements.append(
            {
                "image": final_image,
                "position_x": self._getElementXPosition(final_image.get_size()[0], "centered"),
                "height": final_image.get_size()[1]
            }
        )

    @staticmethod
    def _mergeImages(images: [pg.Surface]) -> pg.Surface:
        """Merges two images into a single one"""
        final_size = (
            sum([img.get_size()[0] for img in images]),
            max([img.get_size()[1] for img in images])
        )
        final_image = pg.Surface(final_size, pg.SRCALPHA)
        x_offset = 0
        for image in images:
            final_image.blit(
                image,
                (
                    x_offset,
                    (final_size[1] - image.get_size()[1]) // 2
                )
            )
            x_offset += image.get_size()[0]

        return final_image

    @staticmethod
    def _getElementXPosition(element_size: int, position: str, min_pos_x: int = 0, max_pos_x: int = 1152) -> int:
        """Returns the position on the x axis of an element"""
        if position == "centered":
            return (max_pos_x - element_size) / 2
        if position == "left":
            return min_pos_x
        if position == "right":
            return max_pos_x - element_size
        return 0

    def draw(self, screen: Screen, y_offset: int):
        """Draws the credits elements on screen with the given offset"""
        for element in self.elements:
            if element["image"] is not None:
                screen.blit(
                    element["image"],
                    (element["position_x"], y_offset)
                )
            y_offset += element["height"] + 10
