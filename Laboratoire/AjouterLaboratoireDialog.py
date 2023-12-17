from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QDateEdit
from PyQt5.QtCore import Qt, QDate
import psycopg2

class AjouterLaboratoireDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ajouter Laboratoire")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        self.labno_edit = QLineEdit(self)
        self.layout.addRow("Labno:", self.labno_edit)

        self.labnom_edit = QLineEdit(self)
        self.layout.addRow("Labnom:", self.labnom_edit)

        self.faculty_combo = QComboBox(self)
        self.populate_faculty_combo()
        self.layout.addRow("Faculté:", self.faculty_combo)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.ajouter_laboratoire)
        self.layout.addRow(self.btn_ajouter)

        self.setLayout(self.layout)

    def populate_faculty_combo(self):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT facnom FROM Faculte")
                faculties = cursor.fetchall()
                self.faculty_combo.addItems([fac[0] for fac in faculties])

        finally:
            connection.close()

    def ajouter_laboratoire(self):
        try:
            laboratoire_info = {
                "labno": int(self.labno_edit.text()),
                "labnom": self.labnom_edit.text(),
                "facno": self.get_facno()
            }

            self.add_laboratoire_to_database(laboratoire_info)

            self.accept()

        except Exception as e:
            self.show_error_message(str(e))

    def get_facno(self):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                selected_faculty = self.faculty_combo.currentText()
                cursor.execute("SELECT facno FROM Faculte WHERE facnom = %s", (selected_faculty,))
                facno = cursor.fetchone()
                return facno[0] if facno else None

        finally:
            connection.close()

    def add_laboratoire_to_database(self, laboratoire_info):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("Insert Into Laboratoire Values ({}, {}, {})"\
                               .format(laboratoire_info["labno"], laboratoire_info["labnom"],
                                       laboratoire_info["facno"]))

        finally:
            connection