from PyQt6.QtWidgets import (
    QMainWindow, QFileDialog, QToolBar, QMessageBox, QTextEdit, QDockWidget
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSize, Qt
from editor.code_editor import CodeEditor
import subprocess
import tempfile
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_file = None
        self.editor = CodeEditor()
        self.setCentralWidget(self.editor)

        # Output oynasi
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        dock = QDockWidget("Output", self)
        dock.setWidget(self.output_console)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(toolbar)

        # Open
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        # Save
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        # Run
        run_action = QAction("Run", self)
        run_action.triggered.connect(self.run_code)
        toolbar.addAction(run_action)

        self.setWindowTitle("Python Code Editor")
        self.resize(1000, 700)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Python Files (*.py);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.editor.setText(content)
                self.current_file = file_path
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\n{str(e)}")

    def save_file(self):
        if not self.current_file:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", "Python Files (*.py);;All Files (*)"
            )
            if not file_path:
                return
            self.current_file = file_path

        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.editor.text())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")

    def run_code(self):
        """ Editor ichidagi kodni ishga tushirish """
        try:
            # Faylni vaqtinchalik saqlash
            if not self.current_file:
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
                tmp_file.write(self.editor.text().encode("utf-8"))
                tmp_file.close()
                file_to_run = tmp_file.name
            else:
                self.save_file()
                file_to_run = self.current_file

            # Kodni subprocess orqali ishga tushirish
            result = subprocess.run(
                ["python", file_to_run],
                capture_output=True,
                text=True
            )

            # Natijani chiqarish
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += "\nErrors:\n" + result.stderr

            self.output_console.setPlainText(output)

            # Agar temporary file bo‘lsa – o‘chirib tashlash
            if not self.current_file:
                os.remove(file_to_run)

        except Exception as e:
            QMessageBox.critical(self, "Run Error", str(e))
