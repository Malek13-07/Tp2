from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
# aide par l'ai pour cette classe

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class CanvasMpl(FigureCanvasQTAgg):
    def __init__(self):
        # La figure contient les deux graphiques
        self.fig = Figure(layout="constrained")
        super().__init__(self.fig)

        self.ax_f = self.fig.add_subplot(1, 2, 1)   # gauche : la fonction
        self.ax_d = self.fig.add_subplot(1, 2, 2)   # droite : la dérivée

    def dessiner(self, xs, ys, dxs, dys, txs, tys, px, py, pente, taux):
        # --- Graphique de gauche : f(x) ---
        self.ax_f.clear()                        # on efface l'ancien dessin
        self.ax_f.plot(xs, ys)                   # la courbe de f
        self.ax_f.plot(txs, tys, color="red")    # la tangente en rouge
        self.ax_f.plot(px, py, "o", color="red") # le point de tangence
        self.ax_f.set_ylim(min(ys), max(ys))
        self.ax_f.set_title("f(x)")
        self.ax_f.grid(True)

        # --- Graphique de droite : f'(x) ---
        self.ax_d.clear()
        self.ax_d.plot(dxs, dys, color="green")                 # la courbe de f'
        self.ax_d.axhline(taux, linestyle="--", color="gray")
        self.ax_d.plot(px, pente, "o", color="red")             # le point (x0, f'(x0))
        self.ax_d.set_title("f'(x)")
        self.ax_d.grid(True)

        self.draw()