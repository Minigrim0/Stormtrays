import glob
import math
import time
import random
import pygame
import constantes


def FindAngle(delta_x, delta_y):
    if delta_x != 0:
        angle = math.atan(delta_y/delta_x)
    else:
        if delta_y < 0:
            angle = -math.pi/2
        else:
            angle = math.pi/2

    if delta_x < 0:
        angle = angle+math.pi

    return angle


class Levels(object):
    def __init__(self, file, img, nivrect):
        self.File = file
        self.Img = img
        self.Nivrect = nivrect

# ---------------------------------------------------------------------------------------------------------------------


class GoldAnim(object):
    def __init__(self, x, y, n):
        self.posx = x
        self.posy = y
        self.nbrs = n
        self.i = 0
        myfont = pygame.font.SysFont("Viner Hand ITC", 15)
        self.NbrsAffiche = myfont.render(str(self.nbrs), 1, (0, 0, 0))

    def bouge(self, fenetre, goldImg, goldObj, niveau):
        self.i += 1
        self.posy -= 2
        if self.i == 24:
            niveau.GoldTab.remove(goldObj)
        fenetre.blit(
            goldImg, (self.posx - 12 + 3*math.cos(self.i), self.posy - 6))
        fenetre.blit(
            self.NbrsAffiche, (self.posx + 3*math.cos(self.i), self.posy - 6))

# ---------------------------------------------------------------------------------------------------------------------


