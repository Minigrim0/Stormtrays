import pygame
from src.constantes import Invocation_Attak, Invocation_Attak2, InvocationRet_Attak, InvocationRet_Attak2, Invocation_1
from src.utils import findAngle
import math


class Invocation:
    """
    The character power after level 5, a basic "AI"
    that will attack the first ennemy it sees
    """

    def __init__(self, Tab, Tab_Ret, King):
        self.myfont = pygame.font.SysFont("Viner Hand ITC", 25)
        self.Img = pygame.image.load(Invocation_1).convert_alpha()
        self.nanim = pygame.transform.scale(self.Img, (int(96), int(96)))

        self.Duree_Invocation = King.Level_Roi * 4
        self.degats = King.Level_Roi * 1.5

        self.i = 0
        self.tic = 0
        self.Anim_King_i = 0
        self.Is_Returned = False
        self.posx = King.posx
        self.posy = King.posy

        self.InvocationAttak = pygame.image.load(Invocation_Attak).convert_alpha()
        self.InvocationAttak2 = pygame.image.load(Invocation_Attak2).convert_alpha()

        self.InvocationRetAttak = pygame.image.load(InvocationRet_Attak).convert_alpha()
        self.InvocationRetAttak2 = pygame.image.load(InvocationRet_Attak2).convert_alpha()

        self.Invocation_Attak = pygame.transform.scale(self.InvocationAttak, (int(96), int(96)))
        self.Invocation_Attak2 = pygame.transform.scale(self.InvocationAttak2, (int(96), int(96)))

        self.Invocation_Attak_ret = pygame.transform.scale(self.InvocationRetAttak, (int(96), int(96)))
        self.Invocation_Attak2_ret = pygame.transform.scale(self.InvocationRetAttak2, (int(96), int(96)))

        self.Tab = Tab
        self.TabRet = Tab_Ret

        self.xp = 0

        self.posx_Old = None
        self.posy_Old = None

    def vit(self, fenetre, Liste_Mechants, niveau, coin, King):
        """Updates the AI, making it move and attack

        Args:
            fenetre ([type]): [description]
            Liste_Mechants ([type]): [description]
            niveau ([type]): [description]
            coin ([type]): [description]
            King ([type]): [description]

        Returns:
            [type]: [description]
        """
        self.tic += 1

        TimeLeftPrint = self.myfont.render(str(self.Duree_Invocation), 1, (0, 0, 25))

        if self.tic == 24:
            self.Duree_Invocation -= 1
            self.tic = 0

        if Liste_Mechants:
            self.bouge_vers_ennemi(Liste_Mechants[0], Liste_Mechants, niveau, fenetre, King)

        if self.Duree_Invocation == 0:
            return False

        fenetre.blit(self.nanim, (self.posx, self.posy))
        fenetre.blit(TimeLeftPrint, (self.posx, self.posy))
        return True

    def bouge_vers_ennemi(self, ennemi, Liste_Mechants, niveau, fenetre, King):
        """Detects first ennemy and make the AI move towards it

        Args:
            ennemi ([type]): [description]
            Liste_Mechants ([type]): [description]
            niveau ([type]): [description]
            fenetre ([type]): [description]
            King ([type]): [description]
        """
        dist = math.sqrt(((self.posx - ennemi.PosAbsolue[0]) ** 2) + ((self.posy - ennemi.PosAbsolue[1]) ** 2))

        if dist > 32 and self.Anim_King_i == 0:
            delta_y = ennemi.PosAbsolue[1] - self.posy
            delta_x = ennemi.PosAbsolue[0] - self.posx

            angle = findAngle(delta_x, delta_y)

            if delta_x < 0:
                self.Is_Returned = True
            else:
                self.Is_Returned = False

            self.posx_Old = self.posx
            self.posy_Old = self.posy

            self.posy = self.posy + math.sin(angle) * 10
            self.posx = self.posx + math.cos(angle) * 10

            self.i += 1

            if self.Is_Returned:
                self.anim_ret(self.TabRet)
            else:
                self.anim(self.Tab)

            self.Anim_King_i = 0

        else:
            if not self.Is_Returned:
                self.Anim_King_i += 1
                if self.Anim_King_i == 1:
                    self.nanim = self.Invocation_Attak
                    fenetre.blit(self.nanim, (self.posx, self.posy))
                elif self.Anim_King_i == 3:
                    self.nanim = self.Invocation_Attak2
                    fenetre.blit(self.nanim, (self.posx, self.posy))
                elif self.Anim_King_i == 6:
                    self.i = 6
                    self.anim(self.Tab)
                    fenetre.blit(self.nanim, (self.posx, self.posy))
                    self.Anim_King_i = 0
                    ennemi.enleve_vie(self.degats, Liste_Mechants, ennemi, niveau, King)
                    if ennemi.vie - self.degats <= 0:
                        self.xp += ennemi.vie_bas / 3

                self.Is_Returned = False
            else:
                self.Anim_King_i += 1
                if self.Anim_King_i == 1:
                    self.nanim = self.Invocation_Attak_ret
                    fenetre.blit(self.nanim, (self.posx, self.posy))
                elif self.Anim_King_i == 3:
                    self.nanim = self.Invocation_Attak2_ret
                    fenetre.blit(self.nanim, (self.posx, self.posy))
                elif self.Anim_King_i == 6:
                    self.i = 6
                    self.anim(self.TabRet)
                    fenetre.blit(self.nanim, (self.posx, self.posy))
                    self.Anim_King_i = 0
                    ennemi.enleve_vie(self.degats, Liste_Mechants, ennemi, niveau, King)
                    if ennemi.vie - self.degats <= 0:
                        self.xp += ennemi.vie_bas / 3
                self.Is_Returned = True

    def anim(self, tab):
        """Animates the AI's sprites

        Args:
            tab ([type]): [description]
        """
        if self.i == 12:
            self.i = 0
        self.nanim = tab[self.i // 2]
        self.Is_Returned = False

    def anim_ret(self, tab):
        """Animates the AI's sprites flipped

        Args:
            tab ([type]): [description]
        """
        if self.i == 12:
            self.i = 0
        self.nanim = tab[self.i // 2]
        self.Is_Returned = True
