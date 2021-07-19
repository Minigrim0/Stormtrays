class EndScreen(Menu, Runnable):
    def __init__(self):
        while Ecran_Perdu:

            screen.blit(Fond_Menu_Opt, (1152 // 2 - 200, 704 // 2 - 200))
            screen.blit(Perdutxt, (1152 // 2 - 190, 704 // 2 - 200))
            screen.blit(quitpaus, (1152 // 2 - 60, 704 // 2 + 35))
            screen.flip()

            for event in screen.getEvent():
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                    # Quitter le niveau en cours
                    if quitjrect.collidepoint(event.pos):
                        Ecran_Perdu = False
                        Menu_Selection = True
