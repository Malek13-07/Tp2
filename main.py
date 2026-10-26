
import sys
from PyQt6.QtWidgets import QApplication
from vues.fenetre_principale import FenetrePrincipale

app = QApplication(sys.argv)
fenetre = FenetrePrincipale()
fenetre.show()
sys.exit(app.exec())
