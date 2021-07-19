import pygame


class Button:
    """A button that can be clicked and may induce a callback"""

    def __init__(self, pos: tuple, size: tuple, image: pygame.Surface = None, callback: callable = None, *cargs, **ckwargs):
        self.pos = pos
        self.size = size
        self.image = image
        self.rect = pygame.Rect(self.pos, self.size)
        self.callback: callable = callback
        self.cargs = cargs
        self.ckwargs = ckwargs

    def setCallaback(self, callback: callable, *cargs, **ckwargs):
        self.callback = callback
        self.cargs = cargs
        self.ckwargs = ckwargs

    def draw(self, screen):
        """Draws the button on the screen"""
        screen.blit(self.image, self.pos)

    def collide(self, pos: tuple):
        """Checks whether the position is colliding the button"""
        return self.rect.collidepoint(pos)

    def click(self, pos: tuple):
        """Execute the callback if the position collide the button"""
        if self.collide(pos) and self.callback is not None:
            self.callback(*self.cargs, **self.ckwargs)

    def move(self, offset: tuple):
        """Moves a button by the given offset"""
        self.pos = tuple(self.pos[i] + offset[i] for i, _ in enumerate(self.pos))
        self.rect = self.rect.move(offset)
