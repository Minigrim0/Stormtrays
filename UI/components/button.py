import pygame as pg


class Button:
    """A button that can be clicked and may induce a callback"""

    def __init__(
        self, pos: tuple, size: tuple, toggleable: bool = False,
        image: pg.Surface = None, enabled=True, callback: callable = None,
        **ckwargs
    ):
        self.pos = pos
        self.size = size
        self.image = image
        self.rect = pg.Rect(self.pos, self.size)
        self.callback: callable = callback
        self.ckwargs = ckwargs
        self.toggleable = toggleable
        self.toggled = False
        self.enabled = enabled
        if self.toggleable and len(self.image) == 1:
            raise RuntimeError("No second image available for toggleable button")

    @staticmethod
    def toPos(position: tuple, insize: tuple, outsize: tuple):
        """Tranforms the given position into a real position: eg. ("CENTER", "CENTER") becomes to int values"""
        final_position = []
        for axis, var in enumerate(position):
            if type(var) is int:
                final_position.append(var)
            elif type(var) is str:
                if var == "CENTER":
                    outlength = outsize[axis]
                    inlength = insize[axis]
                    final_position.append((outlength - inlength) // 2)
                if var == "TOP":
                    final_position.append(0)
                if var == "BOTTOM":
                    outlength = outsize[axis]
                    inlength = insize[axis]
                    final_position.append(outlength - inlength)

        return tuple(final_position)

    def build(
        self,
        text: str,
        font: pg.font.Font,
        text_position: tuple,
        background: pg.Surface = None,
        text_color: tuple = (0, 0, 0),
    ):
        """Builds the button with the given text"""
        if background is not None:
            self.image = background

        text = font.render(text, 1, text_color)
        self.image.blit(text, self.toPos(text_position, text.get_size(), self.image.get_size()))

    def setCallback(self, callback: callable, **ckwargs):
        """Sets the button callback with its parameters"""
        self.callback = callback
        self.ckwargs = ckwargs

    def draw(self, screen):
        """Draws the button on the screen"""
        if self.toggleable:
            screen.blit(self.image[self.toggled], self.pos)
        else:
            screen.blit(self.image, self.pos)

    def collide(self, pos: tuple):
        """Checks whether the position is colliding the button"""
        return self.rect.collidepoint(pos)

    def click(self, pos: tuple):
        """Execute the callback if the position collide the button"""
        if self.collide(pos) and self.callback is not None and self.enabled:
            self.callback(**self.ckwargs)
            if self.toggleable:
                self.toggled = not self.toggled

    def move(self, offset: tuple):
        """Moves a button by the given offset"""
        self.pos = tuple(self.pos[i] + offset[i] for i, _ in enumerate(self.pos))
        self.rect = self.rect.move(offset)
