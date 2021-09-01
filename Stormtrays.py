import logging

import pygame

from models.stormtrays import Stormtrays

logging.basicConfig(level=logging.WARNING)

logging.info("Initializing pygame")
pygame.init()

logging.info("launching game")
stormtrays = Stormtrays.getInstance()
stormtrays.run()
