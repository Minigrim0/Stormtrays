class OptionMenu(Menu, Runnable):
    """The menu of options"""

    def __init__(self):
        if Menu_Options:
        screen.blit(FondSombre, (0, 0))

    def loop(self):
        pass

    def draw(self):
        # Affiche les éléments du menu
        screen.blit(Fond_Menu_Principal, (0, 0))

        Volumetxt = myfont3.render("Volume : {}".format(int(Volume * 10)), 1, (255, 50, 20))
        Diffictxt = myfont3.render("Difficulté : {}".format(Difficulte), 1, (255, 50, 20))

        screen.blit(Fond_Menu_Opt, (386, 142))
        screen.blit(OptionsTxt, (386, 132))
        screen.blit(Volumetxt, (410, 302))
        screen.blit(Diffictxt, (410, 347))
        screen.blit(Moins, (655, 302))
        screen.blit(Plus, (705, 302))
        screen.blit(Moins, (655, 347))
        screen.blit(Plus, (705, 347))
        screen.blit(quitpaus, (516, 407))
        screen.flip()

    def handleEvent(self):
        """Handles pygame events and yields it to the calling method"""
        for event in super().handleEvent():
            if event.type == pygame.locals.MOUSEBUTTONDOWN:

                # quitter le niveau en cours
                if quitOrect.collidepoint(event.pos):
                    Menu_Principal = True
                    Menu_Options = False
                    break

                if VolPlus.collidepoint(event.pos) and Volume < 10:
                    Volume += 1

                if VolMoins.collidepoint(event.pos) and Volume > 0:
                    Volume -= 1

                if DifPlus.collidepoint(event.pos) and Difficulte < 10:
                    Difficulte += 1

                if DifMoins.collidepoint(event.pos) and Difficulte > 0:
                    Difficulte -= 1

    def updateVolume(self, value):
