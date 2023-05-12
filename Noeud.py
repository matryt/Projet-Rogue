class Noeud:
    def __init__(self, position=None):
        self.parent = None
        self.cout_g = 0
        self.cout_h = 0
        self.cout_f = 0
        self.position = position   # ajout de l'attribut position