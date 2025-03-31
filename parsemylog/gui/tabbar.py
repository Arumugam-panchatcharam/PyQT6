from PyQt6.QtWidgets import (
    QTabWidget, 
    QPlainTextEdit,
    QTableView,
    QMessageBox
)
from PyQt6 import QtGui
from PyQt6 import QtCore
from gui.layout_colorwidget import Color

class ParseMyLogTabBar(QTabWidget):
    def __init__(self):
        super().__init__()

        # Text Edit TAB
        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMovable(True)

        self.text_edit = QPlainTextEdit()
        self.text_edit.setStyleSheet('QPlainTextEdit {background-color: rgb(50,50,50); color: white;}')
        font = QtGui.QFont(["Courier New"],12)
        self.text_edit.setFont(font)

        highlight = ParseMyLogHighlighter(self)
        highlight.setDocument(self.text_edit.document())

        self.addTab(self.text_edit, "File &View")
        self.text_edit.setToolTip("Text View")

        # Table View TAB
        self.table_view = QTableView()
        self.addTab(self.table_view, "Log &Insight")
        self.table_view.setToolTip("Log Insight")

    def tabbar_clear(self):
        currentWidget=self.currentWidget()
        if currentWidget == self.text_edit :
            self.text_edit.clear()

    def tabbar_load(self, file_path):
        self.setStatusTip(file_path)
        currentWidget=self.currentWidget()
        if currentWidget == self.text_edit :
            #in_file = QtCore.QFile(file_path)
            #if in_file.open(QtCore.QFile.OpenModeFlag.ReadOnly | QtCore.QFile.OpenModeFlag.Text):
            #    stream = QtCore.QTextStream(in_file)
            #    self.text_edit.setPlainText(stream.readAll())
            try:
                with open(file_path, "r") as fp:
                    text = fp.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.text_edit.setPlainText(text)

class ParseMyLogHighlighter (QtGui.QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    # keywords
    log0 = [
        'err', 'error',
    ]
    log1 = [
        'warn', 'warning',
    ]
    log2 = [
        'notice', 'info'
    ]
    log3 = [
        'debug',
    ]

    def __init__(self, parent: QtGui.QTextDocument) -> None:
        super().__init__(parent)

            # Syntax styles that can be shared by all languages
        STYLES = {
            'log0': self.format('red'),
            'log1': self.format('yellow'),
            'log2': self.format('aqua'),
            'log3':self.format('mediumspringgreen'),
            'mac': self.format('magenta'),
            'numbers': self.format('dodgerblue'),
            'cmd': self.format('skyblue'),
            'comment': format('darkGreen'),
        }

        rules = []

        # MAC Address
        rules += [(r'(?:[0-9a-fA-F]:?){12}',STYLES['mac'])]

        # Logging
        rules += [(r'\b%s\b' % w, STYLES['log0'])
            for w in ParseMyLogHighlighter.log0]
        
        rules += [(r'\b%s\b' % w, STYLES['log1'])
            for w in ParseMyLogHighlighter.log1]
        
        rules += [(r'\b%s\b' % w, STYLES['log2'])
            for w in ParseMyLogHighlighter.log2]
        
        rules += [(r'\b%s\b' % w, STYLES['log3'])
            for w in ParseMyLogHighlighter.log3]
        
        # All other rules
        rules += [
            # command arguments
            (r'(?:--\w+)', STYLES['cmd']),
            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', STYLES['numbers']),

            # From '#' until a newline
            (r'#[^\n]*', STYLES['comment']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QtCore.QRegularExpression(pat,QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption), fmt)
            for (pat, fmt) in rules]

    def format(self, color, style=''):
        """Return a QTextCharFormat with the given attributes.
        """
        _color = QtGui.QColor()
        _color.setNamedColor(color)

        _format = QtGui.QTextCharFormat()
        _format.setForeground(_color)
        if 'bold' in style:
            _format.setFontWeight(QtGui.QFont.Weight.Bold)
        if 'italic' in style:
            _format.setFontItalic(True)

        return _format
    
    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, format in self.rules:
            i = expression.globalMatch(text)
            while i.hasNext():
                match = i.next()
                try:
                    self.setFormat(match.capturedStart(), match.capturedLength(), format)
                except Exception as e:
                    pass
                else:
                    pass