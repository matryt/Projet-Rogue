import copy
import random

import Coord
import Element
import Room
import Creature
import Hero
import theGame


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
	_hero : Hero.Hero
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
		'z': Coord.Coord(0, -1),
		's': Coord.Coord(0, 1),
		'd': Coord.Coord(1, 0),
		'q': Coord.Coord(-1, 0)
	}

	def __init__(self, size=20, hero=None, nbrooms=7, simulation=False):
		"""

		Parameters
		----------
		size : int, optional
			La taille de la carte
		hero : Hero.Hero, optional
			Le héros du jeu
		nbrooms : int, optional
			Le nombre de salles dans la carte
		simulation : bool, optional
			Si on est en simulation ou non
		"""
		self.size = size
		if hero is None:
			hero = Hero.Hero(abbrv="@")
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
		self._visibleMap = [["~" for _ in range(self.size)] for _ in range(self.size)]
		self.setVisible(self.rangeElement(self._hero))
		self._simulation = simulation
		if simulation:
			self._roomsVisited = []

	def __repr__(self):
		c = ""
		for ligne in self._visibleMap:
			for elem in ligne:
				c += str(elem)
			c += "\n"
		return c

	def __len__(self):
		return self.size

	def __contains__(self, item):
		if isinstance(item, Coord.Coord):
			return 0 <= item.x < len(self) and 0 <= item.y < len(self)
		if isinstance(item, str):
			for ligne in self._mat:
				if item in ligne:
					return True
		return False

	def getRooms(self):
		"""
		Returns
		-------
		list
			La liste des salles de la carte
		"""
		return self._rooms

	def getElem(self):
		"""
		Returns
		-------
		list
			La liste des éléments de la carte
		"""
		return self._elem

	def getVisitedRooms(self):
		"""
		Returns
		-------
		list
			La liste des salles visitées par le héros
		"""
		if self._simulation:
			return self._roomsVisited
		raise ValueError("Not in simulation")

	def isInSimulation(self):
		"""
		Returns
		-------
		bool
			Si on est en simulation ou non
		"""
		return self._simulation

	def setVisitedRooms(self, rooms):
		"""
		Permet de mettre à jour les salles visitées par le héros
		"""
		if self._simulation:
			self._roomsVisited = rooms
		else:
			raise ValueError("Not in simulation")

	def shuffleRooms(self):
		"""
		Mélange les salles de la carte
		"""
		random.shuffle(self._rooms)

	def checkCoord(self, c):
		"""

		Parameters
		----------
		c
			Un objet dont on veut tester si c'est un Coord

		"""
		if not isinstance(c, Coord.Coord):
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
		if not isinstance(e, Element.Element):
			raise TypeError("Not a Element")

	def get(self, c):
		"""

		Parameters
		----------
		c : Coord.Coord
			La coordonnée dont on veut connaître le contenu

		Returns
		-------
		str | Hero.Hero | Creature.Creature | Equipment.Equipment
			L'élément contenu à la coordonnée spécifiée

		"""
		self.checkCoord(c)
		return self._mat[c.y][c.x]

	def pos(self, elem):
		"""

		Parameters
		----------
		elem : Element.Element
			L'objet à chercher dans la carte

		Returns
		-------
		Coord.Coord | None
			La première coordonnée à laquelle se trouve cet élément ou None s'il ne s'y trouve pas
		"""
		self.checkElement(elem)
		for i in range(len(self)):
			for j in range(len(self)):
				if self._mat[j][i] == elem:
					return Coord.Coord(i, j)
		return None

	def put(self, c, e):
		"""

		Parameters
		----------
		c : Coord.Coord
			La coordonnée à laquelle on veut ajouter un élément
		e : Element.Element
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
		self._visibleMap = self._mat
		self.setVisible(self.rangeElement(self._hero))
		if e != Map.ground:
			self._elem[e] = c

	def addRoom(self, room):
		"""
		Ajoute une salle à la carte
		Parameters
		----------
		room : Room.Room
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
		coord : Coord.Coord
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

	def move(self, e, way):
		"""
		Permet de bouger un élément e d'une case à une autre
		Parameters
		----------
		e : str | Element.Element
			Element à déplacer
		way : Coord.Coord
			Vecteur déplacement à appliquer à l'élément
		"""
		orig = self.pos(e)
		dest = orig + way
		if dest in self:
			if self.get(dest) == Map.ground:
				self._mat[orig.y][orig.x] = Map.ground
				self._mat[dest.y][dest.x] = e
				self._elem[e] = dest
			if self.get(dest) != Map.empty and self.get(dest) != e and self.get(dest).meet(e) and self.get(dest) != self._hero:
				self.rm(dest)
			if self._simulation:
				for m in self._rooms:
					if dest in m.coordsInRoom() and m not in self._roomsVisited:
						self._roomsVisited.append(m)
		self.setVisible(self.rangeElement(self._hero))

	def __getitem__(self, key):
		if isinstance(key, Coord.Coord):
			return self.get(key)
		return self.pos(key)

	def __setitem__(self, key, value):
		if isinstance(key, Coord.Coord):
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
		coord : Coord.Coord
			Coordonnée à trouver

		Returns
		-------
		Room.Room | bool
			La première salle contenant la coordonnée demandée, ou False à défaut
		"""
		return next((s for s in self._roomsToReach if coord in s), False)

	def intersectNone(self, room):
		"""
		Vérifie que la salle passée en paramètre n'entrecroise aucune autre salle
		Parameters
		----------
		room : Room.Room
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
		coord : Coord.Coord
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
		start : Coord.Coord
			Coordonnée de départ
		end : Coord.Coord
			Coordonnée d'arrivée
		"""
		self.dig(start)
		if start.y < end.y:
			cY = Coord.Coord(0, 1)
		else:
			cY = Coord.Coord(0, -1)
		if start.x < end.x:
			cX = Coord.Coord(1, 0)
		else:
			cX = Coord.Coord(-1, 0)
		s = start
		while s.y != end.y:
			s += cY
			self.dig(s)
		while s.x != end.x:
			s += cX
			self.dig(s)

	def reach(self):
		"""Rejoint deux salles au hasard (entre une déjà rejointe et une pas encore atteinte)"""
		A = random.choice(self._rooms)
		B = random.choice(self._roomsToReach)
		self.corridor(A.center(), B.center())

	def reachAllRooms(self):
		"""Permet de relier toutes les salles créées"""
		self._rooms.append(self._roomsToReach.pop(0))
		while self._roomsToReach:
			self.reach()

	def moveAllMonsters(self):
		"""Permet de déplacer tous les monstres de la carte"""
		posHero = self._elem[self._hero]
		if not self._hero._invisible:
			for m in self._elem:
				posMonster = self._elem[m]
				if (
						isinstance(m, Creature.Creature)
						and not isinstance(m, Hero.Hero)
						and posHero.distance(posMonster) < 8
				):
					d = posMonster.direction(posHero, self)
					if d:
						if self.get(posMonster + d) in [Map.ground, self._hero]:
							self.move(m, d)

	def randRoom(self):
		"""
		Renvoie une salle au hasard dans la carte

		Returns
		-------
		Room.Room
			Une salle au hasard
		"""
		x1 = random.randint(0, len(self)-3)
		y1 = random.randint(0, len(self)-3)
		longueur = random.randint(3, 8)
		h = random.randint(3, 8)
		x2 = min(len(self) - 1, x1 + longueur)
		y2 = min(len(self) - 1, y1 + h)
		return Room.Room(Coord.Coord(x1, y1), Coord.Coord(x2, y2))

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

	def setVisible(self, coords):
		"""
		Permet de rendre visible la liste de coordonnées passée en paramètre
		Parameters
		----------
		coords : list
			Liste de coordonnées à rendre visibles
		"""
		self._visibleMap = [["~" for _ in range(len(self))] for _ in range(len(self))]
		for c in coords:
			self._visibleMap[c.y][c.x] = self._mat[c.y][c.x]

	def rangeElement(self, element):
		"""
		Permet de renvoyer un ensemble de coordonnées à une distance donnée d'un élément
		Parameters
		----------
		element : Element.Element
			L'élément à partir duquel on veut calculer les coordonnées

		Returns
		-------
		list

		"""
		coordDepart = self.pos(element)
		dist = theGame.theGame().range
		listeCoordonnees = []
		for i in range(coordDepart.x-dist, coordDepart.x+dist+1):
			for j in range(coordDepart.y-dist, coordDepart.y+dist+1):
				if Coord.Coord(i, j) in self and coordDepart.distance(Coord.Coord(i, j)) <= dist:
					listeCoordonnees.append(Coord.Coord(i, j))
		return listeCoordonnees