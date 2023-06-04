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
    usage
    resum
    """

    def __init__(self, name, abbrv="", usage=None, resum="a thing"):
        """

        Parameters
        ----------
        name : str
                Le nom de l'équipement
        abbrv : str, optional
                L'abréviation représentant l'équipement
        usage : function, optional
                La fonction à appeler quand l'équipement est utilisé
        resum : str, optional
                Un resumé sur l'equipment
        """
        super().__init__(name, abbrv, resum)
        self.usage = usage

    def __eq__(self, other):
        if isinstance(other, Equipment):
            return self._name == other._name
        return False

    def __hash__(self):
        return hash(f"{self._name},{self._abbrv}")

    def meet(self, elem):
        """
        Méthode appelée quand l'objet est rencontré par un autre élément
        Parameters
        ----------
        elem : Creature.Creature
                L'élément qui rencontre l'objet

        Returns
        -------
        bool
            True
        inventaire limité: return False quand un equipment est rencontré par un element si l'inventaire du héro dépasse X valeur."""
        elem._invisible = False
        if len(theGame.theGame().getHero().getInventory()) == 10 and self._name != "gold":
            theGame.theGame().addMessage(
                f"Your inventory is full {str(theGame.theGame().getHero().getName())}"
            )
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

    def meetAffichage(self, elem):
        return self.meet(elem)
