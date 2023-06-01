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
            theGame.theGame().addMessage(f"the chest has already been opened")
            return
        if self.size == "normal":
            i = 0
            keyFound = False
            while i < len(hero._inventory) and not keyFound:
                object = hero._inventory[i]
                if object._name == "key":
                    self.chestopened = True
                    Totalequipments = theGame.theGame().equipments
                    theGame.theGame().addMessage(f"you open the chest with the key")
                    theGame.theGame().addMessage(f"wowie, you just gained gold and stuff : ")
                    hero.GoldCount += random.randint(5 * theGame.theGame()._level, 25 * theGame.theGame()._level)
                    for rarete in Totalequipments:
                        if rarete == 2 * theGame.theGame()._level and len(hero.getInventory()) <= 10:
                            hero.take(Totalequipments[rarete][random.randint(0, len(Totalequipments[rarete]) - 1)])
                            print()

                    hero._inventory.remove(object)
                    keyFound = True
                i += 1

            if self.chestopened:
                self._abbrv="Mo"
                theGame.theGame().addMessage(f"the chest has been opened")
                return
            theGame.theGame().addMessage(f"it seems that a key is needed to open this chest")

        # note: on supprimera plutot le coffre, c'est plus simple mais dans l'ideal on preferera le laisser sur la map,ouvert.

        if self.size == "big":
            for object in hero._inventory:
                if object._name == "key":
                    self.chestopened = True
                    Totalequipments = theGame.theGame().equipments
                    theGame.theGame().addMessage(f"you open the chest with the key")
                    theGame.theGame().addMessage(f"wowie, you just gained a lot of gold and rare stuff : ")
                    hero.GoldCount += random.randint(5 * theGame.theGame()._level, 25 * theGame.theGame()._level)
                    for rarete in Totalequipments:
                        if rarete == 2 * theGame.theGame()._level and len(hero.getInventory()) <= 10:
                            hero.take(Totalequipments[rarete][random.randint(3, len(Totalequipments[rarete]) - 1)])
                            print()
                    hero._inventory.remove(object)

            if self.chestopened:
                theGame.theGame().addMessage(f"the luxurious chest has been opened")
                return
            theGame.theGame().addMessage(f"it seems that a key is needed to open this luxurious chest ! ")

    def meetAffichage(self, hero):
        return self.meet(hero)
