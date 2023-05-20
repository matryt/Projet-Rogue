import Element
import importlib

theGame = importlib.import_module("theGame")


class Equipment(Element.Element):
	"""
	Equipement que peut prendre le joueur

	...
	Attributes
	----------
	_name
	_abbrv
	"""

	def __init__(self, name, abbrv="", usage=None,resum = "a thing"):
		"""

		Parameters
		----------
		name : str
			Le nom de l'équipement
		abbrv : str, optional
			L'abréviation représentant l'équipement
		"""
		super().__init__(name, abbrv,resum)
		self.usage = usage

	def meet(self, elem):
		"""
		Méthode appelée quand l'objet est rencontré par un autre élément
		Parameters
		----------
		elem : Element.Element
			L'élément qui rencontre l'objet

		Returns
		-------
		bool
			True
		"""
		"""inventaire limité: return False quand un equipment est rencontré par un element si l'inventaire du héro dépasse X valeur."""
		if len(theGame.theGame()._hero._inventory) == 10:
            
			theGame.theGame().addMessage("Your inventory is full "+str(theGame.theGame()._hero._name))
			return False

		elem.take(self)
		theGame.theGame().addMessage(f"You pick up a {self._name}")
		return True

	def getName(self):
		"""
		Returns
		-------
		str
			Le nom de l'équipement
		"""
		return self._name

	def use(self, creature):
		"""
		Permet d'utiliser l'objet

		Parameters
		----------
		creature : Creature.Creature
			La créature qui utilise l'objet

		Returns
		-------
		bool
			True si l'objet a été utilisé, False sinon
		"""
		if self.usage:
			theGame.theGame().addMessage(f"The {creature.getName()} uses the {self._name}")
			return self.usage(self, creature)
		theGame.theGame().addMessage(f"The {self._name} is not usable")
		return False
