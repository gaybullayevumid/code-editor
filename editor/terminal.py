from PyQt6.QtWidgets import QPlainTextEdit
import subprocess


class Terminal(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Type commands here...")

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.stdout:
                self.appendPlainText(result.stdout)
            if result.stderr:
                self.appendPlainText(result.stderr)
        except Exception as e:
            self.appendPlainText(f"Error: {e}")
