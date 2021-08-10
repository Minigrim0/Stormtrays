import time

import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION

from models.game_options import GameOptions


class Screen:
    """The singleton class that handles the screen related actions"""

    instance = None

    @staticmethod
    def getInstance(*args, **kwargs):
        """Returns the model's instance, creating it if needed"""
        if Screen.instance is None:
            Screen(*args, **kwargs)
        return Screen.instance

    def __init__(self, size: tuple, name: str, icon: str, fullScreen=True):
        if Screen.instance is not None:
            raise RuntimeError("Trying to instanciate another instance of a singleton")
        Screen.instance = self

        self.initial_size = size

        info = pygame.display.Info()
        self.fullSize = (info.current_w, info.current_h)
        self.screen = None

        self.fullScreen = fullScreen
        if self.fullScreen:
            self.resize(self.fullSize)
        else:
            self.resize(self.initial_size)

        from UI.components.button import Button  # NOQA

        self.scaleButton = Button(
            (2, self.initial_size[1] - 22), (20, 20),
            image=pygame.image.load("UI/assets/images/scale.png").convert_alpha()
        )
        self.scaleButton.callback = self.rescale

        self.fenetre = pygame.Surface(self.initial_size)

        pygame.display.set_caption(name)
        if icon is not None and icon != "":
            pygame.display.set_icon(pygame.image.load(icon).convert_alpha())

        self.time_elapsed = 0
        self.startTime = time.time()

        self.FPS = 0
        self.showFPS = False

    @property
    def elapsed_time(self):
        options = GameOptions.getInstance()
        return self.time_elapsed * options.game_speed

    def rescale(self):
        """Resizes the screen to either fullscreen or native size"""
        self.fullScreen = not self.fullScreen
        if self.fullScreen:
            self.resize(self.fullSize)
        else:
            self.resize(self.initial_size)

    def resize(self, size: tuple):
        """Resizes the screen to the given size

        Args:
            size (tuple): the new size for the screen
        """
        if self.fullScreen:
            self.screen = pygame.display.set_mode(self.fullSize, pygame.locals.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size, pygame.locals.RESIZABLE)

        taillex = size[0] / self.initial_size[0]
        tailley = size[1] / self.initial_size[1]
        self.taille = min(taillex, tailley)

        self.posAffiche = (
            (size[0] - int(self.taille * self.initial_size[0])) // 2,
            (size[1] - int(self.taille * self.initial_size[1])) // 2,
        )

    def flip(self):
        """Refreshes the screen"""
        self.update()
        self.scaleButton.draw(self)
        self.screen.blit(
            pygame.transform.scale(
                self.fenetre, (int(self.initial_size[0] * self.taille), int(self.initial_size[1] * self.taille))
            ),
            self.posAffiche,
        )
        pygame.display.flip()

    def blit(self, surface: pygame.Surface, pos: tuple, *args, **kwargs):
        """Draws an image to the screen"""
        self.fenetre.blit(surface, pos, *args, **kwargs)

    def getEvent(self):
        """Handles user events, reacting of needed, and yielding
            the event list to the calling function

        Yields:
            pygame.event: The event list
        """
        for event in pygame.event.get():
            if event.type in (MOUSEMOTION, MOUSEBUTTONDOWN):
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

    def get_size(self):
        return self.initial_size

    def isPosOutOfScreen(self, pos: tuple):
        """Checks whether the position is out of the rendered screen or not"""
        return pos[0] < 0 or pos[1] < 0 or pos[0] >= self.initial_size[0] or pos[1] >= self.initial_size[1]

    def convertToRelativePos(self, pos: tuple):
        """Converts an real position to a relative position"""
        return (int((pos[0] - self.posAffiche[0]) / self.taille), int((pos[1] - self.posAffiche[1]) / self.taille))

    def subsurface(self, rect: pygame.Rect):
        """Returns a subsurface of the screen"""
        return self.fenetre.subsurface(rect)

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
        self.time_elapsed = time.time() - self.startTime
        self.startTime = time.time()
        self.FPS = 1 / self.time_elapsed

        if self.showFPS:
            font = GameOptions.getInstance().fonts["MedievalSharp-xOZ5"]["14"]
            self.fenetre.blit(font.render(str(round(self.FPS)), 0, (0, 0, 0)), (0, 0))
