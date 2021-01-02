from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MatplotlibWidget import MatplotlibWidget

class TableWidget(QTableWidget):
    def __init__(self, parent, data, headTitle, xcol, ycol):
        super(TableWidget, self).__init__(parent)
        self.father = parent
        
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
        
        self.data = data
        self.Head_Title = headTitle
        self.flag = [0]
        self.forwardingInformation = ""
        self.bottom = 0.0
        self.top = 0.0
        self.inversionFlag = 0
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
        
        self.model_count =0
        self.point_count = 0
        self.dx = 0.0
        self.dy = 0.0
        self.nx = 0
        self.ny = 0
        self.nz = 0

        self.x = []
        self.y = []
        self.mx = []
        self.my = []
        self.mz = []
        self. Vzz= []
        self.thick = []
        self.zc = []
        
        self.m_result = []
        
        aa=[]
        for i in range(0, len(self.data)):
            if self.data[i][self.ycol-1] not in aa:
                aa.append(self.data[i][self.ycol-1])
        self.lineNumber = len(aa)
        self.ny = len(aa)
        
        self.cb = QComboBox(self)
        cbItems = []
        for i in range(1, len(aa)+1):
            cbItems.append('Line'+str(i))
        self.cb.addItems(cbItems)
        
        self.lieCount = len(self.data[0])
        self.hangCount = len(self.data)//self.lineNumber
        self.setColumnCount(self.lieCount+1)
        self.setRowCount(self.hangCount+1)
        
        self.horizontalHeader().setVisible(0)
        self.verticalHeader().setVisible(0)
        
        for i in range(1, self.lieCount+1):
            self.setItem(0, i, QTableWidgetItem(headTitle[i]))
        self.item(0,self.xcol).setFlags(Qt.NoItemFlags)
        self.item(0,self.ycol).setFlags(Qt.NoItemFlags)
        for i in range(1, self.hangCount+1):
            self.setItem(i, 0, QTableWidgetItem(str(i)))
            self.item(i, 0).setFlags(Qt.NoItemFlags)
        
        self.setCellWidget(0, 0, self.cb)
        
        for i in range(1, self.hangCount+1):
            for j in range(1, self.lieCount+1):
                self.setItem(i, j, QTableWidgetItem(str(self.data[i-1][j-1])))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);
        
        self.rightKeyMenu = QMenu()
        self.actionCopy = QAction("Copy",self)
        self.actionCopy.setShortcut("Ctrl+C")
        self.actionCut = QAction("Cut",self)
        self.actionCut.setShortcut("Ctrl+X")
        self.actionDelete = QAction("Delete",self)
        self.actionDelete.setShortcut(QKeySequence.Delete)
        self.actionPaste = QAction("Paste",self)
        self.actionPaste.setShortcut("Ctrl+V")
        
        self.page = 0
        
        self.cb.currentIndexChanged.connect(self.lineChanged)
        
        self.actionCopy.triggered.connect(self.onActionCopy)
        self.actionCut.triggered.connect(self.onActionCut)
        self.actionDelete.triggered.connect(self.onActionDelete)
        self.actionPaste.triggered.connect(self.onActionPaste)
   
    def lineChanged(self):
        position = self.father.tab.currentIndex()
        tableWidget = self.father.tab.widget(position).activeSubWindow().widget()
        index = self.father.tab.widget(position).activeSubWindow().windowTitle()
        
        for i in range(1, self.hangCount+1):
                for j in range(1, self.lieCount+1):
                    self.data[self.page*self.hangCount+i-1][j-1] = self.item(i, j).text()
        lineNo = self.cb.currentIndex()
        
        self.page = lineNo
        for i in range(1, self.hangCount+1):
            for j in range(1, self.lieCount+1):
                self.setItem(i, j, QTableWidgetItem(str(self.data[lineNo*self.hangCount+i-1][j-1])))
        
        root = self.father.tree.topLevelItem(position-1)
        
        mdiarea = self.father.tab.currentWidget()
        
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
   
    def onActionCopy(self):
        stringCopy=""
        selectList = self.selectedItems()
        for i in range(0, len(selectList)-1):
            stringCopy = stringCopy + selectList[i].text() +","
        stringCopy += selectList[len(selectList)-1].text()
        board = QApplication.clipboard()
        board.setText(stringCopy)
        
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
        
    def onActionDelete(self):
        selectList = self.selectedItems()
        for i in range(0, len(selectList)):
            selectList[i].setText("")
        
    def onActionPaste(self):
        board = QApplication.clipboard()
        stringPaste = board.text()
        selectList = self.selectedItems()
        stringPasteList = stringPaste.split(',')
        for i in range (0, min(len(stringPasteList), len(selectList))):
            selectList[i].setText(stringPasteList[i])
            
    def contextMenuEvent(self, event):
        self.rightKeyMenu.clear
        point = event.pos()
        item = self.itemAt(point)
        if item != None:
            self.rightKeyMenu.addAction(self.actionCopy)
            self.rightKeyMenu.addAction(self.actionCut)
            self.rightKeyMenu.addAction(self.actionDelete)
            self.rightKeyMenu.addAction(self.actionPaste)
            self.rightKeyMenu.addSeparator()
            self.rightKeyMenu.exec(QCursor.pos())
            event.accept()
        
    def chooseAllColumn(self, row, column):
        if row == 0 and column !=0:
            for i in range(self.hangCount, 0, -1):
                self.item(i, column).setSelected(1)
            self.item(0, column).setSelected(0)        
