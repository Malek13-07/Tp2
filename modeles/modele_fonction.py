import numpy as np
import sympy as sp
class Modele_Fonction:

    def __init__(self):
        self.x=sp.Symbol("x")
        self.expression=None       # la fonction f sous la forme de sympy
        self.derivee=None          # la fonction derviée
        self.x_min=-5.0
        self.x_max=5.0
        self.x0=0.0               #point de la tengence

    def set_fonction(self, texte: str) -> bool:
        # Transforme le texte tapé par l'utilisateur en fonction et  Retourne False si invalide
        try:
            self.expression = sp.sympify(texte)
            self.derivee = sp.diff(self.expression, self.x)
            return True
        except (sp.SympifyError, TypeError):
            return False