class Niveau(object):

    def __init__(self):

        self.Tableau_Musique = []
        for Muse in glob.glob("../musique/Themes/*.wav"):
            self.Tableau_Musique.append(Muse)

        self.img = {}
        self.img["c1", 0] = pygame.image.load(
            constantes.chem1).convert_alpha()
        self.img["t2", 0] = pygame.image.load(
            constantes.tour2).convert_alpha()
        self.img["t1", 0] = pygame.image.load(
            constantes.tour1).convert_alpha()
        self.img["x1", 0] = pygame.image.load(
            constantes.croix1).convert_alpha()
        self.img["p1", 0] = pygame.image.load(
            constantes.poubelle).convert_alpha()
        self.img["k1", 0] = pygame.image.load(
            constantes.fort1).convert_alpha()
        self.img["v1", 0] = pygame.image.load(
            constantes.Vide1).convert_alpha()
        for rot in [90, 180, 270]:
            self.img["c1", rot] = pygame.transform.rotate(
                self.img["c1", 0], rot)
            self.img["t2", rot] = pygame.transform.rotate(
                self.img["t2", 0], rot)
            self.img["t1", rot] = pygame.transform.rotate(
                self.img["t1", 0], rot)
            self.img["x1", rot] = pygame.transform.rotate(
                self.img["x1", 0], rot)
            self.img["p1", rot] = pygame.transform.rotate(
                self.img["p1", 0], rot)
            self.img["k1", rot] = pygame.transform.rotate(
                self.img["k1", 0], rot)
            self.img["v1", rot] = pygame.transform.rotate(
                self.img["v1", 0], rot)

        self.imgE = {}
        self.imgE["c1", 0] = pygame.image.load(
            constantes.chem1E).convert_alpha()
        self.imgE["t2", 0] = pygame.image.load(
            constantes.tour2E).convert_alpha()
        self.imgE["t1", 0] = pygame.image.load(
            constantes.tour1E).convert_alpha()
        self.imgE["x1", 0] = pygame.image.load(
            constantes.croix1E).convert_alpha()
        self.imgE["p1", 0] = pygame.image.load(
            constantes.poubelleE).convert_alpha()
        self.imgE["k1", 0] = pygame.image.load(
            constantes.fort1E).convert_alpha()
        self.imgE["v1", 0] = pygame.image.load(
            constantes.Vide1E).convert_alpha()
        self.imgE["QG", 0] = pygame.image.load(
            "../Img/QuestGiverF1.png").convert_alpha()
        for rot in [90, 180, 270]:
            self.imgE["c1", rot] = pygame.transform.rotate(
                self.imgE["c1", 0], rot)
            self.imgE["t2", rot] = pygame.transform.rotate(
                self.imgE["t2", 0], rot)
            self.imgE["t1", rot] = pygame.transform.rotate(
                self.imgE["t1", 0], rot)
            self.imgE["x1", rot] = pygame.transform.rotate(
                self.imgE["x1", 0], rot)
            self.imgE["p1", rot] = pygame.transform.rotate(
                self.imgE["p1", 0], rot)
            self.imgE["k1", rot] = pygame.transform.rotate(
                self.imgE["k1", 0], rot)
            self.imgE["v1", rot] = pygame.transform.rotate(
                self.imgE["v1", 0], rot)
            self.imgE["QG", rot] = pygame.transform.rotate(
                self.imgE["QG", 0], rot)

        self.videtab()

        self.gold = 500
        self.Vie_Chateau = 100
        self.Nombre_Ennemis_Tue = 0
        self.fondimg = pygame.image.load("../Img/fond.png").convert_alpha()

        self.GoldTab = []

    def Cinematic(self, screen, myfont3, myfontt):

        TabTexts = []
        TabTexts.append("Les forces du mal se sont réveillées...")
        TabTexts.append("""Le seigneur des ténébres souhaite la destruction
            d'un peuple""")
        TabTexts.append("qui l'a autrefois détruit.")
        TabTexts.append("""Les principales puissances
        d'Ethsilaar sont faibles et vous""")
        TabTexts.append("""avez été appelé comme mercanaire
        pour empêcher le mal de""")
        TabTexts.append("se répandre.")
        TabTexts.append("Bonne chance...")
        STORMTRAYS = "STORMTRAYS"
        Texti = ""

        fondu = pygame.image.load(constantes.sombre__).convert_alpha()

        for x in range(5):
            screen.blit(fondu, (0, 0))
            screen.flip()

        y = 20
        for Text in TabTexts:
            for Char in Text:
                Texti += Char
                Textb = myfont3.render(Texti, 1, (255, 255, 255))
                screen.blit(Textb, (10, y))
                screen.flip()
            Texti = ""
            y += 50

        for Char in STORMTRAYS:
            Texti += Char
            Textb = myfontt.render(Texti, 1, (255, 255, 255))
            screen.blit(Textb, (230, 425))
            screen.flip()
            time.sleep(0.2)

        time.sleep(0.5)

    def videtab(self):
        self.tableau = {}
        for y in range(11):
            for x in range(18):
                self.tableau[x, y] = "  ", 0

    def sauve(self, nomfichier):
        f = open(nomfichier, "w")
        for y in range(11):
            for x in range(18):
                img, rot = self.tableau[x, y]
                f.write("%s%d/" % (img, rot/90))
            f.write("\n")

    def sauveF(self, nomfichier, Fond, QGPos):
        f = open(nomfichier+"_Pref.txt", "w")
        f.write(Fond)
        Posx = QGPos[0]
        Posy = QGPos[1]
        f.write("\n")
        f.write(str(Posx) + "/" + str(Posy))

    def construit(self, nomfichier):
        f = open(nomfichier)
        self.tableau = {}
        for y, l in enumerate(f):
            for x in range(18):
                img = l[x*4:x*4+2]
                rot = l[x*4+2]
                self.tableau[x, y] = img, int(rot)*90

        self.FondFenetre = pygame.Surface((1152, 704))

        fondimgf = pygame.transform.scale(self.fondimg, (int(1152), int(704)))
        self.FondFenetre.blit(fondimgf, (0, 0))
        for y in range(11):
            for x in range(18):
                lettre, rot = self.tableau[x, y]
                if lettre != "  " and lettre != "k1" and lettre != "QG":
                    img = pygame.transform.scale(
                        self.img[lettre, rot], (int(65), int(65)))
                    self.FondFenetre.blit(img, (int((x*64)), int((y*64))))
                elif lettre == "k1":
                    if rot == 90 or rot == 270:
                        img = pygame.transform.scale(
                            self.img[lettre, rot], (64, 3*64)
                        )
                        self.FondFenetre.blit(img, (int((x*64)), int((y*64))))
                        self.pos_Chateau = [x, y+1]
                    else:
                        img = pygame.transform.scale(
                            self.img[lettre, rot], (3*64, 64)
                        )
                        self.FondFenetre.blit(img, (int((x*64)), int((y*64))))
                        self.pos_Chateau = [x+1, y]

            try:
                self.FondFenetre.blit(self.nanim, (self.posx, self.posy))
            except Exception as e:
                print("Error ! :", e)

    def deffond(self, nomfichier):
        f = open(nomfichier+"_Pref.txt", "r")
        imagetl = f.read()
        image = ""
        for char in imagetl:
            if char != '\n':
                image += char
            else:
                break
        print(image)
        self.fondimg = pygame.image.load(image).convert_alpha()

    def affiche(self, fenetre, fond):
        fenetre.blit(fond, (0, 0))
        for y in range(11):
            for x in range(18):
                lettre, rot = self.tableau[x, y]
                if lettre != "  " and lettre != "QG":
                    fenetre.blit(self.img[lettre, rot], (x*64, y*64))

    def ConvertToHMS(self, Time):

        M = math.floor(Time / 60)
        S = math.floor(Time % 60)
        H = math.floor(M / 60)
        M = math.floor(M % 60)

        tab = [H, M, S]

        return tab

    def PlayMusic(self):

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(
                self.Tableau_Musique[
                    random.randrange(len(self.Tableau_Musique))
                ]
            )
            pygame.mixer.music.play()

    def afficheE(self, fenetre, fond):
        fenetre.blit(fond, (0, 0))
        for y in range(11):
            for x in range(18):
                lettre, rot = self.tableau[x, y]
                if lettre != "  ":
                    fenetre.blit(self.imgE[lettre, rot], (x*64, y*64))

    def affichem(self, fenetre):

        fenetre.blit(self.FondFenetre, (0, 0))

    def Set_Difficulty(self, Difficulte):

        Level_Difficulty = 0

        if Difficulte == 10:
            Difficulty = 1
        if Difficulte == 9:
            Difficulty = 2
        if Difficulte == 8:
            Difficulty = 3
        if Difficulte == 7:
            Difficulty = 4
        if Difficulte == 5:
            Difficulty = 5
        if Difficulte == 6:
            Difficulty = 6
        if Difficulte == 4:
            Difficulty = 7
        if Difficulte == 3:
            Difficulty = 8
        if Difficulte == 2:
            Difficulty = 9
        if Difficulte == 1:
            Difficulty = 10

        if self.Nombre_Ennemis_Tue >= 0:
            Level_Difficulty = 10*Difficulty
        if self.Nombre_Ennemis_Tue >= 10:
            Level_Difficulty = 9*Difficulty
        if self.Nombre_Ennemis_Tue >= 25:
            Level_Difficulty = 8*Difficulty
        if self.Nombre_Ennemis_Tue >= 50:
            Level_Difficulty = 7*Difficulty
        if self.Nombre_Ennemis_Tue >= 100:
            Level_Difficulty = 6*Difficulty
        if self.Nombre_Ennemis_Tue >= 200:
            Level_Difficulty = 5*Difficulty
        if self.Nombre_Ennemis_Tue >= 400:
            Level_Difficulty = 4*Difficulty
        if self.Nombre_Ennemis_Tue >= 750:
            Level_Difficulty = 3*Difficulty
        if self.Nombre_Ennemis_Tue >= 1000:
            Level_Difficulty = 2*Difficulty
        if self.Nombre_Ennemis_Tue >= 2500:
            Level_Difficulty = 1*Difficulty

        return Level_Difficulty

