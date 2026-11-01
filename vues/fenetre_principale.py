from PyQt6 import uic
from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout,QSlider,QHBoxLayout, QLabel, QLineEdit
from modeles.modele_liste import ModeleListeFonctions
from vues.fenetre_liste import FenetreListe
from modeles.modele_fonction import Modele_Fonction
from vues.canvas_mpl import CanvasMpl


class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Path(__file__).parent / "fenetre_principale.ui", self)

        # Le modèle
        self.modele = Modele_Fonction()


        layout_canvas = QVBoxLayout(self.widgetCanvas)
        layout_canvas.setContentsMargins(0, 0, 0, 0)
        self.canvas = CanvasMpl()
        layout_canvas.addWidget(self.canvas)

        # Valeurs de départ
        self.champFonction.setText("x**2")
        self.spinXMin.setRange(-1000, 1000)
        self.spinXMax.setRange(-1000, 1000)
        self.spinXMin.setValue(-10)
        self.spinXMax.setValue(10)

        # Signaux et slots
        self.champFonction.textChanged.connect(self.mise_a_jour)
        self.spinXMin.valueChanged.connect(self.mise_a_jour)
        self.spinXMax.valueChanged.connect(self.mise_a_jour)
        self.sliderX0.valueChanged.connect(self.mise_a_jour)
        # Modèle de la liste : chargé depuis le JSON au démarrage
        chemin_json = Path(__file__).parent.parent / "fonctions.json"
        self.modele_liste = ModeleListeFonctions(str(chemin_json))
        self.modele_liste.charger_json()

        # Fenêtre de la liste
        self.fenetre_liste = FenetreListe(self.modele_liste)
        self.fenetre_liste.show()
        self.mise_a_jour()

    def mise_a_jour(self):
        #  Fonction : le modèle valide, la vue colore
        fonction_ok = self.modele.set_fonction(self.champFonction.text())
        self.champFonction.setStyleSheet("" if fonction_ok else "background-color: #ffb3b3;")

        bornes_ok = self.modele.set_bornes(self.spinXMin.value(), self.spinXMax.value())

        # Le slider envoie juste sa fraction et le modèle calcule x0
        if bornes_ok:
            self.modele.set_x0_fraction(self.sliderX0.value() / 1000)
            self.labelX0.setText(f"x0 = {self.modele.x0:.2f}")

        # Dessin ssi tout est valide
        if fonction_ok and bornes_ok:
            xs, ys = self.modele.valeurs_f()
            dxs, dys = self.modele.valeurs_derivee()
            txs, tys = self.modele.valeurs_tangente()
            px, py = self.modele.point_tangence()
            pente = self.modele.derivee_x0()
            taux = float(self.modele.taux_variation())
            self.canvas.dessiner(xs, ys, dxs, dys, txs, tys, px, py, pente, taux)
            self.labelTaux.setText(f"{taux:.3f}")
            self.labelPointX0.setText(f"{px:.3f}")
            self.labelDerivee.setText(f"{pente:.3f}")
