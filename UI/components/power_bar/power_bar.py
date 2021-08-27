import logging

import pygame as pg

from UI.components.power_bar.box import Box


class PowerBar:
    """The character's power bar"""

    def __init__(
        self, position: tuple = ("CENTERED", "BOTTOM"), rows: int = 1, columns: int = 5,
        box_size: int = 32
    ):
        self.box_size = box_size
        self.columns = columns
        self.rows = rows
        self.boxes: [Box] = []

        self.image: pg.Surface = None
        self._build()

    def _build(self):
        """Builds the UI of the Power Bar"""
        total_size = (
            self.box_size * self.columns,
            self.box_size * self.rows
        )
        self.image = pg.Surface(total_size, pg.SRCALPHA)
        self.image.fill((0, 0, 0, 128))
        for row in range(self.rows):
            for column in range(self.columns):
                pg.draw.rect(
                    self.image, (255, 255, 255),
                    pg.Rect(
                        (column * self.box_size, row * self.box_size),
                        (self.box_size, self.box_size)
                    ),
                    width=1
                )

    def addBox(self, icon: pg.Surface, name: str, cooldown: int, callback: callable, **ckwargs):
        logging.info(f"Adding '{name}' to power bar")
        self.boxes.append(
            Box(icon, self.box_size, cooldown, callback, **ckwargs)
        )

    def draw(self, screen):
        screen.blit(self.image, self.position)
        for index, box in enumerate(self.boxes):
            box.draw(
                screen, (self.position[0] + (self.box_size * index), self.position[1])
            )

    def update(self, elapsed_time: float):
        for box in self.boxes:
            box.update(elapsed_time)

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_1:
            self.boxes[0].trigger()
