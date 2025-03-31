from PyQt6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QWidget,
)

from gui.toolbar import ParseMyLogToolbar
from gui.statusbar import ParseMyLogStatusbar
from gui.explorer import ParseMyLogExplorer
from gui.tabbar import ParseMyLogTabBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ParseMyLog")
        self.setGeometry(300, 300, 1200, 600)

        self.toolbar = ParseMyLogToolbar()
        self.statusbar = ParseMyLogStatusbar()
        self.explorer = ParseMyLogExplorer()
        self.tabbar = ParseMyLogTabBar()

        self.addToolBar(self.toolbar)
        self.setStatusBar(self.statusbar)
        self.CreateMenu()

        layout = QHBoxLayout()
        layout.addWidget(self.explorer, stretch=1)
        layout.addWidget(self.tabbar, stretch=4)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.connect_signals()

    def connect_signals(self):
        self.toolbar.open.triggered.connect(lambda _, explorer=self.explorer: self.toolbar.OpenFolder(explorer))
        self.explorer.clicked.connect(lambda sel, tabbar=self.tabbar: self.explorer.selection_changed(sel, tabbar))

    def CreateMenu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(self.toolbar.open)
