from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class CanvasMpl(FigureCanvasQTAgg):

    def __init__(self):
        figure = Figure(figsize=(10, 4))
        super().__init__(figure)   # relie la figure Matplotlib à Qt

        # Deux graphiques côte à côte : f à gauche, f' à droite
        self.ax_f = figure.add_subplot(1, 2, 1)
        self.ax_df = figure.add_subplot(1, 2, 2)

    def dessiner_fonction(self, xs, ys,x0,y0):

        self.ax_f.clear()              # efface l'ancien dessin
        self.ax_f.plot(xs, ys)
        self.ax_f.plot(x0, y0)
        self.ax_f.set_title("f(x)")
        self.ax_f.grid(True)
        self.draw()