import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    )
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyIDLE")
        self.setGeometry(100, 100, 900, 600)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        new_action = QAction("New Text File", self)
        file_menu.addAction(new_action)

        view_menu = menu_bar.addMenu("View")
        full_screen_action = QAction("Fullscreen", self)
        view_menu.addAction(full_screen_action)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())