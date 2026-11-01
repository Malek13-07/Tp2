from PyQt6 import uic
from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSlider, QHBoxLayout, QLabel, QLineEdit, QFileDialog
from modeles.modele_liste import ModeleListeFonctions
from vues.fenetre_liste import FenetreListe
from modeles.modele_fonction import Modele_Fonction
from vues.canvas_mpl import CanvasMpl


class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Path(__file__).parent / "fenetre_principale.ui", self)

        # Modèles
        self.modele = Modele_Fonction()
        chemin_json = Path(__file__).parent.parent / "fonctions.json"
        self.modele_liste = ModeleListeFonctions(str(chemin_json))
        self.modele_liste.charger_json()

        # Canvas dans le widget vide
        layout_canvas = QVBoxLayout(self.widgetCanvas)
        layout_canvas.setContentsMargins(0, 0, 0, 0)
        self.canvas = CanvasMpl()
        layout_canvas.addWidget(self.canvas)

        # Le combo affiche la liste du modèle
        self.comboFonctions.setModel(self.modele_liste)
        self.comboFonctions.setCurrentIndex(0)

        # Bornes de départ
        self.spinXMin.setRange(-1000, 1000)
        self.spinXMax.setRange(-1000, 1000)
        self.spinXMin.setValue(-10)
        self.spinXMax.setValue(10)

        # Fenêtre de la liste
        self.fenetre_liste = FenetreListe(self.modele_liste)
        self.fenetre_liste.show()

        # Signaux
        self.comboFonctions.currentIndexChanged.connect(self.mise_a_jour)
        self.modele_liste.rowsInserted.connect(self.selectionner_derniere)
        self.spinXMin.valueChanged.connect(self.borne_changee)
        self.spinXMax.valueChanged.connect(self.borne_changee)
        self.sliderX0.valueChanged.connect(self.mise_a_jour)
        self.actionGrille.setChecked(True)
        self.actionGrille.toggled.connect(self.changer_grille)
        self.actionExporterPdf.triggered.connect(self.exporter_pdf)

        self.borne_changee()

    def selectionner_derniere(self):
        # Après un ajout, on sélectionne la nouvelle fonction
        self.comboFonctions.setCurrentIndex(self.modele_liste.rowCount() - 1)

    def mise_a_jour(self):
        # Fonction : le modèle valide, la vue colore
        fonction_ok = self.modele.set_fonction(self.comboFonctions.currentText())
        self.comboFonctions.setStyleSheet("" if fonction_ok else "background-color: #ffb3b3;")

        # Bornes et point de tangence
        bornes_ok = self.modele.set_bornes(self.spinXMin.value(), self.spinXMax.value())
        if bornes_ok:
            self.modele.set_x0_fraction(self.sliderX0.value() / 1000)
            self.labelX0.setText(f"x0 = {self.modele.x0:.2f}")

        # Dessin et valeurs affichées
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

    def borne_changee(self):
        #  xMax reste au-dessus de xMin
        pas = 0.1
        self.spinXMax.setMinimum(self.spinXMin.value() + pas)
        self.spinXMin.setMaximum(self.spinXMax.value() - pas)
        self.mise_a_jour()

    def changer_grille(self, visible):
        # Le menu coché envoie True ou False
        self.canvas.grille = visible
        self.mise_a_jour()

    def exporter_pdf(self):
        # Boîte de dialogue pour choisir où enregistrer
        chemin, _ = QFileDialog.getSaveFileName(self, "Exporter en PDF", "graphique.pdf", "PDF (*.pdf)")
        if chemin:
            self.canvas.fig.savefig(chemin)   # savefig écrit la figure dans le fichier