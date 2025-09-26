from PyQt6.Qsci import QsciScintilla, QsciLexerPython
from PyQt6.QtGui import QColor, QFont


class CodeEditor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 🔹 Font sozlamalari
        font = QFont("Consolas", 16)
        self.setFont(font)
        self.setMarginsFont(font)

        # 🔹 Margin (line number) sozlamalari
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "00000")
        self.setMarginsForegroundColor(QColor("#555555"))  # quyuq kulrang
        self.setMarginsBackgroundColor(QColor("#f5f5f5"))  # yumshoq kulrang

        # 🔹 Qavs matching rejimi
        self.setBraceMatching(QsciScintilla.BraceMatch.StrictBraceMatch)
        self.setMatchedBraceBackgroundColor(QColor("#cce8ff"))  # qavs moslashganida fon rangi
        self.setMatchedBraceForegroundColor(QColor("#000000"))  # qavs rangi

        # 🔹 Avtomatik indentation
        self.setAutoIndent(True)

        # 🔹 Tab uzunligi (4 ta bo‘sh joy)
        self.setTabWidth(4)

        # 🔹 Python uchun syntax highlight
        lexer = QsciLexerPython()
        lexer.setDefaultFont(font)

        # 🔹 Syntax ranglarini sozlash
        lexer.setColor(QColor("#000000"), QsciLexerPython.Default)            # default text
        lexer.setColor(QColor("#007f00"), QsciLexerPython.Comment)            # izohlar yashil
        lexer.setColor(QColor("#FFFF00"), QsciLexerPython.Number)             # sonlar ko‘k
        lexer.setColor(QColor("#ffffff"), QsciLexerPython.SingleQuotedString) # single-quoted string
        lexer.setColor(QColor("#ffffff"), QsciLexerPython.DoubleQuotedString) # double-quoted string
        lexer.setColor(QColor("#FFFF00"), QsciLexerPython.Keyword)            # kalit so‘zlar qizil
        lexer.setColor(QColor("#FFFF00"), QsciLexerPython.Operator)           # operatorlar ko‘k
        lexer.setColor(QColor("#FFFF00"), QsciLexerPython.ClassName)          # class nomi qizil
        lexer.setColor(QColor("#646457"), QsciLexerPython.FunctionMethodName) # funksiya nomi qizil
        lexer.setColor(QColor("#7f7f00"), QsciLexerPython.Decorator)          # decorator sariq

        self.setLexer(lexer)

        # 🔹 Cursor highlight
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor(200, 230, 255, 60))  # yumshoq ko‘k

        # 🔹 Text rangi (default qora)
        self.setColor(QColor("#000000"))
