import Element
import Game


class Stairs(Element.Element):
	"""
	Escaliers permettant de descendre ou de monter d'un étage

	Attributes:
	_name : str
		Le nom de l'escalier
	_abbrv : str
		L'abréviation représentant l'escalier
	"""

	def __init__(self):
		super().__init__("Stairs", "E")

	@staticmethod
	def meet():
		"""Permet de descendre d'un étage"""
		Game.theGame().buildFloor()
		Game.theGame().addMessage(f"The {Game.theGame().getHero().getName()} goes down")
