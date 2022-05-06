# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/anton/code/nRCM-Viewer/resources/ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        self.menu_Menu = QtWidgets.QMenu(self.menubar)
        self.menu_Menu.setObjectName("menu_Menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_zip = QtWidgets.QAction(MainWindow)
        self.actionLoad_zip.setObjectName("actionLoad_zip")
        self.actionLoad_Workspace = QtWidgets.QAction(MainWindow)
        self.actionLoad_Workspace.setObjectName("actionLoad_Workspace")
        self.menu_Menu.addAction(self.actionLoad_zip)
        self.menu_Menu.addAction(self.actionLoad_Workspace)
        self.menubar.addAction(self.menu_Menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Not RCM Viewer"))
        self.menu_Menu.setTitle(_translate("MainWindow", "&File"))
        self.actionLoad_zip.setText(_translate("MainWindow", "Load .zip"))
        self.actionLoad_Workspace.setText(_translate("MainWindow", "Load Workspace"))
