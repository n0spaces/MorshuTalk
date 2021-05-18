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

import res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(416, 388)
        self.action_view_sprite = QAction(MainWindow)
        self.action_view_sprite.setObjectName(u"action_view_sprite")
        self.action_view_sprite.setCheckable(True)
        self.action_quit = QAction(MainWindow)
        self.action_quit.setObjectName(u"action_quit")
        self.action_use_phoneme_priority = QAction(MainWindow)
        self.action_use_phoneme_priority.setObjectName(u"action_use_phoneme_priority")
        self.action_use_phoneme_priority.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.layout_sprite = QHBoxLayout()
        self.layout_sprite.setObjectName(u"layout_sprite")
        self.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_sprite.addItem(self.horizontalSpacer)

        self.lbl_sprite = QLabel(self.centralwidget)
        self.lbl_sprite.setObjectName(u"lbl_sprite")
        self.lbl_sprite.setPixmap(QPixmap(u":/sprites/82.png"))
        self.lbl_sprite.setScaledContents(True)
        self.lbl_sprite.setAlignment(Qt.AlignCenter)
        self.lbl_sprite.setTextInteractionFlags(Qt.NoTextInteraction)

        self.layout_sprite.addWidget(self.lbl_sprite)

        self.horizontalSpacer_2 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_sprite.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.layout_sprite)

        self.textedit = QTextEdit(self.centralwidget)
        self.textedit.setObjectName(u"textedit")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit.sizePolicy().hasHeightForWidth())
        self.textedit.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        self.textedit.setFont(font)
        self.textedit.setTabChangesFocus(True)
        self.textedit.setAcceptRichText(False)

        self.verticalLayout_2.addWidget(self.textedit)

        self.layout_playback = QHBoxLayout()
        self.layout_playback.setObjectName(u"layout_playback")
        self.layout_playback.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.btn_load = QToolButton(self.centralwidget)
        self.btn_load.setObjectName(u"btn_load")

        self.layout_playback.addWidget(self.btn_load)

        self.btn_play = QToolButton(self.centralwidget)
        self.btn_play.setObjectName(u"btn_play")

        self.layout_playback.addWidget(self.btn_play)

        self.slider = QSlider(self.centralwidget)
        self.slider.setObjectName(u"slider")
        self.slider.setMaximum(0)
        self.slider.setPageStep(1000)
        self.slider.setTracking(True)
        self.slider.setOrientation(Qt.Horizontal)

        self.layout_playback.addWidget(self.slider)

        self.lbl_time = QLabel(self.centralwidget)
        self.lbl_time.setObjectName(u"lbl_time")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lbl_time.sizePolicy().hasHeightForWidth())
        self.lbl_time.setSizePolicy(sizePolicy1)

        self.layout_playback.addWidget(self.lbl_time)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.layout_playback.addWidget(self.label)

        self.lbl_time_end = QLabel(self.centralwidget)
        self.lbl_time_end.setObjectName(u"lbl_time_end")
        sizePolicy1.setHeightForWidth(self.lbl_time_end.sizePolicy().hasHeightForWidth())
        self.lbl_time_end.setSizePolicy(sizePolicy1)

        self.layout_playback.addWidget(self.lbl_time_end)


        self.verticalLayout_2.addLayout(self.layout_playback)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 416, 21))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName(u"menuOptions")
        self.menu_view = QMenu(self.menuOptions)
        self.menu_view.setObjectName(u"menu_view")
        self.menuMorshuTalk = QMenu(self.menuOptions)
        self.menuMorshuTalk.setObjectName(u"menuMorshuTalk")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menu_file.addAction(self.action_quit)
        self.menuOptions.addAction(self.menuMorshuTalk.menuAction())
        self.menuOptions.addAction(self.menu_view.menuAction())
        self.menu_view.addAction(self.action_view_sprite)
        self.menuMorshuTalk.addAction(self.action_use_phoneme_priority)

        self.retranslateUi(MainWindow)
        self.action_view_sprite.toggled.connect(self.lbl_sprite.setVisible)
        self.action_quit.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MorshuTalk", None))
        self.action_view_sprite.setText(QCoreApplication.translate("MainWindow", u"Morshu", None))
        self.action_quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.action_use_phoneme_priority.setText(QCoreApplication.translate("MainWindow", u"Use phoneme priority", None))
        self.lbl_sprite.setText("")
        self.textedit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type some text here, click Load to generate the audio, then click Play.", None))
        self.btn_load.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.btn_play.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.lbl_time.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"/", None))
        self.lbl_time_end.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.menu_view.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuMorshuTalk.setTitle(QCoreApplication.translate("MainWindow", u"MorshuTalk", None))
    # retranslateUi

