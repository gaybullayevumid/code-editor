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

        menu_bar.setStyleSheet(
            """
                QMenuBar {
                    background-color: #181818;
                    color: #878787;
                    font-size: 14px;
                    
                    border: 1px solid #2D2D2D;
                    padding: 3px;
                }
                QMenuBar::item {
                    background-color: transparent;
                    color: #878787;
                    padding: 6px 18px;
                    margin: 1px;
                    border-radius: 5px;
                    border: none;
                }
                QMenuBar::item:selected {
                    background-color: #2D2E2E;
                    color: #FFFFFF;
                }
                QMenuBar::item:pressed {
                    background-color: #3D3E3E;
                }
                
                QMenu {
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                    font-size: 13px;
                    border-radius: 8px;
                    border: 1px solid #404040;
                    margin: 0px;
                    padding: 2px;
                }
                QMenu::item {
                    padding: 6px 28px;
                    margin: 1px;
                    border-radius: 4px;
                    border: none;
                    background-color: transparent;
                }
                QMenu::item:selected {
                    background-color: #0078D4;
                    color: #FFFFFF;
                }
                QMenu::item:pressed {
                    background-color: #106EBE;
                }
                QMenu::separator {
                    height: 1px;
                    background: #404040;
                    margin: 4px 8px;
                }
            """
        )

        file_menu = menu_bar.addMenu("File")
        new_file = QAction("New File", self)
        save = QAction("Save", self)
        open_file = QAction("Open File", self)
        open_folder = QAction("Open Folder", self)
        save = QAction("Save", self)
        save_as = QAction("Save As", self)
        exit = QAction("Exit", self)
        file_menu.addAction(new_file)
        file_menu.addAction(open_file)
        file_menu.addAction(open_folder)
        file_menu.addAction(save)
        file_menu.addAction(save_as)
        file_menu.addAction(exit)

        edit_menu = menu_bar.addMenu("Edit")
        undo = QAction("Undo", self)
        redo = QAction("Redo", self)
        edit_menu.addAction(undo)
        edit_menu.addAction(redo)

        view_menu = menu_bar.addMenu("View")
        full_screen_action = QAction("Fullscreen", self)
        view_menu.addAction(full_screen_action)

        terminal_menu = menu_bar.addMenu("Terminal")
        new_terminal = QAction("New Terminal", self)
        split_terminal = QAction("Split Terminal", self)
        terminal_menu.addAction(new_terminal)
        terminal_menu.addAction(split_terminal)

        help_menu = menu_bar.addMenu("Help")
        about = QAction("About", self)
        help_menu.addAction(about)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
