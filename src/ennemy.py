import pygame
import src.constantes as constantes
from src.gold import GoldAnim

from models.level import Level
from UI.components.imageAnimation import ImageAnimation
from UI.components.loading_bar import LoadingBar


class EnnemyDO:
    """Represent an in game ennemy, keeps the health etc..."""

    def __init__(self, data):
        self.posx = 0
        self.posy = 0
        self.count = 0
        self.PosAbsolue = (0, 0)
        self.i = 0
        self.Returned = False
        self.IsAttacked = False
        self.BlitLife = False
        self.tab = []
        self.tab_ret = []
        self.Dir_x = 0
        self.Dir_y = 0
        self.Tics = 0

        self.pose_ennemi()

        self.propriete = data

        self.Name = self.propriete["Name"]
        # self.meurt = pygame.mixer.Sound(self.propriete["DeathSound"])
        self.vie = self.propriete["LifePts"]
        self.vie_bas = self.propriete["LifePts"]
        self.vitesse = self.propriete["Speed"]
        self.height = self.propriete["Height"]

        self.healthBar = LoadingBar((self.posx - 10, self.posy), (self.height, 5), initial_adv=self.height)
        self.animation = ImageAnimation(self.propriete["ImgFolder"], flippable=True, speed=6)

        self.HitBox = None
        self.Vie_Rect = None

    def pose_ennemi(self):
        """Adds an ennemy to the game

        Args:
            tableau ([type]): [description]
        """
        self.posx = 0
        self.posy = 0
        level = Level.getInstance()

        x = 0
        for y in range(11):
            tile = level.map[x][y]
            if tile is not None and (tile.code, tile.rotation) == ("c1", 0):
                self.posy = y
                self.PosAbsolue = (0, y * 64)
                self.HitBox = pygame.Rect((0, y), (64, 64))

    def draw(self, screen):
        """Blits the ennemy on the screen

        Args:
            screen ([type]): [description]
        """
        self.healthBar.draw(screen)
        self.animation.draw(screen, self.PosAbsolue)

    def update(self, timeElapsed: float):
        """Makes the ennemy move

        Args:
            tableau ([type]): [description]
            fenetre ([type]): [description]
            niveau ([type]): [description]
            Liste_Mechants ([type]): [description]
            coin ([type]): [description]
            King ([type]): [description]
        """
        self.healthBar.set_advancement(self.vie * (self.height / self.vie_bas))

        self.animation.update(timeElapsed)
        self.healthBar.move((self.posx - 10, self.posy))

        level = Level.getInstance()
        if self.IsAttacked:
            self.Tics += 1
            self.BlitLife = True
        if self.Tics == 50:
            self.IsAttacked = False
            self.BlitLife = False
            self.Tics = 0

        tile = level.map[self.posx][self.posy]

        new_dir = tile.direction()
        if new_dir is None:
            self.pose_ennemi()
        elif new_dir != (0, 0):
            self.Dir_x, self.Dir_y = new_dir

        self.count += 1
        if self.count == round(64 / self.vitesse):

            self.count = 0
            self.posx += self.Dir_x
            self.posy += self.Dir_y
        else:
            self.PosAbsolue = (
                self.posx * 64 + (self.count * self.vitesse * self.Dir_x),
                self.posy * 64 + (self.count * self.vitesse * self.Dir_y),
            )
            self.HitBox = pygame.Rect(self.PosAbsolue, (64, 64))

        # if self.posx == niveau.pos_Chateau[0] and self.posy == niveau.pos_Chateau[1]:
        #     niveau.Vie_Chateau -= self.vie // 1.5
        #     self.enleve_vie(2000, Liste_Mechants, self, niveau, King)

    def enleve_vie(self, viemoins, liste_mech, ennemi, niveau, King):
        """Makes the ennemy loose life

        Args:
            viemoins ([type]): [description]
            liste_mech ([type]): [description]
            ennemi ([type]): [description]
            niveau ([type]): [description]
            King ([type]): [description]

        Returns:
            [type]: [description]
        """
        self.vie -= viemoins
        self.IsAttacked = True
        self.Tics = 0

        if self.vie <= 0:
            constantes.DicoEnnemisKilled[self.Name] += 1
            liste_mech.remove(ennemi)
            # self.meurt.play()
            if King.capacite1 is True:
                FlyingGold = GoldAnim(
                    (self.PosAbsolue[0] + self.height // 2, self.PosAbsolue[1] + self.height // 2), self.vie_bas
                )
                constantes.GoldGained[0] += self.vie_bas
                niveau.GoldTab.append(FlyingGold)
                niveau.gold += self.vie_bas

            else:
                FlyingGold = GoldAnim((self.PosAbsolue[0] + 32, self.PosAbsolue[1] + 32), self.vie_bas // 2)
                constantes.GoldGained[0] += self.vie_bas // 2
                niveau.GoldTab.append(FlyingGold)
                niveau.gold += self.vie_bas // 2

            niveau.Nombre_Ennemis_Tue += 1
            return True
        return False
