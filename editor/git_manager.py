from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
import subprocess


class GitManager(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        self.btn_status = QPushButton("Git Status")
        self.btn_status.clicked.connect(self.git_status)

        self.btn_commit = QPushButton("Auto Commit")
        self.btn_commit.clicked.connect(self.git_commit)

        layout.addWidget(self.btn_status)
        layout.addWidget(self.btn_commit)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def git_status(self):
        result = subprocess.run("git status", shell=True, capture_output=True, text=True)
        self.log.append(result.stdout)

    def git_commit(self):
        subprocess.run("git add .", shell=True)
        subprocess.run('git commit -m "Auto commit"', shell=True)
        self.log.append("✅ Auto commit done")
