from PyQt6.QtWidgets import QToolBar, QFileDialog, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QColor
from PyQt6.QtCore import QSize
from resources.qt_material_icons import MaterialIcon
from os.path import expanduser

class ParseMyLogToolbar(QToolBar):
    def __init__(self):
        super().__init__()
        self.setMovable(False)
        self.setIconSize(QSize(25,25))
        self.setStyleSheet("background-color:aliceblue")

        self.open = QAction("Open File", self)
        folder_open_icon = MaterialIcon('folder_open',size=24)
        # Set a color
        color = QColor('cadetblue')
        folder_open_icon.set_color(color)
        #self.open.setIcon()

        # Set a color for a state, for example when a button is checked
        #folder_open_icon.set_color(color, state=QIcon.State.On)

        # Set a different icon for a state, for example when a button is checked
        #folder_icon = MaterialIcon('folder_open',size=48)
        #folder_open_icon = MaterialIcon('folder_open')
        #folder_icon.set_icon(folder_open_icon, state=QIcon.State.On)

        self.open.setIcon(folder_open_icon)
        self.open.setStatusTip("Open File")
        self.addAction(self.open)

    def OpenFolder(self, explorer):
        dialog = QFileDialog()
        folder_selected = dialog.getExistingDirectory(self, 
                                             "Select Folder",
                                             expanduser("~"))
        print("folder {0}".format(folder_selected))
        if folder_selected:
            explorer.setRootDir(folder_selected)