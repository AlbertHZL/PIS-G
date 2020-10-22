from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DialogNewPro(QDialog):
    def __init__(self, parent = None):
        super(DialogNewPro, self).__init__(parent)
        self.father = parent
        self.resize(350, 150)
        # 设置控件
        layout = QVBoxLayout()
        # 第一个为 QGridLayout 排列
        label = QLabel("Project Name",  self)
        self.le = QLineEdit(self)
        order= self.number()
        self.le.setText("Project "+str(order))
        layout1 = QHBoxLayout()
        layout1.addWidget(label,  3)
        layout1.addWidget(self.le, 5)
        layout.addLayout(layout1)
        #按钮的 QHboxLayout 排列
        layout3 = QHBoxLayout()
        ok = QPushButton("ok", self)
        cancel = QPushButton("Cancel",  self)
        layout3.addStretch(1)
        layout3.addWidget(ok)
        layout3.addStretch(1)
        layout3.addWidget(cancel)
        layout3.addStretch(1)
        layout.addLayout(layout3)
        
        self.setLayout(layout)
        self.setWindowTitle("New Project")
        self.setWindowIcon(QIcon(".\\image\\logo.png"))
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        cancel.clicked.connect(self.on_cancel_clicked)
        ok.clicked.connect(self.on_ok_clicked)
        
    def on_cancel_clicked(self):
        self.close()
        return
    
    def on_ok_clicked(self):
        pro_name = self.le.text()
        if pro_name =="":
            QMessageBox.information(self, "ATTENTION", "Please Input Project Name")
            return 
        if pro_name in self.father.tree_record:
            QMessageBox.information(self, "Attention", "Project name already exists.")
            return 
        # 添加tree和tree_record还有tab页
        #在self.father的tree加入root
        root = QTreeWidgetItem(self.father.tree)
        #设置项目名称
        root.setText(0, pro_name)
        #记录 tree_record 及flag 记录
        self.father.tree_record[pro_name]={}
        # 初始值设为0
        self.father.paintCount.append(0)
        #设置标签页的控件
        mdiAreaForTab = QMdiArea(self.father)
        self.father.tab.addTab(mdiAreaForTab, pro_name)
        self.father.tab.setCurrentWidget(mdiAreaForTab)
        self.close()
    
    def number(self):
        s = 1
        while "Project "+str(s) in self.father.tree_record:
            s+=1
        return s
