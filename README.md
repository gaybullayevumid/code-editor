# code-editor


```markdown
code-editor/
│── fast_editor.py          # Asosiy dastur (entry point)
│── requirements.txt        # Kutubxonalar ro‘yxati
│
├── editor/                 # Editor bilan bog‘liq modullar
│   │── __init__.py
│   │── main_window.py      # Asosiy oyna (QMainWindow)
│   │── text_editor.py      # Matn muharriri (QPlainTextEdit)
│   │── file_explorer.py    # Fayl ko‘rish qismi (QFileSystemModel, QTreeView)
│   │── syntax_highlighter.py # Pygments yordamida rang berish
│   │── autocomplete.py     # Jedi yordamida autocomplete
│   │── linter.py           # Pylint/flake8 integratsiyasi
│   │── debugger.py         # Debugger (debugpy)
│   │── git_integration.py  # Git bilan ishlash
│   │── terminal.py         # Terminal integratsiyasi
│   │── settings.py         # Config sozlamalar (tema, shrift va h.k.)
│
├── themes/                 # Mavzular (dark, light va boshqalar)
│   │── dark.json
│   │── light.json
│
├── assets/                 # Ikonkalar, qo‘shimcha fayllar
│   │── icons/
│       │── open.png
│       │── save.png
│       │── run.png
```