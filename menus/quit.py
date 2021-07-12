from menus.menu import Menu
from src.runnable import Runnable

from src.button import Button


class QuitMenu(Menu, Runnable):

    def __init__(self, screen):
        super().__init__(self, screen)

        self.buttons.append(Button((516, 297), (120, 50), reprise))
        self.buttons.append(Button((516, 367), (120, 50), quitpaus))

    def loop(self):
        self.draw()
        self.handleEvent()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(ConfirmQuit, (376, 152))
        super().draw()

        self.screen.flip()

    def handleEvent():
        for event in screen.getEvent():
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                self.running = False

            if event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 1:
                if ConfirmReprise.collidepoint(event.pos):
                    Confirm_Quit = False
                    Menu_Principal = True

                elif ConfirmQuitter.collidepoint(event.pos):
                    Confirm_Quit = False
                    Programme_Actif = False

    def cancel(self):
        self.running = False

    def confirm(self):
        self.running = False
        # TODO: Trouver un moyen de quitter le jeu completement