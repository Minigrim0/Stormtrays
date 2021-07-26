import pygame as pg

from models.screen import Screen
from src.runnable import Runnable
from src.invocation import Invocation
from src.tourClasse import Tours_IG

from models.level import Level
from models.ennemy import Ennemy
from models.character import Character

from UI.components.game_ui import GameUI


class Game(Runnable):
    def __init__(self, screen: Screen, levelPath: str):
        super().__init__()
        self.level = Level.getInstance()
        self.level.build(levelPath)
        self.screen = screen

        # double_invoque = False

        # count = 0
        # Level_Number = 1
        # Liste_Tours_IG = []
        # Tab_Projectile = []
        # CooldownInvoc = 0
        # TpsCoolDown = 0

        self.level.gold = 500
        self.level.Nombre_Ennemis_Tue = 0

        self.ui = GameUI.getInstance()
        # TpsLvl = 0
        # Icapacite1 = 0
        # HaveSeenLvl5Msg = False
        # ImgInvoc = True
        # Accelerex2 = False
        # invocation = None
        # Tps_Invoc_affiche = None
        # AfficheStatTour = False

        # Compteur_Iteration = 0
        # Time_50 = myfont2.render("0", 1, (0, 0, 0))

    def loop(self):
        Level.getInstance().update(self.screen.timeElapsed)
        Ennemy.getInstance().update(self.screen.timeElapsed)
        Character.getInstance().update(self.screen.timeElapsed)
        self.ui.update()

        self.draw()

        self.handleEvent()
        """
        if niveau.Vie_Chateau <= 0:
            jeu = False
            Ecran_Perdu = True

        frappe = 0

        if TpsCoolDown != 0:
            Tps_Invoc_affiche = myfont2.render(str(TpsCoolDown), 1, (255, 255, 255))
        else:
            Tps_Invoc_affiche = None

        King.vit(King.Perso_Tab, King.Perso_Tab_ret)
        """

    def handleEvent(self):
        for event in self.screen.getEvent():

            Character.getInstance().handleEvent(event)

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False

    def draw(self):
        self.level.draw(self.screen)

        Ennemy.getInstance().draw(self.screen)
        Character.getInstance().draw(self.screen)

        self.ui.draw(self.screen)
        """
        # Bouger les ennemis
        for ennemi in Liste_Mechants:

            ennemi.bouge(niveau.map, screen, niveau, Liste_Mechants, King)
            ennemi.meurt.set_volume(Volume / 10)

        for projectileObj in Tab_Projectile:
            projectileObj.Avance(screen, Liste_Mechants, niveau, Tab_Projectile, King)

        # Faire attaquer les tours
        for tour in Liste_Tours_IG:
            tour.attaque(Liste_Mechants, Tab_Projectile)
            tour.affiche_jeu(screen)

        if invocation and not invocation.vit(screen, Liste_Mechants, niveau):
            King.XpToAdd += invocation.xp
            invocation = None

        Level_Difficulty = niveau.Set_Difficulty(Difficulte)

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
                invocation = Invocation(Invoc_Tab, Invoc_Tab_ret, King)
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

        if King.Level_Roi == 5 and not HaveSeenLvl5Msg:
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
                    tourSelectionee.placetour(position_souris, screen, niveau)
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
                        tourSelectionee = Tours_IG(tour, tour.DirImg)
                        message_argent = myfont2.render("", 1, (255, 0, 0))

            # si on est pas dans Menu des tour
            else:
                message_argent = myfont2.render("", 1, (255, 0, 0))
                deplace = False

                if event.type == pygame.locals.KEYDOWN and not animInvocation:

                    k = pygame.key.get_pressed()

                    if k[pygame.locals.K_i] and King.Level_Roi >= 5 and not invocation and CooldownInvoc == 0:
                        animInvocation = True
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

                if King.Level_Roi == 5 and HaveSeenLvl5Msg is False and InfoLvl5Rect.collidepoint(event.pos):
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

        """
        self.screen.flip()
