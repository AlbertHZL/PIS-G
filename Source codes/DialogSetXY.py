from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DialogSetXY(QDialog):
    def __init__(self, parent=None):
        super(DialogSetXY, self).__init__(parent)
        self.father = parent
        tableWidget = self.father.tableWidget
        #设计界面，可以让用户选择x，y，下拉菜单
        label1 = QLabel("set X:")
        label2 = QLabel("set Y:")
        self.xcb = QComboBox(self)
        self.ycb = QComboBox(self)
        for i in range(1, tableWidget.lieCount+1):
            self.xcb.addItem(tableWidget.item(0, i).text())
            self.ycb.addItem(tableWidget.item(0, i).text())
        layout1 = QHBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(label1, 2)
        layout1.addWidget(self.xcb, 1)
        layout1.addStretch(1)
        
        layout2 = QHBoxLayout()
        layout2.addStretch(1)
        layout2.addWidget(label2, 2)
        layout2.addWidget(self.ycb, 1)
        layout2.addStretch(1)
        
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addLayout(layout1, 1)
        layout.addStretch(2)
        layout.addLayout(layout2, 1)
        layout.addStretch(2)
        
        layoutBottom = QHBoxLayout()
        layoutBottom.addStretch(1)
        ok = QPushButton("ok", self)
        cancel = QPushButton("Cancel", self)
        layoutBottom.addWidget(ok, 1)
        layoutBottom.addStretch(2)
        layoutBottom.addWidget(cancel, 1)
        layoutBottom.addStretch(1)
        layout.addLayout(layoutBottom)
        
        self.setLayout(layout)
        self.setWindowTitle("Set X&Y")
        self.setWindowIcon(QIcon(".\\image\\logo.png"))
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        cancel.clicked.connect(self.on_cancel_clicked)
        ok.clicked.connect(self.on_ok_clicked)
    
    def on_ok_clicked(self):
        tableWidget = self.father.tableWidget
        tableWidget.xcol = self.xcb.currentIndex()
        tableWidget.ycol = self.ycb.currentIndex()
        QMessageBox.information(self, "Congratulation", "Set Success")
        self.close()
    def on_cancel_clicked(self):
        self.close()
        
