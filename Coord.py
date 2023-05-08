import math


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

    def direction(self, other):
        """
        Calcule la direction entre deux points

        Parameters
        ----------
        other : Coord
            Le deuxième point

        Returns
        -------
        Coord
            La direction entre les deux points

        """
        difference = self - other
        cos = difference.x / self.distance(other)
        if cos > 1 / math.sqrt(2):
            return Coord(-1, 0)
        elif cos < -1 / math.sqrt(2):
            return Coord(1, 0)
        elif difference.y > 0:
            return Coord(0, -1)
        else:
            return Coord(0, 1)
