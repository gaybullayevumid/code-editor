from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QFileSystemModel


class FileExplorer(QTreeView):
    def __init__(self):
        super().__init__()
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.setModel(self.model)
        self.setRootIndex(self.model.index("."))
