from PyQt6.QtWidgets import (
    QTabWidget, 
    QPlainTextEdit,
    QTableView,
    QMessageBox
)
from PyQt6 import QtGui

from gui.tableview import ParseMyLogTableView
from gui.highlighter import ParseMyLogHighlighter
import core.global_var as globalvar

class ParseMyLogTabBar(QTabWidget):
    def __init__(self):
        super().__init__()

        # log
        self.log = globalvar.get_val("LOGGER")

        # Text Edit TAB
        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMovable(True)

        self.text_edit = QPlainTextEdit()
        self.text_edit.setStyleSheet('QPlainTextEdit {background-color: rgb(50,50,50); color: white;}')
        _font = QtGui.QFont(["Courier New"],14)
        self.text_edit.setFont(_font)

        _highlight = ParseMyLogHighlighter(self.text_edit)
        _highlight.setDocument(self.text_edit.document())

        self.addTab(self.text_edit, "File &View")
        self.text_edit.setToolTip("Text View")

        # Table View TAB
        self.table_view = ParseMyLogTableView()
        self.addTab(self.table_view, "Log &Insight")
        self.table_view.setToolTip("Log Insight")

    def tabbar_clear(self):
        _currentWidget=self.currentWidget()
        if _currentWidget == self.text_edit :
            self.text_edit.clear()

    def tabbar_load(self, file_path):
        self.setStatusTip(file_path)
        _currentWidget=self.currentWidget()
        if _currentWidget == self.text_edit :
            #in_file = QtCore.QFile(file_path)
            #if in_file.open(QtCore.QFile.OpenModeFlag.ReadOnly | QtCore.QFile.OpenModeFlag.Text):
            #    stream = QtCore.QTextStream(in_file)
            #    self.text_edit.setPlainText(stream.readAll())
            try:
                with open(file_path, "r") as fp:
                    _text = fp.read()
            except Exception as e:
                self.dialog_critical(str(e))
                self.log.error(f"Error opening file: {file_path}")
            else:
                self.text_edit.setPlainText(_text)
        elif _currentWidget == self.table_view:
            self.table_view._update_table(file_path)