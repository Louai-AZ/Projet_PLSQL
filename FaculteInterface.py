import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import pyqtSignal
import psycopg2
from AjouterFaculteDialog import AjouterFaculteDialog

class FaculteInterface(QMainWindow):
    faculte_selected = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Faculte Interface")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.table_Faculte = QTableWidget(self)
        self.layout.addWidget(self.table_Faculte)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.show_ajouter_faculte_dialog)
        self.layout.addWidget(self.btn_ajouter)

        self.central_widget.setLayout(self.layout)

        self.populate_Faculte()

    def populate_Faculte(self):
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    facno, facnom, adresse, libelle
                FROM Faculte
            """)
            faculte_data = cursor.fetchall()

            self.table_Faculte.setColumnCount(len(faculte_data[0]))
            self.table_Faculte.setHorizontalHeaderLabels([
                "Facno", "Facnom", "Adresse", "Libelle"
            ])

            self.table_Faculte.setRowCount(len(faculte_data))
            for row, faculte in enumerate(faculte_data):
                for col, value in enumerate(faculte):
                    item = QTableWidgetItem(str(value))
                    self.table_Faculte.setItem(row, col, item)

        connection.close()


    def show_ajouter_chercheur_dialog(self):
        dialog = AjouterFaculteDialog(self)
        if dialog.exec_():
            faculte_info = dialog.get_faculte_info()
            self.chercheur_selected.emit(faculte_info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaculteInterface()
    window.show()
    sys.exit(app.exec_())