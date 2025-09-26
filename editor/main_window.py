from PyQt6.QtWidgets import (
    QMainWindow, QDockWidget, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from editor.file_explorer import FileExplorer
from editor.code_editor import CodeEditor
from editor.terminal import Terminal
from editor.git_manager import GitManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast Python Editor")
        self.setGeometry(100, 100, 1200, 700)

        # Kod muharriri
        self.editor = CodeEditor()
        self.setCentralWidget(self.editor)

        # Fayl menejer (chapda)
        dock_files = QDockWidget("Files", self)
        self.file_explorer = FileExplorer()
        dock_files.setWidget(self.file_explorer)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_files)

        # Terminal (pastda)
        dock_terminal = QDockWidget("Terminal", self)
        self.terminal = Terminal()
        dock_terminal.setWidget(self.terminal)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock_terminal)

        # Git panel (pastda)
        dock_git = QDockWidget("Git", self)
        self.git_manager = GitManager()
        dock_git.setWidget(self.git_manager)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock_git)

        # Menyu
        self._create_menu()

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Python Files (*.py)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            QMessageBox.information(self, "Saved", f"File saved: {path}")
