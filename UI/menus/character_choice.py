import glob
import json
import os

import pygame as pg

from models.game import Game
from models.game_options import GameOptions
from src.runnable import Runnable
from UI.components.animation import Animation
from UI.components.image_animation import ImageAnimation
from UI.components.button import Button
from UI.menus.menu import Menu


class ChacracterChoiceMenu(Menu, Runnable):
    """The character selection menu"""

    def __init__(self, level: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scrollAmount = 60

        self.dark_background = pg.Surface((576, 704), pg.SRCALPHA)
        self.dark_background.fill((0, 0, 0, 128))

        self.animations: list = []
        self.selected_character: int = 0
        self.current_animation: str = "idle"

        self._load(level)

    def _load(self, level):
        options = GameOptions.getInstance()
        self.buttons["back"] = Button(
            (654, 0),
            (500, 50),
            image=pg.image.load(options.fullPath("images", "buttons/MenuButton.png")).convert_alpha(),
            callback=self.back,
        )
        self.buttons["back"].build("Retour", options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        button_image = pg.image.load(options.fullPath("images", "buttons/small_button.png")).convert_alpha()

        self.buttons["choose"] = Button(
            (516, 387), button_image.get_size(),
            image=button_image,
            callback=self.runLevel,
            level=level
        )
        self.buttons["choose"].build(
            "Continuer", options.fonts["MedievalSharp-xOZ5"]["25"],
            ("CENTER", "CENTER")
        )

        self._loadCharacters()

    def _loadCharacters(self):
        for character_folder in glob.glob("assets/character/*"):
            with open(os.path.join(character_folder, "setup.json")) as data_file:
                data = json.load(data_file)

            self.animations.append({
                "name": data["name"],
                "animations": {
                    name: ImageAnimation(initial_data=state, image_size=(256, 256)) for name, state in data["states"].items()
                }
            })
        self.animations[self.selected_character]["animations"][self.current_animation].play()

    def loop(self):
        """The bit of code called at each iteration"""
        super().loop()

        self.draw()
        self.screen.flip()

        self.animations[self.selected_character]["animations"][self.current_animation].update(self.screen.time_elapsed)

        self.handleEvent()

    def _draw(self):
        """Draws the buttons/images on screen and refreshes it"""
        self.screen.blit(self.dark_background, (576, 0))

        self.animations[self.selected_character]["animations"][self.current_animation].draw(self.screen, (500, 200))

    def handleEvent(self):
        """Handles the user inputs"""
        for event in super().handleEvent():
            if event.type == pg.locals.KEYDOWN and event.key == pg.locals.K_ESCAPE:
                self.back()

    def scroll(self, amount):
        """Moves the levelss cards up or down"""
        self.scrollAmount += amount
        for levelcard in self.cards:
            levelcard.move((0, amount))

    def runLevel(self, level):
        """Callback for the levels' cards, launches the selected level"""
        options = GameOptions.getInstance()
        levelPath = options.fullPath("levels", f"{level}.json")
        Game.getInstance()(self.screen, levelPath)

    def back(self):
        """Callback for the back button, gets the user back to the Level Selection menu"""
        self.running = False
