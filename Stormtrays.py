import logging

import coloredlogs
import pygame

from models.stormtrays import Stormtrays

coloredlogs.install(level='WARNING')

logging.info("Initializing pygame")
pygame.init()

logging.info("launching game")
stormtrays = Stormtrays.getInstance()
stormtrays.run()
