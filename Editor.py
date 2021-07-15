import pygame
import pygame.locals

import tkinter

import src.constantes as constantes

from models.screen import Screen
from models.editor import Editor

pygame.init()

screen = Screen((constantes.WINDOW_WIDTH + 158, constantes.WINDOW_HEIGHT), "Stormtray's Editor", "img/Icon.png", False)

root = tkinter.Tk()
root.withdraw()

editor = Editor()

editor.run(screen)
