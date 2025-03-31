import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QComboBox,
    QGridLayout
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar", self)
        toolbar.setIconSize(QSize(16, 16))
        
        toolbar1 = QToolBar("My main toolbar", self)
        toolbar1.setIconSize(QSize(16, 16))

        self.button_action = QAction(QIcon("bug.png"), "&Your button", self)
        self.button_action.setStatusTip("This is your button")
        self.button_action.triggered.connect(self.onMyToolBarButtonClick)
        self.button_action.setCheckable(True)
        toolbar.addAction(self.button_action)

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        combobox = QComboBox(self)
        combobox.addItem("Option 1")
        combobox.addItem("Option 2")
        combobox.addItem("Option 3")
        combobox.move(50, 50)
        toolbar1.addWidget(combobox)
        
        toolbar1.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.add_menu_theme(self.main, self.main.menuStyles)

        self.addToolBar(toolbar)
        self.addToolBar(toolbar1)

    def onMyToolBarButtonClick(self, s):
        print("click", s)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()