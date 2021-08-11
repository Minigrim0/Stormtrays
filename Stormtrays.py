import pygame

from models.stormtrays import Stormtrays

pygame.init()

stormtrays = Stormtrays.getInstance()
stormtrays.run()
