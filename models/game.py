import pygame as pg

from models.character import Character
from models.ennemy import Ennemy
from models.game_options import GameOptions
from models.level import Level
from models.projectile import Projectile
from models.screen import Screen
from models.tower import Tower
from src.runnable import Runnable
from UI.components.gui.game_ui import GameUI
from UI.components.gui.tower_ui import TowerUI
from UI.menus.endMenu import EndScreen


class Game(Runnable):
    """The game in itself, runs on its own and updates/draws all the elements"""

    instance = None

    @staticmethod
    def getInstance():
        """Singleton Pattern"""
        if Game.instance is None:
            Game()
        return Game.instance

    def __init__(self):
        if Game.instance is not None:
            raise RuntimeError("Trying to instanciate a second class from a singleton")
        Game.instance = self

        super().__init__()
        self.level = Level.getInstance()
        self.screen: Screen = None

    def _start(self, screen: Screen, levelPath: str):  # skipcq PYL-W0221
        """Called before the first loop, reinit the whole game"""
        self.level.load(levelPath)
        self.screen = screen
        Tower.getInstance().reset()
        Ennemy.getInstance().reset()
        Character.getInstance().reset()
        GameUI.getInstance().reset()

    def _end(self):
        """Called at the end of the last loop of the runnable"""
        # Make sure to reinit the game speed
        options = GameOptions.getInstance()
        options.setSpeed(1)

    def loop(self):
        """Gets called at each code loop"""
        self.update()
        self.draw()
        self.screen.flip()
        self.handleEvent()

    def draw(self):
        """Draws the game"""
        self.level.draw(self.screen)

        Ennemy.getInstance().draw(self.screen)
        Tower.getInstance().draw(self.screen)
        Character.getInstance().draw(self.screen)
        Projectile.getInstance().draw(self.screen)
        GameUI.getInstance().draw(self.screen)
        TowerUI.getInstance().draw(self.screen)

    def update(self):
        """Updates all the objects of the game"""
        Level.getInstance().update(self.screen.elapsed_time)
        Ennemy.getInstance().update(self.screen.elapsed_time)
        Character.getInstance().update(self.screen.elapsed_time)
        TowerUI.getInstance().update(self.screen.elapsed_time)
        GameUI.getInstance().update(self.screen.elapsed_time)
        Tower.getInstance().update(self.screen.elapsed_time)
        Projectile.getInstance().update(self.screen.elapsed_time)

        if Level.getInstance().health <= 0:
            self.endGame()

    def handleEvent(self):
        """Handles user events"""
        for event in self.screen.getEvent():
            GameUI.getInstance().handleEvent(event)
            TowerUI.getInstance().handleEvent(event)
            Character.getInstance().handleEvent(event)
            Tower.getInstance().handleEvent(event)

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                GameUI.pauseMenu()

    def endGame(self):
        """Shows the end screen"""
        EndScreen(self.screen, background=self.draw)()
        self.running = False
