from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MatplotlibWidget import MatplotlibWidget

class TableWidget(QTableWidget):
    def __init__(self, parent, data, headTitle, xcol, ycol):
        super(TableWidget, self).__init__(parent)
        self.father = parent
        #获取X、Y所在列
        self.xcol=0
        self.ycol=0
        if xcol != 0 and ycol !=0 :
            self.xcol = xcol
            self.ycol = ycol
        else:
            for i in range(1, len(headTitle)):
                if headTitle[i]=='Y' or headTitle[i]=='y':
                    self.ycol=i
                if headTitle[i]=='X' or headTitle[i]=='x':
                    self.xcol=i
        #读取文件数据
        self.data = data
        #文件头
        self.Head_Title = headTitle
        #反演进行时标记
        self.flag = [0]
        #正演参数
        self.forwardingInformation = ""#正演所有数据
        #反演范围
        self.bottom = 0.0
        self.top = 0.0
        #反演成功的标志
        self.inversionFlag = 0 #0代表未反演，1代表正在反演
        #反演数据,不同的后面都加上不同的数字，便于以后添加新的方法
        #初始第一个算法为不加后缀，后面可以以 _i 来区分
        self.kmax = 0
        self.lz = 0
        self.m_min = 0.0
        self.m_max = 0.0
        self.z_obs = 0.0
        self.dz = 0.0
        self.zmax = 0.0
        self.epsilon = 0.0
        self.miu = 0.0
        self.wn = 0.0
        self.sigma = 0.0
        self.Max_GPU_Number = 0
        self.nThreadPerBlock = 0
        #共有数据
        self.model_count =0
        self.point_count = 0
        self.dx = 0.0
        self.dy = 0.0
        self.nx = 0
        self.ny = 0
        self.nz = 0

        #需要计算的列表
        self.x = []
        self.y = []
        self.mx = []
        self.my = []
        self.mz = []
        self. Vzz= []
        self.thick = []#每一层的厚度
        self.zc = []#每一层测点的深度
        #反演返回值
        self.m_result = []#反演返回数组
        #求测线的数量
        #QMessageBox.information(self, "Attention", str(len(self.data))+" "+str(len(self.data[0]))+self.data[399][0])
        aa=[]
        for i in range(0, len(self.data)):
            if self.data[i][self.ycol-1] not in aa:
                aa.append(self.data[i][self.ycol-1])
        self.lineNumber = len(aa)
        self.ny = len(aa)
        #设置下拉列表框
        self.cb = QComboBox(self)
        cbItems = []
        for i in range(1, len(aa)+1):
            cbItems.append('Line'+str(i))
        self.cb.addItems(cbItems)#添加下拉选项
        
        #设置表格
        self.lieCount = len(self.data[0])
        self.hangCount = len(self.data)//self.lineNumber
        self.setColumnCount(self.lieCount+1)#设置列数
        self.setRowCount(self.hangCount+1)#设置行数
        
        self.horizontalHeader().setVisible(0)
        self.verticalHeader().setVisible(0)
        #设置表头
        for i in range(1, self.lieCount+1):
            self.setItem(0, i, QTableWidgetItem(headTitle[i]))
        self.item(0,self.xcol).setFlags(Qt.NoItemFlags)
        self.item(0,self.ycol).setFlags(Qt.NoItemFlags)
        for i in range(1, self.hangCount+1):
            self.setItem(i, 0, QTableWidgetItem(str(i)))
            self.item(i, 0).setFlags(Qt.NoItemFlags)
        #设置（0,0）位下拉框
        self.setCellWidget(0, 0, self.cb)
        
        #设置初始化的数据
        for i in range(1, self.hangCount+1):
            for j in range(1, self.lieCount+1):
                self.setItem(i, j, QTableWidgetItem(str(self.data[i-1][j-1])))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);#平分长度
        
        #右键事件
        self.rightKeyMenu = QMenu()
        self.actionCopy = QAction("Copy",self)
        self.actionCopy.setShortcut("Ctrl+C")
        self.actionCut = QAction("Cut",self)
        self.actionCut.setShortcut("Ctrl+X")
        self.actionDelete = QAction("Delete",self)
        self.actionDelete.setShortcut(QKeySequence.Delete)
        self.actionPaste = QAction("Paste",self)
        self.actionPaste.setShortcut("Ctrl+V")
        
        #当前显示的页面
        self.page = 0
        
        #信号槽
        self.cb.currentIndexChanged.connect(self.lineChanged)
        #self.cellClicked.connect(self.chooseAllColumn)
        
        self.actionCopy.triggered.connect(self.onActionCopy)
        self.actionCut.triggered.connect(self.onActionCut)
        self.actionDelete.triggered.connect(self.onActionDelete)
        self.actionPaste.triggered.connect(self.onActionPaste)
        
        
    #切换测线并且换图
    def lineChanged(self):
        #消除底部图
        position = self.father.tab.currentIndex()#当前Tab页索引
        tableWidget = self.father.tab.widget(position).activeSubWindow().widget()
        index = self.father.tab.widget(position).activeSubWindow().windowTitle()
        #换页之前保存当前页到self.data
        for i in range(1, self.hangCount+1):
                for j in range(1, self.lieCount+1):
                    self.data[self.page*self.hangCount+i-1][j-1] = self.item(i, j).text()
        lineNo = self.cb.currentIndex()
        #展示新的数据
        self.page = lineNo
        for i in range(1, self.hangCount+1):
            for j in range(1, self.lieCount+1):
                self.setItem(i, j, QTableWidgetItem(str(self.data[lineNo*self.hangCount+i-1][j-1])))
        #获得当前文件树的子目录列表
        root = self.father.tree.topLevelItem(position-1)
        #获得当前容器句柄
        mdiarea = self.father.tab.currentWidget()
        #切换只对Paint_Section有效
        #获得当前容器子窗口列表
        list = mdiarea.subWindowList()
        order = -1
        key = root.text(0)
        headTitle = self.Head_Title
        for key1, value in self.father.tree_record[key].items():
            order = order +1
            if key1 == 'data' : 
                continue
            if 'index' in self.father.tree_record[key][key1]:
                if self.father.tree_record[key][key1]['index'] == index and self.father.tree_record[key][key1]['type'] == 'Paint_Section':
                    mw = MatplotlibWidget()
                    fileName = self.father.tree_record[key][key1]['paint_name']
                    x = []
                    y = []
                    xunit = self.father.tree_record[key][key1]['X_axis_unit']
                    vunit = self.father.tree_record[key][key1]['V_axis_unit']
                    flag = int(self.father.tree_record[key][key1]['Show_Symbol'])
                    xposition=tableWidget.xcol
                    for i in range(1,len(headTitle)):
                        if headTitle[i]=="X" or headTitle[i]=="Y" or headTitle[i]=="x" or headTitle[i]=="y":continue
                        for t in range(0, len(fileName)):
                            if fileName[t] == headTitle[i]:
                                for j in range(1, tableWidget.hangCount+1):
                                    y.append(float(tableWidget.item(j, i).text()))
                                break
                    for i in range (1, tableWidget.hangCount+1):
                        x.append(float(tableWidget.item(i, xposition).text()))
                    if xunit == 'km':
                        x = [i / 1000 for i in x]
                    mw.mpl.section(lineNo+1, fileName, x, y, xunit, vunit, flag)
                    list[order].setWidget(mw)
            
                
    #复制
    def onActionCopy(self):
        stringCopy=""
        selectList = self.selectedItems()
        for i in range(0, len(selectList)-1):
            stringCopy = stringCopy + selectList[i].text() +","
        stringCopy += selectList[len(selectList)-1].text()
        board = QApplication.clipboard()
        board.setText(stringCopy)
        
    #剪切
    def onActionCut(self):
        stringCopy=""
        selectList = self.selectedItems()
        for i in range(0, len(selectList)-1):
            stringCopy = stringCopy + selectList[i].text() +","
            selectList[i].setText("")
        stringCopy += selectList[len(selectList)-1].text()
        selectList[len(selectList)-1].setText("")
        board = QApplication.clipboard()
        board.setText(stringCopy)
        
    #删除
    def onActionDelete(self):
        selectList = self.selectedItems()
        for i in range(0, len(selectList)):
            selectList[i].setText("")
        
    #粘贴
    def onActionPaste(self):
        board = QApplication.clipboard()
        stringPaste = board.text()
        selectList = self.selectedItems()
        stringPasteList = stringPaste.split(',')
        for i in range (0, min(len(stringPasteList), len(selectList))):
            selectList[i].setText(stringPasteList[i])
            
    #右键事件
    def contextMenuEvent(self, event):
        self.rightKeyMenu.clear
        #得到窗口坐标
        point = event.pos()
        item = self.itemAt(point)
        if item != None:
            self.rightKeyMenu.addAction(self.actionCopy)
            self.rightKeyMenu.addAction(self.actionCut)
            self.rightKeyMenu.addAction(self.actionDelete)
            self.rightKeyMenu.addAction(self.actionPaste)
            self.rightKeyMenu.addSeparator()
            #菜单出现的位置为当前鼠标的位置
            self.rightKeyMenu.exec(QCursor.pos())
            event.accept()
        
    #点击表头选中整列
    def chooseAllColumn(self, row, column):
        if row == 0 and column !=0:
            for i in range(self.hangCount, 0, -1):
                self.item(i, column).setSelected(1)
            self.item(0, column).setSelected(0)
        
