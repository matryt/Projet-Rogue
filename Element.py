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

    def __init__(self, name, abbrv=None, resum="a thing"):
        """

        Parameters
        ----------
        name : str
                Le nom de l'élément
        abbrv : str, optional
                L'abréviation représentant l'élément
        """
        self._name = name
        self._abbrv = abbrv or name[0]
        self.resume = resum

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
        """
        Raises
        -------
        NotImplementedError
                Cette méthode doit être implémentée dans les classes filles
        """
        raise NotImplementedError("Not implemented yet")
