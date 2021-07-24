import os
import glob
import json
import logging

import pygame as pg
from models.screen import Screen


class ImageAnimation:
    def __init__(self, position: tuple, flippable: bool = False):
        self.images: list(pg.Surface) = []
        self.images_flipped: list(pg.Surface) = []

        self.position: tuple = position

        self.flippable: bool = flippable
        self.flipped = False
        self.last_step: int = None  # The time since last step

        self.step: int = 0
        self.playing: bool = True
        self.spleed: int = 1  # 1 image par seconde

    def loadFolder(self, folder_path: str):
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
            self.last_step = 0
            self.step += 1
            self.step %= len(self.images)

    def draw(self, screen: Screen):
        if self.flipped:
            screen.blit(self.images_flipped, self.position)
        else:
            screen.blit(self.images, self.position)
