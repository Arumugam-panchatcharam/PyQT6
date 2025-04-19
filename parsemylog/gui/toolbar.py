from PyQt6.QtWidgets import ( 
    QToolBar, 
    QFileDialog, 
    QComboBox,
    QSizePolicy,
    QSpacerItem,
    QLineEdit,
    QToolButton,
)
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QColor
from PyQt6.QtCore import QSize
from resources.qt_material_icons import MaterialIcon
from os.path import expanduser
import core.global_var as globalvar

TOOL_BAR_STYLE = """
    QToolBar {
        background-color: #292F36;
        spacing : 4px;
    }
    QToolBar QToolButton{
        color: white;
        font-size : 14px;
    }
"""

class ParseMyLogToolbar(QToolBar):
    def __init__(self):
        super().__init__()
        self.log = globalvar.get_val("LOGGER")
        self.setMovable(False)
        self.setIconSize(QSize(25,25))
        #self.setStyleSheet("background-color:aliceblue")
        self.setStyleSheet(TOOL_BAR_STYLE)

        self.open = QAction("Open File", self)
        self.open.setShortcuts(["Ctrl+O", "Ctrl+Shift+O"])
        self.open.setCheckable(False)
        folder_open_icon = MaterialIcon('folder_open',size=24)

        # log insight toolbar
        self.filter_log_level = QAction("Filter Log Level", self)
        self.filter_log_level.setCheckable(True)
        self.filter_log_level.setChecked(False)
        self.filter_log_level.setText("Filter Log Level")
        #filter_log_level_icon = MaterialIcon('filter_alt',size=24)

        self.drop_duplicates = QAction("Drop Duplicates", self)
        self.drop_duplicates.setCheckable(True)
        self.drop_duplicates.setChecked(False)
        self.drop_duplicates.setText("Drop Duplicates")

        self.regex_search = QAction("Regex Search", self)
        # Set a color
        #color = QColor('cadetblue')
        #folder_open_icon.set_color(color)
        #self.open.setIcon()

        # Set a color for a state, for example when a button is checked
        #folder_open_icon.set_color(color, state=QIcon.State.On)

        # Set a different icon for a state, for example when a button is checked
        #folder_icon = MaterialIcon('folder_open',size=48)
        #folder_open_icon = MaterialIcon('folder_open')
        #folder_icon.set_icon(folder_open_icon, state=QIcon.State.On)

        self.open.setIcon(folder_open_icon)
        self.open.setStatusTip("Open File")
        self.addSeparator()
        self.addAction(self.open)
        
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding,
                             QSizePolicy.Policy.Expanding)
        self.addWidget(spacer)

        self.addAction(self.filter_log_level)
        self.addAction(self.drop_duplicates)

    def OpenFolder(self, explorer):
        _dialog = QFileDialog()
        _folder_selected = _dialog.getExistingDirectory(self, 
                                             "Select Folder",
                                             expanduser("~/Downloads"))
        self.log.debug(f"Selected folder: {_folder_selected}")
        if _folder_selected:
            explorer.setRootDir(_folder_selected)