# editor.py
from PyQt6.QtWidgets import QApplication, QPlainTextEdit
from PyQt6 import QtGui
from syntax import PythonHighlighter

app = QApplication([])
editor = QPlainTextEdit()
highlighter1 = PythonHighlighter(editor.document())
editor.show()

# Load syntax.py into the editor for demo purposes
infile = open('syntax.py', 'r')
editor.setPlainText(infile.read())

app.exec()