import pygame
import src.constantes as constantes
from src.gold import GoldAnim
from src.utils.bound import bound

from models.level import Level

from UI.components.imageAnimation import ImageAnimation
from UI.components.loading_bar import LoadingBar


class EnnemyDO:
    """Represent an in game ennemy, keeps the health etc..."""

    def __init__(self, data):
        self.position = (0, 0)
        self.count = 0
        self.PosAbsolue = (0, 0)

        self.Returned = False
        self.is_attacked = False
        self.BlitLife = False

        self.direction = (1, 0)
        self.Tics = 0

        self.pose_ennemi()

        self.propriete = data

        self.name = self.propriete["Name"]
        # self.meurt = pygame.mixer.Sound(self.propriete["DeathSound"])
        self.health = self.propriete["LifePts"]
        self.max_health = self.propriete["LifePts"]
        self.speed = self.propriete["speed"]
        self.height = self.propriete["Height"]

        print(self.height)
        self.healthBar = LoadingBar(
            (0, 0),
            (self.height, 5),
            max_val=self.max_health, initial_val=self.max_health
        )
        self.animation = ImageAnimation(
            self.propriete["ImgFolder"], flippable=True, speed=self.propriete["animation_speed"])

        self.HitBox = None
        self.Vie_Rect = None

    def pose_ennemi(self):
        """Adds an ennemy to the game

        Args:
            tableau ([type]): [description]
        """
        self.position = (0, 0)
        level = Level.getInstance()
        self.direction = (1, 0)

        x = 0
        for y in range(11):
            tile = level.map[x][y]
            if tile is not None and (tile.code, tile.rotation) == ("c1", 0):
                self.position = (0, y)
                self.PosAbsolue = (0, y * 64)
                self.HitBox = pygame.Rect((0, y), (64, 64))

    def draw(self, screen):
        """Blits the ennemy on the screen

        Args:
            screen ([type]): [description]
        """
        if self.is_attacked:
            self.healthBar.draw(screen, self.PosAbsolue)
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
        self.animation.update(timeElapsed)
        self.healthBar.update(timeElapsed)

        level = Level.getInstance()

        if self.is_attacked:
            self.Tics += 1
        if self.Tics == 50:
            self.is_attacked = False
            self.Tics = 0

        self.count += self.speed * 64 * timeElapsed
        if self.count >= 64:

            self.count = 0
            self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])

            if level.hitBastion(self.position, damage=(self.health / 2)):
                self.hit(2000)
            else:
                tile = level.map[self.position[0]][self.position[1]]
                new_dir = tile.direction()
                if new_dir is None:
                    self.pose_ennemi()
                elif new_dir != (0, 0):
                    if new_dir[0] != self.direction[0]:
                        self.animation.flip()
                    self.direction = new_dir

        self.PosAbsolue = (
            self.position[0] * 64 + (self.count * self.direction[0]),
            self.position[1] * 64 + (self.count * self.direction[1]),
        )
        self.HitBox = pygame.Rect(self.PosAbsolue, (64, 64))

    def hit(self, damage: int):
        """Hits the ennemy with the given amount of damage

        Args:
            damage (int): The amount of damage to deal
        """
        self.health -= damage
        self.health = bound(0, self.max_health, self.health)
        self.is_attacked = True
        self.healthBar.set_advancement(self.health)

    @property
    def alive(self) -> bool:
        """Returns true if the ennemy is alive"""
        return self.health > 0

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
        self.health -= viemoins
        self.is_attacked = True
        self.Tics = 0

        if self.health <= 0:
            constantes.DicoEnnemisKilled[self.name] += 1
            liste_mech.remove(ennemi)
            # self.meurt.play()
            if King.capacite1 is True:
                FlyingGold = GoldAnim(
                    (self.PosAbsolue[0] + self.height // 2, self.PosAbsolue[1] + self.height // 2), self.max_health
                )
                constantes.GoldGained[0] += self.max_health
                niveau.GoldTab.append(FlyingGold)
                niveau.gold += self.max_health

            else:
                FlyingGold = GoldAnim((self.PosAbsolue[0] + 32, self.PosAbsolue[1] + 32), self.max_health // 2)
                constantes.GoldGained[0] += self.max_health // 2
                niveau.GoldTab.append(FlyingGold)
                niveau.gold += self.max_health // 2

            niveau.Nombre_Ennemis_Tue += 1
            return True
        return False
