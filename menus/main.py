import pygame

import src.constantes as constantes
from src.runnable import Runnable
from UI.components.button import Button
from menus.menu import Menu


class MainMenu(Menu, Runnable):
    def __init__(self, screen):
        super().__init__(screen)
        self.background = pygame.image.load(constantes.fondm).convert_alpha()
        self.buttons.append(Button((652, 464), (500, 50), pygame.image.load(constantes.joue).convert_alpha()))
        self.buttons[-1].callback = (self.launch, "game")
        self.buttons.append(Button((752, 584), (500, 50), pygame.image.load(constantes.option).convert_alpha()))
        self.buttons[-1].callback = (self.launch, "options")
        self.buttons.append(Button((702, 524), (500, 50), pygame.image.load(constantes.credits_path).convert_alpha()))
        self.buttons[-1].callback = (self.launch, "credits")
        self.buttons.append(Button((802, 644), (500, 50), pygame.image.load(constantes.quit_path).convert_alpha()))
        self.buttons[-1].callback = (self.launch, "quit")

    def loop(self):
        super().loop()
        self.draw()
        self.handleEvent()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        super().draw()

        self.screen.flip()

    def handleEvent(self):
        for event in super().handleEvent():
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                self.launch("quit")

    def launch(self, type):
        print(f"Launching {type}")
