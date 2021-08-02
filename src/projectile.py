class Projectile:
    """Represents a projectile launched by a tower"""

    def __init__(self, t, tower, ennemi):
        self.vitesse = tower.vitesse_Projectile

        image2rot = pygame.image.load(tower.Projectile_Image).convert_alpha()

        NewPosEnnemi_x = ennemi.PosAbsolue[0] + ennemi.vitesse * ennemi.Dir_x * t
        NewPosEnnemi_y = ennemi.PosAbsolue[1] + ennemi.vitesse * ennemi.Dir_y * t

        self.delta_x = NewPosEnnemi_x - tower.Position_IG[0] * 64
        self.delta_y = NewPosEnnemi_y - tower.Position_IG[1] * 64

        self.Dist = math.sqrt(self.delta_x ** 2 + self.delta_y ** 2)

        if self.delta_x != 0:
            Angle = -math.atan(self.delta_y / self.delta_x)
            if self.delta_x > 0:
                Angle -= math.pi
            Angle = Angle * 180 / math.pi
        else:
            if ennemi.posy < tower.Position_IG[1]:
                Angle = -90
            else:
                Angle = 90

        self.image = utils.rot_center(image2rot, Angle)

        self.Centre_d_x = (NewPosEnnemi_x + tower.Position_IG[0] * 64) / 2
        self.Centre_d_y = (NewPosEnnemi_y + tower.Position_IG[1] * 64) / 2

        self.degats = tower.degats

        self.Compteur = -1

        self.tower = tower

    def Avance(self, fenetre, ListeEnnemis, niveau, Tab_Projectile, King):
        """Makes a projectile move

        Args:
            fenetre ([type]): [description]
            ListeEnnemis ([type]): [description]
            niveau ([type]): [description]
            Tab_Projectile ([type]): [description]
            King ([type]): [description]
        """
        self.Compteur += 2 * self.vitesse / self.Dist

        x0 = self.Centre_d_x + self.Compteur * (self.delta_x / 2)
        y0 = self.Centre_d_y + self.Compteur * (self.delta_y / 2)

        h = (1 - self.Compteur ** 2) * self.tower.RoundTraj * self.Dist

        x = x0
        y = y0 - h

        fenetre.blit(self.image, (x, y))

        if self.Compteur >= 1:
            for ennemi in ListeEnnemis:
                dist = math.sqrt(((x - ennemi.PosAbsolue[0]) ** 2) + ((y - ennemi.PosAbsolue[1]) ** 2))
                if dist < 64:
                    died = ennemi.enleve_vie(self.degats, ListeEnnemis, ennemi, niveau, King)
                    if died:
                        self.tower.EnnemiKilled += 1
                    self.tower.TotalDegats += self.degats
                    if self.tower.Zone_Degats != "Y":
                        break
            Tab_Projectile.remove(self)
