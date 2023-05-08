import copy
import math
import random
import time


class Coord(object):
    """
    Point d'un plan représenté par une abscisse et une ordonnée

    ...
    Attributes
    ----------
    x
    y
    """

    def __init__(self, x = 0, y = 0):
        """
        Parameters
        ----------
        x : int, optional
            Abscisse du point
        y : int, optional
            Ordonnée du point
        """
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<{self.x},{self.y}>"

    def __eq__(self, other):
        if type(self) == type(other):
            return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Coord(self.x+other.x, self.y+other.y)


class Element(object):
    """
    Définit les caractéristiques communes de tous les éléments du jeu (nom, abréviation)

    ...
    Attributes
    ----------
    _name
    _abbrv

    Warnings
    ----------
    Cette classe est abstraite et ne doit pas être instanciée.
    """

    def __init__(self, name, abbrv=None):
        """

        Parameters
        ----------
        name : str
            Le nom de l'élément
        abbrv : str, optional
            L'abréviation représentant l'élément
        """
        self._name = name
        if not abbrv:
            self._abbrv = name[0]
        else:
            self._abbrv = abbrv

    def __repr__(self):
        return self._abbrv

    def description(self):
        """
        Returns
        -------
        str
            La description de l'élément
        """
        return f"<{self._name}>"

    def meet(self, elem):
        raise NotImplementedError()


class Equipment(Element):
    """
    Equipement que peut prendre le joueur

    ...
    Attributes
    ----------
    _name
    _abbrv
    """
    def __init__(self, name, abbrv=None):
        """

        Parameters
        ----------
        name : str
            Le nom de l'équipement
        abbrv : str, optional
            L'abréviation représentant l'équipement
        """
        super().__init__(name, abbrv)

    def meet(self, elem):
        """
        Méthode appelée quand l'objet est rencontré par un autre élément
        Parameters
        ----------
        elem : L'élément ayant rencontré l'équipement

        Returns
        -------
        bool
            True
        """
        elem.take(self)
        theGame().addMessage(f"You pick up a {self._name}")
        return True


class Creature(Element):
    """
    Créature du jeu (monstre...)

    ...
    Attributes
    ----------
    _name
    _abbrv
    _hp
    _strength
    """
    def __init__(self, name, hp, abbrv=None, strength=1):
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
        """
        super().__init__(name, abbrv)
        self._hp = hp
        self._strength = strength

    def description(self):
        return f"{super().description()}({self._hp})"

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

    def meet(self, creature):
        """
        Méthode appelée quand une autre créature rencontre cette créature

        Parameters
        ----------
        creature : Creature
            L'autre créature

        Returns
        -------
        bool
            True si la créature a encore des points de vie, False sinon
        """
        self._hp -= creature.getStrength()
        theGame().addMessage(f"The {creature.getName()} hits the {self.description()}")
        return self._hp <= 0


class Hero(Creature):
    """
    Héros du jeu

    ...
    Attributes
    ----------
    _name
    _abbrv
    _hp
    _strength
    _inventory
    _timeCreation : float
        Heure de création du héros

    """
    def __init__(self, name = "Hero", hp = 10, abbrv=None, strength=2, inventory=None):
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
        inventory : list, optional
            L'inventaire du héros
        """
        self._timeCreation = time.monotonic()
        if inventory is None:
            inventory = []
        if not abbrv:
            abbrv = "@"
        super().__init__(name, hp, abbrv, strength)
        self._inventory = inventory

    def __eq__(self, other):
        if isinstance(other, Hero):
            return self._name == other._name and self._abbrv == other._abbrv and self._timeCreation == other._timeCreation
        return False

    def __hash__(self):
        return hash(f"{self._name},{self._abbrv},{self._hp},{self._strength}, {self._inventory}, {self._timeCreation}")

    def take(self, elem):
        """

        Parameters
        ----------
        elem : Equipment
            L'équipement que doit prendre le héros

        Raises
        -------
        TypeError
            Si l'objet passé en paramètre n'est pas du type Equipment
        """
        if not isinstance(elem, Equipment):
            raise TypeError("L'élément à prendre doit être du type Equipment")
        self._inventory.append(elem)

    def meet(self, creature):
        self._hp -= creature._strength
        theGame().addMessage(f"The {creature._name} hits the {self.description()}")

    def description(self):
        return f"{super().description()}{self._inventory}"


