from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QTableWidget, QFormLayout, QLineEdit, QComboBox, QPushButton, QDateEdit
from PyQt5.QtCore import Qt, QDate
import psycopg2

class BibliographieDialog(QDialog):
    pubno = ""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Bibliographie")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        self.table_chercheurs = QTableWidget(self)
        self.layout.addWidget(self.table_chercheurs)

        self.populate_chercheurs()

        self.setLayout(self.layout)

    def populate_chercheurs(self):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    c.chno, c.chnom, c.grade, c.statut, c.daterecrut,
                    c.salaire, c.prime, c.email, s.chnom AS supnom,
                    l.labnom, f.facnom
                FROM Chercheur c
                LEFT JOIN Chercheur s ON c.supno = s.chno
                LEFT JOIN Laboratoire l ON c.labno = l.labno
                LEFT JOIN Faculte f ON c.facno = f.facno
                WHERE c.chno = (
                SELECT chno FROM Publier pr
                LEFT JOIN Publication pn ON pr.pubno = pn.pubno
                WHERE pn.pubno = %s )
            """, (self.pubno))
            chercheurs_data = cursor.fetchall()

            self.table_chercheurs.setColumnCount(len(chercheurs_data[0]))
            self.table_chercheurs.setHorizontalHeaderLabels([
                "Chno", "Chnom", "Grade", "Statut", "DateRecrut", "Salaire",
                "Prime", "Email", "Supnom", "Labnom", "Facnom"
            ])

            self.table_chercheurs.setRowCount(len(chercheurs_data))
            for row, chercheur in enumerate(chercheurs_data):
                for col, value in enumerate(chercheur):
                    item = QTableWidgetItem(str(value))
                    self.table_chercheurs.setItem(row, col, item)

        connection.close()