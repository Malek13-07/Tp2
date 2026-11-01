import sys
from PyQt6.QtWidgets import QApplication
from vues.fenetre_principale import FenetrePrincipale
from modeles.modele_liste import ModeleListeFonctions
if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    fenetre.show()
    sys.exit(app.exec())

m = ModeleListeFonctions("fonctions.json")
m.charger_json()
print(m.fonctions)               # doit afficher les 3 fonctions
print(m.ajouter("cos(x)"))       # True
print(m.ajouter("y + 1"))
m.sauvegarder_json()