import math
import random
import Hero
import Map


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

	def direction(self, other, map):
		"""
		Calcule la direction entre deux points

		Parameters
		----------
		other : Coord
			Le deuxième point
		map : Map.Map
			La carte du jeu

		Returns
		-------
		Coord
			La direction entre les deux points

		"""
		l = []
		for d in map.dir.values():
			elem = map.get(self + d)
			if isinstance(elem, Hero.Hero) or elem == Map.Map.ground and other.distance(self+d) <= other.distance(self) and self+d in map:
				l.append(d)
		if l:
			return random.choice(l)