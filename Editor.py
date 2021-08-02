import pygame
import pygame.locals

import tkinter

import src.constantes as constantes

from models.screen import Screen
from models.editor import Editor
from models.game_options import GameOptions

pygame.init()

options = GameOptions.getInstance()

screen = Screen(
    (constantes.WINDOW_WIDTH + 158, constantes.WINDOW_HEIGHT),
    "Stormtray's Editor",
    "UI/assets/images/icon.png",
    False,
)

root = tkinter.Tk()
root.withdraw()

editor = Editor(screen)
editor()
