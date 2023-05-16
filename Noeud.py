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
		raise NotImplementedError

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
					if voisin not in listeOuverte or newCost < voisin.cout:
						voisin.cout = newCost
						voisin.heuristique = newCost + voisin.manhattanDistance(other)
						voisin.parent = noeudCourant

						if voisin not in listeOuverte:
							listeOuverte.append(voisin)
			if noeudCourant not in listeFermee:
				listeFermee.append(noeudCourant)
			if len(listeFermee) >= len(map)**2:
				return None
		return None

	def voisins(self, map):
		listeVoisins = [
			Noeud(Coord.Coord(self.pos.x, self.pos.y+1), self.cout+1),
			Noeud(Coord.Coord(self.pos.x, self.pos.y-1), self.cout+1),
			Noeud(Coord.Coord(self.pos.x+1, self.pos.y), self.cout+1),
			Noeud(Coord.Coord(self.pos.x-1, self.pos.y), self.cout+1)
		]
		i = 0
		while i < len(listeVoisins):
			v = listeVoisins[i]
			if v.pos not in map or map.get(v.pos) not in [Map.Map.ground, map._hero]:
				listeVoisins.pop(i)
			else:
				i+=1
		return listeVoisins

	def reconstructPath(self, noeud):
		path = []
		while noeud.parent:
			path.append(noeud.pos)
			noeud = noeud.parent
		return path[::-1]