from PyQt5.QtWidgets import QApplication
from MainDashboard import MainDashboard

def main():
    app = QApplication([])
    main_dashboard = MainDashboard()
    main_dashboard.show()
    app.exec_()

if __name__ == "__main__":
    main()