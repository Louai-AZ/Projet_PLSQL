from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QDateEdit
from PyQt5.QtCore import Qt, QDate
import psycopg2
from Laboratoire.HierarchieDialog import HierarchieDialog

class AfficherHierarchieDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Afficher Bibliographie")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        self.laboratoire_combo = QComboBox(self)
        self.populate_lab_combo()
        self.layout.addRow("Laboratoire:", self.laboratoire_combo)

        self.btn_afficher = QPushButton("Afficher", self)
        self.btn_afficher.clicked.connect(self.afficher_hierarchie)
        self.layout.addRow(self.btn_afficher)

        self.setLayout(self.layout)

    def populate_lab_combo(self):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT labnom FROM Laboratoire ")
                labs = cursor.fetchall()
                self.lab_combo.addItems([lab[0] for lab in labs])

        finally:
            connection.close()

    def afficher_hierarchie(self):
        dialog = HierarchieDialog(self, labno=self.laboratoire_combo.currentText())
