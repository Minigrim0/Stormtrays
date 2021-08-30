import logging

import pygame

from models.stormtrays import Stormtrays

logging.basicConfig(level=logging.INFO)

logging.info("Initializing pygame")
pygame.init()

logging.info("launching game")
stormtrays = Stormtrays.getInstance()
stormtrays.run()
