from __future__ import annotations
from PySide6 import QtGui
from qt_material_icons import MaterialIcon

from PySide6.QtCore import Qt, QSignalBlocker, Slot
from PySide6.QtGui import QGuiApplication, QClipboard, QFont, QFontDatabase
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFontComboBox,
                               QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                               QPushButton, QScrollArea,
                               QVBoxLayout, QWidget)

import sys

from PySide6.QtWidgets import QApplication

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create a QIcon object
        icon = MaterialIcon('search')

        # Set a color
        color = QtGui.QColor('red')
        icon.set_color(color)

        # Set a color for a state, for example when a button is checked
        icon.set_color(color, state=QtGui.QIcon.State.On)

        # Set a different icon for a state, for example when a button is checked
        toggle_icon = MaterialIcon('toggle_off')
        toggle_icon_on = MaterialIcon('toggle_on')
        toggle_icon.set_icon(toggle_icon_on, state=QtGui.QIcon.State.On)
        layout = QVBoxLayout()
        button = QCheckBox()
        button.setIcon(icon)
        widget = QWidget()
        layout.addWidget(button, stretch=4)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        

"""PySide6 port of the widgets/widgets/ charactermap example from Qt6"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())