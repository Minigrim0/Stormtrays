import pygame
import pygame.locals

import tkinter
import sys

pygame.init()
sys.path.insert(0, "src/")

import classes
import constantes
from Screen import Screen


# init des bibliotheques
root = tkinter.Tk()
root.withdraw()

fenetre = Screen(
    (constantes.WINDOW_WIDTH+200, constantes.WINDOW_HEIGHT),
    "Stormtray's Editor",
    "../Img/Icon.png",
    False
)
from EditorUI import EditorUI

editorUI = EditorUI()

edit = 1
choix = "  "
rot = 0
niveau = classes.Niveau()

possouris = (0, 0)

while edit:

    niveau.afficheE(fenetre, editorUI.fond)
    editorUI.draw(fenetre)

    if editorUI.QGPos:
        fenetre.blit(editorUI.QGImg, (editorUI.QGPos))

    if choix != "  ":
        fenetre.blit(
            niveau.imgE[choix, rot],
            ((possouris[0]//64)*64, (possouris[1]//64)*64)
        )

    for v in editorUI.rect:
        fenetre.blit(
            niveau.imgE[v, 0], (editorUI.rect[v].x, editorUI.rect[v].y))

    for event in fenetre.GetEvent():
        if event.type == pygame.locals.QUIT:
            edit = 0

        possouris, rot, choix = editorUI.update(
            fenetre, event, niveau, choix, rot, possouris)

        if event.type == pygame.locals.MOUSEMOTION:
            possouris = (event.pos[0]-16, event.pos[1]-16)

            if event.buttons[0] == 1 and choix != "  ":
                x = event.pos[0]//64
                y = event.pos[1]//64
                if pygame.Rect((x*64, y*64), (64, 64)).collidepoint(event.pos):
                    if choix == "p1":
                        niveau.tableau[x, y] = "  ", 0
                    else:
                        niveau.tableau[x, y] = choix, rot

    fenetre.flip()
