
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
        self.grille = True
        self.couleur_f = "#1f77b4"
        self.couleur_derivee = "#2ca02c"
        self.couleur_tangente = "#d62728"

    def dessiner(self, xs, ys, dxs, dys, txs, tys, px, py, pente, taux):
        # --- Graphique de gauche : f(x) ---
        self.ax_f.clear()                        # on efface l'ancien dessin
        self.ax_f.plot(xs, ys, color=self.couleur_f)
        self.ax_f.plot(txs, tys, color=self.couleur_tangente)
        self.ax_f.plot(px, py, "o", color=self.couleur_tangente)
        self.ax_f.set_ylim(min(ys), max(ys))
        self.ax_f.set_title("f(x)")
        self.ax_f.grid(self.grille)

        # --- Graphique de droite : f'(x) ---
        self.ax_d.clear()
        self.ax_d.plot(dxs, dys, color=self.couleur_derivee)
        self.ax_d.plot(px, pente, "o", color=self.couleur_tangente)
        self.ax_d.set_title("f'(x)")
        self.ax_d.grid(self.grille)

        self.draw()