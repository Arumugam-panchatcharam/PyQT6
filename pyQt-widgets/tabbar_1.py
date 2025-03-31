from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QTabWidget, 
    QVBoxLayout, 
    QWidget, 
    QHBoxLayout,
    QGroupBox,
    QPushButton
)
import sys, os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainWidget=QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QVBoxLayout()
        mainWidget.setLayout(mainLayout)

        self.tabWidget = QTabWidget()
        mainLayout.addWidget(self.tabWidget)
        self.tabWidget.setMovable(True)

        self.tabWidget.tabBarClicked.connect(lambda sel: self.tabSelected(sel))

        myBoxLayout = QVBoxLayout()
        self.tabWidget.setLayout(myBoxLayout)

        self.tabWidget.addTab(QWidget(),'Tab_01')
        self.tabWidget.addTab(QWidget(),'Tab_02')
        self.tabWidget.addTab(QWidget(),'Tab_03')          


        ButtonBox = QGroupBox() 
        ButtonsLayout = QHBoxLayout()
        ButtonBox.setLayout(ButtonsLayout)

        Button_01 = QPushButton("What Tab?")
        ButtonsLayout.addWidget(Button_01)
        Button_01.clicked.connect(self.whatTab)

        mainLayout.addWidget(ButtonBox)


    def tabSelected(self, sel):
        print ("\n\t tabSelected() current Tab index =", sel)

    def whatTab(self):
        currentIndex=self.tabWidget.currentIndex()
        currentWidget=self.tabWidget.currentWidget()

        print ("\n\t Query: current Tab index =", currentIndex)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()