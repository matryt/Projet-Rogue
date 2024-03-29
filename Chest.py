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

    def meet(self, hero):
        """Permet d'ouvrir le coffre à condition d'avoir une clé'"""
        if self.chestopened:
            theGame.theGame().addMessage("the chest has already been opened")
            return
        if len(hero.getInventory()) > 10:
            return
        if self.size == "normal":
            i = 0
            keyFound = False
            while i < len(hero.getInventory()) and not keyFound:
                obj = hero.getInventory()[i]
                if obj.getName() == "key":
                    hero._inventory.remove(obj)
                    self.chestopened = True
                    Totalequipments = theGame.theGame().equipments
                    theGame.theGame().addMessage("you open the chest with the key")
                    theGame.theGame().addMessage("wowie, you just gained gold and stuff : ")
                    hero.GoldCount += random.randint(5 * theGame.theGame().getLevel(), 25 * theGame.theGame().getLevel())
                    for rarete in Totalequipments:
                        if len(hero.getInventory()) < 10:
                            hero.take(Totalequipments[rarete][random.randint(0, len(Totalequipments[rarete]) - 1)])

                    keyFound = True
                i += 1

            if self.chestopened:
                self._abbrv="Mo"
                theGame.theGame().addMessage("the chest has been opened")
                return
            theGame.theGame().addMessage("it seems that a key is needed to open this chest")

        if self.size == "big":
            for obj in hero.getInventory():
                if obj.getName() == "key":
                    hero.removeFromInventory(obj)
                    self.chestopened = True
                    Totalequipments = theGame.theGame().equipments
                    theGame.theGame().addMessage("you open the chest with the key")
                    theGame.theGame().addMessage("wowie, you just gained a lot of gold and rare stuff : ")
                    hero.GoldCount += random.randint(5 * theGame.theGame().getLevel(), 25 * theGame.theGame().getLevel())
                    for rarete in Totalequipments:
                        if len(hero.getInventory()) < 10:
                            try:
                                hero.take(Totalequipments[rarete][random.randint(3, len(Totalequipments[rarete]) - 1)])
                            except:
                                pass

            if self.chestopened:
                theGame.theGame().addMessage("the luxurious chest has been opened")
                return
            theGame.theGame().addMessage("it seems that a key is needed to open this luxurious chest ! ")

    def meetAffichage(self, hero):
        return self.meet(hero)


class Tresor(Chest):
    def __init__(self, chestopened=False):
        super().__init__(chestopened, "big")
        self._abbrv="M"

    def meet(self, hero):
        super().meet(hero)
