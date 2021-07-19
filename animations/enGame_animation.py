class EndGameAnimation:
    def __init__(self):
        while anim_Perdu:

            i += 5
            niveau.construit("../level/" + lvl + ".txt")
            niveau.affichem(screen)

            screen.blit(FondSombre, (0, 0))
            screen.blit(Fond_Menu_Opt, (1152 // 2 - 200, 704 // 2 - 200))
            screen.blit(Perdutxt, (1152 // 2 - 190, i - 20))
            screen.blit(quitpaus, (1152 // 2 - 60, 704 - i))
            screen.flip()

            screen.getEvent()

            if i >= 220:
                anim_Perdu = False
