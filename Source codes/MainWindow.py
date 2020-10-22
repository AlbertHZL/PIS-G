'''
该程序为在毛天笑学长的框架基础上进行一些功能的添加及一些细节的修改
编译环境如下:
window10 + python3.6 +eric6-19.10
Pyqt5--5.13.2      xlrd--1.2.0        xlwt--1.3.0       xlutils--2.0.0
matplotlib--3.1.2       numpy--1.17.4       pyqt5-tools--5.13.0.1.5     
CUDA--10.2.89       CUDA Driver(Windows)>=441.22    CUDA Driver(Linux)>=440.33
2020.1.14 wjk
'''
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Dialog import Dialog
from DialogGrid import DialogGrid
from TreeWidget import TreeWidget
from ModelWidget import ModelWidget
from TableWidget import TableWidget
from MatplotlibWidget import MatplotlibWidget
from InversionSection import InversionSection
from Matplotlib3DWidget import Matplotlib3DWidget
from ThreeViewsWidget import ThreeViewsWidget
# import xlrd
import xlwt
import json
import os
# from xlutils.copy import copy
from DialogClose import DialogClose
from DialogAlgorithm import DialogAlgorithm
from Dialog3D import Dialog3D
from DialogInversionRange import DialogInversionRange
from DialogSetXY import DialogSetXY
from DialogNewPro import DialogNewPro
from Wizard import Wizard
from ModelWizard import ModelWizard

