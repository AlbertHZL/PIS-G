from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Matplotlib3DWidget import Matplotlib3DWidget

class Dialog3D(QDialog):
    def __init__(self, parent):
        super(Dialog3D, self).__init__(parent)
        self.father = parent
        #绘制
        layout = QVBoxLayout()
        
        label = QLabel(self)
        label.setText("Please Choose the Variable to Paint")#请选择需要绘制3D图的测线
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1)
        
        #获取当前表格
        tableWidget = self.father.tableWidget
        groupBox = QGroupBox("Variable")
        groupBox.setFlat(True)
        self.button=[]
        for i in range(1, tableWidget.lieCount+1):
            if tableWidget.item(0, i).text()=="X" or tableWidget.item(0, i).text()=="Y" or tableWidget.item(0, i).text()=="x" or tableWidget.item(0, i).text()=="y":
                continue
            bt = QRadioButton(tableWidget.item(0, i).text())
            self.button.append(bt)
        layoutCenter = QHBoxLayout()
        for i in range(0, len(self.button)):
            layoutCenter.addWidget(self.button[i])
        groupBox.setLayout(layoutCenter)
        layout.addWidget(groupBox, 3)
        layout.addStretch(1)
        #添加选项
        #添加选项
        label1 = QLabel()
        label1.setText("Color Bar Title：")
        label2 = QLabel()
        label2.setText("Z axis:")
        label3 = QLabel()
        label3.setText("unit：")
        label4 = QLabel()
        label4.setText("X axis:")
        label5 = QLabel()
        label5.setText("Y axis:")
        
        self.le = QLineEdit()
        self.cb1 = QComboBox(self)
        self.cbItems1 = ['g.u.', 'E', 'mGal']
        self.cb1.addItems(self.cbItems1)#添加下拉选项
        self.cb3 = QComboBox(self)
        self.cbItems3 = ['m', 'km']
        self.cb3.addItems(self.cbItems3)#添加下拉选项
        self.cb4 = QComboBox(self)
        self.cbItems4 = ['m', 'km']
        self.cb4.addItems(self.cbItems4)#添加下拉选项
        #写界面
        layout2 = QHBoxLayout()
        layout2.addStretch(1)
        layout2.addWidget(label1, 2)
        layout2.addWidget(self.le, 2)
        layout2.addStretch(1)
        layout.addLayout(layout2, 1)
        layout.addStretch(1)
        
        layout1 = QHBoxLayout()
        layout1.addWidget(label3, 2)
        layout1.addWidget(label4, 2)
        layout1.addWidget(self.cb3, 2)
        layout1.addWidget(label5, 2)
        layout1.addWidget(self.cb4, 2)
        layout1.addWidget(label2, 2)
        layout1.addWidget(self.cb1, 2)
        layout.addLayout(layout1)
        layout.addStretch(1)
        
        #添加按钮
        layoutBottom = QHBoxLayout()
        layoutBottom.addStretch(5)
        ok = QPushButton("OK", self)
        cancel = QPushButton("Cancel", self)
        layoutBottom.addWidget(ok, 10)
        layoutBottom.addStretch(20)
        layoutBottom.addWidget(cancel, 10)
        layoutBottom.addStretch(5)
        layout.addLayout(layoutBottom, 1)
        
        self.setLayout(layout)
        self.setWindowTitle("Choose Variable to Paint")
        #去掉问号
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        #信号槽
        ok.clicked.connect(self.on_ok_clicked)
        cancel.clicked.connect(self.on_cancel_clicked)
        
        
    #ok
    def on_ok_clicked(self):
        #绘制剖面图
        position = self.father.tab.currentIndex()#当前Tab页索引
        tableWidget = self.father.tableWidget
        index = self.father.index
        #获取X&Y的位置
        xposition=tableWidget.xcol
        yposition=tableWidget.ycol
        fileName=""
        x=[]
        y=[]
        z=[]
        for i in range(0, len(self.button)):
            if self.button[i].isChecked()==True:
                #获取当前侧线的位置
                vposition=0
                for k in range(1, tableWidget.lieCount+1):
                    if tableWidget.item(0, k).text()==self.button[i].text():
                        vposition=k
                        break
                fileName += self.button[i].text()
                for j in range(0,  len(tableWidget.data)):
                    try:
                        z.append(float(tableWidget.data[j][vposition-1]))
                    except ValueError:
                        QMessageBox.information(self, "Error", "Variable "+str(int(j*tableWidget.lineNumber/len(tableWidget.data))+1)+" ("+\
                        str(int(j-int(j*tableWidget.lineNumber/len(tableWidget.data))*len(tableWidget.data)/tableWidget.lineNumber+1))+", "+\
                        str(vposition)+") cannot be converted into numbers")
                        return
                    try:
                        if float(tableWidget.data[j][yposition-1]) not in y:
                            y.append(float(tableWidget.data[j][yposition-1]))
                    except ValueError:
                        QMessageBox.information(self, "Error", "Variable "+str(int(j*tableWidget.lineNumber/len(tableWidget.data))+1)+" ("+\
                        str(int(j-int(j*tableWidget.lineNumber/len(tableWidget.data))*len(tableWidget.data)/tableWidget.lineNumber+1))+", "+\
                        str(yposition)+") cannot be converted into numbers")
                        return
                    try:
                        if float(tableWidget.data[j][xposition-1]) not in x:
                            x.append(float(tableWidget.data[j][xposition-1]))
                    except ValueError:
                        QMessageBox.information(self, "Error", "Variable "+str(int(j*tableWidget.lineNumber/len(tableWidget.data))+1)+" ("+\
                        str(int(j-int(j*tableWidget.lineNumber/len(tableWidget.data))*len(tableWidget.data)/tableWidget.lineNumber+1))+", "+\
                        str(xposition)+") cannot be converted into numbers")
                        return
                        
        if fileName=="":
            return
        #此处获得的数据：1、x列表；2、y列表；3、图名；4、x单位；5、y轴单位；6、z列表；7、colorbarTitle；#8、是否显示等值线；9、是否显示数值；
        xunit = self.cbItems3[self.cb3.currentIndex()]
        yunit = self.cbItems4[self.cb4.currentIndex()]
        zunit = self.cbItems1[self.cb1.currentIndex()]
        colorbarTitle = self.le.text()#可能为空
        
        if xunit == 'km':
            x = [i / 1000 for i in x]
        if yunit == 'km':
            y = [i / 1000 for i in y]
        
        mw = Matplotlib3DWidget()
        mw.mpl.D3Paint(fileName, x, y, z, xunit, yunit, zunit, colorbarTitle)
        
        finalName = fileName + " 3D Map"
        #设置子窗口
        sub = QMdiSubWindow()
        sub.setWindowIcon(QIcon(".\\image\\logo.png"))
        sub.setWidget(mw)
        # sub.setWindowTitle(finalName)
        self.father.tab.widget(position).addSubWindow(sub)
        self.father.tab.widget(position).setActiveSubWindow(sub)
        #self.father.tab.widget(position).cascadeSubWindows()#级联显示
        sub.show()
        #更改 tree_record 的值
        root = self.father.tree.topLevelItem(position-1)
        child_name = 'view_'+str(self.father.paintCount[position-1]) 
        root_name = root.text(0)
        # 判断重名
        order = 1
        flag = 0
        name_temp = finalName
        while flag == 0:
            flag = 1
            for key, value in self.father.tree_record[root_name].items():
                if 'tree_name' not in self.father.tree_record[root_name][key]:
                    flag = 2
                    continue
                if name_temp == self.father.tree_record[root_name][key]['tree_name']:
                    flag = 0
                    break
            if flag ==2:    continue
            if flag == 1:    finalName = name_temp
            name_temp = finalName + '_' +str(order)
            order = order + 1
        sub.setWindowTitle(finalName)
        #添加子树
        newItem = QTreeWidgetItem(root)
        newItem.setText(0, finalName)
        
        self.father.tree_record[root_name][child_name] ={'tree_name':finalName,'paint_name':fileName,'type':'Paint_3D', \
        'color_Bar_Title':str(colorbarTitle), 'X_axis_unit':str(xunit), 'Y_axis_unit':str(yunit), 'Z_axis_unit':str(zunit), \
        'Choose':str(vposition), 'index':index}
        self.father.paintCount[position-1] = self.father.paintCount[position-1] +1
        #设置树上root为选中状态
        for i in range(0, root.childCount()):
            root.child(i).setSelected(0)
        newItem.setSelected(1)
        root.setSelected(0)
        self.close()
        
    #cancel
    def on_cancel_clicked(self):
        self.close()
        
        
        
        
        
        
        
        
        
