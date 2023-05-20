import Equipment
import Creature
import importlib
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
	def __init__(self, name="Hero", hp=10, abbrv=None, strength=2, inventory=None, xp = 0):
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
		"""

		if inventory is None:
			inventory = []
		if not abbrv:
			abbrv = "@"
		super().__init__(name, hp, abbrv, strength)
		self._inventory = inventory
		self.xp = xp

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
		self._inventory.append(elem)

	def meet(self, creature):
		"""Est appelé lorsque le héros rencontre une créature

		Parameters
		-------
		creature : Creature.Creature
			La créature qui est rencontrée
		"""
		self._hp -= creature.getStrength()
		theGame.theGame().addMessage(f"The {creature.getName()} hits the {self.description()}")

	def description(self):
		return f"{super().description()}{self._inventory}"

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
	
	def opendescription(self,item):
		choice = getch()
		try:
			c = int(choice)
			
		except:
			print("t con où ? faut rentrer un chiffre")
			self.opendescription(item)


		if c < 0 or c > 2:
			print("arreteeeeeee")
			return 
		## il y a parfois des problèmes de confusion entre les touches de l'inventaire et de cette methode:
		#pour palier à ça on pourrait remplacer les numeros par d'autres input qui sont pas des chiffres
		if int(choice) == 0:  
			self.use(item)
		if int(choice) == 1:
			print(item.resume)
		if int(choice) == 3:
			self._inventory.remove(item)
			Map.put(Map.get(self),item)

		#itemdescription = {0: "Use" , 1: "description", 2: "jeter"}
		
		#return itemdescription[int(choice)]
