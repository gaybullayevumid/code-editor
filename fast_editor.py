# filename: fast_editor.py
import sys, os, platform, tempfile
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPlainTextEdit, QTextEdit,
    QFileSystemModel, QTreeView, QSplitter, QWidget,
    QVBoxLayout, QToolBar, QAction, QFileDialog, QMessageBox,
    QListWidget
)
from PyQt5.QtCore import Qt, QProcess, QDir, QPoint
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QTextCursor
import jedi
import re

# ---------- Simple Python syntax highlighter ----------
class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rules = []
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#C586C0"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [
            "False","class","finally","is","return","None","continue","for","lambda","try",
            "True","def","from","nonlocal","while","and","del","global","not","with",
            "as","elif","if","or","yield","assert","else","import","pass","break","except","in","raise"
        ]
        for kw in keywords:
            pattern = r"\b" + kw + r"\b"
            self._rules.append((re.compile(pattern), keyword_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        self._rules.append((re.compile(r"(['\"]).*?\1"), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        self._rules.append((re.compile(r"#.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self._rules:
            for m in pattern.finditer(text):
                start, end = m.span()
                self.setFormat(start, end - start, fmt)

# ---------- Main Window ----------
class EditorMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast Python Editor")
        self.resize(1100, 700)

        # Splitter: left tree, right editor+output
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Project explorer (left)
        self.model = QFileSystemModel()
        home = QDir.currentPath()
        self.model.setRootPath(home)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(home))
        self.tree.clicked.connect(self.on_tree_clicked)
        self.tree.setColumnWidth(0, 250)
        splitter.addWidget(self.tree)

        # Right side: editor and output stacked vertically
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        # Editor
        self.editor = QPlainTextEdit()
        font = QFont("Consolas", 12)
        self.editor.setFont(font)
        right_layout.addWidget(self.editor)

        # Highlighter
        self.highlighter = PythonHighlighter(self.editor.document())

        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumHeight(180)
        right_layout.addWidget(self.output)

        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 3)

        self.setCentralWidget(splitter)

        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        open_act = QAction("Open", self)
        open_act.triggered.connect(self.open_file)
        toolbar.addAction(open_act)

        save_act = QAction("Save", self)
        save_act.triggered.connect(self.save_file)
        toolbar.addAction(save_act)

        run_act = QAction("Run (internal)", self)
        run_act.triggered.connect(self.run_internal)
        toolbar.addAction(run_act)

        run_term_act = QAction("Run in Terminal", self)
        run_term_act.triggered.connect(self.run_in_terminal)
        toolbar.addAction(run_term_act)

        # Process for running code and capturing output
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.on_stdout)
        self.process.readyReadStandardError.connect(self.on_stderr)
        self.process.finished.connect(self.on_finished)

        # Autocomplete popup
        self.comp_popup = QListWidget()
        self.comp_popup.setWindowFlags(Qt.WindowType.ToolTip)
        self.comp_popup.itemClicked.connect(self.on_completion_clicked)
        self.editor.textChanged.connect(self.on_text_changed)
        self.editor.keyPressEvent = self.editor_keypress_override(self.editor.keyPressEvent)

    # ---------- File actions ----------
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Python Files (*.py);;All Files (*)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
            self.current_file = path
            self.statusBar().showMessage(f"Opened: {path}")

    def save_file(self):
        if getattr(self, "current_file", None):
            path = self.current_file
        else:
            path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Python Files (*.py);;All Files (*)")
            if not path:
                return
            self.current_file = path
        with open(self.current_file, "w", encoding="utf-8") as f:
            f.write(self.editor.toPlainText())
        self.statusBar().showMessage(f"Saved: {self.current_file}")

    def on_tree_clicked(self, idx):
        path = self.model.filePath(idx)
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
            self.current_file = path
            self.statusBar().showMessage(f"Opened: {path}")

    # ---------- Running code (internal) ----------
    def run_internal(self):
        code = self.editor.toPlainText()
        # write to temp file
        fd, path = tempfile.mkstemp(suffix=".py")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        self.output.clear()
        # start process
        self.process.start(sys.executable, [path])

    def on_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output.moveCursor(QTextCursor.End)
        self.output.insertPlainText(data)

    def on_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output.moveCursor(QTextCursor.End)
        self.output.insertPlainText(data)

    def on_finished(self):
        self.output.append("\n[Process finished]\n")

    # ---------- Run in external terminal (for input support) ----------
    def run_in_terminal(self):
        # save current to temp file
        code = self.editor.toPlainText()
        fd, path = tempfile.mkstemp(suffix=".py")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        sys_pl = platform.system().lower()
        if sys_pl.startswith("windows"):
            # start cmd and run
            os.system(f'start cmd /k "{sys.executable} {path}"')
        elif sys_pl == "darwin":
            # macOS: use Terminal.app open with osascript
            os.system(f'osascript -e \'tell application "Terminal" to do script "{sys.executable} {path}"\'')
        else:
            # Linux: try gnome-terminal, xterm fallback
            if os.system("which gnome-terminal >/dev/null 2>&1") == 0:
                os.system(f'gnome-terminal -- {sys.executable} {path} &')
            else:
                os.system(f'xterm -e {sys.executable} {path} &')

    # ---------- Autocomplete using jedi ----------
    def editor_keypress_override(self, original_keypress):
        def new_keypress(event):
            original_keypress(event)
            # show completions when dot or ctrl+space
            if event.text() == ".":
                self.show_completions()
            elif event.key() == Qt.Key.Key_Space and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self.show_completions()
        return new_keypress

    def on_text_changed(self):
        # hide popup if user types more
        if self.comp_popup.isVisible():
            # simple heuristic: hide when text changes
            self.comp_popup.hide()

    def show_completions(self):
        cursor = self.editor.textCursor()
        pos = cursor.position()
        text = self.editor.toPlainText()
        try:
            script = jedi.Script(code=text, path='')
            completions = script.complete(*self._cursor_to_line_col(text, pos))
            items = [c.name for c in completions]
        except Exception as e:
            items = []
        if not items:
            return
        self.comp_popup.clear()
        for it in items:
            self.comp_popup.addItem(it)
        # position popup near cursor
        rect = self.editor.cursorRect()
        global_pos = self.editor.mapToGlobal(rect.bottomRight())
        self.comp_popup.move(global_pos + QPoint(0, 5))
        self.comp_popup.setFixedWidth(200)
        self.comp_popup.show()

    def _cursor_to_line_col(self, text, pos):
        # convert absolute pos to (line, column) 1-based for jedi
        before = text[:pos]
        line = before.count("\n") + 1
        if "\n" in before:
            col = len(before.split("\n")[-1])
        else:
            col = len(before)
        return line, col

    def on_completion_clicked(self, item):
        # insert completion at cursor
        cur = self.editor.textCursor()
        cur.insertText(item.text())
        self.comp_popup.hide()

# ---------- Run application ----------
def main():
    app = QApplication(sys.argv)
    w = EditorMain()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
