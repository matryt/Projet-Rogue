import Element
import importlib
import random

theGame = importlib.import_module("theGame")


class Chest(Element.Element):
    """
    Coffre contenanr des items de niveau supérieur et de l'or

    Attributes:
    _name : str
                    Le nom du coffre
    _abbrv : str
                    L'abréviation représentant le coffre
    """

    def __init__(self, chestopened=False, size="normal"):
        super().__init__("Chest", "M")
        self.chestopened = chestopened
        self.size = size

    def normalChestMeet(self, hero):
        i = 0
        keyFound = False
        while i < len(hero.getInventory()) and not keyFound:
            obj = hero.getInventory()[i]
            if obj.getName() == "key":
                levelGame = theGame.theGame().getLevel()
                self.chestopened = True
                Totalequipments = theGame.theGame().equipments
                theGame.theGame().addMessage("you open the chest with the key")
                theGame.theGame().addMessage("wowie, you just gained gold and stuff : ")
                hero.GoldCount += random.randint(5 * levelGame, 25 * levelGame)
                for rarete in Totalequipments:
                    if rarete == 2 * levelGame or len(hero.getInventory()) <= 10:
                        hero.take(Totalequipments[rarete][random.randint(0, len(Totalequipments[rarete]) - 1)])
                        print()

                hero.removeFromInventory(obj)
                keyFound = True
            i += 1
        if self.chestopened:
            theGame.theGame().addMessage("the chest has been opened")
            return

        theGame.theGame().addMessage("it seems that a key is needed to open this chest")

    def bigChestMeet(self, hero):
        for obj in hero.getInventory():
            if obj.getName() == "key":
                levelGame = theGame.theGame().getLevel()
                self.chestopened = True
                Totalequipments = theGame.theGame().equipments
                theGame.theGame().addMessage("you open the chest with the key")
                theGame.theGame().addMessage("wowie, you just gained a lot of gold and rare stuff : ")
                hero.GoldCount += random.randint(5 * levelGame, 25 * levelGame)
                for rarete in Totalequipments:
                    if rarete == 2 * levelGame or True:
                        hero.take(Totalequipments[rarete][random.randint(3, len(Totalequipments[rarete]) - 1)])
                        print()
                # if creature._inventory == 10:

                hero.removeFromInventory(obj)

        if self.chestopened:
            theGame.theGame().addMessage("the luxurious chest has been opened")
            return
        theGame.theGame().addMessage("it seems that a key is needed to open this luxurious chest ! ")

    def meet(self, hero):
        """Permet d'ouvrir le coffre à condition d'avoir une clé'"""
        if self.chestopened:
            theGame.theGame().addMessage("the chest has already been opened")
            return
        if self.size == "normal":
            self.normalChestMeet(hero)
            return

        # note: on supprimera plutot le coffre, c'est plus simple mais dans l'ideal on preferera le laisser sur la map,ouvert.

        if self.size == "big":
            self.bigChestMeet(hero)
            return
