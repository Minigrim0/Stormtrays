import pygame
import pygame.locals
import glob
import os
import random
import src.constantes as constantes
from src.classes import Levels, Niveau
from src.screen import Screen
from src.invocation import Invocation
from src.ennemis import Ennemi_IG
from src.tourClasse import Tours, Tours_IG
from src.perso import Perso

pygame.init()

screen = Screen((1152, 704), "StormTarys", constantes.IconImg)

Tableau_Musique = []
for Muse in glob.glob("musique/Themes/*.wav"):
    Music = Muse
    Tableau_Musique.append(Music)

# ------------------------------------------------------------------

# Images
joue = pygame.image.load(constantes.joue).convert_alpha()
quit = pygame.image.load(constantes.quit).convert_alpha()
Coin = pygame.image.load(constantes.Coin).convert_alpha()
menutour = pygame.image.load(constantes.mt).convert_alpha()
pause = pygame.image.load(constantes.pause).convert_alpha()
Plus = pygame.image.load(constantes.Plus__).convert_alpha()
XpBar = pygame.image.load(constantes.XpBar).convert_alpha()
option = pygame.image.load(constantes.option).convert_alpha()
retour = pygame.image.load(constantes.retour).convert_alpha()
Moins = pygame.image.load(constantes.Moins__).convert_alpha()
InvocBar = pygame.image.load(constantes.Invoc).convert_alpha()
credits = pygame.image.load(constantes.credits).convert_alpha()
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

# ------------------------------------------------------------------

# ------------------------------------------------------------------

Invoc_Tab = [Invocation_1, Invocation_2, Invocation_3, Invocation_4, Invocation_5, Invocation_6]
Invoc_Tab_ret = [pygame.transform.flip(c, True, False) for c in Invoc_Tab]

# ------------------------------------------------------------------

Catapulte_Tab = [Catapulte_1, Catapulte_2, Catapulte_3, Catapulte_4, Catapulte_5, Catapulte_6]
Catapulte_Tab_Ret = [pygame.transform.flip(c, True, False) for c in Catapulte_Tab]

# ------------------------------------------------------------------

