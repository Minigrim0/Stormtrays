import pygame


class Button:
    def __init__(self, pos: tuple, size: tuple, image: pygame.Surface):
        self.pos = pos
        self.size = size
        self.image = image
        self.rect = pygame.Rect(self.pos, self.size)
        self.callback = None

    def draw(self, screen):
        """Draws the button on the screen

        Args:
            screen (Screen): The object to draw on
        """
        screen.blit(self.image, self.pos)

    def collide(self, pos: tuple):
        """Checks whether the position is colliding the button

        Args:
            pos (tuple): The position to test

        Returns:
            bool: whether the pos is colliding the button or not
        """
        return self.rect.collidepoint(pos)

    def click(self, pos: tuple):
        """Execute the callback if the position collide the button

        Args:
            pos (tuple): the position to click on
        """
        if self.collide(pos) and self.callback is not None:
            if type(self.callback) is tuple:
                self.callback[0](*self.callback[1:])
            else:
                self.callback()
