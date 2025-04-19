from PyQt6 import QtGui
from PyQt6 import QtCore

import core.global_var as globalvar

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
        
        # Log
        self.log = globalvar.get_val("LOGGER")

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
                    self.log.error(f"Error in highlightBlock: {e}")
                else:
                    pass