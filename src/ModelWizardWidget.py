from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ModelWizardWidget(QWidget):
    def __init__(self, parent=None):
        super(ModelWizardWidget, self).__init__(parent)
        
        self.aa=[]
        self.label1=QLabel()
        self.label1.setText("Model Shape：")
        self.label2=QLabel()
        self.label2.setText("Residual Density：")
        self.label3=QLabel()
        self.label3.setText("g/cm^3")
        self.cb=QComboBox()
        self.cbItems = ["Drop-down to Select Model", "Cube"]
        self.cb.addItems(self.cbItems)
        self.le=QLineEdit()
        self.layout1=QHBoxLayout()
        self.layout1.addWidget(self.label1, 2)
        self.layout1.addWidget(self.cb, 2)
        self.layout1.addWidget(self.label2, 1)
        self.layout1.addWidget(self.le, 1)
        self.layout1.addWidget(self.label3, 1)
        self.le1=QLineEdit()
        self.le2=QLineEdit()
        self.le3=QLineEdit()
        self.le4=QLineEdit()
        self.le5=QLineEdit()
        self.le6=QLineEdit()
        
        self.tableWidget=QTableWidget()
        self.tableWidget.horizontalHeader().setVisible(0)
        self.tableWidget.verticalHeader().setVisible(0)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setItem(0, 0, QTableWidgetItem(" "))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("lower limit"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("upper limit"))
        for i in range(0, 3):
            self.tableWidget.item(0, i).setFlags(Qt.NoItemFlags)
        self.tableWidget.setItem(1, 0, QTableWidgetItem("X-Range"))
        self.tableWidget.item(1, 0).setFlags(Qt.NoItemFlags)
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Y-Range"))
        self.tableWidget.item(2, 0).setFlags(Qt.NoItemFlags)
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Z-Range"))
        self.tableWidget.item(3, 0).setFlags(Qt.NoItemFlags)
        
        self.tableWidget.setCellWidget(1, 1, self.le1)
        self.tableWidget.setCellWidget(1, 2, self.le2)
        self.tableWidget.setCellWidget(2, 1, self.le3)
        self.tableWidget.setCellWidget(2, 2, self.le4)
        self.tableWidget.setCellWidget(3, 1, self.le5)
        self.tableWidget.setCellWidget(3, 2, self.le6)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("unit:m"))
        self.tableWidget.item(0, 0).setFlags(Qt.NoItemFlags)
        
        layout=QVBoxLayout()
        layout.addStretch(2)
        layout.addLayout(self.layout1, 1)
        layout.addWidget(self.tableWidget, 3)
        layout.addStretch(1)
        self.setLayout(layout)
        
        self.cb.currentIndexChanged.connect(self.lineChanged)
        
    def lineChanged(self):
        id = self.cb.currentIndex()
        tableWidget=self.tableWidget
        if id==1:
            self.le1=QLineEdit()
            self.le2=QLineEdit()
            self.le3=QLineEdit()
            self.le4=QLineEdit()
            self.le5=QLineEdit()
            self.le6=QLineEdit()
            tableWidget.clearContents()
            tableWidget.setColumnCount(3)
            tableWidget.setRowCount(4)
            tableWidget.setItem(0, 0, QTableWidgetItem(" "))
            tableWidget.setItem(0, 1, QTableWidgetItem("lower limit"))
            tableWidget.setItem(0, 2, QTableWidgetItem("upper limit"))
            for i in range(0, 3):
                tableWidget.item(0, i).setFlags(Qt.NoItemFlags)
            tableWidget.setItem(1, 0, QTableWidgetItem("X-Range"))
            tableWidget.item(1, 0).setFlags(Qt.NoItemFlags)
            tableWidget.setItem(2, 0, QTableWidgetItem("Y-Range"))
            tableWidget.item(2, 0).setFlags(Qt.NoItemFlags)
            tableWidget.setItem(3, 0, QTableWidgetItem("Z-Range"))
            tableWidget.item(3, 0).setFlags(Qt.NoItemFlags)
            
            tableWidget.setCellWidget(1, 1, self.le1)
            tableWidget.setCellWidget(1, 2, self.le2)
            tableWidget.setCellWidget(2, 1, self.le3)
            tableWidget.setCellWidget(2, 2, self.le4)
            tableWidget.setCellWidget(3, 1, self.le5)
            tableWidget.setCellWidget(3, 2, self.le6)
            tableWidget.setItem(0, 0, QTableWidgetItem("unit:m"))
            tableWidget.item(0, 0).setFlags(Qt.NoItemFlags)
