import logging
import tkinter
import coloredlogs

import pygame

import src.constantes as cst
from models.editor import Editor
from models.game_options import GameOptions
from models.screen import Screen

coloredlogs.install(level='WARNING')
logging.basicConfig(level=logging.WARNING)

pygame.init()

options = GameOptions.getInstance()

screen = Screen.getInstance(
    size=(cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT),
    name="Stormtray's Editor",
    icon="UI/assets/images/icon.png",
    fullscreen=False,
    resizable=False
)

root = tkinter.Tk()
root.withdraw()

editor = Editor()
editor()
