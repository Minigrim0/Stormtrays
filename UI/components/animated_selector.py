import pygame as pg

from UI.components.animated_selectable import AnimatedSelectable
from UI.components.image_animation import ImageAnimation


class AnimatedSelector:
    """A list of animated selectable items"""

    def __init__(self, position, size, selectable_size: tuple = (256, 256)):
        self.elements: list(AnimatedSelectable) = []
        self.position = position
        self.size = size
        self.selectable_size = selectable_size

    @property
    def _selected(self) -> AnimatedSelectable:
        """Returns the selected AnimatedSelectable"""
        for element in self.elements:
            if element.selected:
                return element
        return None

    @property
    def selected_name(self) -> AnimatedSelectable:
        """Returns the name of the selected selectable"""
        for element in self.elements:
            if element.selected:
                return element.name
        return None

    def update(self, timeElapsed):
        """Updates the selectables"""
        for selectable in self.elements:
            selectable.update(timeElapsed)

    def draw(self, screen):
        """Draws the selector on the screen"""
        for selectable in self.elements:
            selectable.draw(screen, offset=self.position)

    def handleEvent(self, event):
        """Handles user events"""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            selected_element = self._selected
            for element in self.elements:
                if element != selected_element and element.click(event.pos, offset=self.position):
                    selected_element.unselect()
                    element.select()

    def addElement(self, name, animations: dict):
        """Adds a selectable to the selector"""
        position = (
            (len(self.elements) % 2) * self.selectable_size[0],
            (len(self.elements) // 2) * self.selectable_size[1]
        )
        selectable = AnimatedSelectable(position, name=name)
        for animation_name, animation in animations.items():
            image_animation = ImageAnimation(initial_data=animation, image_size=self.selectable_size)
            selectable.addAnimation(animation_name, image_animation)
            if len(self.elements) == 0:
                selectable.selected = True
        self.elements.append(selectable)
