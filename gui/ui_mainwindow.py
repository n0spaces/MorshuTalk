# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(324, 220)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.btn_load = QToolButton(self.centralwidget)
        self.btn_load.setObjectName(u"btn_load")

        self.gridLayout.addWidget(self.btn_load, 2, 0, 1, 1)

        self.btn_play = QToolButton(self.centralwidget)
        self.btn_play.setObjectName(u"btn_play")

        self.gridLayout.addWidget(self.btn_play, 2, 1, 1, 1)

        self.lbl_time_end = QLabel(self.centralwidget)
        self.lbl_time_end.setObjectName(u"lbl_time_end")

        self.gridLayout.addWidget(self.lbl_time_end, 2, 5, 1, 1)

        self.slider = QSlider(self.centralwidget)
        self.slider.setObjectName(u"slider")
        self.slider.setMaximum(0)
        self.slider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.slider, 2, 2, 1, 1)

        self.textedit = QTextEdit(self.centralwidget)
        self.textedit.setObjectName(u"textedit")
        self.textedit.setAcceptRichText(False)

        self.gridLayout.addWidget(self.textedit, 0, 0, 2, 6)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 4, 1, 1)

        self.lbl_time = QLabel(self.centralwidget)
        self.lbl_time.setObjectName(u"lbl_time")

        self.gridLayout.addWidget(self.lbl_time, 2, 3, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 324, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MorshuTalk", None))
        self.btn_load.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.btn_play.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.lbl_time_end.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"/", None))
        self.lbl_time.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
    # retranslateUi

