import Element
import importlib
import random
import Equipment
import tkinter as tk

theGame = importlib.import_module("theGame")
root2 = tk.Tk()
root2.withdraw()


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

    def __init__(self, name, hp, abbrv=None, strength=1, idCreature=None, isPoisoning=False, isBlinding=False):
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
        isBlinding : bool, optional
                Indique si la créature aveugle le héros
        """
        super().__init__(name, abbrv)
        self._hp = hp
        self.hpMax = hp
        self._strength = strength
        self._armure_equipee = None
        self._idCreature = idCreature
        self.isPoisoning = isPoisoning
        self.isBlinding = isBlinding
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
        self.hpMax += 3

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
        creature : Hero.Hero
                La créature
        """
        creature.xp += random.randint(1 * self._strength, 20 * self._strength)
        creature.xpMax += creature.xp
        if self._idCreature == theGame.theGame().special_id and len(creature.getInventory()) < 10:
            creature._inventory.append(Equipment.Equipment("key", "k"))
            theGame.theGame().addMessage("vous avez trouvé un objet ! ")
        if creature.xp >= 20 * creature._level:
            creature._level += 1
            if creature.chance <=1 :
                creature.chance+=0.05
            theGame.theGame().addMessage(f"You just advanced to level {creature._level}")
            creature.hpMax += random.randint(1, 3)
            creature.strengthMax += random.randint(1, 3)
            creature.xpMax += creature.xp
            creature.xp = 0
            creature._hp = creature.hpMax
            creature._strength = creature.strengthMax
            if creature._arme_equipee is not None:
                creature._strength += creature._arme_equipee.effect.get('strength', 0)

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
        self._hp = max(self._hp - creature.getStrength(), 0)
        theGame.theGame().addMessage(f"The {creature.getName()} hits the {self.description()}")
        creature._invisible = False
        if creature._arme_equipee is not None:
            creature._arme_equipee.durability -= 1
            if creature._arme_equipee.durability == 0:
                theGame.theGame().addMessage(
                    f"Your {str(creature._arme_equipee._name)} just broke"
                )
                creature._inventory.remove(creature._arme_equipee)
                creature._strength -= creature._arme_equipee.effect.get('strength', 0)
                creature.strengthMax -= creature._arme_equipee.effect.get('strength', 0)
                creature._arme_equipee = None
        if creature._armure_equipee is not None:
            creature._armure_equipee.durability -= 1
            if creature._armure_equipee.durability == 0:
                theGame.theGame.addMessage(
                    f"Your {str(creature._armure_equipee.getName())} just broke"
                )
                creature._inventory.remove(creature._armure_equipee)
                creature.armor -= creature._armure_equipee.effect.get('armor', 0)
                creature._armure_equipee = None
        if self._hp <= 0:
            self.advanceLevel(creature)
            return True
        return False

    def meetAffichage(self, creature):
        self._hp = max(self._hp - creature.getStrength(), 0)
        creature._invisible = False
        if creature._arme_equipee is not None:
            creature._arme_equipee.durability -= 1
            if creature._arme_equipee.durability == 0:
                messageFenetre(f"Your {str(creature._arme_equipee.getName())} just broke")
                creature.removeFromInventory(creature._arme_equipee)
                creature._strength -= creature._arme_equipee.effect.get('strength', 0)
                creature.strengthMax -= creature._arme_equipee.effect.get('strength', 0)
                creature._arme_equipee = None
        if creature._armure_equipee is not None:
            creature._armure_equipee.durability -= 1
            if creature._armure_equipee.durability == 0:
                messageFenetre(f"Your {str(creature._armure_equipee.getName())} just broke")
                creature.removeFromInventory(creature._armure_equipee)
                creature.armor -= creature._armure_equipee.effect.get('armor', 0)
                creature._armure_equipee = None
        if self._hp <= 0:
            self.advanceLevel(creature)
            return True
        return False


def on_closing():
    root2.quit()
    root2.destroy()


def messageFenetre(message, titre="A message"):
    global root2
    root2 = tk.Tk()
    root2.title(titre)
    width = 420
    height = 100
    screen_width = root2.winfo_screenwidth()
    screen_height = root2.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    label = tk.Label(root2, text=message)
    label.pack()
    label.config(font=("Arial", 24))
    root2.protocol("WM_DELETE_WINDOW", on_closing)
    root2.geometry(f"{width}x{height}+{x}+{y}")
    root2.mainloop()
