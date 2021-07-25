import pygame as pg

from models.screen import Screen
from models.level import Level
from models.gameOptions import GameOptions
from models.character import Character


class GameUI:
    def __init__(self):
        self.font = GameOptions.getInstance().fonts["MedievalSharp-xOZ5"]["20"]

        self.stats_background = pg.image.load("assets/images/stats_background.png")
        self.update()

    def update(self):
        level = Level.getInstance()
        character = Character.getInstance()

        self.gold_amount = self.font.render("Or : %i" % level.gold, 1, (0, 0, 0))
        # self.bastion_health = self.font.render("Bastion : %i pv." % level.Vie_Chateau, 1, (0, 0, 0))
        self.character_level = self.font.render("Niveau %i" % character.level, 1, (0, 0, 0))
        self.ennemies_killed = self.font.render("Victimes : %i" % level.killed_ennemies, 1, (0, 0, 0))
        self.character_damage = self.font.render("Dégats : %i" % character.damage, 1, (0, 0, 0))
        self.character_speed = self.font.render("Vitesse : %i " % character.speed, 1, (0, 0, 0))

    def draw(self, screen: Screen):
        screen.blit(self.stats_background, (870, 0))

        screen.blit(self.gold_amount, (872, 5))
        # screen.blit(self.bastion_health, (872, 27))
        screen.blit(self.character_speed, (872, 54))
        screen.blit(self.character_level, (1020, 3))
        screen.blit(self.ennemies_killed, (1020, 27))
        screen.blit(self.character_damage, (1020, 53))
