# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Nov 11 15:06:11 2013
#      by: PyQt5 UI code generator 5.1.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from gui.desktop.lib.videowidget import VideoWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.menuTree = QtWidgets.QTreeWidget(self.centralwidget)
        self.menuTree.setMaximumSize(QtCore.QSize(300, 16777215))
        self.menuTree.setObjectName("menuTree")
        self.menuTree.headerItem().setText(0, "Catalog")
        self.menuTree.setMinimumSize(QtCore.QSize(100, 100))
        self.horizontalLayout.addWidget(self.menuTree)

        frame = QtWidgets.QFrame(self.centralwidget)
        self.horizontalLayout.addWidget(frame)
        self.verticalLayout = QtWidgets.QVBoxLayout(frame)
        self.itemList = QtWidgets.QListWidget(frame)
        self.itemList.setMaximumSize(QtCore.QSize(99999, 16777215))
        self.itemList.setObjectName("itemList")
#        self.itemList.headerItem().setText(0, "Items")
        self.itemList.setMinimumSize(QtCore.QSize(100, 100))
        self.verticalLayout.addWidget(self.itemList)

        self.statusArea = QtWidgets.QLabel(frame)
        self.statusArea.setObjectName("statusArea")
        self.verticalLayout.addWidget(self.statusArea)

        self.videoArea = VideoWidget(frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.videoArea.sizePolicy().hasHeightForWidth())
        self.videoArea.setSizePolicy(sizePolicy)
        self.videoArea.setObjectName("videoArea")
        self.videoArea.setMinimumSize(QtCore.QSize(100, 100))
        self.verticalLayout.addWidget(self.videoArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "P2C - new way to watching videos"))

