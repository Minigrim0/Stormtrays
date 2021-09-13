import glob
import json
import os

from gettext import gettext as _

import pygame as pg

from models.character import Character
from models.game import Game
from models.game_options import GameOptions
from src.runnable import Runnable
from UI.components.animated_selector import AnimatedSelector
from UI.components.button import Button
from UI.menus.menu import Menu


class ChacracterChoiceMenu(Menu, Runnable):
    """The character selection menu"""

    def __init__(self, level: str = None, **kwargs):
        super().__init__(**kwargs)
        self.scrollAmount = 60

        self.dark_background = pg.Surface((576, 704), pg.SRCALPHA)
        self.dark_background.fill((0, 0, 0, 128))

        self.selector = AnimatedSelector((576, 50), (576, 550))

        self._load(level)

    def _load(self, level):
        """Loads the buttons for the menu"""
        options = GameOptions.getInstance()
        self.buttons["back"] = Button(
            (654, 0),
            (500, 50),
            image=pg.image.load(options.fullPath("images", "buttons/MenuButton.png")).convert_alpha(),
            callback=self.back,
        )
        self.buttons["back"].build(_("menu_cc_back"), options.fonts["MedievalSharp-xOZ5"]["35"], (20, "CENTER"))

        button_image = pg.image.load(options.fullPath("images", "buttons/small_button.png")).convert_alpha()
        self.buttons["choose"] = Button(
            (864 - button_image.get_size()[0]//2, 600), button_image.get_size(),
            image=button_image,
            callback=self.runLevel,
            level=level
        )
        self.buttons["choose"].build(
            _("menu_cc_start"), options.fonts["MedievalSharp-xOZ5"]["25"],
            ("CENTER", "CENTER")
        )

        self._loadCharacters()

    def _loadCharacters(self):
        """Loads the available characters and put them in the animated selector"""
        for character_folder in glob.glob("assets/character/*"):
            with open(os.path.join(character_folder, "setup.json")) as data_file:
                data = json.load(data_file)

            self.selector.addElement(name=data["name"], animations=data["states"])

    def loop(self):
        """The bit of code called at each iteration"""
        super().loop()

        self.draw()
        self.screen.flip()

        self.selector.update(self.screen.time_elapsed)

        self.handleEvent()

    def _draw(self):
        """Draws the buttons/images on screen and refreshes it"""
        self.screen.blit(self.dark_background, (576, 0))

        self.selector.draw(self.screen)

    def handleEvent(self):
        """Handles the user inputs"""
        for event in super().handleEvent():
            if event.type == pg.locals.KEYDOWN and event.key == pg.locals.K_ESCAPE:
                self.back()

            self.selector.handleEvent(event)

    def runLevel(self, level):
        """Runs the level selected in the previous menu with the selected character"""
        character = Character.getInstance()
        character.setStyle(self.selector.selected_name)
        options = GameOptions.getInstance()
        levelPath = options.fullPath("levels", f"{level}.json")
        Game.getInstance()(self.screen, levelPath)
        self.back()

    def back(self):
        """Callback for the back button, gets the user back to the Level Selection menu"""
        self.running = False
