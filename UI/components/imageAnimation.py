import os
import glob
import json
import logging

import pygame as pg
from models.screen import Screen


class ImageAnimation:
    """An animation of images"""

    def __init__(
        self, folder_path: str = None, flippable: bool = False,
        callback: callable = None, speed: int = 2, image_size: tuple = (-1, -1),
        loop: int = 1
    ):
        self.images: list(pg.Surface) = []
        self.images_flipped: list(pg.Surface) = []

        self.flippable: bool = flippable
        self.flipped = False
        self.last_step: int = 0  # The time since last step

        self.step: int = 0
        self.playing: bool = True
        self.speed: int = speed
        self.trigger = callback

        self.loop = loop  # -1 means infinite
        self.current_loop = 0

        if folder_path is not None:
            self.loadFolder(folder_path, image_size=image_size)

    def loadFolder(self, folder_path: str, image_size: tuple):
        """Loads an animation from a folder

        Args:
            folder_path (str): The path to the animation folder
        """
        setup_file = os.path.join(folder_path, "setup.json")
        if not os.path.exists(setup_file):
            logging.warning("No setup file found for {}, trying fuzzy load".format(folder_path))
            images_format = os.path.join(folder_path, "*.png")
        else:
            with open(setup_file) as setup_file:
                setup = json.load(setup_file)
            file_format = setup["format"]
            images_format = os.path.join(folder_path, file_format)

        for image in sorted(glob.glob(images_format)):
            self.images.append(
                pg.image.load(image).convert_alpha()
            )

            if image_size != (-1, -1):
                self.images[-1] = pg.transform.scale(self.images[-1], image_size)

            if self.flippable:
                self.images_flipped.append(
                    pg.transform.flip(self.images[-1], True, False)
                )

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def reset(self):
        self.playing = False
        self.step = 0

    def flip(self):
        if self.flippable:
            self.flipped = True

    def setDirection(self, right: bool):
        """Sets the direction of the animation"""
        self.flipped = not right

    def update(self, timeElapsed):
        """Updates the animation frame, time,..."""
        if self.playing():
            self.last_step += timeElapsed
            if self.last_step > (1 / self.speed):
                self._stepUp()

    def _stepUp(self):
        """Called at each animation step"""
        self.last_step = 0
        self.step += 1
        if self.step == len(self.images):
            self._endLoop()

    def _endLoop(self):
        """Bit of code executed at each loop's end"""
        if self.trigger is not None:
            self.trigger()
        self.current_loop += 1
        self.step %= len(self.images)
        if self.current_loop > self.loop and self.loop > 0:
            self.pause()

    def currentFrame(self):
        """Returns the animation's current frame"""
        if self.flipped:
            return self.images_flipped[self.step]
        else:
            return self.images[self.step]

    def draw(self, screen: Screen, position: tuple, centered: bool = False):
        """Draws the current frame on the screen, at the given position"""
        # pg.draw.rect(self.currentFrame(), (255, 0, 0), pg.Rect((0, 0), self.currentFrame().get_size()), width=2)
        if centered:
            size = self.currentFrame().get_size()
            position = (position[0] - (size[0] // 2), position[1] - (size[1] // 2))
        screen.blit(self.currentFrame(), position)
