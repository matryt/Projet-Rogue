import Element
import importlib
import random
import Equipment

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

    def __init__(self, name, hp, abbrv=None, strength=1, idCreature=None, isPoisoning=False):
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
        isPoisoning : bool, optional
                Indique si la créature empoisonne le héros
        """
        super().__init__(name, abbrv)
        self._hp = hp
        self._strength = strength
        self._idCreature = idCreature
        self.isPoisoning = isPoisoning
        self.xp = 0
        self.xpMax = 0

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

    def getID(self):
        """
        Returns
        -------
        int
                L'identifiant de la créature
        """
        return self._idCreature

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

    def advanceLevel(self, creature):
        """
        Parameters
        ----------
        creature : self
                La créature
        """
        creature.xp += random.randint(1 * self._strength, 20 * self._strength)
        creature.xpMax += creature.xp
        if self._idCreature == theGame.theGame().special_id:
            creature._inventory.append(Equipment.Equipment("key", "k"))
            theGame.theGame().addMessage("vous avez trouvé un objet ! ")
        if creature.xp >= 20 * creature._level:
            creature._level += 1
            print(creature._level)
            theGame.theGame().addMessage(f"You just advanced to level {creature._level}")
            creature.hpMax += random.randint(1, 3)
            creature.strengthMax += random.randint(1, 3)
            creature.xpMax += creature.xp
            creature.xp = 0
            creature._hp = creature.hpMax
            creature._strength = creature.strengthMax

    def meet(self, creature):
        """
        Méthode appelée quand une autre créature rencontre cette créature

        Parameters
        ----------
        creature : self
                L'autre créature

        Returns
        -------
        bool
                True si la créature a encore des points de vie, False sinon
        """
        self._hp -= creature.getStrength()
        self._hp = max(self._hp, 0)
        theGame.theGame().addMessage(f"The {creature.getName()} hits the {self.description()}")
        creature._invisible = False
        if creature._arme_equipee != None:
            creature._arme_equipee.durability -= 1
            if creature._arme_equipee.durability == 0:
                theGame.theGame().addMessage(
                    f"Your {str(creature._arme_equipee._name)} just broke"
                )
                creature._inventory.remove(creature._arme_equipee)
                creature.strengthMax -= creature._arme_equipee.effect.get('strength', 0)
        if self._hp <= 0:
            self.advanceLevel(creature)
            return True
        return False
