import numpy as np
import sympy as sp
class Modele_Fonction:

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
            derivee = sp.diff(expression, self.x)
            self.f = sp.lambdify(self.x, expression, "numpy")
            self.df = sp.lambdify(self.x, derivee, "numpy")
            return True
        except Exception:
            return False

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

        # broadcast_to sert pour les fonctions constantes
        ys = np.broadcast_to(self.f(xs), xs.shape)
        return xs, ys


    def valeurs_derivee(self):
        # Retourne les x et les y de f' entre les bornes
        xs = np.linspace(self.x_min, self.x_max, 400)
        ys = np.broadcast_to(self.df(xs), xs.shape)
        return xs, ys

    def taux_variation(self):
        #Pente moyenne entre x_min et x_max : (f(b) - f(a)) / (b - a)
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
