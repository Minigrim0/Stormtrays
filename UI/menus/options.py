import pygame as pg

from models.game_options import GameOptions
from models.screen import Screen
from src.runnable import Runnable
from UI.components.animation import Animation
from UI.components.button import Button
from UI.menus.menu import Menu


class OptionMenu(Menu, Runnable):
    """The menu of options"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        options = GameOptions.getInstance()

        self.menu_background = pg.image.load(
            options.fullPath("images", "backgrounds/submenu_background.png")
        ).convert_alpha()
        self.menu_background_position = (
            (Screen.getInstance().get_size()[0] - self.menu_background.get_size()[0]) / 2,
            (Screen.getInstance().get_size()[1] - self.menu_background.get_size()[1]) / 2
        )

        self._build()

        self.Diffictxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Difficulté : {}".format(options.difficulty), 1, (0, 0, 0)
        )
        self.Volumetxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Volume : {}".format(int(options.volume * 10)), 1, (0, 0, 0)
        )

        Moins = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "-", 1, (0, 0, 0)
        )
        Plus = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "+", 1, (0, 0, 0)
        )

        self.buttons["lessVolume"] = Button((655, 302), (40, 40), image=Moins, callback=self.updateVolume, value=-1)
        self.buttons["moreVolume"] = Button((705, 302), (40, 40), image=Plus, callback=self.updateVolume, value=1)
        self.buttons["lessDifficulty"] = Button(
            (655, 347), (40, 40), image=Moins, callback=self.updateDifficulty, value=-1)
        self.buttons["moreDifficulty"] = Button(
            (705, 347), (40, 40), image=Plus, callback=self.updateDifficulty, value=1)
        self.buttons["quitOptions"] = Button(
            (516, 407), (120, 50),
            image=pg.image.load(options.fullPath("images", "buttons/small_button.png")).convert_alpha(),
            callback=self.quitMenu
        )
        self.buttons["quitOptions"].build(
            "Retour", options.fonts["MedievalSharp-xOZ5"]["25"],
            text_position=("CENTER", "CENTER")
        )

        self.buttons["play"] = Button((1102, 464), (500, 50), image=self.pickFromBase["play"])
        self.buttons["credits"] = Button((1102, 524), (500, 50), image=self.pickFromBase["credits"])
        self.buttons["options"] = Button((1002, 584), (500, 50), image=self.pickFromBase["options"])
        self.buttons["quit"] = Button((1102, 644), (500, 50), image=self.pickFromBase["quit"])

    def _build(self):
        """Builds menu's background"""
        options = GameOptions.getInstance()

        title = options.fonts["MedievalSharp-xOZ5"]["60"].render(
            "Options", 1, (0, 0, 0)
        )

        title_pos = (self.menu_background.get_size()[0] - title.get_size()[0]) / 2

        self.menu_background.blit(
            title,
            (title_pos, 15)
        )

    def loop(self):
        """The bit of code called at each iteration"""
        super().loop()

        self.draw()
        self.screen.flip()

        self.handleEvent()

    def _draw(self):
        """Draws the buttons/images on screen, called by Menu class, in between background and buttons"""
        self.screen.blit(self.menu_background, self.menu_background_position)
        self.screen.blit(self.Volumetxt, (410, 302))
        self.screen.blit(self.Diffictxt, (410, 347))

    def handleEvent(self):
        """Handles user inputs"""
        for _ in super().handleEvent():  # skipcq PTC-W0047
            pass

    def updateDifficulty(self, value: int):
        """Updates the difficulty of the game"""
        GameOptions.getInstance().changeDifficulty(value)
        options = GameOptions.getInstance()

        self.Diffictxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Difficulté : {}".format(options.difficulty), 1, (0, 0, 0)
        )

    def updateVolume(self, value: int):
        """Updates the volume of the music"""
        GameOptions.getInstance().changeVolume(value)
        options = GameOptions.getInstance()

        self.Volumetxt = options.fonts["MedievalSharp-xOZ5"]["40"].render(
            "Volume : {}".format(int(options.volume * 10)), 1, (0, 0, 0)
        )

    def quitMenu(self):
        """Quits the option menu"""
        anim = Animation(
            "UI/animations/mainToOptions.json",
            self.screen,
            pickFrom=self.pickFrom,
            background=self.backgroundCallback if self.backgroundCallback is not None else self._draw,
            **self.background_kwargs
        )
        anim.invert()
        anim()
        self.running = False
