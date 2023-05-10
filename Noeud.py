class Noeud:
    def __init__(self, parent=None, cout_g=0, cout_h=0):
        self.parent = parent
        self.cout_g = cout_g
        self.cout_h = cout_h
        self.cout_f = cout_g + cout_h
