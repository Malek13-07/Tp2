from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout,QSlider,QHBoxLayout, QLabel, QLineEdit

from modeles.modele_fonction import Modele_Fonction
from vues.canvas_mpl import CanvasMpl


class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("fenetre_principale.ui", self)  # crée tous les widgets du .ui comme attributs

        self.modele = Modele_Fonction()
        self.canvas = CanvasMpl()
        self.layoutCanvas.addWidget(self.canvas)  # le canvas MPL est inséré dans le layout du .ui

        # Valeurs de départ
        self.spinXMin.setRange(-1000, 1000)
        self.spinXMax.setRange(-1000, 1000)
        self.spinXMin.setValue(-10)
        self.spinXMax.setValue(10)

        # Signaux
        self.champFonction.textChanged.connect(self.a_jour)
        self.spinXMin.valueChanged.connect(self.a_jour)
        self.spinXMax.valueChanged.connect(self.a_jour)
        self.sliderX0.valueChanged.connect(self.a_jour)

        self.a_jour()

    def a_jour(self):
        #  Fonction : le modèle valide, la vue colore
        fonction_ok = self.modele.set_fonction(self.champFonction.text())
        self.champFonction.setStyleSheet("" if fonction_ok else "background-color: #ffb3b3;")

        bornes_ok = self.modele.set_bornes(self.spinXMin.value(), self.spinXMax.value())

        # Le slider envoie juste sa fraction (0 à 1) ; le modèle calcule x0
        if bornes_ok:
            self.modele.set_x0_fraction(self.sliderX0.value() / 1000)
            self.labelX0.setText(f"x0 = {self.modele.x0:.2f}")

        # Dessin seulement si tout est valide
        if fonction_ok and bornes_ok:
            xs, ys = self.modele.valeurs_f()
            px, py = self.modele.point_tangence()
            self.canvas.dessiner_fonction(xs, ys, px, py)

#git config --global --add safe.directory "*"