import Element
import importlib

theGame = importlib.import_module("theGame")


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
    def meet(*args):
        """Permet de descendre d'un étage"""
        if theGame.theGame().getFloor().isInSimulation():
            theGame.theGame().buildFloor(True)
        else:
            theGame.theGame().buildFloor()
        theGame.theGame().addMessage(
            f"The {theGame.theGame().getHero().getName()} goes down to level {theGame.theGame().getLevel()-1}"
        )
