import Element
import importlib
import random

theGame = importlib.import_module("theGame")


class Creature(Element.Element):
	"""
	Créature du jeu (monstre...)

	...
	Attributes
	----------
	_name
	_abbrv
	_hp
	_strength
	_idCreature
	"""

	def __init__(self, name, hp, abbrv=None, strength=1, idCreature=None):
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
		idCreature : int, optional
			L'identifiant de la créature
		"""
		super().__init__(name, abbrv)
		self._hp = hp
		self._strength = strength
		self._idCreature = idCreature

	def __eq__(self, other):
		if isinstance(other, Creature):
			return self._name == other._name and self._abbrv == other._abbrv and self._idCreature == other._idCreature
		return False

	def __hash__(self):
		return hash(f"{self._name},{self._abbrv},{self._idCreature}")

	def description(self):
		"""
		Returns
		-------
		str
			La description de la créature
		"""
		return f"{super().description()}({self._hp})"

	def heal(self):
		"""Permet de soigner la créature"""
		self._hp += 3

	def getName(self):
		"""
		Returns
		-------
		str
			Le nom de la créature
		"""
		return self._name

	def getStrength(self):
		"""
		Returns
		-------
		int
			La force de la créature
		"""
		return self._strength

	def setID(self, idToSet):
		"""
		Parameters
		----------
		idToSet : int
			L'identifiant à donner à la créature
		"""
		self._idCreature = idToSet

	def meet(self, creature):
		"""
		Méthode appelée quand une autre créature rencontre cette créature

		Parameters
		----------
		creature : Creature
			L'autre créature

		Returns
		-------
		bool
			True si la créature a encore des points de vie, False sinon
		"""
		self._hp -= creature.getStrength()
		theGame.theGame().addMessage(f"The {creature.getName()} hits the {self.description()}")
		if self._hp <= 0:
			creature.xp += random.randint(1*self._strength,20*self._strength)
			if creature.xp >= 20*creature._level:
				creature._level += 1
				print(creature._level)
				theGame.theGame().addMessage("vous avez gagné un niveau ! ")
				creature.hpMax += 2
				creature.strengthMax += 1
				creature._hp = creature.hpMax
				creature._strength = creature.strengthMax
				



			#print(creature.xp)
			return True   
		return False  
