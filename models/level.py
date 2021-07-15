import time
import json
import pygame

import src.constantes as consts

from exceptions.invalidPositionException import InvalidPositionException


class Level:
    """The level class contains information and logic about the current level
    such as the list of gold anim objects and the number of ennemy killed
    """

    instance = None

    @staticmethod
    def getInstance():
        """Return the only instance of Level"""
        if Level.instance is None:
            Level()
        return Level.instance

    def __init__(self):
        if Level.instance is not None:
            raise RuntimeError("This class is a singleton")
        Level.instance = self

        images = [
            (consts.chem1, "c1"),
            (consts.tour2, "t2"),
            (consts.tour1, "t1"),
            (consts.croix1, "x1"),
            (consts.poubelle, "p1"),
            (consts.fort1, "k1"),
            (consts.Vide1, "v1"),
        ]

        self.img = {}
        self.editorImage = {}

        for path, id in images:
            self.img[id, 0] = pygame.image.load(path[0]).convert_alpha()
            self.editorImage[id, 0] = pygame.image.load(path[1]).convert_alpha()
            for rot in [90, 180, 270]:
                self.img[id, rot] = pygame.transform.rotate(self.img[id, 0], rot)
                self.editorImage[id, rot] = pygame.transform.rotate(self.editorImage[id, 0], rot)

        self.editorImage["QG", 0] = pygame.image.load("img/QuestGiverF1.png").convert_alpha()

        self.gold = 500
        self.Vie_Chateau = 100
        self.Nombre_Ennemis_Tue = 0
        self.background = pygame.image.load("img/fond.png").convert_alpha()
        self.backgroundName = "fond1"
        self.size = {"x": 18, "y": 11}

        self.GoldTab = []
        self.pos_Chateau = None
        self.FondFenetre = None
        self.map = None
        self.empty()

    @staticmethod
    def Cinematic(screen, myfont3, myfontt):
        """Shows introduction cinematic"""
        TabTexts = []
        TabTexts.append("Les forces du mal se sont réveillées...")
        TabTexts.append(
            """Le seigneur des ténébres souhaite la destruction
            d'un peuple"""
        )
        TabTexts.append("qui l'a autrefois détruit.")
        TabTexts.append(
            """Les principales puissances
        d'Ethsilaar sont faibles et vous"""
        )
        TabTexts.append(
            """avez été appelé comme mercanaire
        pour empêcher le mal de"""
        )
        TabTexts.append("se répandre.")
        TabTexts.append("Bonne chance...")
        STORMTRAYS = "STORMTRAYS"
        Texti = ""

        fondu = pygame.image.load(consts.sombre__).convert_alpha()

        for _ in range(5):
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

    def empty(self):
        """Empties the level"""
        self.map = []
        for x in range(18):
            self.map.append([])
            for _ in range(11):
                self.map[x].append(("  ", 0))

    def sauve(self, nomfichier: str, thumbnail_path: str):
        """Saves the level

        Args:
            nomfichier (str): The name of the file to save the level in
            thumbnail_path (str): The path of the level's thumbnail
        """
        level = {"background": self.backgroundName, "size": self.size, "map": self.map, "thumbnail": thumbnail_path}

        with open(nomfichier, "w") as f:
            f.write(json.dumps(level))

    def construit(self, nomfichier):
        """Builds the level from a file

        Args:
            nomfichier ([type]): [description]
        """
        with open(nomfichier) as f:
            self.map = {}
            for y, l in enumerate(f):
                for x in range(18):
                    img = l[x * 4 : x * 4 + 2]
                    rot = l[x * 4 + 2]
                    self.map[x, y] = img, int(rot) * 90

        self.FondFenetre = pygame.Surface((1152, 704))

        fondimgf = pygame.transform.scale(self.background, (int(1152), int(704)))
        self.FondFenetre.blit(fondimgf, (0, 0))
        for y in range(11):
            for x in range(18):
                lettre, rot = self.map[x, y]
                if lettre not in ("  ", "k1", "QG"):
                    img = pygame.transform.scale(self.img[lettre, rot], (int(65), int(65)))
                    self.FondFenetre.blit(img, (int((x * 64)), int((y * 64))))
                elif lettre == "k1":
                    if rot in (90, 270):
                        img = pygame.transform.scale(self.img[lettre, rot], (64, 3 * 64))
                        self.FondFenetre.blit(img, (int((x * 64)), int((y * 64))))
                        self.pos_Chateau = [x, y + 1]
                    else:
                        img = pygame.transform.scale(self.img[lettre, rot], (3 * 64, 64))
                        self.FondFenetre.blit(img, (int((x * 64)), int((y * 64))))
                        self.pos_Chateau = [x + 1, y]

            self.FondFenetre.blit(self.nanim, (self.posx, self.posy))

    def deffond(self, nomfichier):
        """Defines the background of the current level

        Args:
            nomfichier ([type]): [description]
        """
        with open(nomfichier + "_Pref.txt", "r") as f:
            imagetl = f.read()
        image = ""
        for char in imagetl:
            if char != "\n":
                image += char
            else:
                break
        self.background = pygame.image.load(image).convert_alpha()

    def placeTile(self, position: tuple, tile):
        """Places a tile at the given coordinates

        Args:
            position (tuple): the position to place the tile at
            tile ([type]): [description]
        """
        if position[0] not in list(range(self.size["x"])) or position[1] not in list(range(self.size["y"])):
            raise InvalidPositionException("Tile is outside of the map !")

        self.map[position[0]][position[1]] = tile

    def draw(self, fenetre, editor=False):
        """Draws the current level

        Args:
            fenetre (Screen): The screen to blit the level on
        """
        images = self.editorImage if editor is True else self.img

        fenetre.blit(self.background, (0, 0))
        for y in range(11):
            for x in range(18):
                lettre, rot = self.map[x][y]
                if lettre not in ("  ", "QG"):
                    fenetre.blit(images[lettre, rot], (x * 64, y * 64))

    def affichem(self, fenetre):
        """Draws the background

        Args:
            fenetre ([type]): [description]
        """
        fenetre.blit(self.FondFenetre, (0, 0))

    def Set_Difficulty(self, Difficulte):
        """Changes variables relative to the diffculty information

        Args:
            Difficulte ([type]): [description]

        Returns:
            [type]: [description]
        """
        Level_Difficulty = 0

        Difficulty = 11 - Difficulte

        if self.Nombre_Ennemis_Tue >= 0:
            Level_Difficulty = 10 * Difficulty
        if self.Nombre_Ennemis_Tue >= 10:
            Level_Difficulty = 9 * Difficulty
        if self.Nombre_Ennemis_Tue >= 25:
            Level_Difficulty = 8 * Difficulty
        if self.Nombre_Ennemis_Tue >= 50:
            Level_Difficulty = 7 * Difficulty
        if self.Nombre_Ennemis_Tue >= 100:
            Level_Difficulty = 6 * Difficulty
        if self.Nombre_Ennemis_Tue >= 200:
            Level_Difficulty = 5 * Difficulty
        if self.Nombre_Ennemis_Tue >= 400:
            Level_Difficulty = 4 * Difficulty
        if self.Nombre_Ennemis_Tue >= 750:
            Level_Difficulty = 3 * Difficulty
        if self.Nombre_Ennemis_Tue >= 1000:
            Level_Difficulty = 2 * Difficulty
        if self.Nombre_Ennemis_Tue >= 2500:
            Level_Difficulty = 1 * Difficulty

        return Level_Difficulty
