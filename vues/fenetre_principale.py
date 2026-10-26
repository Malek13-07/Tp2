from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout,QSlider,QHBoxLayout, QLabel, QLineEdit

from modeles.modele_fonction import Modele_Fonction
from vues.canvas_mpl import CanvasMpl


class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fonction et dérivée")

        # Le modèle : c'est lui qui fait les maths
        self.modele = Modele_Fonction()

        # Les champs de saisie
        self.champ_fonction = QLineEdit("x**2")
        self.champ_xmin = QLineEdit("-10")
        self.champ_xmax = QLineEdit("10")

        # le slider pour x0
        self.slider=QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0,1000)
        self.slider.setValue(500)
        self.label_x0=QLabel("x0 = 0")


        #  Le canvas Matplotlib
        self.canvas = CanvasMpl()

        #  Disposition : une ligne de champs, puis le canvas
        ligne_champs = QHBoxLayout()
        ligne_champs.addWidget(QLabel("f(x) ="))
        ligne_champs.addWidget(self.champ_fonction)
        ligne_champs.addWidget(QLabel("x min"))
        ligne_champs.addWidget(self.champ_xmin)
        ligne_champs.addWidget(QLabel("x max"))
        ligne_champs.addWidget(self.champ_xmax)

        ligne_slider=QHBoxLayout()
        ligne_slider.addWidget(QLabel("le point de tengance :"))
        ligne_slider.addWidget(self.slider)
        ligne_slider.addWidget(self.label_x0)


        disposition = QVBoxLayout()
        disposition.addLayout(ligne_champs)
        disposition.addWidget(self.canvas)

        conteneur = QWidget()
        conteneur.setLayout(disposition)
        self.setCentralWidget(conteneur)

        # Dès qu'on modifie un champ, on met à jour le dessin
        self.champ_fonction.textChanged.connect(self.a_jour)
        self.champ_xmin.textChanged.connect(self.a_jour)
        self.champ_xmax.textChanged.connect(self.a_jour)
        self.slider.valueChanged.connect(self.a_jour)

        self.a_jour()  # premier dessin au démarrage

    def a_jour(self):
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

        # conversion de la position du slider en vraie valeur de x0
        fraction= self.slider.value()/1000
        x0= x_min + fraction*(x_max-x_min)
        self.modele.set_x0(x0)
        self.label_x0.setText(str(x0))


        # On dessine seulement si tout est valide
        if fonction_ok and bornes_ok:
            xs, ys = self.modele.valeurs_f()
            px,py = self.modele.point_tangence()
            self.canvas.dessiner_fonction(xs, ys,px,py)
