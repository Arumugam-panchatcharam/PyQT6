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

        self.toolbar = QToolBar("My main toolbar", self)
        self.toolbar.setIconSize(QSize(16, 16))
        
        self.toolbar1 = QToolBar("My main toolbar", self)
        self.toolbar1.setIconSize(QSize(16, 16))

        self.button_action = QAction(QIcon("bug.png"), "&Your button", self)
        self.button_action.setStatusTip("This is your button")
        self.button_action.triggered.connect(self.onMyToolBarButtonClick)
        self.button_action.setCheckable(True)
        self.toolbar.addAction(self.button_action)

        self.toolbar.addWidget(QLabel("Hello"))
        self.toolbar.addWidget(QCheckBox())

        combobox = QComboBox(self)
        combobox.addItem("Option 1")
        combobox.addItem("Option 2")
        combobox.addItem("Option 3")
        combobox.move(50, 50)
        self.toolbar1.addWidget(combobox)
        
        self.toolbar1.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        #self.add_menu_theme(self.main, self.main.menuStyles)

        self.addToolBar(self.toolbar)
        self.addToolBar(self.toolbar1)
        self.toolbar1.hide()
        

    def onMyToolBarButtonClick(self, s):
        if (s == True):
            self.toolbar1.show()
            print("show")
        else:
            self.toolbar1.hide()
            print("Hide")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()