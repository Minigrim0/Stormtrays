import pygame as pg

from models.character import Character
from models.ennemy import Ennemy
from models.level import Level
from models.projectile import Projectile
from models.screen import Screen
from models.game_options import GameOptions
from models.tower import Tower
from src.invocation import Invocation
from src.runnable import Runnable
from UI.menus.game_ui import GameUI


class Game(Runnable):
    def __init__(self, screen: Screen, levelPath: str):
        super().__init__()
        self.level = Level.getInstance()
        self.level._build(levelPath)
        self.screen = screen

        self.level.gold = 500
        self.level.Nombre_Ennemis_Tue = 0

        # CooldownInvoc = 0
        # TpsCoolDown = 0

        # TpsLvl = 0
        # Icapacite1 = 0
        # ImgInvoc = True
        # invocation = None
        # Tps_Invoc_affiche = None
        # Compteur_Iteration = 0
        # Time_50 = myfont2.render("0", 1, (0, 0, 0))

    def _end(self):
        """Called at the end of the last loop of the runnable"""
        # Make sure to reinit the game speed
        options = GameOptions.getInstance()
        options.setSpeed(1)

    def _draw(self):
        """Draws the game without refreshing the screen"""
        self.level.draw(self.screen)

        Ennemy.getInstance().draw(self.screen)
        Tower.getInstance().draw(self.screen)
        Character.getInstance().draw(self.screen)
        GameUI.getInstance().draw(self.screen)
        Projectile.getInstance().draw(self.screen)

        """
        if invocation and not invocation.vit(screen, Liste_Mechants, niveau):
            King.XpToAdd += invocation.xp
            invocation = None

        Level_Difficulty = niveau.Set_Difficulty(Difficulte)

        if Tps_Invoc_affiche and King.Level_Roi >= 5:
            screen.blit(TpsRestInvocSombre, (1152 - 550, 10))
            screen.blit(Tps_Invoc_affiche, (1152 - 535, 25))
        elif King.Level_Roi >= 5:
            screen.blit(TpsRestInvoc, (1152 - 550, 10))

        if King.Level_Roi == 5 and not HaveSeenLvl5Msg:
            screen.blit(InfoLvl5Img, (0, 0))
        """

    def loop(self):
        """Updates whole the objects of the game"""
        Level.getInstance().update(self.screen.elapsed_time)
        Ennemy.getInstance().update(self.screen.elapsed_time)
        Character.getInstance().update(self.screen.elapsed_time)
        GameUI.getInstance().update(self.screen.elapsed_time, menu_background=self._draw)
        Tower.getInstance().update(self.screen.elapsed_time)
        Projectile.getInstance().update(self.screen.elapsed_time)

        self.draw()

        self.handleEvent()

    def handleEvent(self):
        """Handles user events"""
        for event in self.screen.getEvent():
            Character.getInstance().handleEvent(event)
            GameUI.getInstance().handleEvent(event)
            Tower.getInstance().handleEvent(event)

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False

    def draw(self):
        """Draws the game ond refresh the screen"""
        self._draw()
        self.screen.flip()
