import Coord
import Map

class Noeud(object):
	def __init__(self, pos, cout=0, heuristique = 0, parent = None):
		self.pos = pos
		self.cout = cout
		self.heuristique = heuristique
		self.parent = parent

	def manhattanDistance(self, other):
		if isinstance(other, Noeud):
			return abs(self.pos.x - other.pos.x) + abs(self.pos.y - other.pos.y)

	def shortestPath(self, other, map):
		listeFermee = []
		listeOuverte = [self]

		while listeOuverte:
			listeOuverte.sort(key=lambda x: x.heuristique)
			noeudCourant = listeOuverte.pop(0)
			if noeudCourant.pos == other.pos:
				return self.reconstructPath(noeudCourant)
			voisins = noeudCourant.voisins(map)
			for voisin in voisins:
				if voisin not in listeFermee:
					newCost = noeudCourant.cout + 1
					if voisin not in listeOuverte or newCost < voisin.cost:
						voisin.cout = newCost
						voisin.heuristique = newCost + voisin.manhattanDistance(other)
						voisin.parent = noeudCourant

						if voisin not in listeOuverte:
							listeOuverte.append(voisin)
			listeFermee.append(noeudCourant)
		return None

	def voisins(self, map):
		listeVoisins = []
		for i in range(self.pos.x-1, self.pos.x+2):
			for j in range(self.pos.y-1, self.pos.y+2):
				if i == j == 0:
					continue
				if map.get(Coord.Coord(i, j)) in [Map.Map.ground, map._hero]:
					listeVoisins.append(Noeud(Coord.Coord(i, j), self.cout+1, self.heuristique, self))
		return listeVoisins


	def reconstructPath(self, noeud):
		path = []
		while noeud.parent:
			path.append(noeud.pos)
			noeud = noeud.parent
		return path[::-1]