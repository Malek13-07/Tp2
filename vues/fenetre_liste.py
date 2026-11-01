from PyQt6.QtWidgets import (QWidget, QListView, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout)

from modeles.modele_fonction import Modele_Fonction


class FenetreListe(QWidget):
    def __init__(self, modele_liste):
        super().__init__()
        self.setWindowTitle("Liste des fonctions")
        self.modele = modele_liste
        # La QListView affiche directement le contenu du modèle
        self.vue_liste = QListView()
        self.vue_liste.setModel(self.modele)

        # Champ pour écrire une nouvelle fonction, et les deux boutons
        self.champ_nouvelle = QLineEdit()
        self.champ_nouvelle.setPlaceholderText("Nouvelle fonction, ex. cos(x)")
        self.bouton_ajouter = QPushButton("Ajouter")
        self.bouton_supprimer = QPushButton("Supprimer")

        # Disposition : liste, champ, puis les boutons côte à côte
        ligne_boutons = QHBoxLayout()
        ligne_boutons.addWidget(self.bouton_ajouter)
        ligne_boutons.addWidget(self.bouton_supprimer)

        disposition = QVBoxLayout(self)
        disposition.addWidget(self.vue_liste)
        disposition.addWidget(self.champ_nouvelle)
        disposition.addLayout(ligne_boutons)

        # Connexions
        self.champ_nouvelle.textChanged.connect(self.verifier_saisie)
        self.bouton_ajouter.clicked.connect(self.ajouter)
        self.bouton_supprimer.clicked.connect(self.supprimer)

    def verifier_saisie(self, texte):
        # Champ rouge si l'expression est invalide
        invalide = texte.strip() != "" and not Modele_Fonction().set_fonction(texte)
        self.champ_nouvelle.setStyleSheet("background-color: #ffb3b3;" if invalide else "")

    def ajouter(self):
        if self.modele.ajouter(self.champ_nouvelle.text()):
            self.champ_nouvelle.clear()
            self.modele.sauvegarder_json()      # sauvegarde dans le JSON à chaque ajout
        else:
            self.champ_nouvelle.setStyleSheet("background-color: #ffb3b3;")

    def supprimer(self):
        index = self.vue_liste.currentIndex()   # la ligne sélectionnée
        if index.isValid():
            self.modele.supprimer(index.row())
            self.modele.sauvegarder_json()      # et à chaque suppression