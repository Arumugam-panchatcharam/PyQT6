from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QFileSystemModel

from os.path import expanduser

class ParseMyLogExplorer(QTreeView):
    def __init__(self):
        super().__init__()
        self.homedir = expanduser("~")

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

    def selection_changed(self, selected, TabBar):
        selected_index_path = self.browser.filePath(selected)
        selected_index_name = self.browser.fileName(selected)
        file_type = self.browser.type(selected)
        print(file_type)
        if self.browser.fileInfo(selected).isFile():
            print(selected_index_name)
            for type in ["text", "log", "C source code", "Python script"]:
                if type in file_type:
                    TabBar.tabbar_load(selected_index_path)
                    break
            else:
                TabBar.tabbar_clear()
        else:
            TabBar.tabbar_clear()