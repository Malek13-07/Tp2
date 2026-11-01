import numpy as np
import sympy as sp
from PyQt6.QtCore import QAbstractItemModel


class Modele_Fonction():

    def __init__(self):
        self.x = sp.symbols("x")
        self.f = None
        self.df = None
        self.x_min = -10.0
        self.x_max = 10.0
        self.x0 = 0.0               #point de la tengence
    # les setters
    def set_fonction(self, texte):
        try:
            expression = sp.sympify(texte)
            if not expression.free_symbols <= {self.x}:
                return False

            derivee = sp.diff(expression, self.x)
            f = sp.lambdify(self.x, expression, "numpy")
            df = sp.lambdify(self.x, derivee, "numpy")

            test = np.array([1.0, 2.0])
            np.broadcast_to(f(test), test.shape)
            np.broadcast_to(df(test), test.shape)
        except Exception:
            return False
        self.f = f
        self.df = df
        return True

    def set_bornes(self, x_min: float, x_max: float) -> bool:
        if x_min >= x_max:
            return False
        self.x_min = x_min
        self.x_max = x_max
        return True

    def set_x0(self, x0):
        self.x0 = x0

    def valeurs_f(self):
        #Retourne les x et les y de f entre les bornes (pour dessiner)
        xs = np.linspace(self.x_min, self.x_max, 400)

        # broadcast_to pour les fonctions constantes
        ys = np.broadcast_to(self.f(xs), xs.shape)
        return xs, ys


    def valeurs_derivee(self):
        # Retourne les x et les y de f' entre les bornes
        xs = np.linspace(self.x_min, self.x_max, 400)
        ys = np.broadcast_to(self.df(xs), xs.shape)
        return xs, ys

    def taux_variation(self):
        #Pente moyenne entre x_min et x_max
        y_min = self.f(self.x_min)
        y_max = self.f(self.x_max)
        return (y_max - y_min) / (self.x_max - self.x_min)

    def point_tangence(self):
        #Retourne le point (x0, f(x0))
        return self.x0, self.f(self.x0)

    def valeurs_tangente(self):
        # Retourne les x et les y de la droite tangente en x0
        xs = np.linspace(self.x_min, self.x_max, 400)
        pente = self.df(self.x0)  # la pente = la dérivée en x0
        y0 = self.f(self.x0)
        ys = y0 + pente * (xs - self.x0)  # équation de la droite
        return xs, ys

    def set_x0_fraction(self, fraction):
        self.set_x0(self.x_min + fraction * (self.x_max - self.x_min))

    def derivee_x0(self):
        # Pente de la tangente
        return float(self.df(self.x0))