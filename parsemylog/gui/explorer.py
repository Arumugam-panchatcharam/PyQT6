from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QFileSystemModel

from os.path import expanduser
import core.global_var as globalvar
class ParseMyLogExplorer(QTreeView):
    def __init__(self):
        super().__init__()
        self.homedir = expanduser("~")
        self.log = globalvar.get_val("LOGGER")

        self.browser = QFileSystemModel(self)
        self.browser.setReadOnly(False)

        self.setModel(self.browser)
        #self.setAlternatingRowColors(True)
        #self.clicked.connect(lambda sel: self.selection_changed(sel))
        for col in range(1,self.browser.columnCount()):
            self.hideColumn(col)

    def setRootDir(self, folder_path):
        if folder_path:
            path = self.browser.setRootPath(folder_path)
            self.setRootIndex(path)
            self.setStatusTip(folder_path)

    def selection_changed(self, selected, TabBar):
        _selected_index_path = self.browser.filePath(selected)
        _selected_index_name = self.browser.fileName(selected)
        _file_type = self.browser.type(selected)
        
        self.log.debug(f"Selected file type: {_file_type}")
        self.log.debug(f"Selected file path: {_selected_index_path}")
        if self.browser.fileInfo(selected).isFile():
            self.log.debug(f"selected filename: {_selected_index_name}")
            for _type in ["text", "log", "C source code", "Python script"]:
                if _type in _file_type:
                    TabBar.tabbar_load(_selected_index_path)
                    break
            else:
                TabBar.tabbar_clear()
        else:
            TabBar.tabbar_clear()