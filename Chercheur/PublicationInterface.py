import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QWidget,QApplication
import psycopg2

class PublicationInterface(QDialog):
    def __init__(self, chno):
        super().__init__()

        self.setWindowTitle("Publication Interface")
        self.setGeometry(250, 250, 800, 500)

        self.central_widget = QWidget(self)

        self.layout = QVBoxLayout()

        self.label = QLabel(f"Publications for Chercheur with Chno: {chno}")
        self.layout.addWidget(self.label)

        self.table_publications = QTableWidget(self)
        self.layout.addWidget(self.table_publications)

        self.populate_publications(chno)

        self.central_widget.setLayout(self.layout)

    def populate_publications(self, chno):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.titre, p.theme,p.apparition, p.editeur, pu.rang
                FROM publication p
                JOIN "publier" pu ON p.pubno = pu.pubno
                WHERE pu.chno = %s
            """, (chno,))

            publications_data = cursor.fetchall()

            print("*"*100)
            print(publications_data)
            print("*"*100)

            self.table_publications.setColumnCount(len(publications_data[0]))
            self.table_publications.setHorizontalHeaderLabels([
                "Titre", "Theme","Apparition" ,"Editeur", "Rang"
            ])

            self.table_publications.setRowCount(len(publications_data))
            for row, publication in enumerate(publications_data):
                for col, value in enumerate(publication):
                    item = QTableWidgetItem(str(value))
                    self.table_publications.setItem(row, col, item)

        connection.close()
