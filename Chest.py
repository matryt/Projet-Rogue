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

	def __init__(self):
		super().__init__("Chest", "M")
		
	def meet(self,hero):
		"""Permet d'ouvrir le coffre à condition d'avoir une clé'"""
		for object in hero._inventory:
			if  object._name == "key":
				Totalequipments = theGame.theGame().equipments 
				theGame.theGame().addMessage(f"you open the chest with the key")
				theGame.theGame().addMessage(f"wowie, you just gained gold and stuff : ")
				hero.GoldCount += random.randint(5*theGame.theGame()._level,25*theGame.theGame()._level)
				for rareté in Totalequipments:
					if rareté == 2*theGame.theGame()._level:
						hero.take(Totalequipments[rareté][random.randint(0,len(Totalequipments[rareté]))])


		theGame.theGame().addMessage(f"it seems that a key is needed to open this chest")
		