import pygame

import src.constantes as constantes
from src.runnable import Runnable
from UI.components.button import Button

from menus.menu import Menu
from menus.levelSelection import LevelSelectMenu
from menus.quit import QuitMenu


class MainMenu(Menu, Runnable):
    """The main menu class"""

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
        """The bit of code called at each iteration"""
        super().loop()
        self.draw()
        self.handleEvent()

    def draw(self):
        """Draws the buttons/images on screen and refreshes it"""
        self.screen.blit(self.background, (0, 0))
        super().draw()

        self.screen.flip()

    def handleEvent(self):
        """Handles the user inputs"""
        for event in super().handleEvent():
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                self.launch("quit")

    def launch(self, toLaunch: str):
        """Callback for the buttons

        Args:
            toLaunch (str): The argument describing the button that's been pressed and what should be launched
        """
        if toLaunch == "game":
            levelMenu = LevelSelectMenu(self.screen)
            levelMenu()
        elif toLaunch == "quit":
            quitMenu = QuitMenu(self.screen)
            if quitMenu() == "q":
                self.running = False
        else:
            print(f"Launching {toLaunch}")
