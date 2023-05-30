import Equipment
import importlib

theGame = importlib.import_module("theGame")


class Wearable(Equipment.Equipment):
    """A wearable equipment."""

    def __init__(self, name, place, effect, abbrv="", usage=None, durability=3):
        Equipment.Equipment.__init__(self, name, abbrv, usage)
        self.place = place
        self.effect = effect
        self.durability = durability

    def __eq__(self, other):
        if isinstance(other, Equipment.Equipment):
            return self._name == other._name
        return False

    def __hash__(self):
        return hash((self._name, self.place))

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
            theGame.theGame().addMessage(f"The {creature.getName()} equip the {self._name}")
            return self.usage(self, creature)
        theGame.theGame().addMessage(f"The {self._name} is not equippable")
        return False