class Room(object):
    """
    Salle de la carte

    ...
    Attributes
    ----------
    c1
    c2
    """
    def __init__(self, c1, c2):
        """

        Parameters
        ----------
        c1 : Coord
            Coin en haut à gauche de la salle
        c2 : Coord
            Coin en bas à droite de la salle
        """
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        return f"[{self.c1}, {self.c2}]"

    def __contains__(self, other):
        return self.c1.x <= other.x <= self.c2.x and self.c1.y <= other.y <= self.c2.y

    def center(self):
        """

        Returns
        -------
        Coord
            Point représentant le centre de la salle
        """
        return Coord((self.c2.x + self.c1.x) // 2, (self.c2.y + self.c1.y) // 2)

    def intersect(self, other):
        """

        Parameters
        ----------
        other : Room
            L'autre salle avec laquelle on doit vérifier l'intersection

        Returns
        -------
        bool
            True si les deux salles possèdent une intersection, False sinon
        """
        coinsSelf = [self.c1, Coord(self.c2.x, self.c1.y), Coord(self.c1.x, self.c2.y), self.c2]
        coinsOther = [other.c1, Coord(other.c2.x, other.c1.y), Coord(other.c1.x, other.c2.y), other.c2]

        if any(x in other for x in coinsSelf) or any(x in self for x in coinsOther) or \
                (other.c1 in self and other.c2 not in self) or (other.c2 in self and other.c1 not in self):
            return True

        cote1 = False
        cote2 = False

        i = 0
        while i < 2 and not cote1:
            if (min(coinsOther[i].x, coinsOther[i+2].x) <= coinsSelf[i].x <= max(coinsOther[i+2].x, coinsOther[i].x)) \
                    and (min(coinsSelf[i].y, coinsSelf[i+2].y) <= coinsOther[i].y <= max(coinsSelf[i].y, coinsSelf[i+2].y)):
                cote1 = True
            i += 1

        if cote1:
            return True

        i = 0
        while i < 2 and not cote2:
            if (min(coinsSelf[i].x, coinsSelf[i+2].x) <= coinsOther[i].x <= max(coinsSelf[i].x, coinsSelf[i+2].x)) and \
                    (min(coinsOther[i].y, coinsOther[i+2].y) <= coinsSelf[i].y <= max(coinsOther[i].y, coinsOther[i+2].y)):
                cote2 = True
            i += 1

        return cote2

    def randCoord(self):
        """

        Returns
        -------
        Coord
            Un point de la salle au hasard
        """
        return Coord(random.randint(self.c1.x, self.c2.x), random.randint(self.c1.y, self.c2.y))

    def existsGround(self, m):
        """
        Parameters
        ----------
        m : Map
            La carte dans laquelle prendre une coordonnée

        Returns
        -------
        bool
            True s'il existe au moins une case dont la valeur est Map.ground dans la salle, False sinon
        """

        for x in range(self.c1.x, self.c2.x+1):
            for y in range(self.c1.y, self.c2.y+1):
                if m.get(Coord(x, y)) == Map.ground:
                    return True
        return False

    def randEmptyCoord(self, m):
        """

        Parameters
        ----------
        m : Map
            La carte dans laquelle prendre une coordonnée

        Returns
        -------
        r : Coord
            Un point de la salle au hasard qui n'est pas déjà rempli

        """
        if not isinstance(m, Map):
            raise TypeError("map doit être de type Map() !")
        if not self.existsGround(m):
            raise ValueError("Il n'existe aucune case de la salle qui ne soit remplie !")
        r = self.randCoord()
        e = m.get(r)
        while e is not Map.ground or r == self.center():
            r = self.randCoord()
            e = m.get(r)
        return r

    def decorate(self, m):
        """

        Parameters
        ----------
        m : Map
            La carte dans laquelle prendre une coordonnée

        """
        m.put(self.randEmptyCoord(m), theGame().randEquipment())
        m.put(self.randEmptyCoord(m), theGame().randMonster())


class Map(object):
    """
    La carte de jeu

    ...
    Attributes
    ----------
    ground : str
        Case vide
    empty : str
        Mur
    dir : dict
        Touches directionnelles pour jouer
    size
    _hero : Hero
        Le héros du jeu
    _mat : list
        Carte du jeu
    nbRooms
    _elem : list
    _roomsToReach
    _rooms

    """
    ground = "."
    empty = " "
    dir = {
        'z': Coord(0, -1),
        's': Coord(0, 1),
        'd': Coord(1, 0),
        'q': Coord(-1, 0)
    }

    def __init__(self, size=20, hero=None, nbrooms=7):
        """

        Parameters
        ----------
        size : int, optional
            La taille de la carte
        nbrooms : int, optional
            Le nombre de salles dans la carte
        """
        self.size = size
        if hero is None:
            hero = Hero(abbrv="@")
        self._hero = hero
        self._mat = [[Map.empty for _ in range(self.size)] for _ in range(self.size)]
        self.nbRooms = nbrooms
        self._elem = {}
        self._roomsToReach = []
        self._rooms = []
        self.generateRooms(self.nbRooms)
        self.reachAllRooms()
        coordH = self._rooms[0].center()
        self._mat[coordH.y][coordH.x] = hero
        self._elem = {hero: coordH}
        for r in self._rooms:
            r.decorate(self)

    def __repr__(self):
        c = ""
        for ligne in self._mat:
            for elem in ligne:
                c += str(elem)
            c += "\n"
        return c

    def __len__(self):
        return self.size

    def __contains__(self, item):
        if isinstance(item, Coord) and 0 <= item.x < len(self) and 0 <= item.y < len(self):
            return True
        if isinstance(item, str):
            for ligne in self._mat:
                if item in ligne:
                    return True
        return False

    def checkCoord(self, c):
        """

        Parameters
        ----------
        c
            Un objet dont on veut tester si c'est un Coord

        """
        if not isinstance(c, Coord):
            raise TypeError("Not a Coord")
        if c not in self:
            raise IndexError("Out of map coord")

    @staticmethod
    def checkElement(e):
        """

        Parameters
        ----------
        e
            Un objet dont on veut tester si c'est un Element

        """
        if not isinstance(e, Element):
            raise TypeError("Not a Element")

    def get(self, c):
        """

        Parameters
        ----------
        c : Coord
            La coordonnée dont on veut connaître le contenu

        Returns
        -------
        str | Hero | Creature | Equipment
            L'élément contenu à la coordonnée spécifiée

        """
        self.checkCoord(c)
        return self._mat[c.y][c.x]

    def pos(self, elem):
        """

        Parameters
        ----------
        elem : Element
            L'objet à chercher dans la carte

        Returns
        -------
        Coord | None
            La première coordonnée à laquelle se trouve cet élément ou None s'il ne s'y trouve pas
        """
        self.checkElement(elem)
        for i in range(len(self)):
            for j in range(len(self)):
                if self._mat[j][i] == elem:
                    return Coord(i, j)

    def put(self, c, e):
        """

        Parameters
        ----------
        c : Coord
            La coordonnée à laquelle on veut ajouter un élément
        e : Element
            L'élément à ajouter sur la carte

        Returns
        ----------
        None
        """
        self.checkCoord(c)
        self.checkElement(e)
        if self.get(c) != Map.ground:
            raise ValueError("Incorrect cell")
        if e in self._elem:
            raise KeyError("Already placed")

        self._mat[c.y][c.x] = e
        if e != Map.ground:
            self._elem[e] = c

    def addRoom(self, room):
        """
        Ajoute une salle à la carte
        Parameters
        ----------
        room : Room
            La salle à ajouter
        """
        self._roomsToReach.append(room)
        for i in range(room.c1.y, room.c2.y+1):
            for j in range(room.c1.x, room.c2.x+1):
                self._mat[i][j] = Map.ground

    def rm(self, coord):
        """
        Permet de supprimer le contenu d'une coordonnée de la carte
        Parameters
        ----------
        coord : Coord
            Coordonnée dont on veut supprimer le contenu
        """
        self.checkCoord(coord)
        toDel = None
        elem = copy.deepcopy(self._elem)
        for key, value in elem.items():
            if value == coord:
                toDel = key
        self._elem = elem
        if toDel is not None:
            self._elem.pop(toDel)
        self._mat[coord.y][coord.x] = Map.ground

    def play(self, hero=None):
        """
        Permet de créer le héros, puis de lancer la boucle de jeu
        Parameters
        ----------
        hero : Hero, optional
            Le héros à utiliser pour le jeu
        """
        if not hero:
            hero = Hero(abbrv="@")
        while True:
            print(self)
            self.move(hero, Map.dir[getch()])

    def move(self, e, way):
        """
        Permet de bouger un élément e d'une case à une autre
        Parameters
        ----------
        e : str | Element
            Element à déplacer
        way : Coord
            Vecteur déplacement à appliquer à l'élément
        """
        p = self.pos(e)
        if p is not None and p+way in self:
            arrive = self.get(p+way)
            if arrive is Map.empty:
                return
            if arrive is Map.ground:
                self.rm(p)
                self.put(p+way, e)
            else:
                r = arrive.meet(e)
                if r:
                    self.rm(p+way)

    def __getitem__(self, key):
        if isinstance(key, Coord):
            return self.get(key)
        return self.pos(key)

    def __setitem__(self, key, value):
        if isinstance(key, Coord):
            self.put(key, value)
        else:
            if key in self:
                self.rm(key)
            self.put(value, key)

    def findRoom(self, coord):
        """
        Permet de trouver la première salle contenant une coordonnée
        Parameters
        ----------
        coord : Coord
            Coordonnée à trouver

        Returns
        -------
        Room | bool
            La première salle contenant la coordonnée demandée, ou False à défaut
        """
        return next((s for s in self._roomsToReach if coord in s), False)

    def intersectNone(self, room):
        """
        Vérifie que la salle passée en paramètre n'entrecroise aucune autre salle
        Parameters
        ----------
        room : Room
            La salle à vérifier

        Returns
        -------
        bool
            True si la salle n'est en contact avec aucune autre, False sinon
        """
        return not any(s.intersect(room) for s in self._roomsToReach)

    def dig(self, coord):
        """
        Permet d'insérer une coordonnée sur la carte
        Parameters
        ----------
        coord : Coord
            La coordonnée
        """
        self._mat[coord.y][coord.x] = Map.ground
        s = self.findRoom(coord)
        if s:
            i = self._roomsToReach.index(s)
            self._rooms.append(self._roomsToReach.pop(i))

    def corridor(self, start, end):
        """
        Permet de tracer un couloir entre start et end
        Parameters
        ----------
        start : Coord
            Coordonnée de départ
        end : Coord
            Coordonnée d'arrivée
        """
        self.dig(start)
        if start.y < end.y:
            cY = Coord(0, 1)
        else:
            cY = Coord(0, -1)
        if start.x < end.x:
            cX = Coord(1, 0)
        else:
            cX = Coord(-1, 0)
        s = start
        while s.y != end.y:
            s += cY
            self.dig(s)
        while s.x != end.x:
            s += cX
            self.dig(s)

    def reach(self):
        """
        Rejoint deux salles au hasard (entre une déjà rejointe et une pas encore atteinte)
        """
        A = random.choice(self._rooms)
        B = random.choice(self._roomsToReach)
        self.corridor(A.center(), B.center())

    def reachAllRooms(self):
        """
        Permet de relier toutes les salles créées
        """
        self._rooms.append(self._roomsToReach.pop(0))
        while len(self._roomsToReach) > 0:
            self.reach()

    def randRoom(self):
        """
        Renvoie une salle au hasard dans la carte

        Returns
        -------
        Room
            Une salle au hasard
        """
        x1 = random.randint(0, len(self)-3)
        y1 = random.randint(0, len(self)-3)
        longueur = random.randint(3, 8)
        h = random.randint(3, 8)
        x2 = min(len(self) - 1, x1 + longueur)
        y2 = min(len(self) - 1, y1 + h)
        return Room(Coord(x1, y1), Coord(x2, y2))

    def generateRooms(self, n):
        """
        Essaye de générer n rooms qui ne s'entrecroisent pas
        Parameters
        ----------
        n : int
            Le nombre de salles à générer, si possible
        """
        for _ in range(n):
            s = self.randRoom()
            if self.intersectNone(s):
                self.addRoom(s)


class Game(object):
    """
    La classe de jeu

    ...
    Attributes
    ----------
    equipments : list
        Equipements qui peuvent être positionnées sur la carte
    monsters : list
        Monstres pouvant être positionnées sur la carte
    _hero
    _messages
    _level
    _floor
    """
    equipments = {0: [Equipment("potion", "!"), Equipment("gold", "o")], 1: [Equipment("sword"), Equipment("bow")],
                  2: [Equipment("chainmail")]}
    monsters = {0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
                1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)], 5: [Creature("Dragon", 20, strength=3)]}

    def __init__(self, hero = None, level = 1, floor = None, messages = None):
        """
        Parameters
        ----------
        hero : Hero | None
            Le héros à insérer dans la carte
        level : int | None
            Le niveau du jeu
        floor : int | None
            La carte
        messages : list | None
            La liste des messages à afficher au joueur
        """
        self._hero = hero or Hero()
        if not messages:
            messages = []
        self._level = level
        self._floor = floor
        self._messages = messages

    def buildFloor(self):
        """
        Construit la carte
        """
        self._floor = Map(hero=self._hero)

    def addMessage(self, msg):
        """
        Ajoute un message dans la liste des messages à afficher
        Parameters
        ----------
        msg : str
            Message à afficher
        """
        self._messages.append(msg)

    def readMessages(self):
        """
        Renvoie une chaîne de caractère composée de tous les messages enregistrés et les supprime de la liste
        Returns
        -------
        str
            Concaténation des messages en question
        """
        if not self._messages:
            return ""
        msg = ". ".join(self._messages)+"."
        self._messages = []
        return msg

    def randElement(self, collection):
        """
        Renvoie un élément au hasard parmi la collection passée en paramètre

        Parameters
        ----------
        collection : dict
            Ensemble des éléments associés par niveau

        Returns
        -------
        Element
            L'élément tiré au hasard
        """
        x = random.expovariate(1/self._level)
        x = math.floor(x)
        while not collection.get(x):
            x -= 1
        return copy.copy(random.choice(collection[x]))

    def randEquipment(self):
        """
        Renvoie un équipement au hasard

        Returns
        -------
        Equipment
            L'équipement tiré au hasard
        """
        return self.randElement(Game.equipments)

    def randMonster(self):
        """
        Renvoie un monstre au hasard

        Returns
        -------
        Monster
            Le monstre tiré au hasard
        """
        return self.randElement(Game.monsters)


def theGame(game = Game()):
    """
    Retourne l'instance Game du programme en cours
    Parameters
    ----------
    game : Game, optional
        L'instance de Game pour ce run

    Returns
    -------
    Game
    """
    return game


def getch():
    """Single char input, only works on Mac/linux/Windows OS terminals"""
    try:
        import termios
        # POSIX system. Create and return a getch that manipulates the tty.
        import sys, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch().decode('utf-8')


Map().play()
