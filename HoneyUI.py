# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'honey_plot.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PySide2 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

class HoneyUI(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1134, 661)
        self.main_widget = QtWidgets.QWidget(main_window)
        self.main_widget.setObjectName("main_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.main_widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.vlayout_left = QtWidgets.QVBoxLayout()
        self.vlayout_left.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.vlayout_left.setObjectName("vlayout_left")
        self.pass_label = QtWidgets.QLabel(self.main_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pass_label.sizePolicy().hasHeightForWidth())
        self.pass_label.setSizePolicy(sizePolicy)
        self.pass_label.setObjectName("pass_label")
        self.vlayout_left.addWidget(self.pass_label)
        self.pass_listview = QtWidgets.QListView(self.main_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pass_listview.sizePolicy().hasHeightForWidth())
        self.pass_listview.setSizePolicy(sizePolicy)
        self.pass_listview.setObjectName("pass_listview")
        self.list_model = QtGui.QStandardItemModel()
        self.pass_listview.setModel(self.list_model)
        self.vlayout_left.addWidget(self.pass_listview)
        self.pass_button = QtWidgets.QPushButton(self.main_widget)
        self.pass_button.setObjectName("pass_button")
        self.vlayout_left.addWidget(self.pass_button)
        self.horizontalLayout_2.addLayout(self.vlayout_left)
        self.vlayout_right = QtWidgets.QVBoxLayout()
        self.vlayout_right.setObjectName("vlayout_right")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.loc_label = QtWidgets.QLabel(self.main_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loc_label.sizePolicy().hasHeightForWidth())
        self.loc_label.setSizePolicy(sizePolicy)
        self.loc_label.setObjectName("loc_label")
        self.horizontalLayout_3.addWidget(self.loc_label)
        self.error_label = QtWidgets.QLabel(self.main_widget)
        self.error_label.setStyleSheet("QLabel { color: red }")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")
        self.horizontalLayout_3.addWidget(self.error_label)
        self.vlayout_right.addLayout(self.horizontalLayout_3)
        self.web_view = QtWebEngineWidgets.QWebEngineView(self.main_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.web_view.sizePolicy().hasHeightForWidth())
        self.web_view.setSizePolicy(sizePolicy)
        self.web_view.setMinimumSize(QtCore.QSize(688, 557))
        self.web_view.setObjectName("web_view")
        self.vlayout_right.addWidget(self.web_view)
        self.hlayout_right = QtWidgets.QHBoxLayout()
        self.hlayout_right.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.hlayout_right.setObjectName("hlayout_right")
        self.api_button = QtWidgets.QPushButton(self.main_widget)
        self.api_button.setObjectName("api_button")
        self.hlayout_right.addWidget(self.api_button)
        self.loc_button = QtWidgets.QPushButton(self.main_widget)
        self.loc_button.setObjectName("loc_button")
        self.hlayout_right.addWidget(self.loc_button)
        self.vlayout_right.addLayout(self.hlayout_right)
        self.horizontalLayout_2.addLayout(self.vlayout_right)
        main_window.setCentralWidget(self.main_widget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Honey Plot"))
        self.pass_label.setText(_translate("main_window", "Top 100 Password Attempts"))
        self.pass_button.setText(_translate("main_window", "Clear Password Data"))
        self.loc_label.setText(_translate("main_window", "Last 100 Unique Locations"))
        self.api_button.setText(_translate("main_window", "Add DB-IP API Key"))
        self.loc_button.setText(_translate("main_window", "Clear Map Data"))

    def link_on_clicks(self, loc_on_click, pass_on_click, api_on_click):
        self.loc_button.clicked.connect(loc_on_click)
        self.pass_button.clicked.connect(pass_on_click)
        self.api_button.clicked.connect(api_on_click)

    def link_map_html(self, file_str):
        self.web_view.load(QtCore.QUrl(file_str))

    def get_scroll_view(self):
        return self.list_model

    def get_error_label(self):
        return self.error_label
