import pygame as pg

from models.character import Character
from models.game_options import GameOptions
from models.level import Level
from models.screen import Screen
from UI.components.button import Button
from UI.components.xp_bar import XPBar
from UI.menus.pause import PauseMenu


class GameUI:
    """Represents the UI of a game"""

    instance = None

    @staticmethod
    def getInstance():
        if GameUI.instance is None:
            GameUI()
        return GameUI.instance

    def __init__(self):
        if GameUI.instance is not None:
            raise RuntimeError("Trying to instanciate a second object from a signleton class")
        GameUI.instance = self

        options: GameOptions = GameOptions.getInstance()
        self.font = options.fonts["MedievalSharp-xOZ5"]["20"]

        self.stats_background = pg.image.load("assets/images/overlays/stats_background.png")

        self.gold_amount: pg.Surface = None
        self.bastion_health: pg.Surface = None
        self.character_level: pg.Surface = None
        self.ennemies_killed: pg.Surface = None
        self.character_damage: pg.Surface = None
        self.character_speed: pg.Surface = None

        self.buttons: [Button] = None
        self.xp_bar: XPBar = None

        self._build()

    def _build(self):
        options: GameOptions = GameOptions.getInstance()
        self.buttons = [
            Button(
                (810, 20), (40, 40),
                image=[
                    pg.image.load(options.fullPath("images", "buttons/speed.png")),
                    pg.image.load(options.fullPath("images", "buttons/speedx.png")),
                ],
                toggleable=True,
                callback=self.toggleSpeed
            ),
            Button(
                (760, 20), (40, 40),
                image=pg.image.load(options.fullPath("images", "buttons/pause.png")),
                callback=self.pauseMenu
            )
        ]

        self.xp_bar = XPBar(
            (870, 86), (270, 18),
            fg_color=(0, 255, 40), bg_color=(-1, -1, -1),
            overlay="assets/images/overlays/xp_bar.png"
        )

        self.update(0)

    def update(self, elapsed_time: float):
        level = Level.getInstance()
        character = Character.getInstance()
        self.xp_bar.update(elapsed_time)

        self.gold_amount = self.font.render("Or : %i" % level.gold, 1, (0, 0, 0))
        self.bastion_health = self.font.render("Vie : %i pv." % level.health, 1, (0, 0, 0))
        self.character_level = self.font.render("Niveau %i" % character.level, 1, (0, 0, 0))
        self.ennemies_killed = self.font.render("Victimes : %i" % character.kills, 1, (0, 0, 0))
        self.character_damage = self.font.render("Dégats : %i" % character.damage, 1, (0, 0, 0))
        self.character_speed = self.font.render("Vitesse : %i " % character.speed, 1, (0, 0, 0))

    def handleEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.click(event.pos)

    def draw(self, screen: Screen):
        screen.blit(self.stats_background, (870, 0))

        screen.blit(self.gold_amount, (872, 5))
        screen.blit(self.bastion_health, (872, 27))
        screen.blit(self.character_speed, (872, 54))
        screen.blit(self.character_level, (1020, 3))
        screen.blit(self.ennemies_killed, (1020, 27))
        screen.blit(self.character_damage, (1020, 53))

        for button in self.buttons:
            button.draw(screen)

        self.xp_bar.draw(screen)

    def add_xp(self, amount: int):
        """Adds xp to the xp_bar, and call the level_up function of the Character if the objective is reached"""
        self.xp_bar.add_xp(amount)

    @staticmethod
    def toggleSpeed():
        options = GameOptions.getInstance()
        options.toggleGameSpeed()

    def pauseMenu(self):
        from models.game import Game
        PauseMenu(background=Game.getInstance()._draw)()

    def reset(self):
        self.xp_bar.resetBar()
        self.update(0)
