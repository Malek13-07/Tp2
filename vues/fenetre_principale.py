from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit)

from modeles.modele_fonction import Modele_Fonction
from vues.canvas_mpl import CanvasMpl


class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fonction et dérivée")

        # Le modèle : c'est lui qui fait les maths
        self.modele = Modele_Fonction()

        # --- Les champs de saisie ---
        self.champ_fonction = QLineEdit("x**2")
        self.champ_xmin = QLineEdit("-10")
        self.champ_xmax = QLineEdit("10")

        # --- Le canvas Matplotlib ---
        self.canvas = CanvasMpl()

        # --- Disposition : une ligne de champs, puis le canvas ---
        ligne_champs = QHBoxLayout()
        ligne_champs.addWidget(QLabel("f(x) ="))
        ligne_champs.addWidget(self.champ_fonction)
        ligne_champs.addWidget(QLabel("x min"))
        ligne_champs.addWidget(self.champ_xmin)
        ligne_champs.addWidget(QLabel("x max"))
        ligne_champs.addWidget(self.champ_xmax)

        disposition = QVBoxLayout()
        disposition.addLayout(ligne_champs)
        disposition.addWidget(self.canvas)

        conteneur = QWidget()
        conteneur.setLayout(disposition)
        self.setCentralWidget(conteneur)

        # Dès qu'on modifie un champ, on met à jour le dessin
        self.champ_fonction.textChanged.connect(self.mettre_a_jour)
        self.champ_xmin.textChanged.connect(self.mettre_a_jour)
        self.champ_xmax.textChanged.connect(self.mettre_a_jour)

        self.mettre_a_jour()   # premier dessin au démarrage

    def mettre_a_jour(self):
        #  La fonction : le modèle dit si elle est valide
        fonction_ok = self.modele.set_fonction(self.champ_fonction.text())
        if fonction_ok:
            self.champ_fonction.setStyleSheet("")                       # normal
        else:
            self.champ_fonction.setStyleSheet("background-color: #ffb3b3;")  # rouge

        # Les bornes : on essaie de convertir le texte en nombre
        try:
            x_min = float(self.champ_xmin.text())
            x_max = float(self.champ_xmax.text())
        except ValueError:
            return

        bornes_ok = self.modele.set_bornes(x_min, x_max)

        # On dessine seulement si tout est valide
        if fonction_ok and bornes_ok:
            xs, ys = self.modele.valeurs_f()
            self.canvas.dessiner_fonction(xs, ys)
