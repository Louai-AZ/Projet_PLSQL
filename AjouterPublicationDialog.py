from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QDateEdit
from PyQt5.QtCore import Qt, QDate
import psycopg2

class AjouterPublicationDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ajouter Publication")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        self.pubno_edit = QLineEdit(self)
        self.layout.addRow("Pubno:", self.pubno_edit)

        self.titre_edit = QLineEdit(self)
        self.layout.addRow("Titre:", self.titre_edit)

        self.theme_edit = QLineEdit(self)
        self.layout.addRow("Theme:", self.theme_edit)

        self.type_combo = QComboBox(self)
        self.type_combo.addItems(['AS', 'PC', 'P', 'L', 'T', 'M'])
        self.layout.addRow("Type:", self.type_combo)

        self.volume_edit = QLineEdit(self)
        self.layout.addRow("Volume:", self.volume_edit)

        self.date_edit = QDateEdit(self)
        self.date_edit.setDate(QDate.currentDate())
        self.layout.addRow("Date:", self.date_edit)

        self.apparition_edit = QLineEdit(self)
        self.layout.addRow("Apparition:", self.apparition_edit)

        self.editeur_edit = QLineEdit(self)
        self.layout.addRow("Editeur:", self.editeur_edit)

        self.rang_edit = QLineEdit(self)
        self.layout.addRow("Rang:", self.rang_edit)

        self.chercheur_combo = QComboBox(self)
        self.populate_chercheur_combo()
        self.layout.addRow("Chercheur:", self.chercheur_combo)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.ajouter_publication)
        self.layout.addRow(self.btn_ajouter)

        self.setLayout(self.layout)

    def populate_chercheur_combo(self):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT chnom FROM Chercheur")
                chercheurs = cursor.fetchall()
                self.chercheur_combo.addItems([chercheur[0] for chercheur in chercheurs])

        finally:
            connection.close()

    def ajouter_publication(self):
        try:
            publication_info = {
                "pubno": self.pubno_edit.text(),
                "titre": self.titre_edit.text(),
                "theme": self.theme_edit.text(),
                "type": self.type_combo.currentText(),
                "volume": int(self.volume_edit.text()),
                "date": self.date_edit.date().toString(Qt.ISODate),
                "apparition": self.apparition_edit.text(),
                "editeur": self.editeur_edit.text(),
                "rang": int(self.rang_edit.text()),
                "chno": self.get_chercheur_chno()
            }

            self.add_publication_to_database(publication_info)

            self.accept()

        except Exception as e:
            self.show_error_message(str(e))

    def get_chercheur_chno(self):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                selected_chercheur = self.chercheur_combo.currentText()
                cursor.execute("SELECT chno FROM Chercheur WHERE chnom = %s", (selected_chercheur,))
                chercheur_chno = cursor.fetchone()
                return chercheur_chno[0] if chercheur_chno else None

        finally:
            connection

    def add_publication_to_database(self, publication_info):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("Insert Into Publication Values ({}, {}, {}, {}, {}, {}, {}, {})"\
                               .format(publication_info["pubno"], publication_info["titre"],
                                       publication_info["theme"], publication_info["type"],
                                       publication_info["volume"], publication_info["date"],
                                       publication_info["apparition"], publication_info["editeur"]))
                cursor.execute("Insert Into Publier Values ({}, {}, {})"\
                               .format(publication_info["chno"], publication_info["pubno"],
                                       publication_info["rang"]))

        finally:
            connection