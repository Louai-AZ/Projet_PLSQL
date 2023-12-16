import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem, QGroupBox
)
from PyQt5.QtCore import pyqtSignal
import psycopg2
from AjouterChercheurDialog import AjouterChercheurDialog  

class ChercheurInterface(QMainWindow):
    chercheur_selected = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chercheur Interface")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Table to display all columns from CHERCHEUR
        self.table_chercheurs = QTableWidget(self)
        self.layout.addWidget(self.table_chercheurs)

        # Buttons for actions
        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.show_ajouter_chercheur_dialog)
        self.layout.addWidget(self.btn_ajouter)

        self.btn_modifier = QPushButton("Modifier", self)
        self.btn_modifier.clicked.connect(self.modifier_chercheur)
        self.layout.addWidget(self.btn_modifier)

        self.btn_supprimer = QPushButton("Supprimer", self)
        self.btn_supprimer.clicked.connect(self.supprimer_chercheur)
        self.layout.addWidget(self.btn_supprimer)

        self.btn_consulter_articles = QPushButton("Consulter Articles", self)
        self.btn_consulter_articles.clicked.connect(self.consulter_articles)
        self.layout.addWidget(self.btn_consulter_articles)

        self.central_widget.setLayout(self.layout)

        # Populate the table with chercheurs data
        self.populate_chercheurs()

        # Connect the signal to handle the selected chercheur
        self.table_chercheurs.cellClicked.connect(self.handle_chercheur_selection)

    def populate_chercheurs(self):
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        with connection.cursor() as cursor:
            # Fetch chercheurs information with joined data
            cursor.execute("""
                SELECT
                    c.chno, c.chnom, c.grade, c.statut, c.daterecrut,
                    c.salaire, c.prime, c.email, s.chnom AS supnom,
                    l.labnom, f.facnom
                FROM Chercheur c
                LEFT JOIN Chercheur s ON c.supno = s.chno
                LEFT JOIN Laboratoire l ON c.labno = l.labno
                LEFT JOIN Faculte f ON c.facno = f.facno
            """)
            chercheurs_data = cursor.fetchall()

            # Populate the table with chercheurs data
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

    def show_ajouter_chercheur_dialog(self):
        dialog = AjouterChercheurDialog(self)
        if dialog.exec_():
            # Dialog was accepted (user clicked "Ajouter" in the dialog)
            chercheur_info = dialog.get_chercheur_info()
            self.chercheur_selected.emit(chercheur_info)

    def modifier_chercheur(self):
        # Implement logic to modify the selected chercheur
        print("Modifier Chercheur clicked")

    def supprimer_chercheur(self):
        # Implement logic to delete the selected chercheur
        print("Supprimer Chercheur clicked")

    def consulter_articles(self):
        # Implement logic to consult articles for the selected chercheur
        print("Consulter Articles clicked")

    def handle_chercheur_selection(self, row, col):
        # Retrieve chercheur information for the selected row
        chercheur_info = {}
        for col in range(self.table_chercheurs.columnCount()):
            header = self.table_chercheurs.horizontalHeaderItem(col).text()
            item = self.table_chercheurs.item(row, col)
            if item:
                chercheur_info[header] = item.text()

        # Emit the signal with the selected chercheur's information
        self.chercheur_selected.emit(chercheur_info)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChercheurInterface()
    window.show()
    sys.exit(app.exec_())


