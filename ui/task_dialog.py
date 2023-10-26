# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/task.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Task(object):
    def setupUi(self, Task):
        Task.setObjectName("Task")
        Task.resize(408, 407)
        Task.setStyleSheet("background-color: white;\n"
"color: black;    \n"
"border: 0px;")
        self.verticalLayout = QtWidgets.QVBoxLayout(Task)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cred_box = QtWidgets.QGroupBox(Task)
        self.cred_box.setStyleSheet("QLineEdit {\n"
"    background-color: #6498BB;\n"
"    border: 20px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    background-color: #73A2C1;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #9ABE74;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #A4C482;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #86B37E;\n"
"}")
        self.cred_box.setTitle("")
        self.cred_box.setObjectName("cred_box")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.cred_box)
        self.verticalLayout_5.setContentsMargins(20, -1, 20, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.input_box = QtWidgets.QGroupBox(self.cred_box)
        self.input_box.setTitle("")
        self.input_box.setObjectName("input_box")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.input_box)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.task_box = QtWidgets.QGroupBox(self.input_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.task_box.sizePolicy().hasHeightForWidth())
        self.task_box.setSizePolicy(sizePolicy)
        self.task_box.setTitle("")
        self.task_box.setObjectName("task_box")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.task_box)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.task_label = QtWidgets.QLabel(self.task_box)
        self.task_label.setObjectName("task_label")
        self.verticalLayout_3.addWidget(self.task_label)
        self.task = QtWidgets.QLineEdit(self.task_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.task.sizePolicy().hasHeightForWidth())
        self.task.setSizePolicy(sizePolicy)
        self.task.setMinimumSize(QtCore.QSize(350, 50))
        self.task.setInputMask("")
        self.task.setText("")
        self.task.setMaxLength(32767)
        self.task.setFrame(True)
        self.task.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.task.setObjectName("task")
        self.verticalLayout_3.addWidget(self.task)
        self.verticalLayout_4.addWidget(self.task_box)
        self.deadline_box = QtWidgets.QGroupBox(self.input_box)
        self.deadline_box.setTitle("")
        self.deadline_box.setObjectName("deadline_box")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.deadline_box)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.deadline_label = QtWidgets.QLabel(self.deadline_box)
        self.deadline_label.setObjectName("deadline_label")
        self.verticalLayout_2.addWidget(self.deadline_label)
        self.deadline = QtWidgets.QCalendarWidget(self.deadline_box)
        self.deadline.setGridVisible(False)
        self.deadline.setSelectionMode(QtWidgets.QCalendarWidget.SingleSelection)
        self.deadline.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.deadline.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.deadline.setObjectName("deadline")
        self.verticalLayout_2.addWidget(self.deadline)
        self.verticalLayout_4.addWidget(self.deadline_box)
        self.verticalLayout_5.addWidget(self.input_box)
        self.create_btn = QtWidgets.QPushButton(self.cred_box)
        self.create_btn.setMinimumSize(QtCore.QSize(350, 50))
        self.create_btn.setStyleSheet("border: 0px;\n"
"border-radius: 10px;")
        self.create_btn.setObjectName("create_btn")
        self.verticalLayout_5.addWidget(self.create_btn)
        self.verticalLayout.addWidget(self.cred_box)

        self.retranslateUi(Task)
        
        QtCore.QMetaObject.connectSlotsByName(Task)

    def retranslateUi(self, Task):
        _translate = QtCore.QCoreApplication.translate
        Task.setWindowTitle(_translate("Task", "Dialog"))
        self.task_label.setText(_translate("Task", "Задача"))
        self.deadline_label.setText(_translate("Task", "Деадлайн"))
        self.create_btn.setText(_translate("Task", "Создать"))
