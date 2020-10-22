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
        label.setText("Do you want to close the current project？")#是否关闭当前项目
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1)
        
        #添加按钮
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
        #去掉问号
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        #信号槽
        ok.clicked.connect(self.on_ok_clicked)
        cancel.clicked.connect(self.on_cancel_clicked)
        
    def on_ok_clicked(self):
        #获取索引
        position = self.father.tab.currentIndex()
        #更改tree_record项目
        file_name = str(self.father.tree.topLevelItem(position-1).text(0))
        del self.father.tree_record[file_name]
        #删除tab页
        self.father.tab.removeTab(position)
        #删除文件树
        self.father.tree.takeTopLevelItem(position-1)
        self.close()
        return
        
    def on_cancel_clicked(self):
        self.close()
        return
