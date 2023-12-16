import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem, QGroupBox ,
    QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit
)
from PyQt5.QtCore import pyqtSignal,Qt, QDate
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
        connection = psycopg2.connect(
            host="localhost",
            database="biblio",
            user="postgres",
            password="HOLUX"
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT facno, facnom FROM Faculte")
                faculties = cursor.fetchall()
                self.faculty_combo.addItems([f"{fac[1]} (FacNo: {fac[0]})" for fac in faculties])

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
                facno = selected_faculty.split("(FacNo: ")[1].split(")")[0]
                cursor.execute("SELECT labno, labnom FROM Laboratoire WHERE facno = %s", (facno,))
                labs = cursor.fetchall()
                self.lab_combo.clear()
                self.lab_combo.addItems([f"{lab[1]} (LabNo: {lab[0]})" for lab in labs])

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
                facno = selected_faculty.split("(FacNo: ")[1].split(")")[0]
                labno = selected_lab.split("(LabNo: ")[1].split(")")[0]
                cursor.execute("SELECT chno, chnom FROM Chercheur WHERE grade IN ('A', 'MA', 'PR', 'MC') AND labno = %s AND facno = %s",
                            (labno, facno))
                supervisors = cursor.fetchall()
                self.supervisor_combo.clear()
                self.supervisor_combo.addItems([f"{sup[1]} (ChNo: {sup[0]})" for sup in supervisors])

        finally:
            connection.close()


    def on_faculty_combo_change(self):
        # Update lab combo and supervisor combo when the faculty combo changes
        self.populate_lab_combo()
        self.populate_supervisor_combo()


    # def ajouter_chercheur(self):
    #     try:
    #         chercheur_info = {
    #             "chno": int(self.chno_edit.text()),
    #             "chnom": self.chnom_edit.text(),
    #             "grade": self.grade_combo.currentText(),
    #             "statut": self.statut_combo.currentText(),
    #             "daterecrut": self.daterecrut_edit.date().toString(Qt.ISODate),
    #             "salaire": float(self.salaire_edit.text()),
    #             "prime": float(self.prime_edit.text()),
    #             "email": self.email_edit.text(),
    #             "supno": int(self.supervisor_combo.currentText().split("(ChNo: ")[1].split(")")[0]),
    #             "labno": int(self.lab_combo.currentText().split("(LabNo: ")[1].split(")")[0]),
    #             "facno": int(self.faculty_combo.currentText().split("(FacNo: ")[1].split(")")[0])
    #         }

    #         self.ajouter_chercheur(chercheur_info)

    #         # Close the dialog
    #         self.accept()

    #     except Exception as e:
    #         # Display an error message in a small interface
    #         self.show_error_message(str(e))


    def ajouter_chercheur(self):
        try:
            # Retrieve attribute values from the fields
            chno = int(self.chno_edit.text())
            chnom = self.chnom_edit.text()
            grade = self.grade_combo.currentText()
            statut = self.statut_combo.currentText()
            daterecrut = self.daterecrut_edit.date().toString(Qt.ISODate)
            salaire = float(self.salaire_edit.text())
            prime = float(self.prime_edit.text())
            email = self.email_edit.text()
            supno = int(self.supervisor_combo.currentText().split("(ChNo: ")[1].split(")")[0])
            labno = int(self.lab_combo.currentText().split("(LabNo: ")[1].split(")")[0])
            facno = int(self.faculty_combo.currentText().split("(FacNo: ")[1].split(")")[0])

            # Call the stored procedure to add chercheur to the database
            self.ajouter_chercheur_procedure(chno, chnom, grade, statut, daterecrut, salaire, prime, email, supno, labno, facno)

            # Close the dialog
            self.accept()

        except Exception as e:
            # Display an error message in a small interface
            self.show_error_message(str(e))


    def ajouter_chercheur_procedure(self, chno, chnom, grade, statut, daterecrut, salaire, prime, email, supno, labno, facno):
        try:
            # Establish a connection to the PostgreSQL database
            connection = psycopg2.connect(
                host="localhost",
                database="biblio",
                user="postgres",
                password="HOLUX"
            )

            # Create a cursor to execute SQL commands
            with connection.cursor() as cursor:
                # Call the stored procedure with the required parameters
                cursor.callproc('ajouter_chercheur', (
                    chno, chnom, grade, statut, daterecrut,
                    salaire, prime, email, supno, labno, facno
                ))

            # Commit the transaction
            connection.commit()

        except psycopg2.Error as e:
            # Handle any exceptions that might occur during the database operation
            print(f"Error: {e}")

        finally:
            # Close the database connection
            connection.close()



    def show_error_message(self, message):
            QMessageBox.critical(self, "Error", message, QMessageBox.Ok)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = AjouterChercheurDialog()
#     window.show()
#     sys.exit(app.exec_())