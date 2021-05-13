#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, psutil, threading
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
                          QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QPushButton)


class App(QWidget):
    PROC_ID, PROC_NAME, PROC_USER, PROC_CPU, PROC_MEM, = range(5)

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 PROC LIST'
        self.left = 20
        self.top = 20
        self.width = 640
        self.height = 840
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.dataGroupBox = QGroupBox("ps")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        self.btn = QPushButton(self)
        self.btn.setText("Refresh")
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        dataLayout.addWidget(self.btn)
        self.dataGroupBox.setLayout(dataLayout)

        self.model = self.createProcModel(self)
        self.dataView.setModel(self.model)
        #for proc in psutil.process_iter():
        #    self.addProc(model, proc.pid, proc.name(), proc.cpu_percent(), proc.memory_percent())
        self.btn.clicked.connect(self.add_procs)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)

        self.show()

    def createProcModel(self, parent):
        model = QStandardItemModel(0, 5, parent)
        model.setHeaderData(self.PROC_ID, Qt.Horizontal, "PID")
        model.setHeaderData(self.PROC_NAME, Qt.Horizontal, "Name")
        model.setHeaderData(self.PROC_USER, Qt.Horizontal, "USER")
        model.setHeaderData(self.PROC_CPU, Qt.Horizontal, "CPU%")
        model.setHeaderData(self.PROC_MEM, Qt.Horizontal, "MEM%")
        return model

    def addProc(self, model, process_id, process_name, proc_cpu, proc_mem):
        model.insertRow(0)
        model.setData(model.index(0, self.PROC_ID), process_id)
        model.setData(model.index(0, self.PROC_NAME), process_name)
        model.setData(model.index(0, self.PROC_CPU), proc_cpu)
        model.setData(model.index(0, self.PROC_MEM), proc_mem)
    def add_procs(self):
        if(self.model.hasChildren()):
            self.model.removeRows(0,self.model.rowCount())
        for proc in psutil.process_iter():
            self.model.insertRow(0)
            self.model.setData(self.model.index(0, self.PROC_ID), proc.pid)
            self.model.setData(self.model.index(0, self.PROC_NAME), proc.name())
            self.model.setData(self.model.index(0, self.PROC_USER), proc.username())
            self.model.setData(self.model.index(0, self.PROC_CPU), proc.cpu_percent())
            self.model.setData(self.model.index(0, self.PROC_MEM), proc.memory_percent())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())