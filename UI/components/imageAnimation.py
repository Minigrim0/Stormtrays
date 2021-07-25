import os
import glob
import json
import logging

import pygame as pg
from models.screen import Screen


class ImageAnimation:
    """An animation of images"""

    def __init__(self, folder_path: str = None, flippable: bool = False, callback: callable = None):
        self.images: list(pg.Surface) = []
        self.images_flipped: list(pg.Surface) = []

        self.flippable: bool = flippable
        self.flipped = False
        self.last_step: int = 0  # The time since last step

        self.step: int = 0
        self.playing: bool = True
        self.speed: int = 1  # 1 image par seconde
        self.trigger = callback

        if folder_path is not None:
            self.loadFolder(folder_path)

    def loadFolder(self, folder_path: str):
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
            if self.flippable:
                self.images_flipped.append(
                    pg.transform.flip(self.images[-1], False, True)
                )

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def reset(self):
        self.playing = False
        self.stop = 0

    def flip(self):
        if self.flippable:
            self.flipped = True

    def update(self, timeElapsed):
        self.last_step += timeElapsed
        if self.last_step > (1 / self.speed):
            if self.trigger is not None:
                self.trigger()
            self.last_step = 0
            self.step += 1
            self.step %= len(self.images)

    def draw(self, screen: Screen, position: tuple):
        if self.flipped:
            screen.blit(self.images_flipped[self.step], position)
        else:
            screen.blit(self.images[self.step], position)
