import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem
)
import psycopg2
from Publication.AjouterPublicationDialog import AjouterPublicationDialog
from Publication.ExtraireBibliographieDialog import ExtraireBibliographieDialog
class PublicationInterface(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Publication Interface")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.table_publication = QTableWidget(self)
        self.layout.addWidget(self.table_publication)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.show_ajouter_publication_dialog)
        self.layout.addWidget(self.btn_ajouter)

        self.btn_extraire_bibliographie = QPushButton("Extraire Bibliographie", self)
        self.btn_extraire_bibliographie.clicked.connect(self.extraire_bibliographie)
        self.layout.addWidget(self.btn_extraire_bibliographie)

        self.central_widget.setLayout(self.layout)

        self.populate_publication()

        self.table_publication.cellClicked.connect(self.handle_publication_selection)


    def populate_publication(self):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    pubno, titre, theme, type, volume, date, apparition,
                    editeur
                FROM Publication
            """)
            publication_data = cursor.fetchall()

            self.table_publication.setColumnCount(len(publication_data[0]))
            self.table_publication.setHorizontalHeaderLabels([
                "Pubno", "Titre", "Theme", "Type", "Volume", "Date",
                "Apparition", "Editeur"
            ])

            self.table_publication.setRowCount(len(publication_data))
            for row, publication in enumerate(publication_data):
                for col, value in enumerate(publication):
                    item = QTableWidgetItem(str(value))
                    self.table_publication.setItem(row, col, item)

        connection.close()

    def show_ajouter_publication_dialog(self):
        dialog = AjouterPublicationDialog(self)
        if dialog.exec_():
            publication_info = dialog.get_publication_info()
            self.publication_selected.emit(publication_info)

    def extraire_bibliographie(self):
        dialog = ExtraireBibliographieDialog(self)

    def handle_publication_selection(self, row, col):
        publication_info = {}
        for col in range(self.table_publication.columnCount()):
            header = self.table_publication.horizontalHeaderItem(col).text()
            item = self.table_publication.item(row, col)
            if item:
                publication_info[header] = item.text()
        self.publication_selected.emit(publication_info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PublicationInterface()
    window.show()
    sys.exit(app.exec_())