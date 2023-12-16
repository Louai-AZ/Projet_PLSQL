import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QStackedWidget
import psycopg2
from ChercheurInterface import ChercheurInterface  

class MainDashboard(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Dashboard")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label_overview = QLabel("Database Overview:")
        self.layout.addWidget(self.label_overview)

        # Stacked widget to manage different sections
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.display_overview()

        self.btn_chercheurs = QPushButton("Chercheurs Section")
        self.btn_chercheurs.clicked.connect(self.show_chercheurs_section)
        self.layout.addWidget(self.btn_chercheurs)

        self.btn_laboratoires = QPushButton("Laboratoires Section")
        self.btn_laboratoires.clicked.connect(self.show_laboratoires_section)
        self.layout.addWidget(self.btn_laboratoires)

        self.btn_facultes = QPushButton("Facultes Section")
        self.btn_facultes.clicked.connect(self.show_facultes_section)
        self.layout.addWidget(self.btn_facultes)

        self.btn_publications = QPushButton("Publications Section")
        self.btn_publications.clicked.connect(self.show_publications_section)
        self.layout.addWidget(self.btn_publications)

        self.central_widget.setLayout(self.layout)


    def display_overview(self):
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        with connection.cursor() as cursor:
            # Fetch faculties along with their laboratories and chercheur counts
            cursor.execute("""
                SELECT
                    f.facno,
                    f.facnom,
                    l.labno,
                    l.labnom,
                    COUNT(c.chno) AS num_chercheurs
                FROM
                    Faculte f
                    LEFT JOIN Laboratoire l ON f.facno = l.facno
                    LEFT JOIN Chercheur c ON l.labno = c.labno
                GROUP BY
                    f.facno, f.facnom, l.labno, l.labnom
                ORDER BY
                    f.facno, l.labno
            """)

            faculties_and_labs = cursor.fetchall()

            # Display the overview information
            overview_text = ""
            current_faculty = None

            for row in faculties_and_labs:
                facno, facnom, labno, labnom, num_chercheurs = row

                # Display faculty name only once
                if facno != current_faculty:
                    overview_text += f"\nFaculty {facno}: {facnom}\n"
                    current_faculty = facno

                # Display laboratory name and chercheur count
                overview_text += f"  - Laboratory {labno}: {labnom} : Number of Chercheurs: {num_chercheurs}\n"

            self.label_overview.setText(overview_text)

        connection.close()


    def show_chercheurs_section(self):
        chercheur_interface = ChercheurInterface()
        chercheur_interface.show()
        print("Chercheurs Section clicked")


    def show_laboratoires_section(self):
        # Implement logic to show the Laboratoires section
        print("Laboratoires Section clicked")


    def show_facultes_section(self):
        # Implement logic to show the Facultes section
        print("Facultes Section clicked")


    def show_publications_section(self):
        # Implement logic to show the Publications section
        print("Publications Section clicked")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainDashboard()
    window.show()
    sys.exit(app.exec_())
