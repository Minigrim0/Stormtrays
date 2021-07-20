import pygame
import pygame.locals
import glob
import src.constantes as constantes
from src.perso import Perso

from models.level import Level
from models.stormtrays import Stormtrays

pygame.init()

stormtrays = Stormtrays.getInstance()
stormtrays.run()

# Images
Coin = pygame.image.load(constantes.Coin).convert_alpha()
menutour = pygame.image.load(constantes.mt).convert_alpha()
pause = pygame.image.load(constantes.pause).convert_alpha()
Plus = pygame.image.load(constantes.Plus__).convert_alpha()
XpBar = pygame.image.load(constantes.XpBar).convert_alpha()
retour = pygame.image.load(constantes.retour).convert_alpha()
Moins = pygame.image.load(constantes.Moins__).convert_alpha()
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

# ------------------------------------------------------------------

InvoqueAnim1 = pygame.image.load(constantes.invoque_anim_1).convert_alpha()
InvoqueAnim2 = pygame.image.load(constantes.invoque_anim_2).convert_alpha()
InvoqueAnim3 = pygame.image.load(constantes.invoque_anim_3).convert_alpha()
InvoqueAnim4 = pygame.image.load(constantes.invoque_anim_4).convert_alpha()
InvoqueAnim5 = pygame.image.load(constantes.invoque_anim_5).convert_alpha()
InvoqueAnim6 = pygame.image.load(constantes.invoque_anim_6).convert_alpha()
InvoqueAnim7 = pygame.image.load(constantes.invoque_anim_7).convert_alpha()
InvoqueAnim8 = pygame.image.load(constantes.invoque_anim_8).convert_alpha()
InvoqueAnim9 = pygame.image.load(constantes.invoque_anim_9).convert_alpha()
InvoqueAnim10 = pygame.image.load(constantes.invoque_anim_10).convert_alpha()
InvoqueAnim11 = pygame.image.load(constantes.invoque_anim_11).convert_alpha()
InvoqueAnim12 = pygame.image.load(constantes.invoque_anim_12).convert_alpha()
InvoqueAnim13 = pygame.image.load(constantes.invoque_anim_13).convert_alpha()
InvoqueAnim14 = pygame.image.load(constantes.invoque_anim_14).convert_alpha()

# ------------------------------------------------------------------

Invocation1 = pygame.image.load(constantes.Invocation_1).convert_alpha()
Invocation2 = pygame.image.load(constantes.Invocation_2).convert_alpha()
Invocation3 = pygame.image.load(constantes.Invocation_3).convert_alpha()
Invocation4 = pygame.image.load(constantes.Invocation_4).convert_alpha()
Invocation5 = pygame.image.load(constantes.Invocation_5).convert_alpha()
Invocation6 = pygame.image.load(constantes.Invocation_6).convert_alpha()

InvocationRet1 = pygame.image.load(constantes.Invocation_1Ret).convert_alpha()
InvocationRet2 = pygame.image.load(constantes.Invocation_2Ret).convert_alpha()
InvocationRet3 = pygame.image.load(constantes.Invocation_3Ret).convert_alpha()
InvocationRet4 = pygame.image.load(constantes.Invocation_4Ret).convert_alpha()
InvocationRet5 = pygame.image.load(constantes.Invocation_5Ret).convert_alpha()
InvocationRet6 = pygame.image.load(constantes.Invocation_6Ret).convert_alpha()

# ------------------------------------------------------------------

Catapulte1 = pygame.image.load(constantes.Catapulte_1).convert_alpha()
Catapulte2 = pygame.image.load(constantes.Catapulte_2).convert_alpha()
Catapulte3 = pygame.image.load(constantes.Catapulte_3).convert_alpha()
Catapulte4 = pygame.image.load(constantes.Catapulte_4).convert_alpha()
Catapulte5 = pygame.image.load(constantes.Catapulte_5).convert_alpha()
Catapulte6 = pygame.image.load(constantes.Catapulte_6).convert_alpha()

# ------------------------------------------------------------------

Tab_AnimLvlUp = {}
Tab_AnimLvlUp[0] = pygame.image.load(constantes.AnimLvlUp01).convert_alpha()
Tab_AnimLvlUp[1] = pygame.image.load(constantes.AnimLvlUp02).convert_alpha()
Tab_AnimLvlUp[2] = pygame.image.load(constantes.AnimLvlUp03).convert_alpha()
Tab_AnimLvlUp[3] = pygame.image.load(constantes.AnimLvlUp04).convert_alpha()
Tab_AnimLvlUp[4] = pygame.image.load(constantes.AnimLvlUp05).convert_alpha()
Tab_AnimLvlUp[5] = pygame.image.load(constantes.AnimLvlUp06).convert_alpha()
Tab_AnimLvlUp[6] = pygame.image.load(constantes.AnimLvlUp07).convert_alpha()
Tab_AnimLvlUp[7] = pygame.image.load(constantes.AnimLvlUp08).convert_alpha()
Tab_AnimLvlUp[8] = pygame.image.load(constantes.AnimLvlUp09).convert_alpha()
Tab_AnimLvlUp[9] = pygame.image.load(constantes.AnimLvlUp10).convert_alpha()

# ------------------------------------------------------------------

