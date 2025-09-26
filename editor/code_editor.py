from PyQt6.Qsci import QsciScintilla, QsciLexerPython
from PyQt6.QtGui import QColor


class CodeEditor(QsciScintilla):
    def __init__(self):
        super().__init__()

        # Sintaksis ranglash (Python lexer)
        lexer = QsciLexerPython(self)
        self.setLexer(lexer)

        # Line raqamlar (chap margin)
        self.setMarginsForegroundColor(QColor("gray"))        # raqam rangi
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)  # raqam margin
        self.setMarginWidth(0, "0000")                # 4 xonali joy
        self.setMarginsBackgroundColor(QColor("lightgray"))   # fon rangi

        # Auto indent
        self.setAutoIndent(True)

        # Tab kengligi (4 probel)
        self.setTabWidth(4)

        # Matnni o‘rashni o‘chirish
        self.setWrapMode(QsciScintilla.WrapMode.WrapNone)

        # Qavslarni yoritish
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)

        # Current line highlight
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("lightyellow"))
