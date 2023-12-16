from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit
from PyQt5.QtCore import Qt, QDate
import psycopg2

class AjouterChercheurDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ajouter Chercheur")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        # Add input fields for chercheur information
        self.chno_edit = QLineEdit(self)
        self.layout.addRow("Chno:", self.chno_edit)

        self.chnom_edit = QLineEdit(self)
        self.layout.addRow("Chnom:", self.chnom_edit)

        self.grade_combo = QComboBox(self)
        self.grade_combo.addItems(['E', 'D', 'A', 'MA', 'MC', 'PR'])
        self.layout.addRow("Grade:", self.grade_combo)

        self.statut_combo = QComboBox(self)
        self.statut_combo.addItems(['P', 'C'])
        self.layout.addRow("Statut:", self.statut_combo)

        self.daterecrut_edit = QDateEdit(self)
        self.daterecrut_edit.setDate(QDate.currentDate())
        self.layout.addRow("Date de recrutement:", self.daterecrut_edit)

        self.salaire_edit = QLineEdit(self)
        self.layout.addRow("Salaire:", self.salaire_edit)

        self.prime_edit = QLineEdit(self)
        self.layout.addRow("Prime:", self.prime_edit)

        self.email_edit = QLineEdit(self)
        self.layout.addRow("Email:", self.email_edit)

        # Add combo boxes for faculties, laboratories, and supervisors
        self.faculty_combo = QComboBox(self)
        self.populate_faculty_combo()
        self.layout.addRow("Faculté:", self.faculty_combo)
        self.faculty_combo.currentTextChanged.connect(self.on_faculty_combo_change)

        self.lab_combo = QComboBox(self)
        self.populate_lab_combo()
        self.layout.addRow("Laboratoire:", self.lab_combo)

        self.supervisor_combo = QComboBox(self)
        self.populate_supervisor_combo()
        self.layout.addRow("Superviseur:", self.supervisor_combo)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.ajouter_chercheur)
        self.layout.addRow(self.btn_ajouter)

        self.setLayout(self.layout)

    def populate_faculty_combo(self):
        # Fetch faculty names from the database and populate the combo box
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

    def populate_lab_combo(self):
        # Fetch laboratory names based on the selected faculty and populate the combo box
        selected_faculty = self.faculty_combo.currentText()

        if not selected_faculty:
            return
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT labnom FROM Laboratoire WHERE facno = (SELECT facno FROM Faculte WHERE facnom = %s)", (selected_faculty,))
                labs = cursor.fetchall()
                self.lab_combo.clear()
                self.lab_combo.addItems([lab[0] for lab in labs])

        finally:
            connection.close()

    def populate_supervisor_combo(self):
        # Fetch names of supervisors (A, MA, PR, MC) working in the selected lab and faculty
        selected_faculty = self.faculty_combo.currentText()
        selected_lab = self.lab_combo.currentText()

        if not selected_faculty or not selected_lab:
            return

        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT chnom FROM Chercheur WHERE grade IN ('A', 'MA', 'PR', 'MC') AND labno = (SELECT labno FROM Laboratoire WHERE labnom = %s AND facno = (SELECT facno FROM Faculte WHERE facnom = %s))", (selected_lab, selected_faculty))
                supervisors = cursor.fetchall()
                self.supervisor_combo.clear()
                self.supervisor_combo.addItems([sup[0] for sup in supervisors])

        finally:
            connection.close()

    def on_faculty_combo_change(self):
        # Update lab combo and supervisor combo when the faculty combo changes
        self.populate_lab_combo()
        self.populate_supervisor_combo()

    def ajouter_chercheur(self):
        try:
            chercheur_info = {
                "chno": int(self.chno_edit.text()),
                "chnom": self.chnom_edit.text(),
                "grade": self.grade_combo.currentText(),
                "statut": self.statut_combo.currentText(),
                "daterecrut": self.daterecrut_edit.date().toString(Qt.ISODate),
                "salaire": float(self.salaire_edit.text()),
                "prime": float(self.prime_edit.text()),
                "email": self.email_edit.text(),
                "supno": self.supervisor_combo(),
                "labno": self.lab_combo.text(),
                "facno": self.faculty_combo.text()
                # Add other parameters as needed
            }

            # Fetch facno, labno, and supno based on selected names
            chercheur_info["facno"] = self.get_facno_from_name(chercheur_info["facno"])
            chercheur_info["labno"] = self.get_labno_from_name(chercheur_info["labno"])
            chercheur_info["supno"] = self.get_supervisor_chno_from_name(chercheur_info["supno"])

            # Call the stored procedure to add chercheur to the database
            self.add_chercheur_to_database(chercheur_info)

            # Close the dialog
            self.accept()

        except Exception as e:
            # Display an error message in a small interface
            self.show_error_message(str(e))




    def get_facno_from_name(self, fac_name):
        # Fetch facno based on the selected faculty name from the database
        # Replace the connection details with your actual database connection
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT facno FROM Faculte WHERE facnom = %s", (fac_name,))
                facno = cursor.fetchone()
                return facno[0] if facno else None

        finally:
            connection.close()

    def get_labno_from_name(self, lab_name, fac_name):
        # Fetch labno based on the selected laboratory name and faculty from the database
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT labno FROM Laboratoire WHERE labnom = %s AND facno = (SELECT facno FROM Faculte WHERE facnom = %s)",
                    (lab_name, fac_name)
                )
                labno = cursor.fetchone()
                return labno[0] if labno else None

        finally:
            connection.close()


    def get_supervisor_chno_from_name(self, sup_name, fac_name, lab_name):
        # Fetch chno of the selected supervisor from the database
        # Replace the connection details with your actual database connection
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT chno FROM Chercheur WHERE chnom = %s AND facno = (SELECT facno FROM Faculte WHERE facnom = %s) AND labno = (SELECT labno FROM Laboratoire WHERE labnom = %s AND facno = (SELECT facno FROM Faculte WHERE facnom = %s))",
                            (sup_name, fac_name, lab_name, fac_name))
                supervisor_chno = cursor.fetchone()
                return supervisor_chno[0] if supervisor_chno else None

        finally:
            connection.close()


    # def get_supervisor_chno(self):
    #     # Fetch chno of the selected supervisor from the database
    #     connection = psycopg2.connect(
    #         host="localhost",
    #         database="biblio",
    #         user="postgres",
    #         password="HOLUX"
    #     )

    #     try:
    #         with connection.cursor() as cursor:
    #             selected_supervisor = self.supervisor_combo.currentText()
    #             cursor.execute("SELECT chno FROM Chercheur WHERE chnom = %s", (selected_supervisor,))
    #             supervisor_chno = cursor.fetchone()
    #             return supervisor_chno[0] if supervisor_chno else None

    #     finally:
    #         connection

    def show_error_message(self, message):
            QMessageBox.critical(self, "Error", message, QMessageBox.Ok)
