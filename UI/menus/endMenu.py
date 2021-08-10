import pygame as pg

from models.game_options import GameOptions
from src.runnable import Runnable
from UI.components.button import Button
from UI.menus.menu import Menu


class EndScreen(Menu, Runnable):
    def __init__(self):
        options: GameOptions = GameOptions.getInstance()

        self.button.append(
            Button(
                (516, 387), (),
                image=pg.image.load(options.fullPath("images", "buttons/small_button.png")).convert_alpha()
            )
        )

    def loop(self):
        super().loop()

    def draw(self):
        self.screen.blit(Fond_Menu_Opt, (1152 // 2 - 200, 704 // 2 - 200))
        self.screen.blit(Perdutxt, (1152 // 2 - 190, 704 // 2 - 200))
        self.screen.blit(quitpaus, (1152 // 2 - 60, 704 // 2 + 35))

    def handleEvent(self):
        for event in super().handleEvent():
            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                # Quitter le niveau en cours
                if quitjrect.collidepoint(event.pos):
                    Ecran_Perdu = False
                    Menu_Selection = True
