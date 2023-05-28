import Equipment
import Creature
import importlib
import random

import Map
from utils import getch

theGame = importlib.import_module("theGame")


class Hero(Creature.Creature):
	"""
	Héros du jeu

	...
	Attributes
	----------
	_name
	_abbrv
	_hp
	_strength
	_inventory
	_xp 

	""" 

	def __init__(self, name="Hero", hp=10, abbrv=None, strength=2, inventory=None, xp = 0,GoldCount = 0,level = 1, poisoned=False, invisible=False, arme_equipee = None,revive = None):
		"""

		Parameters
		----------
		name : str
			Le nom de la créature
		hp : int
			Les points de vie initiaux de la créature
		abbrv : str, optional
			L'abréviation représentant la créature
		strength : int, optional
			La force de la créature
		inventory : list, optional
			L'inventaire du héros
		xp : int, optional 
		  les points d'expérience du héros
		GoldCount : int, optional
			Le nombre de pièces d'or du héros
		level : int, optional
			Le niveau du héros
		poisoned : bool, optional
			Indique si le héros est empoisonné
		invisible : bool, optional
			Indique si le héros est invisible
		arme_equipee : variable
			Indique si une arme est équipée par le héro 
		"""

		if inventory is None:
			inventory = []
		if not abbrv:
			abbrv = "@"
		super().__init__(name, hp, abbrv, strength)
		self._inventory = inventory
		self.xp = xp
		self.GoldCount =  GoldCount 
		self._level = level 
		self.hpMax = 10
		self.strengthMax = 2
		self._poisoned = poisoned
		self._invisible = invisible
		self._arme_equipee = arme_equipee 
		self.revive = revive 

	def __eq__(self, other):
		if isinstance(other, Hero):
			return self._name == other._name and self._abbrv == other._abbrv
		return False

	def __hash__(self):
		return hash(f"{self._name},{self._abbrv}")

	def take(self, elem):
		"""

		Parameters
		----------
		elem : Equipment
			L'équipement que doit prendre le héros

		Raises
		-------
		TypeError
			Si l'objet passé en paramètre n'est pas du type Equipment
		"""
		if not isinstance(elem, Equipment.Equipment):
			raise TypeError("L'élément à prendre doit être du type Equipment")
		if elem._name == "gold":
			self.GoldCount += 1
		else:
			self._inventory.append(elem)

	def meet(self, creature):
		"""Est appelé lorsque le héros rencontre une créature

		Parameters
		-------
		creature : Creature.Creature
			La créature qui est rencontrée
		"""
		if not self._invisible:
			self._hp -= creature.getStrength()
			print(self.revive)
			if self._hp == 0 and self.revive == True:
				self._hp = self.hpMax
				theGame.theGame().addMessage(f"the soul of guardian replace yours and save you from death")
				self.revive = False 


			if creature.isPoisoning and not self._poisoned:
				self.poison()
			theGame.theGame().addMessage(f"The {creature.getName()} hits the {self.conciseDescription()}")
		else:
			theGame.theGame().addMessage(f"The {self.conciseDescription()} is invisible, the {creature.getName()} can't see him")

	def conciseDescription(self):
		return f"{super().description()}{self._inventory}"
	def description(self):
		return f"{super().description()} - Level {self._level} - {self.xp} XP \nYou have {len(self._inventory)} object(s) : {self._inventory} and {self.GoldCount} gold(s)"

	def poison(self):
		"""Empoisonne le héros"""
		theGame.theGame().addMessage("The hero is poisoned")
		self._poisoned = True

	def checkPoison(self):
		if self._poisoned:
			self._hp -= 1
			theGame.theGame().addMessage("The hero suffers from poison")

	def recover(self):
		"""Soigne le héros"""
		self._poisoned = False

	def fullDescription(self):
		"""Affiche une description complète du héros"""
		c = ""
		for name, elem in self.__dict__.items():
			if name.startswith("_"):
				name = name[1:]
			if name == "inventory":
				name = "INVENTORY"
				elem = [e.getName() for e in elem]
			c += f"> {name} : {elem} \n"
		return c[:-2]

	def getInventory(self):
		"""
		Returns
		-------
		list
			L'inventaire du héros
		"""
		return self._inventory

	def getHP(self):
		"""
		Returns
		-------
		int
			Les points de vie du héros
		"""
		return self._hp

	def use(self, item):
		"""
		Permet d'utiliser un item

		Parameters
		-------
		item : Equipment.Equipment
			L'item à utiliser

		"""
		if not item:
			return
		if not isinstance(item, Equipment.Equipment):
			raise TypeError("L'élément à utiliser doit être du type Equipment")
		if item not in self._inventory:
			raise ValueError("L'élément à utiliser doit être dans l'inventaire")

		u = item.use(self)

		if u:
			self._inventory.remove(item)

	def becomeInvisible(self):
		"""Rend le héros invisible"""
		self._invisible = True
		return False
	
	def opendescription(self,item, map):
		choice = getch()
		try:
			c = int(choice)
			if c < 0 or c > 3:
				print("arreteeeeeee")
				return

		except:
			print("t con où ? faut rentrer un chiffre")
			self.opendescription(item)

		## il y a parfois des problèmes de confusion entre les touches de l'inventaire et de cette methode:
		#pour palier à ça on pourrait remplacer les numeros par d'autres input qui sont pas des chiffres
		if c == 0:
			self.use(item)
		if c == 1:
			print(item.resume)
		if c == 3:
			self._inventory.remove(item)
		if c == 2:
			voisins = map.pos(self).voisins(map)
			for v in voisins:
				if map.get(v) != Map.Map.empty:
					voisins.remove(v)
			if v:
				map.put(random.choice(voisins), item)
				self._inventory.remove(item)
			else:
				theGame.theGame().addMessage("There is no place to drop the item")

		#itemdescription = {0: "Use" , 1: "description", 2: "jeter"}
		
		#return itemdescription[int(choice)]
