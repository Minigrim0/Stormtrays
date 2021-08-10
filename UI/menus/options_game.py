    # Menu_Principal d'Options dans menu pause
    while OptionsMenu:

        game.play_music()

        pygame.mixer.music.set_volume(Volume / 10)

        appuye = False

        Volumetxt = myfont3.render("Volume : %i" % int(Volume * 10), 1, (255, 50, 20))
        Diffictxt = myfont3.render("Difficulté : %i" % Difficulte, 1, (255, 50, 20))

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

        for event in screen.getEvent():

            if event.type == pygame.locals.MOUSEBUTTONDOWN:

                # Quitter le niveau en cours
                if quitOrect.collidepoint(event.pos):
                    OptionsMenu = False
                    pausemenu = True

                if VolPlus.collidepoint(event.pos) and Volume < 10:
                    Volume += 1

                if VolMoins.collidepoint(event.pos) and Volume > 0:
                    Volume -= 1

                if DifPlus.collidepoint(event.pos) and Difficulte < 10:
                    Difficulte += 1

                if DifMoins.collidepoint(event.pos) and Difficulte > 0:
                    Difficulte -= 1
