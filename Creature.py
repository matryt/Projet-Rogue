import Element


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
		"""
		Permet de soigner la créature
		"""
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
		import Game

		self._hp -= creature.getStrength()
		Game.theGame().addMessage(f"The {creature.getName()} hits the {self.description()}")
		return self._hp <= 0
