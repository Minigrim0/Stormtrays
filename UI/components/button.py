import pygame


class Button:
    """A button that can be clicked and may induce a callback"""

    def __init__(self, pos: tuple, size: tuple, image: pygame.Surface = None):
        self.pos = pos
        self.size = size
        self.image = image
        self.rect = pygame.Rect(self.pos, self.size)
        self.callback: callable = None

    def draw(self, screen):
        """Draws the button on the screen"""
        screen.blit(self.image, self.pos)

    def collide(self, pos: tuple):
        """Checks whether the position is colliding the button"""
        return self.rect.collidepoint(pos)

    def click(self, pos: tuple):
        """Execute the callback if the position collide the button"""
        if self.collide(pos) and self.callback is not None:
            if type(self.callback) is tuple:
                self.callback[0](*self.callback[1:])
            else:
                self.callback()

    def move(self, offset: tuple):
        """Moves a button by the given offset"""
        self.pos = tuple(self.pos[i] + offset[i] for i, _ in enumerate(self.pos))
        self.rect = self.rect.move(offset)
