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
        label.setText("Calculating begins \nThis may take a few minutes.\n")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1)
        
        layoutBottom = QHBoxLayout()
        layoutBottom.addStretch(5)
        ok = QPushButton("OK", self)
        layoutBottom.addStretch(20)
        layoutBottom.addWidget(ok, 10)
        layout.addStretch(1)
        layout.addLayout(layoutBottom, 1)
        
        self.setLayout(layout)
        self.setWindowTitle('Tips')
        
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        ok.clicked.connect(self.on_ok_clicked)
        
    def on_ok_clicked(self):
        self.hide()
