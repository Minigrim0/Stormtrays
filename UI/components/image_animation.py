import glob
import json
import logging
import os

import pygame as pg

from models.image_bank import ImageBank
from models.screen import Screen


class ImageAnimation:
    """An animation of images"""

    def __init__(
        self, folder_path: str = None, flippable: bool = False,
        callback: callable = None, speed: int = 2, image_size: tuple = (-1, -1),
        loop: int = 1, bank_name: str = None,
        callback_on: list = [-1]
    ):
        self.images: list(pg.Surface) = []
        self.images_flipped: list(pg.Surface) = []

        self.original_image: pg.Surface = None
        self.flipped_original_image: pg.Surface = None

        self.flippable: bool = flippable
        self.flipped = False
        self.last_step: int = 0  # The time since last step

        self.step: int = 0
        self.playing: bool = False
        self.speed: int = speed
        self.trigger = callback

        self.loop = loop  # -1 means infinite
        self.current_loop = 0

        self.multipart = False

        self.callback_on = callback_on  # When to call the callback

        bank = ImageBank.getInstance()
        if (bank_name is None or not bank.exists(bank_name)) and folder_path is not None:
            self.loadFolder(folder_path, image_size=image_size)
            if bank_name is not None:
                bank.set(
                    bank_name,
                    (
                        self.images, self.images_flipped, self.multipart,
                        self.original_image, self.flipped_original_image
                    )
                )
        elif bank_name is not None and bank.exists(bank_name):
            self.images, self.images_flipped, self.multipart, self.original_image, self.flipped_original_image = bank[
                bank_name
            ]

    def _loadMultipart(self, setup: dict, folder_path: str, image_size: tuple = (-1, -1)):
        """Loads an animation from a single """
        cut_size = tuple(setup["size"])
        self.original_image = pg.image.load(os.path.join(folder_path, setup["file"])).convert_alpha()

        if image_size != (-1, -1):
            self.original_image = pg.transform.scale(
                self.original_image,
                (
                    cut_size[0] * image_size[0],
                    cut_size[1] * image_size[1]
                )
            )
        self.flipped_original_image = pg.transform.flip(self.original_image, True, False)
        rect_size = (
            self.original_image.get_size()[0] / cut_size[0],
            self.original_image.get_size()[1] / cut_size[1]
        )
        for y in range(cut_size[1]):
            for x in range(cut_size[0]):
                self.images.append(
                    pg.Rect((x * rect_size[0], y * rect_size[1]), rect_size)
                )
                if self.flippable:
                    self.images_flipped.append(
                        pg.Rect(
                            (self.original_image.get_size()[0] - rect_size[0] - (x * rect_size[0]), y * rect_size[1]),
                            rect_size
                        )
                    )

    def _loadFormat(self, image_format: str, image_size: tuple = (-1, -1)):
        """Loads images in a folder following a certain format (Ex: *.png)"""
        for image in sorted(glob.glob(image_format)):
            self.images.append(
                pg.image.load(image).convert_alpha()
            )

            if image_size != (-1, -1):
                self.images[-1] = pg.transform.scale(self.images[-1], image_size)

            if self.flippable:
                self.images_flipped.append(
                    pg.transform.flip(self.images[-1], True, False)
                )

    def loadFolder(self, folder_path: str, image_size: tuple):
        """Loads an animation from a folder

        Args:
            folder_path (str): The path to the animation folder
        """
        setup_file = os.path.join(folder_path, "setup.json")
        if not os.path.exists(setup_file):
            logging.warning("No setup file found for {}, trying fuzzy load".format(folder_path))
            images_format = os.path.join(folder_path, "*.png")
            self._loadFormat(images_format, image_size=image_size)
        else:
            with open(setup_file) as setup_file:
                setup = json.load(setup_file)
            self.multipart = setup["multipart"]
            if self.multipart is True:
                self._loadMultipart(setup, folder_path, image_size=image_size)
            else:
                images_format = os.path.join(folder_path, setup["format"])
                self._loadFormat(images_format, image_size=image_size)

    def play(self):
        """Sets the animation state to playing"""
        self.playing = True

    def pause(self):
        """Pauses the animation"""
        self.playing = False

    def reset(self):
        """Resets the animation"""
        self.playing = False
        self.step = 0
        self.current_loop = 0

    def flip(self):
        """Flips the animation in the y axis"""
        if self.flippable:
            self.flipped = True

    def setDirection(self, right: bool):
        """Sets the direction of the animation"""
        self.flipped = not right

    def update(self, timeElapsed):
        """Updates the animation frame, time,..."""
        if self.playing:
            self.last_step += timeElapsed
            if self.last_step > (1 / self.speed):
                self._stepUp()

    def _stepUp(self):
        """Called at each animation step"""
        self.last_step = 0
        self.step += 1
        if self.step in self.callback_on:
            self.trigger()
        if self.step == len(self.images):
            if -1 in self.callback_on and self.trigger is not None:
                self.trigger()
            self._endLoop()

    def _endLoop(self):
        """Bit of code executed at each loop's end"""
        self.current_loop += 1
        self.step %= len(self.images)
        if self.current_loop >= self.loop and self.loop > 0:
            self.reset()

    def currentFrame(self):
        """Returns the animation's current frame"""
        if self.flipped:
            return self.images_flipped[self.step]
        else:
            return self.images[self.step]

    def draw(self, screen: Screen, position: tuple, centered: bool = False):
        """Draws the current frame on the screen, at the given position"""
        if self.multipart:
            if centered:
                size = self.currentFrame()
                position = (position[0] - (size.w // 2), position[1] - (size.h // 2))
            if self.flipped:
                screen.blit(self.flipped_original_image, position, area=self.currentFrame())
            else:
                screen.blit(self.original_image, position, area=self.currentFrame())
        else:
            if centered:
                size = self.currentFrame().get_size()
                position = (position[0] - (size[0] // 2), position[1] - (size[1] // 2))
            screen.blit(self.currentFrame(), position)
