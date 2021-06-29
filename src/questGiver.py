import pygame
import pygame.locals
from constantes import GoldGained, DicoTowersBought, DicoEnnemisKilled
import json


class QuestGiver:
    """The quest giver character"""

    def __init__(self, FilePath):
        f = open(FilePath, "r")
        Postl = f.read()
        Posx = ""
        Posy = ""
        FichierPath = ""
        y = 0
        for char in Postl:
            if char == "\n":
                y += 1
            elif y == 1:
                if char != "/":
                    Posx += char
                else:
                    y = 2
            elif y == 2:
                Posy += char
            elif y == 3:
                FichierPath += char

        self.Posx = int(Posx)
        self.Posy = int(Posy)
        self.i = 0
        self.tics = 0

        self.font = pygame.font.SysFont("Viner Hand ITC", 15)
        self.fontQuests = pygame.font.SysFont("Viner Hand ITC", 30)
        self.HitBox = pygame.Rect((self.Posx, self.Posy), (64, 64))

        self.ObjectifDone = [False, False, False]
        self.Recompensegave = [False, False, False]
        self.DoesBlitQuest = False
        self.CompteurAfficheQuetes = 0

        self.TabQuestsNames = []
        self.TabQuestsObjectives = []
        self.TabQuestsTypes = []
        self.TabQuestsNum = []
        self.TabImg = []
        self.Image = pygame.image.load("../Img/QuestGiverF1.png").convert_alpha()
        self.FontTxt = pygame.image.load("../Img/QuestsFont.png").convert_alpha()
        self.TabImg.append(pygame.image.load("../Img/QuestGiverF1.png").convert_alpha())
        self.TabImg.append(pygame.image.load("../Img/QuestGiverF2.png").convert_alpha())
        self.TabImg.append(pygame.image.load("../Img/QuestGiverF3.png").convert_alpha())
        self.TabImg.append(pygame.image.load("../Img/QuestGiverF1.png").convert_alpha())
        self.TabImg.append(pygame.image.load("../Img/QuestGiverF2.png").convert_alpha())
        self.TabImg.append(pygame.image.load("../Img/QuestGiverF3.png").convert_alpha())

        self.IsGiving = False

    def LoadQuests(self, filename):
        """Loads the quests from a json file

        Args:
            filename ([type]): [description]
        """
        with open("../level/QuestFiles/" + filename + ".json") as f:
            self.propriete = json.loads(f.read())

        self.TabQuestsNames.append(self.propriete["FirstQuestName"])
        self.TabQuestsNames.append(self.propriete["SecondQuestName"])
        self.TabQuestsNames.append(self.propriete["ThirdQuestName"])

        self.TabQuestsObjectives.append(int(self.propriete["FirstQuestObjectif"]))
        self.TabQuestsObjectives.append(int(self.propriete["SecondQuestObjectif"]))
        self.TabQuestsObjectives.append(int(self.propriete["ThirdQuestObjectif"]))

        self.TabQuestsTypes.append(self.propriete["FirstTypeObjectif"])
        self.TabQuestsTypes.append(self.propriete["SecondTypeObjectif"])
        self.TabQuestsTypes.append(self.propriete["ThirdTypeObjectif"])

        self.TabQuestsNum.append(self.propriete["FirstNumObjectif"])
        self.TabQuestsNum.append(self.propriete["SecondNumObjectif"])
        self.TabQuestsNum.append(self.propriete["ThirdNumObjectif"])

    def GiveRecompense(self, XPtoAdd):
        """Gives a reward to the user when he reached the goal

        Args:
            XPtoAdd ([type]): [description]
        """
        for x in range(3):
            if self.ObjectifDone[x] and not self.Recompensegave[x]:
                self.Recompensegave[x] = True
                XPtoAdd += 500

    def Live(self, fenetre):
        """Updates the quest giver status

        Args:
            fenetre ([type]): [description]
        """
        fenetre.blit(self.Image, (self.Posx, self.Posy))

        if self.DoesBlitQuest:
            fenetre.blit(self.QuestFinished, (10, 10))
            self.CompteurAfficheQuetes -= 1
            if self.CompteurAfficheQuetes == 0:
                self.DoesBlitQuest = False

        if self.IsGiving:
            self.i += 1
            if self.i == 18:
                self.i = 0
                self.tics += 1

            if self.tics == 5:
                self.i = 0
                self.tics = 0

            TabNumsQuestsTxt = []
            x = 0
            for Objectives in self.TabQuestsObjectives:
                if Objectives == 1:
                    if int(self.TabQuestsTypes[x]) == 1:
                        if DicoTowersBought["Archer"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(str(DicoTowersBought["Archer"]), str(int(self.TabQuestsNum[x]))),
                                    1,
                                    (0, 0, 0),
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(str(int(self.TabQuestsNum[x])), str(int(self.TabQuestsNum[x]))),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 2:
                        if DicoTowersBought["Catapulte Basique"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(
                                        str(DicoTowersBought["Catapulte Basique"]), str(int(self.TabQuestsNum[x]))
                                    ),
                                    1,
                                    (0, 0, 0),
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(int(self.TabQuestsNum[x]), int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 3:
                        if DicoTowersBought["Catapulte Precise"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(DicoTowersBought["Catapulte Precise"], int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 0, 0),
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(int(self.TabQuestsNum[x]), int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 4:
                        if DicoTowersBought["Catapulte Rapide"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(DicoTowersBought["Catapulte Rapide"], int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 0, 0),
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(int(self.TabQuestsNum[x]), int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 5:
                        if DicoTowersBought["Catapulte tres rapide"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(
                                        DicoTowersBought["Catapulte tres rapide"], int(self.TabQuestsNum[x])
                                    ),
                                    1,
                                    (0, 0, 0),
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(int(self.TabQuestsNum[x]), int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 6:
                        if DicoTowersBought["Baliste"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(DicoTowersBought["Baliste"], int(self.TabQuestsNum[x])), 1, (0, 0, 0)
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(int(self.TabQuestsNum[x]), int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                elif Objectives == 2:
                    if int(self.TabQuestsTypes[x]) == 7:
                        if DicoEnnemisKilled["Wolf"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(DicoEnnemisKilled["Wolf"]) + "/" + str(int(self.TabQuestsNum[x])), 1, (0, 0, 0)
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(int(self.TabQuestsNum[x])) + "/" + str(int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 8:
                        if DicoEnnemisKilled["Goblin"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(DicoEnnemisKilled["Goblin"]) + "/" + str(int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 0, 0),
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(int(self.TabQuestsNum[x])) + "/" + str(int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 9:
                        if DicoEnnemisKilled["Golem"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(DicoEnnemisKilled["Golem"]) + "/" + str(int(self.TabQuestsNum[x])), 1, (0, 0, 0)
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(int(self.TabQuestsNum[x])) + "/" + str(int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 10:
                        if DicoEnnemisKilled["Orc"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(DicoEnnemisKilled["Orc"]) + "/" + str(int(self.TabQuestsNum[x])), 1, (0, 0, 0)
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(int(self.TabQuestsNum[x])) + "/" + str(int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 11:
                        if DicoEnnemisKilled["Knight"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(DicoEnnemisKilled["Knight"]) + "/" + str(int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 0, 0),
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(int(self.TabQuestsNum[x])) + "/" + str(int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 12:
                        if DicoEnnemisKilled["Dwarf"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(DicoEnnemisKilled["Dwarf"]) + "/" + str(int(self.TabQuestsNum[x])), 1, (0, 0, 0)
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(int(self.TabQuestsNum[x])) + "/" + str(int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 13:
                        if DicoEnnemisKilled["Dragon"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(DicoEnnemisKilled["Dragon"]) + "/" + str(int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 0, 0),
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(int(self.TabQuestsNum[x])) + "/" + str(int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True
                    elif int(self.TabQuestsTypes[x]) == 14:
                        if DicoEnnemisKilled["Ghost"] < int(self.TabQuestsNum[x]):
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(DicoEnnemisKilled["Ghost"]) + "/" + str(int(self.TabQuestsNum[x])), 1, (0, 0, 0)
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    str(int(self.TabQuestsNum[x])) + "/" + str(int(self.TabQuestsNum[x])),
                                    1,
                                    (0, 200, 50),
                                )
                            )
                            self.ObjectifDone[x] = True

                elif Objectives == 3:
                    if GoldGained[0] < int(self.TabQuestsNum[x]):
                        if GoldGained[0] > 1000000:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}M/{}".format(str(GoldGained[0] // 1000000), str(int(self.TabQuestsNum[x]))),
                                    1,
                                    (0, 0, 0),
                                )
                            )
                        elif GoldGained[0] > 1000:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}K/{}".format(str(GoldGained[0] // 1000), str(int(self.TabQuestsNum[x]))),
                                    1,
                                    (0, 0, 0),
                                )
                            )
                        else:
                            TabNumsQuestsTxt.append(
                                self.font.render(
                                    "{}/{}".format(str(GoldGained[0]), str(int(self.TabQuestsNum[x]))), 1, (0, 0, 0)
                                )
                            )
                    else:
                        TabNumsQuestsTxt.append(
                            self.font.render(
                                "{}/{}".format(str(int(self.TabQuestsNum[x])), str(int(self.TabQuestsNum[x]))),
                                1,
                                (0, 200, 50),
                            )
                        )
                        self.ObjectifDone[x] = True

                x += 1

            fenetre.blit(self.FontTxt, (self.Posx - 180, self.Posy - 180))
            for x in range(3):
                QuestsTxt = self.font.render(self.TabQuestsNames[x], 1, (0, 0, 0))
                fenetre.blit(QuestsTxt, (self.Posx - 170, self.Posy - 115 + x * 25))
                fenetre.blit(TabNumsQuestsTxt[x], (self.Posx - 25, self.Posy - 115 + x * 25))
                if self.ObjectifDone[x] and not self.Recompensegave[x]:
                    self.CompteurAfficheQuetes = 250
                    self.DoesBlitQuest = True
                    self.QuestFinished = self.fontQuests.render("Terminé : " + self.TabQuestsNames[x], 1, (200, 20, 20))

            self.Image = self.TabImg[self.i // 3]

        else:
            self.Image = self.TabImg[0]
