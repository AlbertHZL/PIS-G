from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DialogInformation(QDialog):
    def __init__(self, parent):
        super(DialogInformation, self).__init__(parent)
        self.father = parent
        self.setWindowIcon(QIcon(".\\image\\logo.png"))
        layout = QVBoxLayout()
        layout.addStretch(1)
        label = QLabel(self)
        label.setText("Calculating begins \nThis may take a few minutes.\n")#是否关闭当前项目
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1)
        
        #添加按钮
        layoutBottom = QHBoxLayout()
        layoutBottom.addStretch(5)
        ok = QPushButton("OK", self)
        layoutBottom.addStretch(20)
        layoutBottom.addWidget(ok, 10)
        layout.addStretch(1)
        layout.addLayout(layoutBottom, 1)
        
        self.setLayout(layout)
        self.setWindowTitle('Tips')
        #去掉问号
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        #信号槽
        ok.clicked.connect(self.on_ok_clicked)
        
    def on_ok_clicked(self):
        self.hide()
