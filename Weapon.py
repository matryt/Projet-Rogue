import Wearable
import importlib

theGame = importlib.import_module("theGame")



class Weapon(Wearable.Wearable):
	"""
	armes que peut prendre le joueur

	...
	Attributes
	----------
	_name
	_abbrv
	usage
	"""
	def __init__(self, name, place, effect, abbrv="", usage=None,resum = "a weapon",mainstat = 1):
		"""

		Parameters
		----------
		name : str
			Le nom de l'arme
		abbrv : str, optional
			L'abréviation représentant l'arme sur la map
		usage : function, optional
			La fonction à appeler quand l'arme est utilisée
		resum : str, optional 
			Un resumé sur l'arme 
		"""
		super().__init__(name, abbrv,usage,resum,place,effect)
		self.mainstat = mainstat


	def use(self, creature):
		"""
		Permet d'utiliser l'arme

		Parameters
		----------
		creature : Creature.Creature
			La créature qui utilise l'arme

		Returns
		-------
		bool
			True si l'arme a été utilisé, False sinon
		"""
		if self.usage:
			theGame.theGame().addMessage(f"The {creature.getName()} equip the {self._name}")
			return self.usage(self, creature)
		theGame.theGame().addMessage(f"The {self._name} is broken or you try to equip 2 weapons")
		return False
