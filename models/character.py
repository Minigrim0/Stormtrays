import pygame as pg
import time
import math

from src.ennemy import EnnemyDO
from src.utils.distance_between import distance_between
from src.utils.findAngle import findAngle

from models.screen import Screen

from UI.components.imageAnimation import ImageAnimation


class Character:
    """Reprensents the user's character"""

    instance = None

    @staticmethod
    def getInstance():
        if Character.instance is None:
            Character()
        return Character.instance

    def __init__(self):
        if Character.instance is not None:
            raise RuntimeError("Trying to instanciate a second object of a singleton class")
        Character.instance = self

        self.target = (576, 352)  # Either a position or an ennemy
        self.objectif = 10

        self.posx = 0
        self.posy = 0
        self.xp = 0
        self.Level_Roi = 0
        self.Anim_King_i = 0
        self.XpToAdd = 0
        self.TimeCounter = 0
        self.TimeElapsed = 0
        self.T0 = time.process_time()

        self.XpToAdd = 0
        self.xp = 0
        self.objectif = 10
        self.Level_Roi = 0
        self.Degats = 3
        self.speed = 75

        self.Is_Returned = False
        self.Anim_King = False
        self.Anim_King_Ret = False
        self.capacite1 = False
        self.capacite2 = False
        self.AnimAttak = False
        self.IsMoving = False

        self.animations = {
            "idle": ImageAnimation("assets/images/character/animations/idle/", True),
            "walk": ImageAnimation("assets/images/character/animations/walk/", True, speed=5),
            "attack": ImageAnimation("assets/images/character/animations/attack/", True, speed=3),
            "invoke": ImageAnimation("assets/images/character/animations/invoke/", True, speed=5)
        }
        self.current_animation = "idle"

        self.posx_Old = None
        self.posy_Old = None

    def getCurrentAnimation(self):
        return self.animations[self.current_animation]

    def level_up(self):
        """Upgrades the character skills

        Returns:
            [type]: [description]
        """
        if self.xp >= self.objectif:
            self.xp = self.xp - self.objectif
            self.Level_Roi += 1

            self.objectif = (self.Level_Roi ** 2) * 20
            self.Degats = self.Level_Roi * 0.5 + 3
            self.speed = self.Level_Roi * 0.25 + 5
            return True
        return False

    def AnimKingAttak(self, Liste_Mechants, niveau):
        """Animates an attack

        Args:
            Liste_Mechants ([type]): [description]
            niveau ([type]): [description]
            Coin ([type]): [description]
        """
        self.Anim_King_i += 1

        if self.Anim_King_i == 8:
            self.i = 6
            self.anim()
            self.Anim_King_i = 0
            self.Is_Returned = False
            self.AnimAttak = False

            if not self.target:
                self.AnimAttak = False

        elif self.Anim_King_i >= 4:
            self.nanim = self.King_Attak2
            if self.target.enleve_vie(self.Degats / 4, Liste_Mechants, self.target, niveau, self):
                self.XpToAdd += self.target.vie_bas / 3
                self.target = False

        elif self.Anim_King_i >= 1 and self.Anim_King_i < 4:
            self.nanim = self.King_Attak

    def AnimXp(self):
        """Animates the xp adding"""
        if self.XpToAdd > 90:
            self.XpToAdd -= 10
            self.xp += 10
        elif self.XpToAdd <= 90 and self.XpToAdd > 70:
            self.XpToAdd -= 9
            self.xp += 9
        elif self.XpToAdd <= 70 and self.XpToAdd > 50:
            self.XpToAdd -= 7
            self.xp += 7
        elif self.XpToAdd <= 50 and self.XpToAdd > 30:
            self.XpToAdd -= 5
            self.xp += 5
        elif self.XpToAdd <= 30 and self.XpToAdd > 10:
            self.XpToAdd -= 3
            self.xp += 3
        elif self.XpToAdd <= 10 and self.XpToAdd > 0:
            self.XpToAdd -= 1
            self.xp += 1

    def update(self, timeElapsed):
        """if self.capacite1:
            Icapacite1 += 1
            if Icapacite1 == 160:
                Icapacite1 = 0
                King.capacite1 = False

        if CooldownInvoc > 0:
            CooldownInvoc -= 1
        TpsCoolDown = CooldownInvoc // 24
        """
        if self.level_up():
            self.Degats = self.Level_Roi * 0.5 + 3
            self.speed = self.Level_Roi * 0.25 + 5

        self.move(timeElapsed)
        self.getCurrentAnimation().update(timeElapsed)

    def handleEvent(self, event: pg.event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            self.target = event.pos

    def draw(self, screen: Screen):
        self.getCurrentAnimation().draw(screen, (self.posx, self.posy), centered=True)

    def move(self, timeElapsed: float):
        """Updates the status of the character"""
        # self.AnimXp()

        if isinstance(self.target, EnnemyDO):
            if distance_between(self.target.position, (self.posx, self.posy)) > 10:
                delta_x = self.target.PosAbsolue[0] - self.posx
                delta_y = self.target.PosAbsolue[1] - self.posy

                angle = findAngle(delta_x, delta_y)

                movement_x = math.cos(angle) * self.speed * timeElapsed
                movement_y = math.sin(angle) * self.speed * timeElapsed

                self.posx += movement_x
                self.posy += movement_y

                self.getCurrentAnimation().setDirection(movement_x > 0)
                self.current_animation = "walk"
            else:
                self.current_animation = "attack"
        else:
            if distance_between(self.target, (self.posx, self.posy)) > 10:
                delta_x = self.target[0] - self.posx
                delta_y = self.target[1] - self.posy

                angle = findAngle(delta_x, delta_y)

                movement_x = math.cos(angle) * self.speed * timeElapsed
                movement_y = math.sin(angle) * self.speed * timeElapsed

                self.posx += movement_x
                self.posy += movement_y

                self.getCurrentAnimation().setDirection(movement_x > 0)
                self.current_animation = "walk"
            else:
                self.current_animation = "idle"