class MainWindow(QMainWindow):    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  
        self.setWindowTitle("PIS-G")
        self.setWindowIcon(QIcon(".\\image\\logo.png"))
        #加入菜单栏(文件&绘图)
        bar = self.menuBar()
        file = bar.addMenu("&File(F)")
        newProject_Action = QAction("New project",  self)
        newFile = QAction("Open File Data", self)
        Load_project = QAction("Load project",  self)
        Save_project = QAction("Save project",  self)
        Close_project = QAction("Close project",  self)
        Quit_Action = QAction("Exit",  self)
        
        newProject_Action.setShortcut("Ctrl+N")
        newFile.setShortcut("Ctrl+O")
        Save_project.setShortcut("Ctrl+S")

        file.addAction(newProject_Action)
        file.addAction(newFile)
        file.addAction(Load_project)
        file.addAction(Save_project)
        file.addAction(Close_project)
        file.addAction(Quit_Action)
        paint = bar.addMenu("&Paint(P)")
        sectionPaint = QAction( "Profile", self)
        gridPaint = QAction("Grid", self)
        D3Paint = QAction("3D", self)
        paint.addAction(sectionPaint)
        paint.addAction(gridPaint)
        paint.addAction(D3Paint)
        
        model = bar.addMenu("&Forwarding(F)")
        newModel = QAction("Forwarding", self)
        paintModel = QAction("Painting", self)
        saveModel = QAction("Save Result", self)
        model.addAction(newModel)
        model.addAction(paintModel)
        model.addAction(saveModel)
        
        inversion = bar.addMenu("&Inversion(I)")
        inversion_1 = QMenu("Parallel 3D Inversion", self)
        newInversion = QAction("Calculation", self)
        paintInversion = QAction("Painting", self)
        saveInversion = QAction("Save Result", self)
        
        inversion_1.addAction(newInversion) 
        inversion_1.addAction(paintInversion)
        inversion_1.addAction(saveInversion)
        inversion.addMenu(inversion_1)
        
        setxy = bar.addMenu("&Coordinate(C)")
        setxyAction = QAction("Set X&&Y", self)
        setxy.addAction(setxyAction)
        #记录树的结点的类型，保存工程用
        self.tree_record = {}
        #停靠窗口(加入树)
        self.dockWidget = QDockWidget(self)
        w = QWidget()
        self.dockWidget.setTitleBarWidget(w)
        self.dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        #文件树
        self.tree = TreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(['File List'])
        self.tree.setColumnWidth(0, 300)
        self.dockWidget.setWidget(self.tree)#将文件树加入到停靠窗口
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)#将停靠窗口加入到主窗口
        self.tab = QTabWidget()#主标签页
        #标签开始页面
        self.start = QWidget(self)
        
        label = QLabel(self.start)
        #label.setText("<p><font size=100 face=verdana color=red>Welcome !</font></p><br><h1><font size=100 face=verdana>重力梯度数据三维物性反演软件</font></h1>")#开始页面的欢迎语，需要再添加，或者再加图片
        label.setText("<p><font size=100 face=verdana color=red style=font-weight:bold>Welcome !</font></p><br><h1><font size=100 face=verdana>Parallel Inversion Software of Gravity gradiometry data</font></h1>")#开始页面的欢迎语，需要再添加，或者再加图片
        layout1 = QHBoxLayout()
        layout1.addStretch()
        layout1.addWidget(label)
        layout1.addStretch()
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addLayout(layout1)
        layout.addStretch()
        label.setAlignment(Qt.AlignCenter)
        self.start.setLayout(layout)

        self.tab.addTab(self.start, "start")
        self.setCentralWidget(self.tab)
        #记录用
        #self.tableWidget 记录当前选定的 tableWidget 页面
        self.widg = {}
        self.tableWidget = QTabWidget()
        self.index = ""
        #状态栏提示语
        self.status = self.statusBar()
        #初始最大化显示
        self.showMaximized()
        
        #打开文件数据
        self.paintCount = [] #tree_record记录每个工程的子项用, 避免命名重复
        
        #设置信号槽
        newProject_Action.triggered.connect(self.newpro)#新建工程
        newFile.triggered.connect(self.openfile)#打开文件数据
        Load_project.triggered.connect(self.openPr)#打开工程
        Save_project.triggered.connect(self.savePr)#保存工程
        Close_project.triggered.connect(self.closeOp)#关闭工程
        Quit_Action.triggered.connect(self.quitOp)#退出
        
        sectionPaint.triggered.connect(self.sectionOp)#剖面图
        gridPaint.triggered.connect(self.gridOp)#网格图
        D3Paint.triggered.connect(self.D3Op)#3D图
        
        newModel.triggered.connect(self.buildModel)#建模
        paintModel.triggered.connect(self.paintModel)#绘制
        saveModel.triggered.connect(self.forwardingSave)#保存数据
        
        newInversion.triggered.connect(self.inversion)#反演计算  聚焦反演
        paintInversion.triggered.connect(self.inversionPainting)#反演绘制
        saveInversion.triggered.connect(self.inversionSave)#反演结果保存
        setxyAction.triggered.connect(self.setXY)
        self.tree.clicked.connect(self.onTreeClicked)#点击树
        self.tab.currentChanged.connect(self.onCurrentChanged)#点击Tab标签

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Tips',"Are you sure you want to quit the program?",
                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件
        if reply == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
    
    def getTableWidget(self,  position, index):
        for SubWidget in self.tab.widget(position).subWindowList():
            if SubWidget.windowTitle() == index:
                return SubWidget.widget()
        return 0
    
    def checkDataPage(self, position):
        root = self.tree.topLevelItem(position-1).text(0)
        try:
            child = self.tab.widget(position).activeSubWindow().windowTitle()
            self.index = child
        except:
            return 0
        if child in self.tree_record[root]:
            if self.tree_record[root][child]['type'] != 'FileData' and self.tree_record[root][child]['type'] != 'ForwardingData':
                return 0
        else:
            return 0
        return 1
    
    def newpro(self):
        n = DialogNewPro(self)
        n.show()
        
    def quitOp(self):
        self.close()
        return 
    
    def openfile(self):
        position = self.tab.currentIndex()
        if position ==0 :
            QMessageBox.information(self, "Attention", "Please choose project page")
            return
        wizard = Wizard(self)
        wizard.show()
    
    def openPr(self): # 读档
        filePath = QFileDialog.getOpenFileName(self, 'Choose File', './', '*.json')
        if filePath[0] == "":return
        #判断文件是否存在
        if os.path.isfile(filePath[0]) == False :
            QMessageBox.information(self, "Attention", "Json does not exist")
            return
        #先复原工程及页面，再复原每个子项
        #复原工程时会关闭现有的所有工程
        #清空tab页, 除了start页面
        self.tab.clear()
        self.tab.addTab(self.start, "start")
        self.setCentralWidget(self.tab)
        #清空记录数组及左边树
        self.tree.clear()
        self.widg.clear()
        self.tree_record.clear()
        self.paintCount.clear()
        #导入json文件数据，先不考虑数据损坏的情况
        with open(filePath[0], 'r', encoding = 'utf-8') as json_file:
            jsObj = json.load(json_file)
            #将存档中的tree和table读进来
            for i in jsObj['TableWidget']:
                self.widg[i] = jsObj['TableWidget'][i]
            for i in jsObj['TreeWidget']:
                self.tree_record[i] = jsObj['TreeWidget'][i]
        self.paintCount = self.widg['paintCount']
        #构建左边树的根项目及 tab 页 , widg 和 tree_record 共享字典名称
        position = 1
        for key, value in self.tree_record.items():
            # 导入工程
            root = QTreeWidgetItem(self.tree)
            #设置项目名称
            root.setText(0, key)
            mid = QMdiArea()
            self.tab.addTab(mid, key)
            self.tab.setCurrentWidget(mid)
            count = 0
            #添加具体子窗口
            # key1 就是 title
            for key1, value1 in self.tree_record[key].items():
                # 数据页
                if self.tree_record[key][key1]['type']=='FileData' or self.tree_record[key][key1]['type']=='ForwardingData':
                    # 子节点
                    child = QTreeWidgetItem(root)
                    child.setText(0, key1)
                    # 导入数据
                    data = []
                    for list_x in range(0,  len(self.widg[key][key1]['data'])):
                        tempx = []
                        for list_y in range(0,  len(self.widg[key][key1]['data'][0])):
                            tempx.append(float(self.widg[key][key1]['data'][list_x][list_y]))
                        data.append(tempx)
                    headTitle = self.widg[key][key1]['Head_Title']
                    xcol = int(self.widg[key][key1]['xcol'])
                    ycol = int(self.widg[key][key1]['ycol'])
                    tableWidget = TableWidget(self, data, headTitle, xcol, ycol)
                    #导入 tableWidget 的所有数据
                    #lz, kmax
                    #z_obs, dz, zmax, m_min, m_max, epsilon, miu, sigma,wn
                    #Max_GPU_Number, nThreadPerBlock
                    tableWidget.data = data
                    tableWidget.forwardingInformation = self.widg[key][key1]['forwardingInformation']
                    tableWidget.bottom = float(self.widg[key][key1]['bottom'])
                    tableWidget.top = float(self.widg[key][key1]['top'])
                    tableWidget.inversionFlag= self.widg[key][key1]['inversionFlag']
                    tableWidget.kmax = int(self.widg[key][key1]['kmax'])
                    tableWidget.Max_GPU_Number = int(self.widg[key][key1]['Max_GPU_Number'])
                    tableWidget.nThreadPerBlock = int(self.widg[key][key1]['nThreadPerBlock'])
                    tableWidget.lz = int(self.widg[key][key1]['lz'])
                    tableWidget.m_min = float(self.widg[key][key1]['m_min'])
                    tableWidget.m_max = float(self.widg[key][key1]['m_max'])
                    tableWidget.z_obs = float(self.widg[key][key1]['z_obs'])
                    tableWidget.zmax = float(self.widg[key][key1]['zmax'])
                    tableWidget.dz = float(self.widg[key][key1]['dz'])
                    tableWidget.epsilon = float(self.widg[key][key1]['epsilon'])
                    tableWidget.miu = float(self.widg[key][key1]['miu'])
                    tableWidget.sigma = float(self.widg[key][key1]['sigma'])
                    tableWidget.wn = float(self.widg[key][key1]['wn'])
                    
                    tableWidget.model_count = int(self.widg[key][key1]['model_count'])
                    tableWidget.point_count = int(self.widg[key][key1]['point_count'])
                    tableWidget.dx = float(self.widg[key][key1]['dx'])
                    tableWidget.dy = float(self.widg[key][key1]['dy'])
                    tableWidget.nx = int(self.widg[key][key1]['nx'])
                    tableWidget.ny = int(self.widg[key][key1]['ny'])
                    tableWidget.nz = int(self.widg[key][key1]['nz'])
                    #添加储存的数组数据
                    tableWidget.mx = self.widg[key][key1]['mx']
                    tableWidget.my = self.widg[key][key1]['my']
                    tableWidget.mz = self.widg[key][key1]['mz']
                    tableWidget.Vzz = self.widg[key][key1]['Vzz']
                    tableWidget.m_result = self.widg[key][key1]['m_result']
                    tableWidget.thick = self.widg[key][key1]['thick']
                    tableWidget.zc = self.widg[key][key1]['zc']
                    
                    for i in range(0, len(tableWidget.data)):
                        tableWidget.x.append(float(tableWidget.data[i][tableWidget.xcol-1]))
                        tableWidget.y.append(float(tableWidget.data[i][tableWidget.ycol-1]))
                    # 上方 tab 页
                    sub1 = QMdiSubWindow()
                    sub1.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub1.setWidget(tableWidget)
                    sub1.resize(750, 750)
                    sub1.setWindowTitle(key1)
                    mid.addSubWindow(sub1)
                    mid.setActiveSubWindow(sub1)
                    sub1.show()
                    # 正演产生数据需要额外处理
                    if self.tree_record[key][key1]['type']=='ForwardingData':
                        zmax = 0
                        mwd = ModelWizard(self)
                        mw = ModelWidget(mwd)
                        mw.mpl.setTitle(mwd.title)
                        mwd.xlow = int(self.tree_record[key][key1]['xlow'])
                        mwd.xhigh = int(self.tree_record[key][key1]['xhigh'])
                        mwd.xdistance = int(self.tree_record[key][key1]['xdistance'])
                        mwd.ylow = int(self.tree_record[key][key1]['ylow'])
                        mwd.yhigh = int(self.tree_record[key][key1]['yhigh'])
                        mwd.ydistance = int(self.tree_record[key][key1]['ydistance'])
                        mwd.colorbarTitle.append(self.tree_record[key][key1]['ColorBar_Title'])
                        mwd.mwTitle = self.tree_record[key][key1]['Model_Title']
                        mw.mpl.setTitle(mwd.mwTitle)
                        mw.mpl.setColorbar(mwd.colorbarTitle[0])
                        densityData = []
                        mwd.data = []
                        Forwarding_number = int(self.tree_record[key][key1]['Number_of_Model'])
                        for i in range(0, Forwarding_number):
                            Forwarding_tempname = 'Number_'+str(i+1)
                            aa = []
                            for j in range(0, 5):
                                aa.append(self.tree_record[key][key1][Forwarding_tempname][str(j)])
                            mwd.data.append(aa)
                        # density 数据
                        for i in range(0, len(mwd.data)):
                            if mwd.data[i][0]=="Cube":
                                density = float(mwd.data[i][4])#密度
                                densityData.append(density)
                        mwd.densityMin = min(densityData)
                        mwd.densityMax = max(densityData)
                        if mwd.densityMax==mwd.densityMin:    mwd.densityMax+=1
                        mw.mpl.setRange(mwd.densityMin, mwd.densityMax)
                        for i in range(0, len(mwd.data)):
                            if mwd.data[i][0]=="Cube": 
                                xlim = mwd.data[i][1].split(',')
                                if len(xlim)==1:
                                    xlim = mwd.data[i][1].split('，')
                                ylim = mwd.data[i][2].split(',')
                                if len(ylim)==1:
                                    ylim = mwd.data[i][2].split('，')
                                zlim = mwd.data[i][3].split(',')
                                if len(zlim)==1:
                                    zlim = mwd.data[i][3].split('，')
                                density = float(mwd.data[i][4])#密度
                                if zmax < float(zlim[1]):
                                    k = int(float(zlim[1])/1000)
                                    yu = float(zlim[1])-k*1000
                                    if yu > 0:
                                        zmax = (k+1)*1000
                                    else:
                                        zmax = k*1000
                                mw.mpl.paintCube(xlim, ylim, zlim, density, mwd.xlow-mwd.xdistance/2, mwd.xhigh+mwd.xdistance/2, mwd.ylow-mwd.ydistance/2, mwd.yhigh+mwd.ydistance/2, zmax, 1, 1)
                        mwd.zmax = zmax
                        mw.mpl.setColorbar(mwd.colorbarTitle)
                        #添加右键事件
                        frontView = QAction("X-Z Profile", mwd)
                        sideView = QAction("Y-Z Profile", mwd)
                        downView = QAction("X-Y Profile", mwd)
                        mw.mpl.menu.addAction(frontView)
                        mw.mpl.menu.addAction(sideView)
                        mw.mpl.menu.addAction(downView)
                        frontView.triggered.connect(lambda:mwd.dialog(1, key1))
                        sideView.triggered.connect(lambda:mwd.dialog(2, key1))
                        downView.triggered.connect(lambda:mwd.dialog(3, key1))
                        self.tree_record[key][key1]['ForwardingModel'] = mw
                    
                elif self.tree_record[key][key1]['type'] == 'Paint_Section':
                    index = self.tree_record[key][key1]['index']
                    tableWidget = self.getTableWidget(position,  index)
                    if tableWidget ==0 : continue
                    mw = MatplotlibWidget()
                    fileName = self.tree_record[key][key1]['paint_name']
                    finalName = self.tree_record[key][key1]['tree_name']
                    x = []
                    y = []
                    xunit = self.tree_record[key][key1]['X_axis_unit']
                    vunit = self.tree_record[key][key1]['V_axis_unit']
                    flag = self.tree_record[key][key1]['Show_Symbol']
                    xposition=tableWidget.xcol
                    for i in range(0,len(headTitle)):
                        if headTitle[i]=="X" or headTitle[i]=="Y" or headTitle[i]=="x" or headTitle[i]=="y":continue
                        for t in range(0, len(fileName)):
                            if fileName[t] == headTitle[i]:
                                for j in range(0, tableWidget.hangCount):
                                    y.append(tableWidget.data[j][i-1])
                                break
                    for i in range (0, tableWidget.hangCount):
                        x.append(tableWidget.data[i][xposition-1])
                    if xunit == 'km':
                        x = [i / 1000 for i in x]
                    # 1 表示当前显示 Line 1 的测线
                    mw.mpl.section(1, fileName, x, y, xunit, vunit, flag)
                    #添加子窗口
                    sub = QMdiSubWindow()
                    sub.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub.setWidget(mw)
                    sub.setWindowTitle(finalName)
                    self.tab.widget(position).addSubWindow(sub)
                    self.tab.widget(position).setActiveSubWindow(sub)
                    sub.show()
                    #添加子树
                    newItem = QTreeWidgetItem(root)
                    newItem.setText(0, finalName)
                elif self.tree_record[key][key1]['type'] == 'Paint_Gird':
                    index = self.tree_record[key][key1]['index']
                    tableWidget = self.getTableWidget(position,  index)
                    if tableWidget ==0 : continue
                    xposition=tableWidget.xcol
                    yposition=tableWidget.ycol
                    vposition =int(self.tree_record[key][key1]['Choose'])
                    x=[]
                    y=[]
                    z=[]
                    for j in range(0,  len(tableWidget.data)):
                        z.append(float(tableWidget.data[j][vposition-1]))
                        if float(tableWidget.data[j][yposition-1]) not in y:    y.append(float(tableWidget.data[j][yposition-1]))
                        if float(tableWidget.data[j][xposition-1]) not in x:    x.append(float(tableWidget.data[j][xposition-1]))
                    fileName = self.tree_record[key][key1]['paint_name']
                    finalName = self.tree_record[key][key1]['tree_name']
                    xunit = self.tree_record[key][key1]['X_axis_unit']
                    yunit = self.tree_record[key][key1]['Y_axis_unit']
                    colorbarTitle = self.tree_record[key][key1]['color_Bar_Title']
                    flag1 = int(self.tree_record[key][key1]['Show_Isoline'])
                    flag2 = int(self.tree_record[key][key1]['Show_Value'])
                    if xunit == 'km':
                        x = [i / 1000 for i in x]
                    if yunit == 'km':
                        y = [i / 1000 for i in y]
                    mw = MatplotlibWidget()
                    mw.mpl.gridPaint(fileName, x, y, z, xunit, yunit, colorbarTitle, flag1, flag2)
                    #设置子窗口
                    sub = QMdiSubWindow()
                    sub.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub.setWidget(mw)
                    sub.setWindowTitle(finalName)
                    mid.addSubWindow(sub)
                    sub.show()
                    #添加子树
                    newItem = QTreeWidgetItem(root)
                    newItem.setText(0, finalName)
                elif self.tree_record[key][key1]['type'] == 'Paint_3D':
                    index = self.tree_record[key][key1]['index']
                    tableWidget = self.getTableWidget(position,  index)
                    if tableWidget ==0 : continue
                    xposition=tableWidget.xcol
                    yposition=tableWidget.ycol
                    vposition =int(self.tree_record[key][key1]['Choose'])
                    x=[]
                    y=[]
                    z=[]
                    for j in range(0,  len(tableWidget.data)):
                        z.append(float(tableWidget.data[j][vposition-1]))
                        if float(tableWidget.data[j][yposition-1]) not in y:    y.append(float(tableWidget.data[j][yposition-1]))
                        if float(tableWidget.data[j][xposition-1]) not in x:    x.append(float(tableWidget.data[j][xposition-1]))
                    fileName = self.tree_record[key][key1]['paint_name']
                    finalName = self.tree_record[key][key1]['tree_name']
                    xunit = self.tree_record[key][key1]['X_axis_unit']
                    yunit = self.tree_record[key][key1]['Y_axis_unit']
                    zunit = self.tree_record[key][key1]['Z_axis_unit']
                    colorbarTitle = self.tree_record[key][key1]['color_Bar_Title']
                    if xunit == 'km':
                        x = [i / 1000 for i in x]
                    if yunit == 'km':
                        y = [i / 1000 for i in y]
                    mw = Matplotlib3DWidget()
                    mw.mpl.D3Paint(fileName, x, y, z, xunit, yunit, zunit, colorbarTitle)
                    #设置子窗口
                    sub = QMdiSubWindow()
                    sub.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub.setWidget(mw)
                    sub.setWindowTitle(finalName)
                    mid.addSubWindow(sub)
                    sub.show()
                    #添加子树
                    newItem = QTreeWidgetItem(root)
                    newItem.setText(0, finalName)
                elif self.tree_record[key][key1]['type'] == 'Forwarding_Painting':
                    index = self.tree_record[key][key1]['index']
                    mw = ModelWidget()
                    mw = self.tree_record[key][index]['ForwardingModel']
                    sub2 = QMdiSubWindow()
                    sub2.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub2.setWidget(mw)
                    sub2.setWindowTitle(index + "3D Model")
                    mid.addSubWindow(sub2)
                    sub2.show()
                    child3 = QTreeWidgetItem(root)
                    child3.setText(0, index + "3D Model")
                elif self.tree_record[key][key1]['type'] == 'Forwarding_Paintint_XZ' or \
                self.tree_record[key][key1]['type'] == 'Forwarding_Paintint_XY' or \
                self.tree_record[key][key1]['type'] == 'Forwarding_Paintint_YZ':
                    title = self.tree_record[key][key1]['title']
                    colorbarTitle = self.tree_record[key][key1]['color_Bar_Title']
                    index = self.tree_record[key][key1]['index']
                    densityMin = self.tree_record[key][index]['densityMin']
                    densityMax = self.tree_record[key][index]['densityMax']
                    tvw = ThreeViewsWidget()
                    tvw.mpl.setTitle(title)
                    tvw.mpl.setRange(densityMin, densityMax)
                    xlow = int(self.tree_record[key][index]['xlow'])
                    xhigh = int(self.tree_record[key][index]['xhigh'])
                    dx = int(self.tree_record[key][index]['xdistance'])
                    ylow = int(self.tree_record[key][index]['ylow'])
                    yhigh = int(self.tree_record[key][index]['yhigh'])
                    dy = int(self.tree_record[key][index]['ydistance'])
                    densityData = []
                    data = []
                    Forwarding_number = int(self.tree_record[key][index]['Number_of_Model'])
                    for i in range(0, Forwarding_number):
                        Forwarding_tempname = 'Number_'+str(i+1)
                        aa = []
                        for j in range(0, 5):
                            aa.append(self.tree_record[key][index][Forwarding_tempname][str(j)])
                        data.append(aa)
                    for i in range(0, len(data)):
                        if data[i][0]=="Cube":
                            xlim = data[i][1].split(',')
                            if len(xlim)==1:
                                xlim = data[i][1].split('，')
                            ylim = data[i][2].split(',')
                            if len(ylim)==1:
                                ylim = data[i][2].split('，')
                            zlim = data[i][3].split(',')
                            if len(zlim)==1:
                                zlim = data[i][3].split('，')
                            density = float(data[i][4])
                            if self.tree_record[key][key1]['type'] == 'Forwarding_Paintint_XZ':
                                tvw.mpl.cubeFront(xlim, ylim, zlim, xlow-dx/2, xhigh+dx/2, 0, zmax, density)
                            elif self.tree_record[key][key1]['type'] == 'Forwarding_Paintint_XY':
                                tvw.mpl.cubeSide(xlim, ylim, zlim, ylow-dy/2, yhigh+dy/2, 0, zmax, density)
                            else:
                                tvw.mpl.cubeDown(xlim, ylim, zlim, xlow-dx/2, xhigh+dx/2, ylow-dy/2, yhigh+dy/2, density)
                    tvw.mpl.setColorbar(colorbarTitle)
                    #加子窗口
                    sub3 = QMdiSubWindow()
                    sub3.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub3.setWidget(tvw)
                    sub3.setWindowTitle(title)
                    mid.addSubWindow(sub3)
                    sub3.show()
                    child3 = QTreeWidgetItem(root)
                    child3.setText(0, title)
                elif self.tree_record[key][key1]['type'] == 'Inversion_Paint_parallel':
                    index = self.tree_record[key][key1]['index']
                    tableWidget = self.getTableWidget(position,  index)
                    if tableWidget ==0 : continue
                    flag = 0
                    m_result = tableWidget.m_result
                    zmax1 = tableWidget.zmax
                    DIR = DialogInversionRange(self, tableWidget, flag,  index)
                    bottom = float(self.tree_record[key][key1]['bottom'])
                    top = float(self.tree_record[key][key1]['top'])
                    mwTitle = self.tree_record[key][key1]['title']
                    mwColorBarTitle = self.tree_record[key][key1]['color_Bar_Title']
                    xx = self.tree_record[key][key1]['xx']
                    yy = self.tree_record[key][key1]['yy']
                    mw = ModelWidget(self)
                    mw.mpl.setTitle(mwTitle)
                    minList = []
                    maxList = []
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
                                if m_result[i][j][k] >= bottom and m_result[i][j][k]<=top:
                                    pointPosition = i*tableWidget.nx*tableWidget.ny  + j*tableWidget.nx + k
                                    xlim = [tableWidget.mx[pointPosition]/xx, tableWidget.mx[pointPosition+tableWidget.model_count]/xx]
                                    ylim = [tableWidget.my[pointPosition]/yy, tableWidget.my[pointPosition+tableWidget.model_count]/yy]
                                    zlim = [tableWidget.mz[pointPosition], tableWidget.mz[pointPosition+tableWidget.model_count]]
                                    density = m_result[i][j][k]
                                    xdown = tableWidget.mx[0]/xx
                                    xup = tableWidget.mx[tableWidget.model_count-1]/xx
                                    ydown = tableWidget.my[0]/yy
                                    yup = tableWidget.my[tableWidget.model_count-1]/yy
                                    mw.mpl.paintCube(xlim, ylim, zlim,density, xdown, xup, ydown, yup, zmax, xx, yy)
                    mw.mpl.setColorbar(mwColorBarTitle)
                    #添加右键动作
                    xy = QAction("X-Y Profile", DIR)
                    xz = QAction("X-Z Profile", DIR)
                    yz = QAction("Y-Z Profile", DIR)
                    mw.mpl.menu.addAction(xy)
                    mw.mpl.menu.addAction(xz)
                    mw.mpl.menu.addAction(yz)
                    xy.triggered.connect(lambda:DIR.xy(tableWidget), flag)
                    xz.triggered.connect(lambda:DIR.xz(tableWidget), flag)
                    yz.triggered.connect(lambda:DIR.yz(tableWidget), flag)
                    #加子窗口
                    sub = QMdiSubWindow()
                    sub.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub.setWidget(mw)
                    sub.setWindowTitle(mwTitle)
                    mid=self.tab.currentWidget()
                    mid.addSubWindow(sub)
                    sub.show()
                    #树
                    child3 = QTreeWidgetItem(root)
                    child3.setText(0, mwTitle)
                    
                else :
                    index = self.tree_record[key][key1]['index']
                    depth =float(self.tree_record[key][key1]['depth'])
                    inversionTitle = self.tree_record[key][key1]['title']
                    inversionColorbarTitle = self.tree_record[key][key1]['color_Bar_Title']
                    xx = int(self.tree_record[key][key1]['xx'])
                    yy = int(self.tree_record[key][key1]['yy'])
                    
                    tableWidget = self.getTableWidget(position,  index)
                    if tableWidget ==0 : continue
                    m_result = []
                    x = []
                    zmax1 = 0
                    id = int(self.tree_record[key][key1]['id'])
                    z = []
                    x1 = tableWidget.x[0]/xx
                    x2 = tableWidget.x[-1]/xx
                    y1 = tableWidget.y[0]/yy
                    y2 = tableWidget.y[-1]/yy
                    dx = tableWidget.dx/xx
                    dy = tableWidget.dy/yy
                    dz = 0.0
                    z1 = tableWidget.zc[0]
                    z2 = tableWidget.zc[-1]
                    y = []
                    
                    inversionSection = InversionSection()
                    inversionSection.mpl.setTitle(inversionTitle)
                    if self.tree_record[key][key1]['type'] == 'Inversion_Paint_parallel_XY':
                        z = tableWidget.m_result[id]
                        dz = tableWidget.dz
                        inversionSection.mpl.xy_section(x1, x2, y1, y2, z, dx, dy, dz, depth, inversionColorbarTitle, xx, yy)
                    elif self.tree_record[key][key1]['type'] == 'Inversion_Paint_parallel_XZ':
                        z = tableWidget.m_result[id]
                        dz = tableWidget.dz
                        for i in range(0, tableWidget.nz):
                            temp = []
                            for j in range(0, tableWidget.nx):temp.append(tableWidget.m_result[i][id][j])
                            y.append(temp)
                        inversionSection.mpl.xz_section(x1, x2, z1, z2, y, dx, dy, dz, depth, inversionColorbarTitle, xx)
                    else:
                        z = tableWidget.m_result[id]
                        dz = tableWidget.dz
                        for i in range(0, tableWidget.nz):
                            temp = []
                            for j in range(0, tableWidget.ny):
                                temp.append(tableWidget.m_result[i][j][id])
                            x.append(temp)
                        inversionSection.mpl.yz_section(y1, y2, z1, z2, x, dx, dy, dz, depth, inversionColorbarTitle, yy)
                    #加子窗口
                    sub = QMdiSubWindow()
                    sub.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub.setWidget(inversionSection)
                    sub.setWindowTitle(inversionTitle)
                    mid.addSubWindow(sub)
                    sub.show()
                    child3 = QTreeWidgetItem(root)
                    child3.setText(0, inversionTitle)
                self.tree.topLevelItem(position-1).child(count).setSelected(1)
                count += 1
            root.setExpanded(1)
            position = position+1
        return
    def savePr(self):   #存档
        if self.tab.count()==0:
            QMessageBox.information(self, "Attention", "No data to save")
            return
        filePath = QFileDialog.getSaveFileName(self, 'Open File', './', '*.json')
        if filePath[0] == "":
            return
        #记录每个tablewidget的所有值
        sum_i = 1
        self.widg.clear()
        if os.path.isfile(filePath[0]) == True: 
            f=open(filePath[0], "r+")
            f.truncate()
            f.close()
        self.widg['paintCount'] = self.paintCount
        for key, value in self.tree_record.items():
            for key1, value1 in self.tree_record[key].items():
                if self.tree_record[key][key1]['type'] == 'ForwardingData':
                    self.tree_record[key][key1]['ForwardingModel'] = 0
        while sum_i <= self.tree.topLevelItemCount():
            #没有子项的话这一项不用记录
            if self.tree.topLevelItem(sum_i-1).childCount() ==0:
                continue
            root = self.tree.topLevelItem(sum_i-1).text(0)
            sum_j = 0
            self.widg[root] = {}
            for key,  value in self.tree_record[root].items():
                # 判断是否为数据页
                if self.tree_record[root][key]['type'] != 'FileData' and self.tree_record[root][key]['type'] != 'ForwardingData':
                    sum_j+=1
                    continue
                #是数据页的话可以进行记录
                #每一个table页要记录的数据
                #lz, kmax
                #z_obs, dz, zmax, m_min, m_max, epsilon, miu, sigma,wn
                #Max_GPU_Number, nThreadPerBlock
                tableWidget = self.tab.widget(sum_i).subWindowList()[sum_j].widget()
                name = self.tree.topLevelItem(sum_i-1).child(sum_j).text(0)
                self.widg[root][name] ={'lieCount': tableWidget.lieCount,'hangCount':len(tableWidget.data),'forwardingInformation': tableWidget.forwardingInformation, \
                'bottom':  tableWidget.bottom, 'top':tableWidget.top, 'inversionFlag':tableWidget.inversionFlag, \
                'kmax':tableWidget.kmax, 'Max_GPU_Number':tableWidget.Max_GPU_Number, 'nThreadPerBlock':tableWidget.nThreadPerBlock, \
                'epsilon':tableWidget.epsilon, 'sigma':tableWidget.sigma, 'lz':tableWidget.lz, \
                'm_min':tableWidget.m_min, 'm_max':tableWidget.m_max, 'z_obs':tableWidget.z_obs, \
                'dz':tableWidget.dz, 'zmax':tableWidget.zmax, 'miu':tableWidget.miu, 'wn':tableWidget.wn, \
                 'model_count':tableWidget.model_count, 'point_count':tableWidget.point_count, \
                'dx':tableWidget.dx, 'dy':tableWidget.dy, 'nx':tableWidget.nx, 'ny':tableWidget.ny, \
                'nz':tableWidget.nz,'Head_Title':tableWidget.Head_Title,'xcol':tableWidget.xcol, 'ycol':tableWidget.ycol, \
                'data':tableWidget.data, 'mx':tableWidget.mx, 'my':tableWidget.my, 'mz':tableWidget.mz, \
                'Vzz':tableWidget.Vzz, 'm_result':tableWidget.m_result, 'thick':tableWidget.thick,'zc':tableWidget.zc}
                sum_j+=1
            sum_i = sum_i+1
        #之后记录左边数的情况
        #保存tree_record即可
        # 导入tableWidget的数据
        name_emb = {'TableWidget':{}, 'TreeWidget':{}}
        for i in self.widg:
            name_emb['TableWidget'][i] = self.widg[i]
        for i in self.tree_record:
            name_emb['TreeWidget'][i] = self.tree_record[i]
        #数据导入到文件中
        jsObj = json.dumps(name_emb)
        with open(os.path.join('./', filePath[0]), "w", encoding= 'utf-8') as fw:
            fw.write(jsObj)
            fw.close()
        QMessageBox.information(self, "Attention", "Save Successfully")
        
    def setXY(self):
        position = self.tab.currentIndex()
        self.tableWidget = self.tab.widget(position).activeSubWindow().widget()
        if position==0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        if self.tree.topLevelItem(position-1).childCount() ==0:
            QMessageBox.information(self, "Attention", "No data page")
            return
        dialog = DialogSetXY(self)
        dialog.show()
    def sectionOp(self):
        position = self.tab.currentIndex()
        if position==0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        if self.tree.topLevelItem(position-1).childCount() ==0:
            QMessageBox.information(self, "Attention", "No data page")
            return
        if self.checkDataPage(position) == 0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Window")
            return
        self.tableWidget = self.tab.widget(position).activeSubWindow().widget()
        self.index = self.tab.widget(position).activeSubWindow().windowTitle()
        dialog = Dialog(self)
        dialog.exec()
        
    def gridOp(self):
        position = self.tab.currentIndex()
        if position==0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        if self.tree.topLevelItem(position-1).childCount() ==0:
            QMessageBox.information(self, "Attention", "No data page")
            return
        if self.checkDataPage(position) == 0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Window")
            return
        self.tableWidget = self.tab.widget(position).activeSubWindow().widget()
        self.index = self.tab.widget(position).activeSubWindow().windowTitle()
        #绘制网格图
        dialog = DialogGrid(self)
        dialog.exec()
        
    def onTreeClicked(self):
        item = self.tree.currentItem()
        #判断是不是顶级节点
        topCount = self.tree.topLevelItemCount()
        for i in range(0,  topCount):
            if self.tree.topLevelItem(i)==item:
                position = i+1
                self.tab.setCurrentIndex(position)
                if self.tree.topLevelItem(i).childCount()==0:
                    self.tree.topLevelItem(i).setSelected(1)
            if self.tree.topLevelItem(i)==item.parent():
                root = self.tree.topLevelItem(i)
                position = i
                #子目录坐标
                ind = root.indexOfChild(item)
                self.tab.setCurrentIndex(position+1)
                mdiarea = self.tab.widget(position+1)
                list = mdiarea.subWindowList()
                list[ind].showNormal()
                list[ind].widget().show()
                mdiarea.setActiveSubWindow(list[ind])
        
    def onCurrentChanged(self):
        position = self.tab.currentIndex()
        if position==0:
            return
        topCount = self.tree.topLevelItemCount()
        for i in range(0, topCount):
            if i == position-1:
                if self.tree.topLevelItem(i).childCount() >0:
                    self.tree.topLevelItem(i).setExpanded(1)
                    self.tree.topLevelItem(i).setSelected(0)
                    mdiarea = self.tab.currentWidget()
                    for j in range(0, self.tree.topLevelItem(i).childCount()):
                        self.tree.topLevelItem(i).child(j).setSelected(0)
                    list = mdiarea.subWindowList()
                    mdiarea.setActiveSubWindow(list[0])
                    self.tree.topLevelItem(i).child(0).setSelected(1)
                else :
                    self.tree.topLevelItem(i).setSelected(1)
            else:
                self.tree.topLevelItem(i).setExpanded(0)
                self.tree.topLevelItem(i).setSelected(0)
    def buildModel(self):
        position = self.tab.currentIndex()
        if position ==0 :
            QMessageBox.information(self, "Attention", "Please choose project page")
            return
        modelWizard = ModelWizard(self)
        modelWizard.show()
        return
    
    def paintModel(self):
        position = self.tab.currentIndex()
        if position == 0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        if self.tree.topLevelItem(position-1).childCount() ==0:
            QMessageBox.information(self, "Attention", "No data page")
            return
        root = self.tree.topLevelItem(position-1).text(0)
        try:
            index = self.tab.widget(position).activeSubWindow().windowTitle()
        except:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        
        root = self.tree.topLevelItem(position-1)
        root_name = root.text(0)
        if self.tree_record[root_name][index]['type'] != 'ForwardingData':
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        if self.tree_record[root_name][index]['ForwardingModelFlag'] ==1:
            QMessageBox.information(self, "Attention", "the picture existed")
            return
        
        mid = self.tab.widget(position)
        mw = ModelWidget()
        mw = self.tree_record[root_name][index]['ForwardingModel']
        sub2 = QMdiSubWindow()
        sub2.setWindowIcon(QIcon(".\\image\\logo.png"))
        sub2.setWidget(mw)
        sub2.setWindowTitle("3D Model")
        mid.addSubWindow(sub2)
        mid.setActiveSubWindow(sub2)
        sub2.show()
        #文件树条目
        selectedList = self.tree.selectedItems()
        for i in range(0, len(selectedList)):
            selectedList[i].setSelected(0)
        position = self.tab.currentIndex()
        child3 = QTreeWidgetItem(root)
        child3.setText(0, index + "3D Model")
        child3.setSelected(1)
        root.setExpanded(1)
        # 记录tree_record
        child_name = 'view_'+str(self.paintCount[position-1]) 
        self.tree_record[root_name][index]['ForwardingModelFlag'] = 1
        self.paintCount[position-1] += 1
        self.tree_record[root_name][child_name] = {'type': 'Forwarding_Painting', 'index':index}
        return
        
    def forwardingSave(self):
        position = self.tab.currentIndex()
        if position == 0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        if self.tree.topLevelItem(position-1).childCount() ==0:
            QMessageBox.information(self, "Attention", "No data page")
            return
        if self.checkDataPage(position) == 0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Window")
            return
        root = self.tree.topLevelItem(position-1)
        root_name = root.text(0)
        child = self.tab.widget(position).activeSubWindow().windowTitle()
        tableWidget = self.tab.widget(position).activeSubWindow().widget()
        if self.tree_record[root_name][child]['type'] == 'FileData':
            QMessageBox.information(self, "Attention", "Please Choose Correct Forwarding Page")
            return
        filePath = QFileDialog.getSaveFileName(self, 'Open File', './', '*.txt \n *.xls')
        suffixList = filePath[0].split('.')
        suffix = suffixList[-1]
        if suffix == "":  return
        if suffix=='txt':
            filename = open(filePath[0], 'w')
            for i in range(0, len(tableWidget.data)):
                for j in range(0, len(tableWidget.data[0])-1):
                    filename.write(str(tableWidget.data[i][j]))
                    filename.write(',')
                filename.write(str(tableWidget.data[i][len(tableWidget.data[0])-1]))
                filename.write('\n')
            filename.close()
            #保存参数
            parameterFilePath = suffixList[0]
            for i in range(1, len(suffixList)-1):
                parameterFilePath=parameterFilePath+'.'+suffixList[i]
            parameterFilePath+="-parameter.txt"
            filename1 = open(parameterFilePath, 'w')
            #存放参数及数据
            filename1.write(tableWidget.forwardingInformation)
            filename1.close()
        elif suffix=='xls':
            f = xlwt.Workbook()
            sheet1 = f.add_sheet('sheet1',cell_overwrite_ok=True)
            for i in range(0,len(tableWidget.data)):
                for j in range(0,len(tableWidget.data[0])):
                    sheet1.write(i, j, str(tableWidget.data[i][j]))
            f.save(filePath[0])
            #保存参数
            parameterFilePath = suffixList[0]
            for i in range(1, len(suffixList)-1):
                parameterFilePath=parameterFilePath+'.'+suffixList[i]
            parameterFilePath+="-parameter.txt"
            filename1 = open(parameterFilePath, 'w')
            #存放参数及数据
            filename1.write(tableWidget.forwardingInformation)
            filename1.close()            
        else:
            QMessageBox.information(self, "Attention", "Please Fill in the Correct Suffix Name.")
            return
        QMessageBox.information(self, "Congratulation", "File Saves Successfully")
    
    def closeOp(self):
        position = self.tab.currentIndex()
        if position==0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        dialogClose = DialogClose(self)
        dialogClose.show()
        return
        
    def D3Op(self):
        position = self.tab.currentIndex()
        if position==0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        if self.tree.topLevelItem(position-1).childCount() ==0:
            QMessageBox.information(self, "Attention", "No data page")
            return
        if self.checkDataPage(position) == 0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Window")
            return
        self.tableWidget = self.tab.widget(position).activeSubWindow().widget()
        self.index = self.tab.widget(position).activeSubWindow().windowTitle()
        dialog3D = Dialog3D(self)
        dialog3D.show()
        return
        
    def inversion(self):
        position = self.tab.currentIndex()
        if position==0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        if self.tree.topLevelItem(position-1).childCount() ==0:
            QMessageBox.information(self, "Attention", "No data page")
            return
        if self.checkDataPage(position) == 0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Window")
            return
        self.tableWidget = self.tab.widget(position).activeSubWindow().widget()
        self.index = self.tab.widget(position).activeSubWindow().windowTitle()
        #判断是否反演进行时
        if self.tableWidget.flag[0] == 1:
            QMessageBox.information(self, "Tips", "Calculation in progress")
            return 
        vzzPosition = 0
        for i in range(1, self.tableWidget.lieCount+1):
            if self.tableWidget.item(0, i).text()=="Vzz":
                vzzPosition = i
        if vzzPosition == 0:
            QMessageBox.information(self, "ATTENTION", "Vz Were Not Found")#未发现相关Vzz数据
            return
        dialog = DialogAlgorithm(self)
        dialog.show()
        return
    
    def inversionPainting(self):
        position = self.tab.currentIndex()
        try:
            index = self.tab.widget(position).activeSubWindow().windowTitle()
        except:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        if position == 0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        if self.tree.topLevelItem(position-1).childCount() ==0:
            QMessageBox.information(self, "Attention", "No data page")
            return
        if self.checkDataPage(position) == 0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Window")
            return
        self.tableWidget = self.tab.widget(position).activeSubWindow().widget()
        if self.tableWidget.inversionFlag == 0:
            QMessageBox.information(self, "Attention", "No Reweighted foucsing inversion Calculation")
            return
        #输入范围
        dialogInversionRange = DialogInversionRange(self, self.tableWidget, 0,  index)
        dialogInversionRange.show()
        return
    
    
    def inversionSave(self):
        position = self.tab.currentIndex()
        if position == 0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Page")
            return
        if self.tree.topLevelItem(position-1).childCount() ==0:
            QMessageBox.information(self, "Attention", "No data page")
            return
        if self.checkDataPage(position) == 0:
            QMessageBox.information(self, "Attention", "Please Choose Correct Window")
            return
        tableWidget = self.tab.widget(position).activeSubWindow().widget()
        if tableWidget.inversionFlag == 0:
            QMessageBox.information(self, "Attention", "No Reweighted foucsing Inversion Calculation")
            return
        filePath = QFileDialog.getSaveFileName(self, 'Open File', './', '*.txt \n *.xls')
        if filePath == "":
            return
        suffixList = filePath[0].split('.')
        suffix = suffixList[-1]
        if suffix=='txt':
            filename = open(filePath[0], 'w')
            for i in range(0, tableWidget.nz):
                for j in range(0, tableWidget.ny):
                    for k in range(0, tableWidget.nx):
                        filename.write(str(tableWidget.m_result[i][j][k]))
                        filename.write('\n')
            filename.close()
            #保存参数
            parameterFilePath = suffixList[0]
            for i in range(1, len(suffixList)-1):
                parameterFilePath=parameterFilePath+'.'+suffixList[i]
            parameterFilePath+="-parameter.txt"
            filename1 = open(parameterFilePath, 'w')
            #存放参数及数据
            #lz,  kmax
            #z_obs, dz, zmax, m_min, m_max, epsilon, lambda, sigma
            filename1.write("the number of divided layers:"+str(tableWidget.lz)+"\n")
            filename1.write("maximum number of iterations:"+str(tableWidget.kmax)+"\n")
            filename1.write("z_obs:"+str(tableWidget.z_obs)+"m\n")
            filename1.write("dz:"+str(tableWidget.dz)+"m\n")
            filename1.write("zmax:"+str(tableWidget.zmax)+"m\n")
            filename1.write("m_min:"+str(tableWidget.m_min)+"g/cm^3\n")
            filename1.write("m_max:"+str(tableWidget.m_max)+"g/cm^3\n")
            filename1.write("epsilon:"+str(tableWidget.epsilon)+"\n")
            filename1.write("miu:"+str(tableWidget.miu)+"\n")
            filename1.write("wn:"+str(tableWidget.wn)+"\n")
            filename1.write("sigma:"+str(tableWidget.sigma)+"\n")
            filename1.write("Max_GPU_Number:"+str(tableWidget.Max_GPU_Number)+"\n")
            filename1.write("nThreadPerBlock:"+str(tableWidget.nThreadPerBlock)+"\n")
            filename1.close()
        elif suffix=='xls':
            f = xlwt.Workbook()
            sheet1 = f.add_sheet('sheet1',cell_overwrite_ok=True)
            for i in range(0, tableWidget.nz):
                for j in range(0, tableWidget.ny):
                    for k in range(0, tableWidget.nx):
                        sheet1.write(i*tableWidget.nx*tableWidget.ny+j*tableWidget.nx+k, 0, str(tableWidget.m_result[i][j][k]))
            f.save(filePath[0])
            #保存参数
            parameterFilePath = suffixList[0]
            for i in range(1, len(suffixList)-1):
                parameterFilePath=parameterFilePath+'.'+suffixList[i]
            parameterFilePath+="-parameter.txt"
            filename1 = open(parameterFilePath, 'w')
            #存放参数及数据
            filename1.write("the number of divided layers:"+str(tableWidget.lz)+"\n")
            filename1.write("maximum number of iterations:"+str(tableWidget.kmax)+"\n")
            filename1.write("z_obs:"+str(tableWidget.z_obs)+"m\n")
            filename1.write("dz:"+str(tableWidget.dz)+"m\n")
            filename1.write("zmax:"+str(tableWidget.zmax)+"m\n")
            filename1.write("m_min:"+str(tableWidget.m_min)+"g/cm^3\n")
            filename1.write("m_max:"+str(tableWidget.m_max)+"g/cm^3\n")
            filename1.write("epsilon:"+str(tableWidget.epsilon)+"\n")
            filename1.write("miu:"+str(tableWidget.miu)+"\n")
            filename1.write("wn:"+str(tableWidget.wn)+"\n")
            filename1.write("sigma:"+str(tableWidget.sigma)+"\n")
            filename1.write("Max_GPU_Number:"+str(tableWidget.Max_GPU_Number)+"\n")
            filename1.write("nThreadPerBlock:"+str(tableWidget.nThreadPerBlock)+"\n")
            filename1.close()            
        else:
            QMessageBox.information(self, "Attention", "Please Fill in the Correct Suffix Name.")
            return
        #状态栏提示保存成功
        self.status.showMessage("File Saves Successfully", 3000)
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())		
