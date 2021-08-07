import pygame
import pygame.locals
import src.constantes as constantes

from models.stormtrays import Stormtrays

pygame.init()

stormtrays = Stormtrays.getInstance()
stormtrays.run()

# Images
Coin = pygame.image.load(constantes.Coin).convert_alpha()
menutour = pygame.image.load(constantes.mt).convert_alpha()
pause = pygame.image.load(constantes.pause).convert_alpha()
XpBar = pygame.image.load(constantes.XpBar).convert_alpha()
retour = pygame.image.load(constantes.retour).convert_alpha()
InvocBar = pygame.image.load(constantes.Invoc).convert_alpha()
reprise = pygame.image.load(constantes.reprise).convert_alpha()
Credits = pygame.image.load(constantes.Credits).convert_alpha()
Quadrille = pygame.image.load(constantes.carrea).convert_alpha()
accelere = pygame.image.load(constantes.accelere).convert_alpha()
quitpaus = pygame.image.load(constantes.quitpaus).convert_alpha()
Poubelle = pygame.image.load(constantes.poubelle[0]).convert_alpha()
FondSombre = pygame.image.load(constantes.sombre__).convert_alpha()
accelerex = pygame.image.load(constantes.accelerex).convert_alpha()
PauseTxt = pygame.image.load(constantes.PauseTxt__).convert_alpha()
optionpaus = pygame.image.load(constantes.optionpaus).convert_alpha()
OptionsTxt = pygame.image.load(constantes.OptionsTxt__).convert_alpha()
ConfirmQuit = pygame.image.load(constantes.ConfirmQuit).convert_alpha()
InfoLvl5Img = pygame.image.load(constantes.InfoLvl5Img).convert_alpha()
boutontour = pygame.image.load(constantes.boutonmenutour).convert_alpha()
TpsRestInvoc = pygame.image.load(constantes.TpsRestInvoc__).convert_alpha()
Fond_Menu_Opt = pygame.image.load(constantes.Fond_Menu_Opti).convert_alpha()
FondHautDroite = pygame.image.load(constantes.FondHautDroite).convert_alpha()
Fond_Noir_Semi_Transparent = pygame.image.load(constantes.sombre).convert_alpha()
TpsRestInvocSombre = pygame.image.load(constantes.TpsRestInvocSombre__).convert_alpha()

if True:

    if pausemenu:
        screen.blit(FondSombre, (0, 0))

    # Tant que Menu_Principal pause est actif
    while pausemenu:

        game.play_music()

        screen.blit(Fond_Menu_Opt, (1152 // 2 - 190, 704 // 2 - 210))
        screen.blit(PauseTxt, (1152 // 2 - 190, 704 // 2 - 210))
        screen.blit(reprise, (1152 // 2 - 60, 704 // 2 - 85))
        screen.blit(optionpaus, (1152 // 2 - 60, 704 // 2 - 25))
        screen.blit(quitpaus, (1152 // 2 - 60, 704 // 2 + 35))
        screen.flip()

        for event in screen.getEvent():

            if event.type == pygame.locals.KEYDOWN:
                # Quitter pausemenu
                if event.key == pygame.locals.K_ESCAPE:
                    pausemenu = False

            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                # Continuer le jeu
                if reprendrect.collidepoint(event.pos):
                    pausemenu = False
                # Aller vers OptionsMenu
                elif optionprect.collidepoint(event.pos):
                    pausemenu = False
                    OptionsMenu = True
                # Quitter le niveau en cours
                elif quitjrect.collidepoint(event.pos):
                    pausemenu = False
                    jeu = False
                    Menu_Selection = True

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
