import pygame as pg

from models.game_options import GameOptions
from UI.components.image_animation import ImageAnimation


class AnimatedSelectable:
    """An animated selectable image"""

    def __init__(
        self, position: tuple, name: str, size: tuple = (256, 256),
        initial_animation: str = "idle", selection_animation: str = "attack"
    ):
        self.animations: {str: ImageAnimation} = {}
        self.position: tuple = position
        self.current_animation: str = initial_animation
        self.initial_animation: str = initial_animation
        self.selection_animation: str = selection_animation
        self.selected: bool = False
        self.name: str = name
        self.size: tuple = size

        self.name_display: pg.Surface = None
        self._build()

    def _build(self):
        """Builds the name surface"""
        options = GameOptions.getInstance()
        self.name_display = options.fonts["MedievalSharp-xOZ5"]["20"].render(self.name, 1, (255, 255, 255))

    def _endSelectAnimation(self):
        """Callback for the selection animation to restart the initial one"""
        self.current_animation = self.initial_animation
        self.animations[self.selection_animation].reset()

    def addAnimation(
        self, animation_name: str, animation: ImageAnimation, is_initial: bool = False, is_selection: bool = False
    ):
        """Adds an animation to the executable

        Args:
            animation_name (str): The name of the new animation
            animation (ImageAnimation): The ImageAnimation
            is_initial (bool, optional): Whether to set the animation as initial. Defaults to False.
            is_selection (bool, optional): Whether to set the animation as selection animation. Defaults to False.
        """
        self.animations[animation_name] = animation
        self.animations[animation_name].play()
        if is_initial or animation_name == self.initial_animation:
            self.initial_animation = animation_name
        if is_selection or animation_name == self.selection_animation:
            self.selection_animation = animation_name
            self.animations[self.selection_animation].setCallback(self._endSelectAnimation)

    def update(self, timeElapsed):
        """Updates the selectable's animations"""
        self.animations[self.current_animation].update(timeElapsed)

    def draw(self, screen, offset: tuple = (0, 0)):
        """Draws the selectable on the screen"""
        position = tuple(map(lambda i, j: i + j, self.position, offset))
        self.animations[self.current_animation].draw(screen, position)
        if self.selected:
            pg.draw.rect(screen.fenetre, (255, 255, 255), pg.Rect(position, (256, 256)), width=2)
        screen.blit(
            self.name_display,
            (position[0] + 128 - self.name_display.get_size()[0]//2, position[1])
        )

    def select(self):
        """Sets the selectable as selected and plays the selection animation"""
        self.selected = True
        self.current_animation = self.selection_animation
        self.animations[self.current_animation].play()

    def unselect(self):
        """Sets the selectable as unselected"""
        self.selected = False

    def click(self, event_pos, offset: tuple = (0, 0)):
        """Returns true if the position overlap the selectable"""
        position = tuple(map(lambda i, j: i + j, self.position, offset))
        if position[0] < event_pos[0] < position[0] + self.size[0]:
            return position[1] < event_pos[1] < position[1] + self.size[1]
        return False
