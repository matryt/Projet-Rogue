import math
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

	def __mul__(self, other):
		if isinstance(other, int):
			return Coord(self.x * other, self.y * other)

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

	def voisins(self, map):
		listeVoisins = [
			Coord(self.x, self.y+1),
			Coord(self.x, self.y-1),
			Coord(self.x+1, self.y),
			Coord(self.x-1, self.y)
		]
		i = 0
		while i < len(listeVoisins):
			v = listeVoisins[i]
			if v not in map or map.get(v) == Map.Map.empty:
				listeVoisins.pop(i)
			else:
				i+=1
		return listeVoisins

	def direction(self, other, floor):
		"""
		Calcule la direction entre deux points
		Parameters
		----------
		other : Coord
			Le deuxième point
		floor : Map.Map
			La carte sur laquelle se trouvent les points

		Returns
		-------
		Coord
			La direction entre les deux points
		"""
		n1 = Noeud.Noeud(self)
		n2 = Noeud.Noeud(other)
		chemin = n1.shortestPath(n2, floor)
		if chemin:
			return chemin[0] - self
		return None
