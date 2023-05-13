import Element
import Game


class Equipment(Element.Element):
	"""
	Equipement que peut prendre le joueur

	...
	Attributes
	----------
	_name
	_abbrv
	"""
	def __init__(self, name, abbrv="", usage=None):
		"""

		Parameters
		----------
		name : str
			Le nom de l'équipement
		abbrv : str, optional
			L'abréviation représentant l'équipement
		"""
		Element.Element.__init__(self, name, abbrv)
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
		if self.usage is not None:
			s = self.usage(self, creature)
			theGame.theGame().addMessage(f"The {creature.getName()} uses the {self._name}")
			return s
		theGame.theGame().addMessage(f"The {self._name} is not usable")
		return False
