import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import pyqtSignal
import psycopg2
from AjouterChercheurDialog import AjouterChercheurDialog
from MainDashboard import MainDashboard  


class ChercheurInterface(QMainWindow):
    chercheur_selected = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chercheur Interface")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.table_chercheurs = QTableWidget(self)
        self.layout.addWidget(self.table_chercheurs)

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
        
        self.btn_back = QPushButton("Back to Main Dashboard", self)
        self.btn_back.clicked.connect(self.return_to_main_dashboard)
        self.layout.addWidget(self.btn_back)

        self.central_widget.setLayout(self.layout)

        self.populate_chercheurs()

        self.table_chercheurs.cellClicked.connect(self.handle_chercheur_selection)


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
                ORDER BY c.chno ASC 
            """)
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


    def show_ajouter_chercheur_dialog(self):
        dialog = AjouterChercheurDialog(self)
        if dialog.exec_():
            chercheur_info = dialog.ajouter_chercheur()
            if chercheur_info:
                self.chercheur_selected.emit(chercheur_info)


    def handle_chercheur_added(self):
        self.populate_chercheurs()


    def modifier_chercheur(self):
        print("Modifier Chercheur clicked")

    def supprimer_chercheur(self):
        print("Supprimer Chercheur clicked")

    def consulter_articles(self):
        print("Consulter Articles clicked")

    def return_to_main_dashboard(self):
        self.close()
        main_dashboard = MainDashboard()
        main_dashboard.show()

    def handle_chercheur_selection(self, row, col):
        chercheur_info = {}
        for col in range(self.table_chercheurs.columnCount()):
            header = self.table_chercheurs.horizontalHeaderItem(col).text()
            item = self.table_chercheurs.item(row, col)
            if item:
                chercheur_info[header] = item.text()
        self.chercheur_selected.emit(chercheur_info)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChercheurInterface()
    window.show()
    sys.exit(app.exec_())


