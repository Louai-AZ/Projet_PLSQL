from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit
from PyQt5.QtCore import Qt, QDate
import psycopg2

class AjouterFaculteDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ajouter Faculte")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        self.facno_edit = QLineEdit(self)
        self.layout.addRow("Facno:", self.facno_edit)

        self.facnom_edit = QLineEdit(self)
        self.layout.addRow("Facnom:", self.facnom_edit)

        self.adresse_edit = QLineEdit(self)
        self.layout.addRow("Adresse:", self.adresse_edit)

        self.libelle_edit = QLineEdit(self)
        self.layout.addRow("Libellé:", self.libelle_edit)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.ajouter_faculte)
        self.layout.addRow(self.btn_ajouter)

        self.setLayout(self.layout)

    def ajouter_faculte(self):
        try:
            faculte_info = {
                "facno": int(self.facno_edit.text()),
                "facnom": self.facnom_edit.text(),
                "adresse": self.adresse_edit.text(),
                "libellé": self.libelle_edit.text()
            }

            self.add_faculte_to_database(faculte_info)

            self.accept()

        except Exception as e:
            self.show_error_message(str(e))

    def add_faculte_to_database(self, faculte_info):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("Insert Into Faculte Values ({}, {}, {}, {})"\
                               .format(faculte_info["facno"], faculte_info["facnom"],
                                       faculte_info["adresse"], faculte_info["libellé"]))
        finally:
            connection