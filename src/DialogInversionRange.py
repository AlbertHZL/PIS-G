from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ctypes import *
from ModelWidget import ModelWidget
from DialogInversionSection import DialogInversionSection

class DialogInversionRange(QDialog):
    def __init__(self, parent, tableWidget, flag,  index):
        super(DialogInversionRange, self).__init__(parent)
        self.father = parent
        
        label1 = QLabel("Please Fill in the Cube Density Range,Model Name,ColorBar Title.")
        label2 = QLabel("lower limit:")
        label3 = QLabel("g/cm^3 upper limit:")
        label4 = QLabel("g/cm^3")
        self.bottom = QLineEdit()
        self.top = QLineEdit()
        label5 = QLabel("Model Name:")
        self.title = QLineEdit()
        label6 = QLabel("ColorBar Title:")
        self.colorbarTitle = QLineEdit()
        
        label7 = QLabel()
        label7.setText("X axis unit:")
        label8 = QLabel()
        label8.setText("Y axis unit:")
        self.cb1 = QComboBox(self)
        self.cbItems1 = ['m', 'km']
        self.cb1.addItems(self.cbItems1)
        self.cb2 = QComboBox(self)
        self.cbItems2 = ['m', 'km']
        self.cb2.addItems(self.cbItems2)
        
        
        ok = QPushButton("OK", self)
        cancel = QPushButton("Cancel", self)
        
        layout1 = QHBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(label2, 1)
        layout1.addWidget(self.bottom, 1)
        layout1.addWidget(label3, 1)
        layout1.addWidget(self.top, 1)
        layout1.addWidget(label4)
        layout1.addStretch(1)
        
        layout2 = QHBoxLayout()
        layout2.addStretch(1)
        layout2.addWidget(label5, 1)
        layout2.addWidget(self.title, 1)
        layout2.addWidget(label6, 1)
        layout2.addWidget(self.colorbarTitle, 1)
        layout2.addStretch(1)
        
        layout3 = QHBoxLayout()
        layout3.addStretch(1)
        layout3.addWidget(label7, 1)
        layout3.addWidget(self.cb1, 1)
        layout3.addWidget(label8, 1)
        layout3.addWidget(self.cb2, 1)
        layout3.addStretch(1)
        
        layoutBottom = QHBoxLayout()
        layoutBottom.addStretch(1)
        layoutBottom.addWidget(ok, 1)
        layoutBottom.addStretch(1)
        layoutBottom.addWidget(cancel, 1)
        layoutBottom.addStretch(1)
        
        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layoutBottom)
        
        self.setLayout(layout)
        self.setWindowTitle("Inversion Information")
        
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        ok.clicked.connect(lambda:self.on_ok_clicked(tableWidget, flag,  index))
        cancel.clicked.connect(self.on_cancel_clicked)
        
    def on_cancel_clicked(self):
        self.close()
        return
    
    def on_ok_clicked(self, tableWidget, flag,  index):
        bottom = self.bottom.text()
        top = self.top.text()
        
        if bottom == "" or top == "":
            QMessageBox.information(self, "ATTENTION", "Please Input Necessary Data")
            return
        
        try:
            tableWidget.bottom = float(bottom)
            tableWidget.top = float(top)
        except ValueError:
            QMessageBox.information(self, "Error", "Please enter the correct data.")
            return
        if float(bottom)>float(top):
            QMessageBox.information(self, "ATTENTION", "Wrong Range!")
            return
        
        xx = 1
        yy = 1
        if self.cbItems1[self.cb1.currentIndex()] == 'km':
            xx = 1000
        if self.cbItems2[self.cb2.currentIndex()] == 'km': 
            yy = 1000
        
        mw = ModelWidget(self.father)
        mwTitle = self.title.text()
        mwColorBarTitle = self.colorbarTitle.text()
        position = self.father.tab.currentIndex()
        root = self.father.tree.topLevelItem(position-1)
        child_name = 'view_'+str(self.father.paintCount[position-1]) 
        root_name = root.text(0)
        if mwTitle == "":
            mwTitle = "Inversion Results"
        else:
            for key, value in self.father.tree_record[root_name].items():
                if 'title' not in self.father.tree_record[root_name][key]: continue
                if mwTitle == self.father.tree_record[root_name][key]['title']:
                    QMessageBox.information(self, "ATTENTION", "Model Name already exists")
                    return
        
        order = 1
        flag1 = 0
        name_temp = mwTitle
        while flag1 == 0:
            flag1 = 1
            for key, value in self.father.tree_record[root_name].items():
                if 'title' not in self.father.tree_record[root_name][key]:
                    flag1 = 2
                    continue
                if name_temp == self.father.tree_record[root_name][key]['title']:
                    flag1 = 0
                    break
            if flag1 ==2:    continue
            if flag1 == 1:    mwTitle = name_temp
            name_temp = mwTitle + '_' +str(order)
            order = order + 1
        
        mw.mpl.setTitle(mwTitle)
       
        minList = []
        maxList = []
        m_result = []
        zmax1 = 0
        type = "Inversion_Paint_parallel"
        if flag == 0:
            m_result = tableWidget.m_result
            zmax1 = tableWidget.zmax
        
        for i in range(0, len(m_result)):
            for j in range(0, len(m_result[0])):
                minList.append(min(m_result[i][j]))
                maxList.append(max(m_result[i][j]))
            
        mw.mpl.setRange(min(minList), max(maxList))
        
        zmax = 0.0
        k = int(zmax1/1000)
        yu = zmax1-k*1000
        if yu > 0:
            zmax = (k+1)*1000
        else:
            zmax = k*1000
        for i in range(0, tableWidget.nz):
            for j in range(0, tableWidget.ny):
                for k in range(0, tableWidget.nx):
                    if m_result[i][j][k] >= tableWidget.bottom and m_result[i][j][k]<=tableWidget.top:
                        pointPosition = i*tableWidget.nx*tableWidget.ny  + j*tableWidget.nx + k
                        xlim = [tableWidget.mx[pointPosition] /xx, tableWidget.mx[pointPosition+tableWidget.model_count] /xx]
                        ylim = [tableWidget.my[pointPosition] /yy, tableWidget.my[pointPosition+tableWidget.model_count] /yy]
                        zlim = [tableWidget.mz[pointPosition], tableWidget.mz[pointPosition+tableWidget.model_count]]
                        density = m_result[i][j][k]
                        xdown = tableWidget.mx[0] / xx
                        xup = tableWidget.mx[tableWidget.model_count-1] / xx
                        ydown = tableWidget.my[0] / yy
                        yup = tableWidget.my[tableWidget.model_count-1] / yy
                        mw.mpl.paintCube( xlim, ylim, zlim,density, xdown, xup, ydown, yup, zmax, xx, yy)
        
        if mwColorBarTitle == "":
            mwColorBarTitle = "density(g/cm^3)"
        mw.mpl.setColorbar(mwColorBarTitle)
        
        xy = QAction("X-Y Profile", self)
        xz = QAction("X-Z Profile", self)
        yz = QAction("Y-Z Profile", self)
        mw.mpl.menu.addAction(xy)
        mw.mpl.menu.addAction(xz)
        mw.mpl.menu.addAction(yz)
        xy.triggered.connect(lambda:self.xy(tableWidget, flag, index))
        xz.triggered.connect(lambda:self.xz(tableWidget, flag, index))
        yz.triggered.connect(lambda:self.yz(tableWidget, flag, index))
        
        sub = QMdiSubWindow()
        sub.setWindowIcon(QIcon(".\\image\\logo.png"))
        sub.setWidget(mw)
        sub.setWindowTitle(mwTitle)
        mid=self.father.tab.currentWidget()
        mid.addSubWindow(sub)
        sub.show()
        
        selectedList = self.father.tree.selectedItems()
        for i in range(0, len(selectedList)):
            selectedList[i].setSelected(0)
        
        child3 = QTreeWidgetItem(root)
        child3.setText(0, mwTitle)
        child3.setSelected(1)
        root.setExpanded(1)
        self.father.tree_record[root_name][child_name] ={'title':mwTitle,'type':type, \
        'color_Bar_Title':str(mwColorBarTitle), 'top':str(top), 'bottom':str(bottom), 'index':index, \
        'xx':xx, 'yy':yy}
        self.father.paintCount[position-1] = self.father.paintCount[position-1] +1
        self.close()
        return
        
    def xy(self, tableWidget, flag, index):
        dialog = DialogInversionSection(self.father, 1, tableWidget, flag, index)
        dialog.show()
        return
        
    def xz(self, tableWidget, flag, index):
        dialog = DialogInversionSection(self.father, 2, tableWidget, flag, index)
        dialog.show()
        return
        
    def yz(self, tableWidget, flag, index):
        dialog = DialogInversionSection(self.father, 3, tableWidget, flag, index)
        dialog.show()
        return
