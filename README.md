# code-editor


```markdown
python_editor/
│── main.py                # Asosiy dastur
│── editor/
│   │── __init__.py
│   │── window.py           # Asosiy oyna (menu, toolbar, layout)
│   │── editor_widget.py    # Kod yoziladigan joy (QScintilla yoki QTextEdit)
│   │── file_explorer.py    # Chap tarafdagi fayl struktura oynasi
│   │── terminal.py         # Ichki terminal
│   │── settings.py         # Sozlamalar (theme, key bindings)
│── core/
│   │── __init__.py
│   │── syntax.py           # Pygments bilan ranglash
│   │── autocomplete.py     # Jedi bilan auto-complete
│   │── runner.py           # Kodni run qilish
│   │── linter.py           # Kodni tekshirish (flake8, pylint)
│── themes/
│   │── dark.qss            # Dark mode style
│   │── light.qss           # Light mode style
│── assets/
│   │── icons/              # Iconlar
│   │── fonts/              # Maxsus shriftlar
│── requirements.txt        # Kutubxonalar ro‘yxati
│── README.md
```