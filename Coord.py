import math
import random
import Hero
import Map
import Noeud


class Coord(object):
	"""
	Point d'un plan représenté par une abscisse et une ordonnée

	...
	Attributes
	----------
	x
	y
	"""

	def __init__(self, x=0, y=0):
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
		if type(self) is type(other):
			return self.x == other.x and self.y == other.y
		return False

	def __hash__(self):
		return hash(str(self))

	def __add__(self, other):
		return Coord(self.x+other.x, self.y+other.y)

	def __sub__(self, other):
		return Coord(self.x-other.x, self.y-other.y)

	def distance(self, other):
		"""
		Calcule la distance entre deux points

		Parameters
		----------
		other : Coord
			Le deuxième point

		Returns
		-------
		float
			La distance entre les deux points
		"""
		return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

	def direction(self, other, floor):
		"""
		Calcule la direction entre deux points

		Parameters
		----------
		other : Coord
			Le deuxième point
		floor : Map.Map
			La carte du jeu

		Returns
		-------
		Coord
			La direction entre les deux points

		"""
		possibleDirections = []
		for d in floor.dir.values():
			if self + d in floor:
				elem = floor.get(self + d)
				if isinstance(elem, Hero.Hero) or elem == Map.Map.ground and other.distance(self + d) <= other.distance(
						self) and self + d in floor:
					possibleDirections.append(d)
		if possibleDirections:
			return random.choice(possibleDirections)

	def direction(self, other, floor):
		n1 = Noeud.Noeud(self)
		n2 = Noeud.Noeud(other)
		chemin = n1.shortestPath(n2, floor)
		return chemin[0] - self
