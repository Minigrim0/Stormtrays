import pygame as pg

from UI.components.image_animation import ImageAnimation


class AnimatedSelectable:
    """An animated selectable image"""

    def __init__(self, position: tuple, initial_animation: str = "idle", selection_animation: str = "attack"):
        self.animations: {str: ImageAnimation} = []
        self.position = position
        self.current_animation: str = initial_animation
        self.initial_animation: str = initial_animation
        self.selection_animation: str = selection_animation
        self.selected = False

    def _endSelectAnimation(self):
        self.current_animation = self.initial_animation

    def addAnimation(
        self, animation_name: str, animation: ImageAnimation, is_initial: bool = False, is_selection: bool = False
    ):
        self.animations[animation_name] = animation
        if is_initial:
            self.initial_animation = animation_name
        if is_selection:
            self.selection_animation = animation_name
            self.animations[self.selection_animation].setCallback(self._endSelectAnimation)

    def update(self, timeElapsed):
        """Updates the selectable's animations"""
        self.animations[self.current_animation].update(timeElapsed)

    def draw(self, screen):
        self.animations[self.current_animation].draw(screen, self.position)
        if self.selected:
            pg.draw.rect(screen, pg.Rect(self.position, (256, 256)))

    def select(self):
        self.selected = True
        self.current_animation = self.selection_animation

    def unselect(self):
        self.selected = False
