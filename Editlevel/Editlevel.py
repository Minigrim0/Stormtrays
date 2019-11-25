import pygame
import pygame.locals
import constantes
import classes
import tkinter
from tkinter import filedialog
import os

# init des bibliotheques
pygame.init()
root = tkinter.Tk()
root.withdraw()

fenetre = pygame.display.set_mode(
    (constantes.largeur_jeu+200, constantes.hauteur_jeu))

rectangle = pygame.Surface((200, constantes.hauteur_jeu))
rectangle.fill((189, 83, 64))

lignevert = pygame.Surface((1, constantes.hauteur_jeu))
lignevert.fill((0, 0, 0))

lignehor = pygame.Surface(
    (constantes.largeur_jeu, 1))
lignehor.fill((0, 0, 0))

rect = {}
rect["c1"] = pygame.Rect((constantes.largeur_jeu + 12, 10), (64, 64))
rect["t2"] = pygame.Rect((constantes.largeur_jeu + 100, 10), (64, 64))
rect["t1"] = pygame.Rect((constantes.largeur_jeu + 12, 84), (64, 64))
rect["x1"] = pygame.Rect((constantes.largeur_jeu + 100, 84), (64, 64))
rect["p1"] = pygame.Rect((constantes.largeur_jeu + 12, 154), (64, 64))
rect["v1"] = pygame.Rect((constantes.largeur_jeu + 100, 154), (64, 64))
rect["k1"] = pygame.Rect((constantes.largeur_jeu + 12, 218), (3*64, 64))
rect["QG"] = pygame.Rect((constantes.largeur_jeu + 12, 282), (64, 64))

FondCrect = pygame.Rect(
    (constantes.largeur_jeu + 10, constantes.hauteur_jeu - 100),
    (72, 44))
effacerect = pygame.Rect(
    (constantes.largeur_jeu + 10, constantes.hauteur_jeu - 40),
    (80, 30))
sauverect = pygame.Rect(
    (constantes.largeur_jeu + 100, constantes.hauteur_jeu - 40), (40, 40))
chargerect = pygame.Rect(
    (constantes.largeur_jeu + 150, constantes.hauteur_jeu - 40), (40, 40))

MicroFond = pygame.image.load(constantes.Mini_Fond).convert_alpha()
fond = pygame.image.load(constantes.fond).convert_alpha()
efface = pygame.image.load(constantes.efface).convert_alpha()
sauve = pygame.image.load(constantes.sauve).convert_alpha()
ouvre = pygame.image.load(constantes.ouvrir).convert_alpha()
QGImg = pygame.image.load("../Img/QuestGiverF1.png").convert_alpha()

fenetre.blit(fond, (0, 0))

Titre_Fenetre = "Sans Titre"
edit = 1
choix = "  "
QGPos = (0, 0)
rot = 0
niveau = classes.Niveau()

possouris = (0, 0)

while edit:

    pygame.display.set_caption(Titre_Fenetre)
    pygame.display.flip()
    niveau.afficheE(fenetre, fond)
    for i in range(1, constantes.tabx):
        fenetre.blit(lignevert, (i*64, 0))
        fenetre.blit(lignehor, (0, i*64))
    fenetre.blit(rectangle, (constantes.largeur_jeu, 0))
    fenetre.blit(efface, (effacerect.x, effacerect.y))
    fenetre.blit(sauve, (sauverect.x,   sauverect.y))
    fenetre.blit(ouvre, (chargerect.x, chargerect.y))
    fenetre.blit(MicroFond, (FondCrect.x,   FondCrect.y))
    if QGPos:
        fenetre.blit(QGImg, (QGPos))

    if choix != "  ":
        fenetre.blit(niveau.imgE[choix, rot], possouris)

    for v in rect:
        fenetre.blit(niveau.imgE[v, 0], (rect[v].x, rect[v].y))

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            edit = 0

        if event.type == pygame.locals.MOUSEBUTTONDOWN:

            for v in rect:
                if rect[v].collidepoint(event.pos):
                    choix = v
                    rot = 0

            if effacerect.collidepoint(event.pos):
                niveau.videtab()
                choix = "  "

            if FondCrect.collidepoint(event.pos):
                filename = filedialog.askopenfilename(
                    initialdir="../Img/Fonds", defaultextension=".png")
                if filename:
                    fond_Edit = os.path.relpath(filename)
                    fond = pygame.image.load(fond_Edit).convert_alpha()
                choix = "  "

            if chargerect.collidepoint(event.pos):
                filename = filedialog.askopenfilename(
                    initialdir="../level", defaultextension=".txt")
                if filename:
                    niveau.construit(filename)
                choix = "  "
                Titre_Fenetre = filename

            if sauverect.collidepoint(event.pos):
                filename = filedialog.asksaveasfilename(
                    initialdir="../level", defaultextension=".txt")
                if filename:
                    niveau.sauve(filename)
                    niveau.sauveF(filename, fond_Edit, QGPos)
                    i = 0
                    while i < 25:
                        niveau.affiche(fenetre, fond)
                        pygame.display.flip()
                        i += 1
                    i = 0
                    arect = pygame.Rect(
                        0, 0, constantes.largeur_jeu, constantes.hauteur_jeu)
                    sub = fenetre.subsurface(arect)
                    sub = pygame.transform.scale(sub, (39*5, 22*5))
                    dirname, filename = os.path.split(filename)
                    filename, ext = os.path.splitext(filename)
                    pygame.image.save(
                        sub, os.path.join(
                            dirname, "mininiveau", filename+".png"
                        )
                    )
                choix = "  "

            if event.button == 1 and choix != "  ":
                for x in range(18):
                    for y in range(11):
                        if pygame.Rect((x*64, y*64), (64, 64)).collidepoint(event.pos):
                            if choix == "p1":
                                niveau.tableau[x, y] = "  ", 0
                            elif choix == "QG":
                                QGPos = (x*64, y*64)
                            else:
                                niveau.tableau[x, y] = choix, rot

            if event.button == 3 and choix != "  ":
                rot = (rot + 90) % 360

        if event.type == pygame.locals.MOUSEMOTION:
            possouris = (event.pos[0]-16, event.pos[1]-16)
            if event.buttons[0] == 1 and choix != "  ":
                for x in range(18):
                    for y in range(22):
                        if pygame.Rect((x*64, y*64), (64, 64)).collidepoint(event.pos):
                            if choix == "p1":
                                niveau.tableau[x, y] = "  ", 0
                            else:
                                niveau.tableau[x, y] = choix, rot
