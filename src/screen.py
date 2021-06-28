import time
import pygame

from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION

import src.constantes as const
from src.button import Button


class Screen:
    def __init__(self, size: tuple, name: str, icon: str, fullScreen=True):
        self.font = pygame.font.SysFont("Viner Hand ITC", 25)
        self.nativeSize = size

        info = pygame.display.Info()
        self.fullSize = (info.current_w, info.current_h)

        self.fullScreen = fullScreen
        if self.fullScreen:
            self.resize(self.fullSize)
        else:
            self.resize(self.nativeSize)

        self.scaleButton = Button(
            (2, self.nativeSize[1] - 22), (20, 20), pygame.image.load(const.ScaleImg).convert_alpha()
        )
        self.scaleButton.callback = self.rescale

        self.fenetre = pygame.Surface(self.nativeSize)

        pygame.display.set_caption(name)
        if icon is not None and icon != "":
            pygame.display.set_icon(pygame.image.load(icon).convert_alpha())

        self.timeElapsed = 0
        self.startTime = time.time()

        self.frameCounter = 0
        self.FPS = 0
        self.showFPS = False

    def rescale(self):
        """Resizes the screen to either fullscreen or native size"""
        self.fullScreen = not self.fullScreen
        if self.fullScreen:
            self.resize(self.fullSize)
        else:
            self.resize(self.nativeSize)

    def resize(self, size: tuple):
        """Resizes the screen to the given size

        Args:
            size (tuple): the new size for the screen
        """
        if self.fullScreen:
            self.fenetreAffiche = pygame.display.set_mode(self.fullSize, pygame.locals.FULLSCREEN)
        else:
            self.fenetreAffiche = pygame.display.set_mode(size, pygame.locals.RESIZABLE)

        taillex = size[0] / self.nativeSize[0]
        tailley = size[1] / self.nativeSize[1]
        self.taille = min(taillex, tailley)

        self.posAffiche = (
            (size[0] - int(self.taille * self.nativeSize[0])) // 2,
            (size[1] - int(self.taille * self.nativeSize[1])) // 2,
        )

    def flip(self):
        """Refreshes the screen"""
        self.update()
        self.scaleButton.draw(self)
        self.fenetreAffiche.blit(
            pygame.transform.smoothscale(
                self.fenetre, (int(self.nativeSize[0] * self.taille), int(self.nativeSize[1] * self.taille))
            ),
            self.posAffiche,
        )
        pygame.display.flip()

    def blit(self, surface: pygame.Surface, pos: tuple):
        """Draws an image to the screen

        Args:
            surface (pygame.Surface): The surface to draw
            pos (tuple): The position to drae it on
        """
        self.fenetre.blit(surface, pos)

    def getEvent(self):
        """Handles user events, reacting of needed, and yielding the event list to the calling function

        Yields:
            pygame.event: The event list
        """
        for event in pygame.event.get():
            if event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN:
                event.pos = self.convertToRelativePos(event.pos)
                if self.isPosOutOfScreen(event.pos):
                    continue
            if event.type == pygame.locals.QUIT:
                exit()
            elif event.type == pygame.locals.KEYDOWN:
                self.handleFKeys(event)
            elif event.type == pygame.locals.VIDEORESIZE:
                self.resize(event.size)
            elif event.type == MOUSEBUTTONDOWN:
                self.scaleButton.click(event.pos)

            yield event

    def isPosOutOfScreen(self, pos: tuple):
        """Checks whether the position is out of the rendered screen or not

        Args:
            pos (tuple): The position to check

        Returns:
            bool: whether the given position is out of the screen or not
        """
        return pos[0] < 0 or pos[1] < 0 or pos[0] >= self.nativeSize[0] or pos[1] >= self.nativeSize[1]

    def convertToRelativePos(self, pos: tuple):
        """Converts an real position to a relative position

        Args:
            pos (tuple): The position to convert

        Returns:
            tuple: the converted position
        """
        return (int((pos[0] - self.posAffiche[0]) / self.taille), int((pos[1] - self.posAffiche[1]) / self.taille))

    def handleFKeys(self, event: pygame.event.Event):
        """Handles events where function keys are pressed

        Args:
            event (pygame.Event): The event to handle
        """
        if event.key == pygame.locals.K_F2:
            self.screenshot()
        elif event.key == pygame.locals.K_F11:
            self.rescale()
        elif event.key == pygame.locals.K_F3:
            self.showFPS = not self.showFPS

    def screenshot(self):
        """Make a screenshot and saves it as a bmp file"""
        pygame.image.save(self.fenetre, "screen/{}.bmp".format(time.strftime("%Y_%m_%d_%H_%M_%S")))

    def update(self):
        """Updates the time variables, and calculate FPS if necessary"""
        self.timeElapsed = time.time() - self.startTime
        self.startTime = time.time()
        self.FPS = 1 / self.timeElapsed

        if self.showFPS:
            self.fenetre.blit(self.font.render(str(round(self.FPS)), 1, (0, 0, 0)), (0, 0))