Fond_Menu_Principal = pygame.image.load(constantes.fondm).convert_alpha()

# ------------------------------------------------------------------

Invocation_1 = pygame.transform.scale(Invocation1, (96, 96))
Invocation_2 = pygame.transform.scale(Invocation2, (96, 96))
Invocation_3 = pygame.transform.scale(Invocation3, (96, 96))
Invocation_4 = pygame.transform.scale(Invocation4, (96, 96))
Invocation_5 = pygame.transform.scale(Invocation5, (96, 96))
Invocation_6 = pygame.transform.scale(Invocation6, (96, 96))

Invocation_1_ret = pygame.transform.scale(InvocationRet1, (96, 96))
Invocation_2_ret = pygame.transform.scale(InvocationRet2, (96, 96))
Invocation_3_ret = pygame.transform.scale(InvocationRet3, (96, 96))
Invocation_4_ret = pygame.transform.scale(InvocationRet4, (96, 96))
Invocation_5_ret = pygame.transform.scale(InvocationRet5, (96, 96))
Invocation_6_ret = pygame.transform.scale(InvocationRet6, (96, 96))

# ------------------------------------------------------------------

Catapulte_1 = pygame.transform.scale(Catapulte1, (64, 64))
Catapulte_2 = pygame.transform.scale(Catapulte2, (64, 64))
Catapulte_3 = pygame.transform.scale(Catapulte3, (64, 64))
Catapulte_4 = pygame.transform.scale(Catapulte4, (64, 64))
Catapulte_5 = pygame.transform.scale(Catapulte5, (64, 64))
Catapulte_6 = pygame.transform.scale(Catapulte6, (64, 64))

Invoc_Tab = [Invocation_1, Invocation_2, Invocation_3, Invocation_4, Invocation_5, Invocation_6]
Invoc_Tab_ret = [pygame.transform.flip(c, True, False) for c in Invoc_Tab]

# ------------------------------------------------------------------

Catapulte_Tab = [Catapulte_1, Catapulte_2, Catapulte_3, Catapulte_4, Catapulte_5, Catapulte_6]
Catapulte_Tab_Ret = [pygame.transform.flip(c, True, False) for c in Catapulte_Tab]

# ------------------------------------------------------------------

# Rectangles
retourrect = pygame.Rect((1152 - 500, 0), (500, 50))
pauserect = pygame.Rect((1152 - 332, 5), (40, 40))
accelererect = pygame.Rect((1152 - 382, 5), (40, 40))
boutontourrect = pygame.Rect((32, 704 - 50), (45, 45))
mtrect = pygame.Rect((975, 704 - 89), (15, 15))
reprendrect = pygame.Rect((1152 // 2 - 100, 704 // 2 - 85), (120, 50))
optionprect = pygame.Rect((1152 // 2 - 100, 704 // 2 - 25), (120, 50))
quitjrect = pygame.Rect((1152 // 2 - 100, 704 // 2 + 35), (120, 50))
quitOrect = pygame.Rect((1152 // 2 - 100, 704 // 2 + 55), (120, 50))
VolMoins = pygame.Rect((655, 302), (40, 40))
VolPlus = pygame.Rect((705, 302), (40, 40))
DifMoins = pygame.Rect((655, 347), (40, 40))
DifPlus = pygame.Rect((705, 347), (40, 40))
PoubelleRect = pygame.Rect((15, 15), (40, 40))
InfoLvl5Rect = pygame.Rect((0, 0), (750, 113))

myfont = pygame.font.SysFont("Viner Hand ITC.ttf", 25)
myfontt = pygame.font.SysFont("Viner Hand ITC.ttf", 100)
myfont2 = pygame.font.SysFont("Viner Hand ITC.ttf", 20)
myfont3 = pygame.font.SysFont("Viner Hand ITC.ttf", 40)
myfont1 = pygame.font.SysFont("Viner Hand ITC.ttf", 10)
TowerFont = pygame.font.SysFont("Viner Hand ITC.ttf", 35)

# Tableau Liste_Tours
num = 0
Liste_Tours = []
for filename in glob.glob("Tours/*.json"):
    Liste_Tours.append(Tours(filename, num, myfont1))
    num += 1

# Variables de "session"
niveau = Level()
King = Perso()
invocation = None
Programme_Actif = True
Menu_Principal = True
Menu_Selection = False
Menu_Options = False
Credits_Anim = False
Confirm_Quit = False
jeu = False
menu_tour = False
pausemenu = False
OptionsMenu = False
Ecran_Perdu = False
anim_Perdu = False
animjouer = False
animmenu = False
Anim_King = False
Anim_King_Ret = False
AfficheLvlUp = False
animInvocation = False

invoque_Boucle = True
deplace = False
lvl = False
affiche_nomTour = False

tps = 0
TpsInvoc = 0
TpsLvl = 0
Anim_King_i = 0
message_argent = myfont2.render("", 1, (255, 0, 0))
position_souris = (0, 0)

tourSelectionee = None
SelectedTower4AfficheStat = None

pygame.key.set_repeat(100, 10)

Volume = 5
Difficulte = 5

pygame.mixer.music.set_volume(Volume / 10)

fondtps = 0
randomVarTF = True


if True:

    # -----------------------------------------------------------------------------------------------------------

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