# ---------------------------------------------------------------------


class Screen(object):

    def __init__(self, size, name, IconImg):

        info = pygame.display.Info()

        self.Font = pygame.font.SysFont("Viner Hand ITC", 25)

        self.nativeSize = size

        self.fullSize = (info.current_w, info.current_h)
        self.fullScreen = True
        self.resize(self.fullSize)

        self.ScaleButton = pygame.image.load(
            constantes.ScaleImg).convert_alpha()
        self.ScaleRect = pygame.Rect((2, self.nativeSize[1] - 22), (20, 20))

        self.fenetre = pygame.Surface(self.nativeSize)
        Icon = pygame.image.load(IconImg).convert_alpha()
        pygame.display.set_caption(name)
        pygame.display.set_icon(Icon)

        self.delais = 0.05
        self.T0 = time.clock()
        self.Tdepart = time.clock()

        self.CompteurFrame = 0
        self.FPS = 0
        self.ShowFPS = False

    def rescale(self):

        if self.fullScreen:

            self.fullScreen = False
            self.resize((1152, 704))

        else:

            self.fullScreen = True
            self.resize(self.fullSize)

    def resize(self, size):

        if self.fullScreen:

            self.fenetreAffiche = pygame.display.set_mode(
                self.fullSize, pygame.locals.FULLSCREEN)

        else:

            self.fenetreAffiche = pygame.display.set_mode(
                size, pygame.locals.RESIZABLE)

        taillex = size[0]/self.nativeSize[0]
        tailley = size[1]/self.nativeSize[1]
        self.taille = min(taillex, tailley)

        self.posAffiche = (
            (size[0] - int(self.taille*self.nativeSize[0]))//2,
            (size[1] - int(self.taille*self.nativeSize[1]))//2
        )

    def flip(self):
        self.Intervalle()
        self.fenetre.blit(self.ScaleButton, self.ScaleRect.topleft)
        self.fenetreAffiche.blit(
            pygame.transform.smoothscale(
                self.fenetre, (
                    int(self.nativeSize[0]*self.taille),
                    int(self.nativeSize[1]*self.taille)
                )
            ), self.posAffiche
        )
        pygame.display.flip()

    def blit(self, Surface, Pos):
        self.fenetre.blit(Surface, Pos)

    def GetEvent(self):

        for event in pygame.event.get():
            if event.type == pygame.locals.MOUSEMOTION or event.type == pygame.locals.MOUSEBUTTONDOWN:
                event.pos = (
                    int((event.pos[0] - self.posAffiche[0])/self.taille),
                    int((event.pos[1] - self.posAffiche[1])/self.taille)
                )
                if event.pos[0] < 0 or event.pos[1] < 0 or event.pos[0] >= 1152 or event.pos[1] >= 704:
                    continue

            if event.type == pygame.locals.QUIT:
                exit()

            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_F2:
                    pygame.image.save(
                        self.fenetre,
                        "screen/{}.bmp".format(
                            time.strftime("%Y_%m_%d_%H_%M_%S")
                        )
                    )
                elif event.key == pygame.locals.K_F11:
                    self.rescale()
                elif event.key == pygame.locals.K_F3:
                    self.ShowFPS = not self.ShowFPS
                else:
                    yield event

            elif event.type == pygame.locals.VIDEORESIZE:
                self.resize(event.size)
            elif event.type == pygame.locals.MOUSEBUTTONDOWN and self.ScaleRect.collidepoint(event.pos):
                self.rescale()
            else:
                yield event

    def Intervalle(self):

        self.T0 = self.T0 + self.delais

        SleepTime = self.T0 - time.clock()
        if SleepTime < 0:
            self.T0 = self.T0 - SleepTime
            SleepTime = 0
        time.sleep(SleepTime)

        self.CompteurFrame += 1
        if self.T0 - self.Tdepart >= 1:
            self.FPS = self.CompteurFrame/(self.T0 - self.Tdepart)
            self.CompteurFrame = 0
            self.Tdepart = self.T0

        if self.ShowFPS:

            self.fenetre.blit(
                self.Font.render(str(round(self.FPS)), 1, (0, 0, 0)), (0, 0))
