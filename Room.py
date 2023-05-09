import random

import Coord
import Map
import Game


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
		c1 : Coord.Coord
			Coin en haut à gauche de la salle
		c2 : Coord.Coord
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
		return Coord.Coord((self.c2.x + self.c1.x) // 2, (self.c2.y + self.c1.y) // 2)

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
		coinsSelf = [self.c1, Coord.Coord(self.c2.x, self.c1.y), Coord.Coord(self.c1.x, self.c2.y), self.c2]
		coinsOther = [other.c1, Coord.Coord(other.c2.x, other.c1.y), Coord.Coord(other.c1.x, other.c2.y), other.c2]

		if any(x in other for x in coinsSelf) or any(x in self for x in coinsOther) or (other.c1 in self and other.c2 not in self) or (other.c2 in self and other.c1 not in self):
			return True

		cote1 = False
		cote2 = False

		i = 0
		while i < 2 and not cote1:
			if (min(coinsOther[i].x, coinsOther[i+2].x) <= coinsSelf[i].x <= max(coinsOther[i+2].x, coinsOther[i].x)) and (min(coinsSelf[i].y, coinsSelf[i+2].y) <= coinsOther[i].y <= max(coinsSelf[i].y, coinsSelf[i+2].y)):
				cote1 = True
			i += 1

		if cote1:
			return True

		i = 0
		while i < 2 and not cote2:
			if (min(coinsSelf[i].x, coinsSelf[i+2].x) <= coinsOther[i].x <= max(coinsSelf[i].x, coinsSelf[i+2].x)) and (min(coinsOther[i].y, coinsOther[i+2].y) <= coinsSelf[i].y <= max(coinsOther[i].y, coinsOther[i+2].y)):
				cote2 = True
			i += 1

		return cote2

	def randCoord(self):
		"""

		Returns
		-------
		Coord.Coord
			Un point de la salle au hasard
		"""
		return Coord.Coord(random.randint(self.c1.x, self.c2.x), random.randint(self.c1.y, self.c2.y))

	def existsGround(self, m):
		"""
		Parameters
		----------
		m : Map.Map
			La carte dans laquelle prendre une coordonnée

		Returns
		-------
		bool
			True s'il existe au moins une case dont la valeur est Map.ground dans la salle, False sinon
		"""

		for x in range(self.c1.x, self.c2.x+1):
			for y in range(self.c1.y, self.c2.y+1):
				if m.get(Coord.Coord(x, y)) == Map.Map.ground:
					return True
		return False

	def randEmptyCoord(self, m):
		"""

		Parameters
		----------
		m : Map.Map
			La carte dans laquelle prendre une coordonnée

		Returns
		-------
		r : Coord.Coord
			Un point de la salle au hasard qui n'est pas déjà rempli

		"""
		if not isinstance(m, Map.Map):
			raise TypeError("map doit être de type Map() !")
		if not self.existsGround(m):
			raise ValueError("Il n'existe aucune case de la salle qui ne soit remplie !")
		r = self.randCoord()
		e = m.get(r)
		while e is not Map.Map.ground or r == self.center():
			r = self.randCoord()
			e = m.get(r)
		return r

	def decorate(self, m):
		"""

		Parameters
		----------
		m : Map.Map
			La carte dans laquelle prendre une coordonnée

		"""
		m.put(self.randEmptyCoord(m), Game.theGame().randEquipment())
		m.put(self.randEmptyCoord(m), Game.theGame().randMonster())
