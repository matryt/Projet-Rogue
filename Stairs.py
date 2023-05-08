import Element
import Game


class Stairs(Element.Element):
	"""
	Escaliers permettant de descendre ou de monter d'un étage


	"""

	def __init__(self):
		super().__init__("Stairs", "E")

	@staticmethod
	def meet():
		Game.theGame().buildFloor()
		Game.theGame().addMessage(f"The {Game.theGame().getHero().getName()} goes down")
