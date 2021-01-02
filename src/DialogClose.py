from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DialogClose(QDialog):
    def __init__(self, parent):
        super(DialogClose, self).__init__(parent)
        self.father = parent
        self.setWindowIcon(QIcon(".\\image\\logo.png"))
        layout = QVBoxLayout()
        layout.addStretch(1)
        label = QLabel(self)
        label.setText("Do you want to close the current project？")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1)
        
        layoutBottom = QHBoxLayout()
        layoutBottom.addStretch(5)
        ok = QPushButton("OK", self)
        cancel = QPushButton("Cancel", self)
        layoutBottom.addWidget(ok, 10)
        layoutBottom.addStretch(20)
        layoutBottom.addWidget(cancel, 10)
        layoutBottom.addStretch(5)
        layout.addStretch(1)
        layout.addLayout(layoutBottom, 1)
        
        self.setLayout(layout)
        self.setWindowTitle("Tips")
        
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        ok.clicked.connect(self.on_ok_clicked)
        cancel.clicked.connect(self.on_cancel_clicked)
        
    def on_ok_clicked(self):
        
        position = self.father.tab.currentIndex()
        
        file_name = str(self.father.tree.topLevelItem(position-1).text(0))
        del self.father.tree_record[file_name]
        
        self.father.tab.removeTab(position)
        
        self.father.tree.takeTopLevelItem(position-1)
        self.close()
        return
        
    def on_cancel_clicked(self):
        self.close()
        return
