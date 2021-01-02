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
import xlwt
import json
import os
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
        
        self.tree_record = {}
        
        self.dockWidget = QDockWidget(self)
        w = QWidget()
        self.dockWidget.setTitleBarWidget(w)
        self.dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        self.tree = TreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(['File List'])
        self.tree.setColumnWidth(0, 300)
        self.dockWidget.setWidget(self.tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        self.tab = QTabWidget()
        
        self.start = QWidget(self)
        
        label = QLabel(self.start)
        label.setText("<p><font size=100 face=verdana color=red style=font-weight:bold>Welcome !</font></p><br><h1><font size=100 face=verdana>Parallel Inversion Software of Gravity gradiometry data</font></h1>")
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
        self.widg = {}
        self.tableWidget = QTabWidget()
        self.index = ""
        self.status = self.statusBar()
        self.showMaximized()
        
        self.paintCount = []
        
        newProject_Action.triggered.connect(self.newpro)
        newFile.triggered.connect(self.openfile)
        Load_project.triggered.connect(self.openPr)
        Save_project.triggered.connect(self.savePr)
        Close_project.triggered.connect(self.closeOp)
        Quit_Action.triggered.connect(self.quitOp)
        
        sectionPaint.triggered.connect(self.sectionOp)
        gridPaint.triggered.connect(self.gridOp)
        D3Paint.triggered.connect(self.D3Op)
        
        newModel.triggered.connect(self.buildModel)
        paintModel.triggered.connect(self.paintModel)
        saveModel.triggered.connect(self.forwardingSave)
        
        newInversion.triggered.connect(self.inversion)
        paintInversion.triggered.connect(self.inversionPainting)
        saveInversion.triggered.connect(self.inversionSave)
        setxyAction.triggered.connect(self.setXY)
        self.tree.clicked.connect(self.onTreeClicked)
        self.tab.currentChanged.connect(self.onCurrentChanged)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Tips',"Are you sure you want to quit the program?",
                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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
    
    def openPr(self):
        filePath = QFileDialog.getOpenFileName(self, 'Choose File', './', '*.json')
        if filePath[0] == "":return
        if os.path.isfile(filePath[0]) == False :
            QMessageBox.information(self, "Attention", "Json does not exist")
            return
        
        self.tab.clear()
        self.tab.addTab(self.start, "start")
        self.setCentralWidget(self.tab)
        self.tree.clear()
        self.widg.clear()
        self.tree_record.clear()
        self.paintCount.clear()
        with open(filePath[0], 'r', encoding = 'utf-8') as json_file:
            jsObj = json.load(json_file)
            for i in jsObj['TableWidget']:
                self.widg[i] = jsObj['TableWidget'][i]
            for i in jsObj['TreeWidget']:
                self.tree_record[i] = jsObj['TreeWidget'][i]
        self.paintCount = self.widg['paintCount']
        position = 1
        for key, value in self.tree_record.items():
            root = QTreeWidgetItem(self.tree)
            root.setText(0, key)
            mid = QMdiArea()
            self.tab.addTab(mid, key)
            self.tab.setCurrentWidget(mid)
            count = 0
           
            for key1, value1 in self.tree_record[key].items():
                if self.tree_record[key][key1]['type']=='FileData' or self.tree_record[key][key1]['type']=='ForwardingData':
                    child = QTreeWidgetItem(root)
                    child.setText(0, key1)
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
                    sub1 = QMdiSubWindow()
                    sub1.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub1.setWidget(tableWidget)
                    sub1.resize(750, 750)
                    sub1.setWindowTitle(key1)
                    mid.addSubWindow(sub1)
                    mid.setActiveSubWindow(sub1)
                    sub1.show()
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
                        for i in range(0, len(mwd.data)):
                            if mwd.data[i][0]=="Cube":
                                density = float(mwd.data[i][4])
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
                                density = float(mwd.data[i][4])
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
                    mw.mpl.section(1, fileName, x, y, xunit, vunit, flag)
                    sub = QMdiSubWindow()
                    sub.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub.setWidget(mw)
                    sub.setWindowTitle(finalName)
                    self.tab.widget(position).addSubWindow(sub)
                    self.tab.widget(position).setActiveSubWindow(sub)
                    sub.show()
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
                    sub = QMdiSubWindow()
                    sub.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub.setWidget(mw)
                    sub.setWindowTitle(finalName)
                    mid.addSubWindow(sub)
                    sub.show()
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
                    sub = QMdiSubWindow()
                    sub.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub.setWidget(mw)
                    sub.setWindowTitle(finalName)
                    mid.addSubWindow(sub)
                    sub.show()
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
                    xy = QAction("X-Y Profile", DIR)
                    xz = QAction("X-Z Profile", DIR)
                    yz = QAction("Y-Z Profile", DIR)
                    mw.mpl.menu.addAction(xy)
                    mw.mpl.menu.addAction(xz)
                    mw.mpl.menu.addAction(yz)
                    xy.triggered.connect(lambda:DIR.xy(tableWidget), flag)
                    xz.triggered.connect(lambda:DIR.xz(tableWidget), flag)
                    yz.triggered.connect(lambda:DIR.yz(tableWidget), flag)
                    sub = QMdiSubWindow()
                    sub.setWindowIcon(QIcon(".\\image\\logo.png"))
                    sub.setWidget(mw)
                    sub.setWindowTitle(mwTitle)
                    mid=self.tab.currentWidget()
                    mid.addSubWindow(sub)
                    sub.show()
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
    def savePr(self):
        if self.tab.count()==0:
            QMessageBox.information(self, "Attention", "No data to save")
            return
        filePath = QFileDialog.getSaveFileName(self, 'Open File', './', '*.json')
        if filePath[0] == "":
            return
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
            if self.tree.topLevelItem(sum_i-1).childCount() ==0:
                continue
            root = self.tree.topLevelItem(sum_i-1).text(0)
            sum_j = 0
            self.widg[root] = {}
            for key,  value in self.tree_record[root].items():
                if self.tree_record[root][key]['type'] != 'FileData' and self.tree_record[root][key]['type'] != 'ForwardingData':
                    sum_j+=1
                    continue
                
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
        
        name_emb = {'TableWidget':{}, 'TreeWidget':{}}
        for i in self.widg:
            name_emb['TableWidget'][i] = self.widg[i]
        for i in self.tree_record:
            name_emb['TreeWidget'][i] = self.tree_record[i]
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
        dialog = DialogGrid(self)
        dialog.exec()
        
    def onTreeClicked(self):
        item = self.tree.currentItem()
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
        selectedList = self.tree.selectedItems()
        for i in range(0, len(selectedList)):
            selectedList[i].setSelected(0)
        position = self.tab.currentIndex()
        child3 = QTreeWidgetItem(root)
        child3.setText(0, index + "3D Model")
        child3.setSelected(1)
        root.setExpanded(1)
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
            parameterFilePath = suffixList[0]
            for i in range(1, len(suffixList)-1):
                parameterFilePath=parameterFilePath+'.'+suffixList[i]
            parameterFilePath+="-parameter.txt"
            filename1 = open(parameterFilePath, 'w')
            filename1.write(tableWidget.forwardingInformation)
            filename1.close()
        elif suffix=='xls':
            f = xlwt.Workbook()
            sheet1 = f.add_sheet('sheet1',cell_overwrite_ok=True)
            for i in range(0,len(tableWidget.data)):
                for j in range(0,len(tableWidget.data[0])):
                    sheet1.write(i, j, str(tableWidget.data[i][j]))
            f.save(filePath[0])
            parameterFilePath = suffixList[0]
            for i in range(1, len(suffixList)-1):
                parameterFilePath=parameterFilePath+'.'+suffixList[i]
            parameterFilePath+="-parameter.txt"
            filename1 = open(parameterFilePath, 'w')
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
            parameterFilePath = suffixList[0]
            for i in range(1, len(suffixList)-1):
                parameterFilePath=parameterFilePath+'.'+suffixList[i]
            parameterFilePath+="-parameter.txt"
            filename1 = open(parameterFilePath, 'w')
           
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
            parameterFilePath = suffixList[0]
            for i in range(1, len(suffixList)-1):
                parameterFilePath=parameterFilePath+'.'+suffixList[i]
            parameterFilePath+="-parameter.txt"
            filename1 = open(parameterFilePath, 'w')
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
        self.status.showMessage("File Saves Successfully", 3000)
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())		
