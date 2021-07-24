import pygame
import random
import time
import math

import src.constantes as constantes

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

        self.targetCoordx = 576
        self.targetCoordy = 352
        self.objectif = 10

        self.i = 0
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
        self.Vitesse = 5

        self.Is_Returned = False
        self.target = None
        self.Anim_King = False
        self.Anim_King_Ret = False
        self.capacite1 = False
        self.capacite2 = False
        self.AnimAttak = False
        self.IsMoving = False

        self.animations = {
            "walk": ImageAnimation((0, 0), True),
            "attack": ImageAnimation((0, 0), True)
        }


        self.Perso_Tab = [self.King_1, self.King_2, self.King_3, self.King_4, self.King_5, self.King_6]
        self.Perso_Tab_ret = [
            self.King_1_ret,
            self.King_2_ret,
            self.King_3_ret,
            self.King_4_ret,
            self.King_5_ret,
            self.King_6_ret,
        ]

        self.nanim = self.King_1

        self.posx_Old = None
        self.posy_Old = None

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
            self.Vitesse = self.Level_Roi * 0.25 + 5
            return True
        return False

    def anim(self):
        """Animates the character"""
        if self.i == 12:
            self.i = 0
        self.nanim = self.Perso_Tab[self.i // 2]
        self.Is_Returned = False

    def anim_ret(self):
        """Animates the character flipped"""
        if self.i == 12:
            self.i = 0
        self.nanim = self.Perso_Tab_ret[self.i // 2]
        self.Is_Returned = True

    def AnimKingAttakRet(self, Liste_Mechants, niveau):
        """Animates an attacked flipped

        Args:
            Liste_Mechants ([type]): [description]
            niveau ([type]): [description]
            Coin ([type]): [description]
        """
        self.Anim_King_i += 1

        if self.Anim_King_i == 8:
            self.i = 6
            self.anim_ret()
            self.Anim_King_i = 0
            self.Is_Returned = True
            self.AnimAttak = False

            if not self.target:
                self.AnimAttak = False

        elif self.Anim_King_i >= 4:
            self.nanim = self.King_Attak2_ret
            if self.target.enleve_vie(self.Degats / 4, Liste_Mechants, self.target, niveau, self):
                self.XpToAdd += self.target.vie_bas / 3
                self.target = False

        elif self.Anim_King_i >= 1:
            self.nanim = self.King_Attak_ret

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

    def AnimMenus(self, Liste_Mechants, niveau):
        """Animates the character in the menu

        Args:
            Liste_Mechants ([type]): [description]
            niveau ([type]): [description]
        """
        self.Vitesse = 10

        if not Liste_Mechants:
            TimeElapsed = time.process_time() - self.T0
            self.T0 = time.process_time()
            self.TimeCounter += TimeElapsed

            if self.TimeCounter >= random.randrange(4, 10):
                self.TimeCounter = 0
                self.targetCoordx = random.randrange(1056)
                self.targetCoordy = random.randrange(608)
        else:
            self.target = Liste_Mechants[0]
            Liste_Mechants[0].IsAttacked = True
        self.vit(Liste_Mechants, niveau)

    def update(self, timeElapsed):
        if self.capacite1:
            Icapacite1 += 1
            if Icapacite1 == 160:
                Icapacite1 = 0
                King.capacite1 = False

        LvlUp = self.level_up()
        if CooldownInvoc > 0:
            CooldownInvoc -= 1
        TpsCoolDown = CooldownInvoc // 24

        # Augmentation du niveau
        if LvlUp:

            AfficheLvlUp = True

            King.Degats = King.Level_Roi * 0.5 + 3
            King.Vitesse = King.Level_Roi * 0.25 + 5


    def vit(self, Liste_Mechants, niveau):
        """Updates the status of the character

        Args:
            Liste_Mechants ([type]): [description]
            niveau ([type]): [description]
        """
        self.AnimXp()

        if self.AnimAttak:
            if self.Is_Returned:
                self.AnimKingAttakRet(Liste_Mechants, niveau)
            elif not self.Is_Returned:
                self.AnimKingAttak(Liste_Mechants, niveau)

        elif self.target:
            self.targetCoordx = self.target.PosAbsolue[0]
            self.targetCoordy = self.target.PosAbsolue[1]

            if (
                math.sqrt(
                    ((self.posx - self.target.PosAbsolue[0]) ** 2) + ((self.posy - self.target.PosAbsolue[1]) ** 2)
                )
                > self.Vitesse
            ):

                self.AnimAttak = False
                delta_y = self.target.PosAbsolue[1] - self.posy
                delta_x = self.target.PosAbsolue[0] - self.posx

                if delta_x != 0:
                    angle = math.atan(delta_y / delta_x)
                else:
                    if delta_y < 0:
                        angle = -math.pi / 2
                    else:
                        angle = math.pi / 2

                if delta_x < 0:
                    angle = angle + math.pi
                    self.Is_Returned = True

                else:
                    self.Is_Returned = False

                self.posx_Old = self.posx
                self.posy_Old = self.posy

                self.posy = self.posy + math.sin(angle) * self.Vitesse
                self.posx = self.posx + math.cos(angle) * self.Vitesse

                self.i += 1
                if self.Is_Returned:
                    self.anim_ret()
                else:
                    self.anim()
            else:
                self.AnimAttak = True

        else:

            if (
                math.sqrt(((self.posx - self.targetCoordx) ** 2) + ((self.posy - self.targetCoordy) ** 2))
                > self.Vitesse
            ):

                delta_y = self.targetCoordy - self.posy
                delta_x = self.targetCoordx - self.posx

                if delta_x != 0:
                    angle = math.atan(delta_y / delta_x)
                else:
                    if delta_y < 0:
                        angle = -math.pi / 2
                    else:
                        angle = math.pi / 2

                if delta_x < 0:
                    angle = angle + math.pi
                    self.Is_Returned = True

                else:
                    self.Is_Returned = False

                self.posx_Old = self.posx
                self.posy_Old = self.posy

                self.posy = self.posy + math.sin(angle) * self.Vitesse
                self.posx = self.posx + math.cos(angle) * self.Vitesse

                self.i += 1
                if self.Is_Returned:
                    self.anim_ret()
                else:
                    self.anim()
