import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import pyqtSignal
import psycopg2
from AjouterLaboratoireDialog import AjouterLaboratoireDialog
from Laboratoire.AfficherHierarchieDialog import AfficherHierarchieDialog

class LaboratoireInterface(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Laboratoire Interface")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.table_laboratoire = QTableWidget(self)
        self.layout.addWidget(self.table_laboratoire)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.show_ajouter_laboratoire_dialog)
        self.layout.addWidget(self.btn_ajouter)

        self.btn_afficher_hierarchie = QPushButton("Afficher Hierarchie", self)
        self.btn_afficher_hierarchie.clicked.connect(self.afficher_hierarchie)
        self.layout.addWidget(self.btn_afficher_hierarchie)

        self.central_widget.setLayout(self.layout)

        self.populate_laboratoire()

    def populate_laboratoire(self):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    l.labno, l.labnom, l.facno
                FROM Laboratoire l
                LEFT JOIN Faculte f ON l.facno = f.facno
            """)
            laboratoire_data = cursor.fetchall()

            self.table_laboratoire.setColumnCount(len(laboratoire_data[0]))
            self.table_laboratoire.setHorizontalHeaderLabels([
                "Labno", "Labnom", "Facno"
            ])

            self.table_laboratoire.setRowCount(len(laboratoire_data))
            for row, laboratoire in enumerate(laboratoire_data):
                for col, value in enumerate(laboratoire):
                    item = QTableWidgetItem(str(value))
                    self.table_laboratoire.setItem(row, col, item)

        connection.close()

    def show_ajouter_laboratoire_dialog(self):
        dialog = AjouterLaboratoireDialog(self)
        if dialog.exec_():
            laboratoire_info = dialog.get_laboratoire_info()
            self.laboratoire_selected.emit(laboratoire_info)

    def extraire_bibliographie(self):
        dialog = AfficherHierarchieDialog(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LaboratoireInterface()
    window.show()
    sys.exit(app.exec_())