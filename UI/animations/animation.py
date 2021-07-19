import json
import pygame as pg

from src.runnable import Runnable

from models.screen import Screen

from UI.animations.animated_element import Animated


class Animation(Runnable):
    """The button animation from main menu to levelSelection"""

    def __init__(self, animation: str, screen: Screen):
        super().__init__()
        self.screen: Screen = screen
        self.elements: list(Animated) = []
        self.totalTime = 1

        with open(animation) as animation:
            data = json.load(animation)
            self.load(data)

    def load(self, data: dict):
        self.duration = data["duration"]
        self.background = pg.image.load(data["background"])

        for elem in data["elements"]:
            self.elements.append(
                Animated(
                    pg.image.load(elem["image"]).convert_alpha(),
                    tuple(elem["from"]),
                    tuple(elem["to"]),
                    style=elem["style"],
                    duration=self.totalTime,
                )
            )

    def loop(self):
        self.draw()
        for animated in self.elements:
            animated.update(self.screen.timeElapsed)
            animated.draw(self.screen)
        self.totalTime -= self.screen.timeElapsed
        self.handleEvent()

        if self.totalTime <= 0:
            self.running = False

        self.screen.flip()

    def invert(self):
        for elem in self.elements:
            elem.invert()

    def handleEvent(self):
        self.screen.getEvent()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
