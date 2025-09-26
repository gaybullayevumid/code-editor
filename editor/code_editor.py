from PyQt6.Qsci import QsciScintilla, QsciLexerPython
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication
import sys


class CodeEditor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 🔹 Yagona font editor va lexer uchun
        font_size = 16
        editor_font = QFont("Consolas", font_size)
        
        # 🔹 Fon rangini aniqlash (Dark theme)
        background_color = QColor("#222222") # To'q kulrang/qora fon
        text_color = QColor("#EEEEEE")    # Oq/och kulrang matn

        # 🔹 Lexer yaratish
        lexer = QsciLexerPython()

        # 💡 MUHIM Lexer sozlamalari: Font va Fonni Default tokeniga o'rnatish
        lexer.setDefaultFont(editor_font)
        lexer.setDefaultColor(text_color)
        lexer.setDefaultPaper(background_color)
        
        # Barcha tokenlar ro'yxati
        token_types = [
            QsciLexerPython.Default, QsciLexerPython.Comment, QsciLexerPython.Number,
            QsciLexerPython.SingleQuotedString, QsciLexerPython.DoubleQuotedString,
            QsciLexerPython.Keyword, QsciLexerPython.Operator, QsciLexerPython.ClassName,
            QsciLexerPython.FunctionMethodName, QsciLexerPython.Decorator,
            QsciLexerPython.UnclosedString # 💡 Yopiq bo'lmagan stringlar uchun ham aniq sozlama
        ]
        
        # Har bir token uchun font va fonni qayta o'rnatish (shrift doimiyligi uchun)
        for token in token_types:
            lexer.setFont(editor_font, token)
            lexer.setPaper(background_color, token)
        
        # 🔹 Syntax ranglarini sozlash 
        lexer.setColor(text_color, QsciLexerPython.Default)
        lexer.setColor(QColor("#808080"), QsciLexerPython.Comment)
        lexer.setColor(QColor("#FFCC66"), QsciLexerPython.Number)
        lexer.setColor(QColor("#FF6666"), QsciLexerPython.SingleQuotedString)
        lexer.setColor(QColor("#FF6666"), QsciLexerPython.DoubleQuotedString)
        lexer.setColor(QColor("#5B9DFD"), QsciLexerPython.Keyword)
        lexer.setColor(text_color, QsciLexerPython.Operator)
        lexer.setColor(QColor("#00BFFF"), QsciLexerPython.ClassName)
        lexer.setColor(QColor("#70C0A0"), QsciLexerPython.FunctionMethodName)
        lexer.setColor(QColor("#FF99FF"), QsciLexerPython.Decorator)
        
        # 💡 Yopiq bo'lmagan string rangini ham o'rnatish (yozish jarayoni uchun muhim)
        lexer.setColor(QColor("#FF6666"), QsciLexerPython.UnclosedString)


        # 🔹 Lexer-ni editorga o'rnatish
        self.setLexer(lexer)

        # 🔹 Editorning umumiy fontini va fonini o'rnatish (qo'shimcha ehtiyot chorasi)
        self.setFont(editor_font)
        self.setPaper(background_color) 

        # 🔹 Margin sozlamalari
        self.setMarginsFont(editor_font)
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "00000") 
        self.setMarginsForegroundColor(QColor("#888888"))
        self.setMarginsBackgroundColor(QColor("#333333"))

        # 🔹 Qavs matching sozlamalari (rasmga ko'ra)
        self.setBraceMatching(QsciScintilla.BraceMatch.StrictBraceMatch)
        self.setMatchedBraceBackgroundColor(QColor("#3A3A55")) # To'q binafsha fon
        self.setMatchedBraceForegroundColor(QColor("#FFFFFF")) # Oq matn

        # 🔹 Joriy qator (Caret Line) sozlamalari
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor(60, 60, 70)) 
        self.setCaretForegroundColor(QColor("#FFFFFF"))

        # 🔹 Qolgan sozlamalar
        self.setAutoIndent(True)
        self.setTabWidth(4)
        self.setColor(text_color)
        self.setSelectionBackgroundColor(QColor(100, 100, 150))
        self.setSelectionForegroundColor(QColor("#FFFFFF"))


# ----------------------------------------------------------------------
# Dasturni ishga tushirish uchun QMainWindow sinfi
# ----------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        # ... (oldingi kod o'zgarishsiz qoladi) ...
        super().__init__()
        self.setWindowTitle("PyQt6 QsciScintilla Code Editor (Fixed Font Consistency)")
        self.setGeometry(100, 100, 800, 600)

        editor = CodeEditor()
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(editor)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())