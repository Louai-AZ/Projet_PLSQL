from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QDateEdit
from PyQt5.QtCore import Qt, QDate
import psycopg2
from BibliographieDialog import BibliographieDialog

class ExtraireBibliographieDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Extraire Bibliographie")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        self.publication_combo = QComboBox(self)
        self.populate_publication_combo()
        self.layout.addRow("Publication:", self.publication_combo)

        self.btn_consulter = QPushButton("Consulter", self)
        self.btn_consulter.clicked.connect(self.extraire_bibliographie)
        self.layout.addRow(self.btn_consulter)

        self.setLayout(self.layout)

    def populate_publication_combo(self):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT titre FROM Publication")
                publications = cursor.fetchall()
                self.publication_combo.addItems([publication[0] for publication in publications])

        finally:
            connection.close()

    def extraire_bibliographie(self):
        dialog = BibliographieDialog(self, pubno=self.publication_combo.currentText())
