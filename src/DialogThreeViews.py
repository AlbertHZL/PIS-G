from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DialogThreeViews(QDialog):
    def __init__(self, parent, number, index):
        super(DialogThreeViews, self).__init__(parent)
        self.father = parent
        
        label1 = QLabel("Painting Title:")
        self.title = QLineEdit()
        label2 = QLabel("ColorBar Title:")
        self.colorbarTitle = QLineEdit()
        
        layout1 = QHBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(label1, 1)
        layout1.addWidget(self.title, 1)
        layout1.addStretch(1)
        
        layout2 = QHBoxLayout()
        layout2.addStretch(1)
        layout2.addWidget(label2, 1)
        layout2.addWidget(self.colorbarTitle, 1)
        layout2.addStretch(1)
        
        layoutBottom = QHBoxLayout()
        layoutBottom.addStretch(1)
        ok = QPushButton("OK", self)
        cancel = QPushButton("Cancel", self)
        layoutBottom.addWidget(ok, 1)
        layoutBottom.addStretch(2)
        layoutBottom.addWidget(cancel, 1)
        layoutBottom.addStretch(1)
        
        layout = QVBoxLayout()
        layout.addLayout(layout1, 1)
        layout.addLayout(layout2, 1)
        layout.addStretch(1)
        layout.addLayout(layoutBottom, 1)
        
        self.setLayout(layout)
        self.setWindowTitle("Input Information")
        
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        ok.clicked.connect(lambda:self.on_ok_clicked(number, index))
        cancel.clicked.connect(self.on_cancel_clicked)
        
    def on_cancel_clicked(self):
        self.close()
        return
        
    def on_ok_clicked(self, number, index):
        self.father.title.clear()
        self.father.colorbarTitle.clear()
        self.father.title.append(self.title.text())
        self.father.colorbarTitle.append(self.colorbarTitle.text())
        if number == 1:
            self.father.front(index)
        if number == 2:
            self.father.side(index)
        if number == 3:
            self.father.down(index)
        self.close()      