# Rectangles
jouerect = pygame.Rect((1152 - 500, 704 - 240), (500, 50))
credirect = pygame.Rect((1152 - 450, 704 - 180), (500, 50))
optionrect = pygame.Rect((1152 - 400, 704 - 120), (500, 50))
quitrect = pygame.Rect((1152 - 350, 704 - 60), (500, 50))
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
ConfirmReprise = pygame.Rect((1152 // 2 - 60, 704 // 2 - 55), (120, 50))
ConfirmQuitter = pygame.Rect((1152 // 2 - 60, 704 // 2 + 15), (120, 50))
PoubelleRect = pygame.Rect((15, 15), (40, 40))
InfoLvl5Rect = pygame.Rect((0, 0), (750, 113))

# rectangles niveaux
Tableau_Niveau = []

# definition des miniatures
Compteur = 10
for filename in glob.glob("level/mininiveau/*.png"):
    dirname, file = os.path.split(filename)
    file, ext = os.path.splitext(file)
    try:
        img = pygame.image.load(filename).convert_alpha()
    except Exception:
        img = pygame.image.load(constantes.Vide1E).convert_alpha()
    nivrect = pygame.Rect((1152 / 2 - 10, Compteur), (500, 110))
    level = Levels(file, img, nivrect)
    Tableau_Niveau.append(level)
    Compteur += 120

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
niveau = Niveau()
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


def play_music():
    if not pygame.mixer.music.get_busy() and len(Tableau_Musique) > 0:
        pygame.mixer.music.load(Tableau_Musique[random.randrange(len(Tableau_Musique))])
        pygame.mixer.music.play()


# -----------------------------------------------------------------------------------------------------------------------------------------------


while Programme_Actif:

    i = 0

    # Menu_Principal
    while Menu_Principal:

        # Affiche les éléments du menu
        screen.blit(Fond_Menu_Principal, (0, 0))
        screen.blit(joue, (652, 464))
        screen.blit(credits, (702, 524))
        screen.blit(option, (752, 584))
        screen.blit(quit, (802, 644))
        screen.flip()

        # Musique
        play_music()

        # Events
        for event in screen.getEvent():

            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    Menu_Principal = False
                    Confirm_Quit = True
                    break

            if event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 1:

                if quitrect.collidepoint(event.pos):
                    Menu_Principal = False
                    Confirm_Quit = True
                    break

                if jouerect.collidepoint(event.pos):
                    Menu_Principal = False
                    animjouer = True
                    break

                if optionrect.collidepoint(event.pos):
                    Menu_Principal = False
                    Menu_Options = True
                    break

                if credirect.collidepoint(event.pos):
                    Menu_Principal = False
                    Credits_Anim = True
                    break

    # --------------------------------------------------------------------------------------------------------------------------------------------

    while Confirm_Quit:
        screen.blit(Fond_Menu_Principal, (0, 0))
        screen.blit(ConfirmQuit, (376, 152))
        screen.blit(reprise, (516, 297))
        screen.blit(quitpaus, (516, 367))
        screen.flip()

        # Musique
        play_music()

        for event in screen.getEvent():

            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                Confirm_Quit = False
                Menu_Principal = True

            if event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 1:
                if ConfirmReprise.collidepoint(event.pos):
                    Confirm_Quit = False
                    Menu_Principal = True

                elif ConfirmQuitter.collidepoint(event.pos):
                    Confirm_Quit = False
                    Programme_Actif = False

    # --------------------------------------------------------------------------------------------------------------------------------------------

    # Menu_Principal de sélection
    if Menu_Selection:
        i = 60
        Compteur_Lvls = 10

    while Menu_Selection:
        Compteur_Mini = i
        Compteur_Lvls = i

        King.posx = 0
        King.posy = 0

        # Affiche les éléments du menu
        screen.blit(Fond_Menu_Principal, (0, 0))
        screen.blit(Fond_Noir_Semi_Transparent, (0, 0))

        for level in Tableau_Niveau:
            Nom_Niveau = myfont.render(level.File, 1, (255, 255, 255))
            screen.blit(level.Img, (586, Compteur_Lvls))
            screen.blit(Nom_Niveau, (796, Compteur_Lvls + 45))

            level.Nivrect = pygame.Rect((586, Compteur_Lvls), (500, 110))
            Compteur_Lvls += 120

        screen.blit(retour, (654, 0))
        screen.flip()

        # Musique
        play_music()

        for event in screen.getEvent():

            if event.type == pygame.locals.KEYDOWN:

                if event.key == pygame.locals.K_ESCAPE:
                    Menu_Selection = False
                    Menu_Principal = True

            if event.type == pygame.locals.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if retourrect.collidepoint(event.pos):
                        animmenu = True
                        Menu_Selection = False
                        break

                    for level in Tableau_Niveau:
                        if level.Nivrect.collidepoint(event.pos):
                            jeu = True
                            lvl = level.File
                            Menu_Selection = False
                            break

                elif event.button == 5:

                    if i > -len(Tableau_Niveau) * 120 + 704:
                        i -= 50

                elif event.button == 4:
                    if i < 60:
                        i += 50

    # --------------------------------------------------------------------------------------------------------------------------------------------

    if Menu_Options:
        screen.blit(FondSombre, (0, 0))

    while Menu_Options:

        # Affiche les éléments du menu
        screen.blit(Fond_Menu_Principal, (0, 0))

        # Musique
        play_music()

        pygame.mixer.music.set_volume(Volume / 10)

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

        for event in screen.getEvent():

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

    # --------------------------------------------------------------------------------------------------------------------------------------------

    while Credits_Anim:

        # Musique
        play_music()

        i = 0
        while i <= 2900:

            screen.flip()
            screen.blit(Fond_Menu_Principal, (0, 0))
            screen.blit(Credits, (0, 0 - i))
            i += 2

            for event in screen.getEvent():

                if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:

                    Credits_Anim = False
                    i = 3000

                if event.type == pygame.locals.MOUSEBUTTONDOWN:

                    if event.button == 5:
                        i += 40
                    elif event.button == 4:
                        i -= 40

        Menu_Principal = True
        Credits_Anim = False

    # --------------------------------------------------------------------------------------------------------------------------------------------

    # Si jeu est actif (action unique)
    if jeu:
        niveau.deffond("level/" + str(lvl) + ".txt")
        niveau.construit("level/" + str(lvl) + ".txt")
        niveau.affichem(screen)

        double_invoque = False

        count = 0
        Level_Number = 1
        Liste_Mechants = []
        Liste_Tours_IG = []
        Tab_Projectile = []
        CooldownInvoc = 0
        TpsCoolDown = 0

        niveau.gold = 500
        niveau.Vie_Chateau = 100
        niveau.Nombre_Ennemis_Tue = 0
        King.XpToAdd = 0
        King.xp = 0
        King.objectif = 10
        King.Level_Roi = 0
        King.Degats = 3
        King.Vitesse = 5
        TpsLvl = 0
        Icapacite1 = 0
        HaveSeenLvl5Msg = False
        ImgInvoc = True
        Accelerex2 = False
        invocation = None
        Tps_Invoc_affiche = None
        AfficheStatTour = False

        Compteur_Iteration = 0
        Time_50 = myfont2.render("0", 1, (0, 0, 0))

    while jeu:
        if King.capacite1:
            Icapacite1 += 1
            if Icapacite1 == 160:
                Icapacite1 = 0
                King.capacite1 = False

        # Musique
        play_music()

        LvlUp = King.level_up()
        if CooldownInvoc > 0:
            CooldownInvoc -= 1
        TpsCoolDown = CooldownInvoc // 24

        # Augmentation du niveau
        if LvlUp:

            AfficheLvlUp = True

            King.Degats = King.Level_Roi * 0.5 + 3
            King.Vitesse = King.Level_Roi * 0.25 + 5

        # Mort Chateau
        if niveau.Vie_Chateau <= 0:
            jeu = False
            Ecran_Perdu = True

        frappe = 0

        # Construction + Affichage + Boutons
        Argent_Possede_Affiche = myfont2.render("Or : %i" % niveau.gold, 1, (0, 0, 0))
        Vie_Chateau_Affiche = myfont2.render("Bastion : %i pv." % niveau.Vie_Chateau, 1, (0, 0, 0))
        Level_Num_Affiche = myfont2.render("Niveau %i" % King.Level_Roi, 1, (0, 0, 0))
        Ennemi_Tue_Affiche = myfont2.render("Victimes : %i" % niveau.Nombre_Ennemis_Tue, 1, (0, 0, 0))
        Degats_Roi_Affiche = myfont2.render("Dégats : %i" % King.Degats, 1, (0, 0, 0))
        Vitesse_Roi_Affiche = myfont2.render("Vitesse : %i " % King.Vitesse, 1, (0, 0, 0))
        Obj_Lvl_Txt = myfont2.render("{}/{}".format(King.xp, King.objectif), 1, (0, 0, 0))

        if TpsCoolDown != 0:
            Tps_Invoc_affiche = myfont2.render(str(TpsCoolDown), 1, (255, 255, 255))
        else:
            Tps_Invoc_affiche = None

        Current_Xp = pygame.Surface(((King.xp / King.objectif) * 255, 18))
        Current_Xp.fill((0, 255, 40))

        niveau.affichem(screen)
        DoAttak = King.vit(King.Perso_Tab, King.Perso_Tab_ret, King.Vitesse)

        if DoAttak:
            if King.Is_Returned and not Anim_King and not Anim_King_Ret:
                Anim_King_Ret = True
            elif not King.Is_Returned and not Anim_King and not Anim_King_Ret:
                Anim_King = True

        # Bouger les ennemis
        for ennemi in Liste_Mechants:

            ennemi.bouge(niveau.map, screen, niveau, Liste_Mechants, Coin, King)
            ennemi.meurt.set_volume(Volume / 10)

        for projectileObj in Tab_Projectile:
            projectileObj.Avance(screen, Liste_Mechants, niveau, Coin, Tab_Projectile, King)

        # Faire attaquer les tours
        for tour in Liste_Tours_IG:

            tour.attaque(tour.Position_IG, Liste_Mechants, niveau, Coin, Tab_Projectile)
            tour.affiche_jeu(screen)

        if invocation:
            if not invocation.vit(screen, Liste_Mechants, niveau, Coin):
                King.XpToAdd += invocation.xp
                invocation = None

        if Anim_King:
            Anim_King = King.AnimKingAttak(Liste_Mechants, niveau, Coin)

        if Anim_King_Ret:
            Anim_King_Ret = King.AnimKingAttakRet(Liste_Mechants, niveau, Coin)

        Level_Difficulty = niveau.Set_Difficulty(Difficulte)

        if niveau.Nombre_Ennemis_Tue >= 5000:
            double_invoque = True

        Aleatoire = random.random() * Level_Difficulty

        # Test random en fonction de Level_Difficulty pour invoquer un ennemi
        if Aleatoire <= 1:
            while invoque_Boucle:
                invoque = random.randrange(10)
                if invoque == 0:
                    ennemi = Ennemi_IG("../Ennemis/Orc.json")
                    ennemi.pose_ennemi(niveau.map, screen)
                    Liste_Mechants.append(ennemi)
                elif invoque == 1 or invoque == 2:
                    ennemi = Ennemi_IG("../Ennemis/Goblin.json")
                    ennemi.pose_ennemi(niveau.map, screen)
                    Liste_Mechants.append(ennemi)
                elif invoque == 3:
                    ennemi = Ennemi_IG("../Ennemis/Dwarf.json")
                    ennemi.pose_ennemi(niveau.map, screen)
                    Liste_Mechants.append(ennemi)
                elif invoque == 4:
                    ennemi = Ennemi_IG("../Ennemis/Knight.json")
                    ennemi.pose_ennemi(niveau.map, screen)
                    Liste_Mechants.append(ennemi)
                elif invoque == 5:
                    ennemi = Ennemi_IG("../Ennemis/Ghost.json")
                    ennemi.pose_ennemi(niveau.map, screen)
                    Liste_Mechants.append(ennemi)
                elif invoque == 6:
                    ennemi = Ennemi_IG("../Ennemis/Golem.json")
                    ennemi.pose_ennemi(niveau.map, screen)
                    Liste_Mechants.append(ennemi)
                elif invoque == 7:
                    invoque = random.randrange(5)
                    if invoque == 0:
                        ennemi = Ennemi_IG("../Ennemis/Dragon.json")
                        ennemi.pose_ennemi(niveau.map, screen)
                        Liste_Mechants.append(ennemi)
                elif invoque == 8 or invoque == 9 or invoque == 10:
                    ennemi = Ennemi_IG("../Ennemis/Wolf.json")
                    ennemi.pose_ennemi(niveau.map, screen)
                    Liste_Mechants.append(ennemi)
                if double_invoque is True:
                    double_invoque = False
                else:
                    invoque_Boucle = False

            invoque_Boucle = True

        # Si le Menu des tours est actif
        if menu_tour:

            num = 0
            screen.blit(Quadrille, (0, 0))
            if not deplace:

                screen.blit(menutour, (0, 604))

            if deplace:

                screen.blit(Poubelle, (15, 15))
                tourSelectionee.bougetoursouris(position_souris, screen)

            else:
                for tour in Liste_Tours:

                    tour.affichemenu(screen, num)
                    num += 1

                    # affiche le nom de la tour
                    if tour.tourrect.collidepoint(position_souris):

                        StatTourCurseur = TowerFont.render(tour.nom, 1, (0, 0, 0))
                        screen.blit(StatTourCurseur, (15, 15))

                        if niveau.gold < tour.prix:

                            message_argent = TowerFont.render("Vous n'avez pas assez d'argent !", 1, (255, 0, 0))
                            screen.blit(message_argent, (15, 50))

        screen.blit(King.nanim, (King.posx, King.posy))
        screen.blit(FondHautDroite, (1152 - 282, 0))
        screen.blit(Argent_Possede_Affiche, (1152 - 280, 5))
        screen.blit(Vie_Chateau_Affiche, (1152 - 280, 27))
        screen.blit(Vitesse_Roi_Affiche, (1152 - 280, 54))
        screen.blit(Level_Num_Affiche, (1152 - 132, 5))
        screen.blit(Ennemi_Tue_Affiche, (1152 - 132, 27))
        screen.blit(Degats_Roi_Affiche, (1152 - 132, 54))
        screen.blit(Current_Xp, (1152 - 270, 86))
        screen.blit(Obj_Lvl_Txt, (1152 - 155, 80))
        screen.blit(XpBar, (1152 - 282, 80))
        screen.blit(pause, (820, 5))

        if Tps_Invoc_affiche and King.Level_Roi >= 5:
            screen.blit(TpsRestInvocSombre, (1152 - 550, 10))
            screen.blit(Tps_Invoc_affiche, (1152 - 535, 25))
        elif King.Level_Roi >= 5:
            screen.blit(TpsRestInvoc, (1152 - 550, 10))

        if AfficheLvlUp:

            TpsLvl += 1
            if TpsLvl < 30:
                screen.blit(Tab_AnimLvlUp[TpsLvl // 3], (426, 277))

            elif TpsLvl <= 50:
                screen.blit(Tab_AnimLvlUp[9], (426, 277))

            else:
                TpsLvl = 0
                AfficheLvlUp = False

        if AfficheStatTour:
            pygame.draw.circle(
                screen.fenetre,
                pygame.Color("red"),
                (
                    SelectedTower4AfficheStat.Position_IG[0] * 64 + 32,
                    SelectedTower4AfficheStat.Position_IG[1] * 64 + 32,
                ),
                SelectedTower4AfficheStat.portee * 64 + 20,
                3,
            )

        if animInvocation:
            TpsInvoc += 1

            if TpsInvoc % 8 == 0:
                ImgInvoc = not ImgInvoc

            if ImgInvoc is True and TpsInvoc < 92:
                King.nanim = InvoqueAnim1
            else:
                King.nanim = InvoqueAnim2
            if TpsInvoc >= 96:
                King.nanim = InvoqueAnim3
            if TpsInvoc >= 98:
                King.nanim = InvoqueAnim4
            if TpsInvoc >= 100:
                King.nanim = InvoqueAnim5
            if TpsInvoc >= 102:
                King.nanim = InvoqueAnim6
            if TpsInvoc >= 104:
                King.nanim = InvoqueAnim7
            if TpsInvoc >= 106:
                King.nanim = InvoqueAnim8
            if TpsInvoc >= 108:
                King.nanim = InvoqueAnim9
            if TpsInvoc >= 110:
                King.nanim = InvoqueAnim10
            if TpsInvoc >= 112:
                King.nanim = InvoqueAnim11
            if TpsInvoc >= 114:
                King.nanim = InvoqueAnim12
            if TpsInvoc >= 116:
                King.nanim = InvoqueAnim13
            if TpsInvoc >= 118:
                King.nanim = InvoqueAnim14

            if TpsInvoc == 120:
                invocation = Invocation(niveau, Invoc_Tab, Invoc_Tab_ret, King.Level_Roi - 5, King)
                TpsInvoc = 0
                King.nanim = King.King_1
                animInvocation = False

            else:
                Invoc_Avancee = pygame.Surface(((TpsInvoc / 120) * 177, 12))
                Invoc_Avancee.fill((215, 75, 0))
                screen.blit(Invoc_Avancee, (16, 69))
                screen.blit(InvocBar, (10, 65))

        if not menu_tour:
            screen.blit(boutontour, (32, 654))
        if Accelerex2:
            screen.blit(accelerex, (770, 5))
        else:
            screen.blit(accelere, (770, 5))

        for Gold in niveau.GoldTab:
            Gold.bouge(screen, Coin, niveau)

        if King.Level_Roi == 5:
            if not HaveSeenLvl5Msg:
                screen.blit(InfoLvl5Img, (0, 0))

        # Events du jeu
        for event in screen.getEvent():

            # Si l'on est dans le Menu_Principal des tours
            if (
                menu_tour
                and event.type == pygame.locals.MOUSEBUTTONDOWN
                and (deplace and not mtrect.collidepoint(event.pos) and not PoubelleRect.collidepoint(event.pos))
            ):
                if niveau.map[(position_souris[0]) // (64), (position_souris[1]) // (64)] == ("  ", 0):
                    niveau.gold -= tourSelectionee.prix
                    Liste_Tours_IG.append(tourSelectionee)
                    tourSelectionee.placetour(
                        position_souris, screen, niveau.map, Liste_Tours_IG, tourSelectionee, niveau
                    )
                    deplace = False
                    menu_tour = False
                    break

                # Pour quitter le Menu_Principal des tours
                if mtrect.collidepoint(event.pos):
                    menu_tour = False
                    deplace = False

                if PoubelleRect.collidepoint(event.pos):

                    deplace = False

                for tour in Liste_Tours:

                    # Si l'on selectionne une tour
                    if tour.tourrect.collidepoint(event.pos) and niveau.gold >= tour.prix:
                        deplace = True
                        tourSelectionee = Tours_IG(tour, num, tour.DirImg)
                        message_argent = myfont2.render("", 1, (255, 0, 0))

            # si on est pas dans Menu des tour
            else:
                message_argent = myfont2.render("", 1, (255, 0, 0))
                deplace = False

                if event.type == pygame.locals.KEYDOWN and not animInvocation:

                    k = pygame.key.get_pressed()

                    if k[pygame.locals.K_i] and King.Level_Roi >= 5 and not invocation and CooldownInvoc == 0:
                        animInvocation = True
                        CooldownInvoc = 2640

                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                    # Menu_Principal tour actif
                    if boutontourrect.collidepoint(event.pos):
                        menu_tour = True

                    if event.button == 3 and not animInvocation:
                        if Liste_Mechants:
                            for ennemi in Liste_Mechants:
                                if ennemi.HitBox.collidepoint(event.pos):
                                    King.target = ennemi
                                    break
                                King.target = None
                                King.targetCoordx = event.pos[0] - 48
                                King.targetCoordy = event.pos[1] - 48
                        else:
                            King.target = None
                            King.targetCoordx = event.pos[0] - 48
                            King.targetCoordy = event.pos[1] - 48

            # Si l'on est dans le Menu_Principal de tour ou pas
            if event.type == pygame.locals.MOUSEMOTION:

                position_souris = event.pos

            # Bouton Pause
            if event.type == pygame.locals.MOUSEBUTTONDOWN:

                AfficheStatTour = False

                if King.Level_Roi == 5 and HaveSeenLvl5Msg is False:
                    if InfoLvl5Rect.collidepoint(event.pos):
                        HaveSeenLvl5Msg = True

                if pauserect.collidepoint(event.pos):
                    pausemenu = True

                if accelererect.collidepoint(event.pos):
                    Accelerex2 = not Accelerex2
                    if Accelerex2:
                        screen.delais = 0.05 / 4
                    else:
                        screen.delais = 0.05

                for Tour in Liste_Tours_IG:
                    if Tour.Rect.collidepoint(event.pos):
                        AfficheStatTour = not AfficheStatTour
                        SelectedTower4AfficheStat = Tour

            if event.type == pygame.locals.KEYDOWN:

                # Bouton "ECHAP"
                if event.key == pygame.locals.K_ESCAPE:
                    pausemenu = True
                    menu_tour = False

                if event.key == pygame.locals.K_a:
                    Accelerex2 = not Accelerex2
                    if Accelerex2:
                        screen.delais = 0.05 / 4
                    else:
                        screen.delais = 0.05

        screen.flip()

        # -----------------------------------------------------------------------------------------------------------

        if pausemenu:
            screen.blit(FondSombre, (0, 0))

        # Tant que Menu_Principal pause est actif
        while pausemenu:

            play_music()

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

            play_music()

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

                    if VolPlus.collidepoint(event.pos):
                        if Volume < 10:
                            Volume += 1

                    if VolMoins.collidepoint(event.pos):
                        if Volume > 0:
                            Volume -= 1

                    if DifPlus.collidepoint(event.pos):
                        if Difficulte < 10:
                            Difficulte += 1

                    if DifMoins.collidepoint(event.pos):
                        if Difficulte > 0:
                            Difficulte -= 1

    # -------------------------------------------------------------------------------------------------------------------------------------------

    if Ecran_Perdu:

        i = 0
        anim_Perdu = True
        Perdutxt = pygame.image.load(constantes.DefeatTxt).convert_alpha()
        pygame.mixer.music.stop()
        pygame.mixer.music.load(constantes.Defeat_Song)
        pygame.mixer.music.play()

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

    # -------------------------------------------------------------------------------------------------------------------------------------------

    screen.delais = 0.03

    # Animation de Menu_Principal à Menu_Selection
    while animjouer:
        i = 0
        while i < 464:
            screen.flip()
            screen.blit(Fond_Menu_Principal, (0, 0))
            screen.blit(joue, (1152 - 500, 704 - 240 - i))
            screen.blit(credits, (1152 - 450 + i, 704 - 180))
            screen.blit(option, (1152 - 400 + i, 704 - 120))
            screen.blit(quit, (1152 - 350 + i, 704 - 60))

            screen.getEvent()
            i += 5

        Menu_Selection = True
        animjouer = False

    # Animation de Menu_Selection à Menu_Principal
    while animmenu:
        i = 0
        while i < 460:

            screen.flip()
            screen.blit(Fond_Menu_Principal, (0, 0))
            screen.blit(joue, (1152 - 500, i + 4))
            screen.blit(credits, (1152 + 10 - i, 704 - 180))
            screen.blit(option, (1152 + 60 - i, 704 - 120))
            screen.blit(quit, (1152 + 110 - i, 704 - 60))

            screen.getEvent()
            i += 5

        Menu_Principal = True
        animmenu = False

    screen.delais = 0.05
