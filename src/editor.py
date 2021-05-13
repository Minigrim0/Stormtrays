import pygame

from src.editorUI import EditorUI
from src.screen import Screen
from src.classes import Niveau


class Editor:
    def __init__(self):
        self.UI = EditorUI()

        self.running = True

        self.choix = "  "
        self.rot = 0
        self.niveau = Niveau()
        self.possouris = (0, 0)

    def run(self, screen: Screen):
        while self.running:
            self.draw(screen)

            for event in screen.getEvent():
                self.handleEvent(screen, event)

    def handleEvent(self, screen: Screen, event: pygame.event.Event):
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            self.possouris, self.rot, self.choix = self.UI.update(
                screen, event, self.niveau, self.choix, self.rot, self.possouris)

        if event.type == pygame.locals.MOUSEMOTION:
            self.possouris = (event.pos[0]-16, event.pos[1]-16)

            if event.buttons[0] == 1 and self.choix != "  ":
                x = event.pos[0]//64
                y = event.pos[1]//64
                if pygame.Rect((x*64, y*64), (64, 64)).collidepoint(event.pos):
                    if self.choix == "p1":
                        self.niveau.tableau[x, y] = "  ", 0
                    else:
                        self.niveau.tableau[x, y] = self.choix, self.rot

    def draw(self, screen):
        self.niveau.afficheE(screen, self.UI.fond)
        self.UI.draw(screen)

        if self.UI.QGPos:
            screen.blit(self.UI.QGImg, (self.UI.QGPos))

        if self.choix != "  ":
            screen.blit(
                self.niveau.imgE[self.choix, self.rot],
                ((self.possouris[0]//64)*64, (self.possouris[1]//64)*64)
            )

        for v in self.UI.rect:
            screen.blit(
                self.niveau.imgE[v, 0], (self.UI.rect[v].x, self.UI.rect[v].y))

        screen.flip()

    def erase(self):
        pass
