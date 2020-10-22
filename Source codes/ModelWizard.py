from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ModelWizardWidget import ModelWizardWidget
from ModelWidget import ModelWidget
from ctypes import *
from TableWidget import TableWidget
from ThreeViewsWidget import ThreeViewsWidget
from DialogThreeViews import DialogThreeViews

class ModelWizard(QWizard):
    SIGNAL_data = pyqtSignal()
    def __init__(self, parent):
        super(ModelWizard, self).__init__(parent)
        self.setWindowTitle("Forwarding Wizard")
        self.setWindowIcon(QIcon(".\\image\\logo.png"))
        self.setGeometry(600, 250, 350, 350)
        self.flag = [0, 0, 0]
        self.father = parent
        #储存中间Page
        self.tablePage = []
        #存储每一页面的xyz的上下限
        self.xrange = []
        self.yrange = []
        self.zrange = []
        #正演数据
        self.information = ""
        #储存每个模型的数据
        self.data=[]
        #第一页的数据
        self.xlow = 0
        self.xhigh = 0
        self.dx = 0
        self.ylow = 0
        self.yhigh = 0
        self.dy = 0
        #z轴最深
        self.zmax = 0
        #密度的最大最小值
        self.densityMin = 0
        self.densityMax = 0
        #三视图的图名和color名
        self.title = []
        self.colorbarTitle = []
        #第几次从初始页面进入
        self.times = 0
        #第一页
        firstPage = QWizardPage()
        firstPage.setSubTitle("welcome")
        firstPage.setPixmap(QWizard.WatermarkPixmap, QPixmap(".\\image\\image.jpg"))
        firstPage.setCommitPage(1)#设置第二页没有back功能
        label = QLabel()
        label.setText("Welcome to the Modeling Information Collection\n Wizard.This wizard will build a cube model \nbased on the information you provide. \n\n")
        label.setAlignment(Qt.AlignCenter)
        
        label2 = QLabel()
        label2.setText("Number of Model:")
        label2.setAlignment(Qt.AlignCenter)
        self.lineEdit = QLineEdit()
        #获取三维模型Title及colorbarTitle
        label3 = QLabel()
        label3.setText("Figure Title:")
        self.le1 = QLineEdit()#获取模型名称
        label4 = QLabel()
        label4.setText("ColorBar Title:")
        self.le2 = QLineEdit()#获取colorbar名称
        label5 = QLabel()
        label5.setText("Observation Height:")
        label5_unit = QLabel("m")
        self.le3 = QLineEdit() #获取观测高度
        
        layoutInFirstUp = QHBoxLayout()
        layoutInFirstUp.addStretch(1)
        #layoutInFirstUp.addWidget(label1, 1)
        #layoutInFirstUp.addWidget(self.le, 1)
        layoutInFirstUp.addStretch(1)
        
        layoutInFirst = QHBoxLayout()
        layoutInFirst.addStretch(1)
        layoutInFirst.addWidget(label2, 1)
        layoutInFirst.addWidget(self.lineEdit, 1)
        layoutInFirst.addStretch(1)
        
        layoutInFirst1 = QHBoxLayout()
        layoutInFirst1.addStretch(1)
        layoutInFirst1.addWidget(label3, 1)
        layoutInFirst1.addWidget(self.le1, 1)
        layoutInFirst1.addStretch(1)
        
        layoutInFirst2 = QHBoxLayout()
        layoutInFirst2.addStretch(1)
        layoutInFirst2.addWidget(label4, 1)
        layoutInFirst2.addWidget(self.le2, 1)
        layoutInFirst2.addStretch(1)
        
        layoutInFirst3 = QHBoxLayout()
        layoutInFirst3.addStretch(1)
        layoutInFirst3.addWidget(label5, 1)
        layoutInFirst3.addWidget(self.le3, 1)
        layoutInFirst3.addWidget(label5_unit, 1)
        layoutInFirst3.addStretch(1)
        
        xlabel1=QLabel()
        xlabel1.setText("X Range:")
        xlabel2=QLabel()
        xlabel2.setText("m——")
        xlabel3=QLabel()
        xlabel3.setText("m dx")
        xlabel4=QLabel()
        xlabel4.setText("m")
        ylabel1=QLabel()
        ylabel1.setText("Y Range:")
        ylabel2=QLabel()
        ylabel2.setText("m——")
        ylabel3=QLabel()
        ylabel3.setText("m dy")
        ylabel4=QLabel()
        ylabel4.setText("m")
        self.xle1=QLineEdit()
        self.xle2=QLineEdit()
        self.xle3=QLineEdit()
        self.yle1=QLineEdit()
        self.yle2=QLineEdit()
        self.yle3=QLineEdit()
        
        xlayout=QHBoxLayout()
        xlayout.addWidget(xlabel1, 2)
        xlayout.addWidget(self.xle1, 1)
        xlayout.addWidget(xlabel2, 1)
        xlayout.addWidget(self.xle2, 1)
        xlayout.addWidget(xlabel3, 1)
        xlayout.addWidget(self.xle3, 1)
        xlayout.addWidget(xlabel4, 1)
        
        ylayout=QHBoxLayout()
        ylayout.addWidget(ylabel1, 2)
        ylayout.addWidget(self.yle1, 1)
        ylayout.addWidget(ylabel2, 1)
        ylayout.addWidget(self.yle2, 1)
        ylayout.addWidget(ylabel3, 1)
        ylayout.addWidget(self.yle3, 1)
        ylayout.addWidget(ylabel4, 1)
        
        layoutFirst = QVBoxLayout()
        layoutFirst.addWidget(label, 3)
        layoutFirst.addStretch(2)
        layoutFirst.addLayout(layoutInFirstUp, 1)
        layoutFirst.addLayout(layoutInFirst, 1)
        layoutFirst.addLayout(layoutInFirst1, 1)
        layoutFirst.addLayout(layoutInFirst2, 1)
        layoutFirst.addLayout(layoutInFirst3, 1)
        layoutFirst.addStretch(2)
        layoutFirst.addLayout(xlayout, 1)
        layoutFirst.addLayout(ylayout, 1)
        layoutFirst.addStretch(2)
        firstPage.setLayout(layoutFirst)
        #第二页--数据收集
        secondPage= QWizardPage()
        secondPage.setTitle("Model Information Collection")
        secondPage.setSubTitle("No."+str(1)+" Model")
        table = ModelWizardWidget(self)
        self.tablePage.append(table)
        layoutSecond=QVBoxLayout()
        layoutSecond.addWidget(table)
        secondPage.setLayout(layoutSecond)
        #最后一页
        self.finalPage = QWizardPage()
        self.finalPage.setTitle("Model Information Preview")
        layout = QVBoxLayout()
        self.showLabel = QLabel()
        layout.addWidget(self.showLabel)
        self.finalPage.setLayout(layout)  
        
        self.setWizardStyle(QWizard.ModernStyle)
        self.setPage(1, firstPage)
        self.setPage(2, secondPage)
        self.setStartId(1)
        self.setWindowFlags(self.windowFlags()&~Qt.WindowContextHelpButtonHint)#设置没有帮助按钮
        #信号槽
        self.SIGNAL_data.connect(self.ModelData)
    
    def validateCurrentPage(self):
        id = self.currentId()
        strNum = self.lineEdit.text()
        if strNum=="":
            QMessageBox.information(self, "Attention", "Please Enter Corrent Number of Model.")
            return 0
        modelNumber = -1
        if strNum != "":
            try:
                modelNumber = int(self.lineEdit.text())
            except ValueError:
                QMessageBox.information(self, "Attention", "Please Enter Corrent Number of Model.")
                return 0
            try:
                ObservationHeight = float(self.le3.text())
            except ValueError:
                QMessageBox.information(self, "Attention", "Please Enter Corrent Observation height.")
                return 0
        if id == 1 and self.times != 1:
            self.times+=1
            if modelNumber == 0:
                QMessageBox.information(self, "Attention", "Please Enter Corrent Number of Model.(>0)")
                self.times-=1
                return 0
            try:
                float(self.xle1.text())
                float(self.xle2.text())
                float(self.xle3.text())
                float(self.yle1.text())
                float(self.yle2.text())
                float(self.yle3.text())
            except ValueError:
                QMessageBox.information(self, "Attention", "Please enter the correct data.")
                self.times-=1
                return 0
            for i in range(1, modelNumber):
                #信息收集页
                dataCollectPage = QWizardPage()
                dataCollectPage.setTitle("Model Information Collection")
                dataCollectPage.setSubTitle(""+str(i+1)+"th Model")
                #dataCollectPage.setPixmap(QWizard.WatermarkPixmap, QPixmap(".\\image\\tower.jpg"))
                table = ModelWizardWidget()
                self.tablePage.append(table)
                layoutSecond=QVBoxLayout()
                layoutSecond.addWidget(table)
                dataCollectPage.setLayout(layoutSecond)
                self.addPage(dataCollectPage)
            if modelNumber>1:
                self.finalPage.setSubTitle(str(modelNumber)+" models in total")
            else:
                self.finalPage.setSubTitle("1 model in total")
            self.addPage(self.finalPage)
            
            #循环检测数据收集页面是否输入数据
        for i in range(0, modelNumber-1):
            if id == i+2:
                temp = self.tablePage[i].le.text()
                temp1=self.tablePage[i].le1.text()
                temp2=self.tablePage[i].le2.text()
                temp3=self.tablePage[i].le3.text()
                temp4=self.tablePage[i].le4.text()
                temp5=self.tablePage[i].le5.text()
                temp6=self.tablePage[i].le6.text()
                cbPosition = self.tablePage[i].cb.currentIndex()
                #检测是否输入数据
                if temp == "" or temp1 == "" or temp2 == "" or temp3 == ""\
                or temp4 == "" or temp5 == "" or temp6 == "":
                    QMessageBox.information(self, "Attention", "Please Enter Relevant Data")
                    return 0
                #检测数据是否合理
                try:
                    float(temp)
                    if float(temp1)>=float(temp2):
                        QMessageBox.information(self, "Attention", "Wrong X-Range")
                        return 0
                    if float(temp3)>=float(temp4):
                        QMessageBox.information(self, "Attention", "Wrong Y-Range")
                        return 0
                    if float(temp5)>=float(temp6):
                        QMessageBox.information(self, "Attention", "Wrong Z-Range")
                        return 0
                except ValueError:
                    QMessageBox.information(self, "Attention", "Please enter the correct data.")
                    return 0
                #检测是否选择下拉菜单
                if cbPosition == 0:
                    QMessageBox.information(self, "Attention", "Please Select the Model Shape")
                    return 0
                #碰撞检测
                if id > 2:
                    for j in range(0, i):
                        if self.xrange[j][1]<=float(temp1) or float(temp2)<=self.xrange[j][0]:
                            continue
                        if self.yrange[j][1]<=float(temp3) or float(temp4)<=self.yrange[j][0]:
                            continue
                        if self.zrange[j][1]<=float(temp5) or float(temp6)<=self.zrange[j][0]:
                            continue
                        QMessageBox.information(self, "Attention", "This model collides with the "+str(j+1)+"th model. Please reenter the data.")
                        return 0
                            
                #记录xyz范围
                xx=[]
                xx.append(float(temp1))
                xx.append(float(temp2))
                self.xrange.append(xx)
                yy=[]
                yy.append(float(temp3))
                yy.append(float(temp4))
                self.yrange.append(yy)
                zz=[]
                zz.append(float(temp5))
                zz.append(float(temp6))
                self.zrange.append(zz)
        if modelNumber != 0 and id == 1+modelNumber:
            #最后一页的前一页————预览页
            i = id-2
            temp = self.tablePage[i].le.text()
            temp1=self.tablePage[i].le1.text()
            temp2=self.tablePage[i].le2.text()
            temp3=self.tablePage[i].le3.text()
            temp4=self.tablePage[i].le4.text()
            temp5=self.tablePage[i].le5.text()
            temp6=self.tablePage[i].le6.text()
            cbPosition = self.tablePage[i].cb.currentIndex()
            #检测数据是否输入
            if temp == "" or temp1 == "" or temp2 == "" or temp3 == ""\
            or temp4 == "" or temp5 == "" or temp6 == "":
                QMessageBox.information(self, "Attention", "Please Enter Relevant Data")
                return 0
            #检测数据是否合理
            try:
                float(temp)
                if float(temp1)>=float(temp2):
                    QMessageBox.information(self, "Attention", "Wrong X-Range")
                    return 0
                if float(temp3)>=float(temp4):
                    QMessageBox.information(self, "Attention", "Wrong Y-Range")
                    return 0
                if float(temp5)>=float(temp6):
                    QMessageBox.information(self, "Attention", "Wrong Z-Range")
                    return 0
            except ValueError:
                QMessageBox.information(self, "Attention", "Please enter the correct data.")
                return 0
            #检测是否选择下拉菜单
            if cbPosition == 0:
                QMessageBox.information(self, "Attention", "Please Select the Model Shape")
                return 0
            #碰撞检测
            if i > 0:
                for j in range(0, i):
                    if self.xrange[j][1]<=float(temp1) or float(temp2)<=self.xrange[j][0]:
                        continue
                    if self.yrange[j][1]<=float(temp3) or float(temp4)<=self.yrange[j][0]:
                        continue
                    if self.zrange[j][1]<=float(temp5) or float(temp6)<=self.zrange[j][0]:
                        continue
                    QMessageBox.information(self, "Attention", "This model collides with the "+str(j+1)+"th model. Please reenter the data.")
                    return 0
            self.SIGNAL_data.emit()
            #获取数据
            self.data.clear()
            for i in range(0, modelNumber):
                self.data.append(self.tablePage[i].aa)
            showLabelString = ""
            for i in range(0, len(self.data)):
                showLabelString = showLabelString + "Model"  + str(i+1) + "："
                showLabelString = showLabelString + self.data[i][0] +"\t"
                showLabelString = showLabelString + "X-Range:[" + self.data[i][1] +"](m) "
                showLabelString = showLabelString + "Y-Range:[" + self.data[i][2] +"](m) "
                showLabelString = showLabelString + "Z-Range:[" + self.data[i][3] +"](m) "
                showLabelString = showLabelString + "Residual density：" + self.data[i][4] +"g/cm^3"
                showLabelString += "\n"
            #设置标签
            self.information += showLabelString
            self.showLabel.setText(showLabelString)
            self.showLabel.setAlignment(Qt.AlignLeft)
            return 1
        #finished
        if self.currentPage().nextId() == -1:
            self.on_finished()
        return 1
        
    def on_finished(self):
        self.xlow = float(self.xle1.text())
        self.xhigh = float(self.xle2.text())
        self.dx = float(self.xle3.text())
        self.ylow = float(self.yle1.text())
        self.yhigh = float(self.yle2.text())
        self.dy = float(self.yle3.text())
        #根据self.data中数据画图
        if len(self.data)==0: return
        #计算xy上下限
        xlow = float(self.xle1.text())
        xhigh = float(self.xle2.text())
        xdistance = float(self.xle3.text())
        ylow = float(self.yle1.text())
        yhigh = float(self.yle2.text())
        ydistance = float(self.yle3.text())
        model_Number = int(self.lineEdit.text())
        Observation_height  = float(self.le3.text())
        #第二个子窗口---3D模型
        mw = ModelWidget(self)
        mwTitle = self.le1.text()
        mwColorBarTitle = self.le2.text()
        if mwTitle == "":   mwTitle ="Forwarding Model"
        mw.mpl.setTitle(mwTitle)
        densityData=[]
        c=[]
        b=[]
        a=[]
        flag=0#标注是否有立方体
        zmax = 0
        #收集density数据
        for i in range(0, len(self.data)):
            if self.data[i][0]=="Cube":
                density = float(self.data[i][4])#密度
                densityData.append(density)
        #设置colorbar上下限
        self.densityMax = max(densityData)
        self.densityMin = min(densityData)
        if self.densityMax==self.densityMin:    
            self.densityMax+=1
        mw.mpl.setRange(self.densityMin, self.densityMax)
        #循环绘制
        for i in range(0, len(self.data)):
            if self.data[i][0]=="Cube":
                flag=1
                xlim = self.data[i][1].split(',')
                if len(xlim)==1:
                    xlim = self.data[i][1].split('，')
                ylim = self.data[i][2].split(',')
                if len(ylim)==1:
                    ylim = self.data[i][2].split('，')
                zlim = self.data[i][3].split(',')
                if len(zlim)==1:
                    zlim = self.data[i][3].split('，')
                density = float(self.data[i][4])#密度
                tem = []
                tem.append(float(zlim[0]))
                tem.append(float(zlim[1]))
                c.append(tem)
                tem1 = []
                tem1.append(float(ylim[0]))
                tem1.append(float(ylim[1]))
                b.append(tem1)
                tem2 = []
                tem2.append(float(xlim[0]))
                tem2.append(float(xlim[1]))
                a.append(tem2)
                if zmax < float(zlim[1]):
                    k = int(float(zlim[1])/1000)
                    yu = float(zlim[1])-k*1000
                    if yu > 0:
                        zmax = (k+1)*1000
                    else:
                        zmax = k*1000
                mw.mpl.paintCube(xlim, ylim, zlim, density, xlow-xdistance/2, xhigh+xdistance/2, ylow-ydistance/2, yhigh+ydistance/2, zmax, 1, 1)
        self.zmax = zmax
        #添加colorbar
        if mwColorBarTitle == "":
            mwColorBarTitle="density(g/cm^3)"
        mw.mpl.setColorbar(mwColorBarTitle)
        #添加右键事件
        frontView = QAction("X-Z Profile", self)
        sideView = QAction("Y-Z Profile", self)
        downView = QAction("X-Y Profile", self)
        mw.mpl.menu.addAction(frontView)
        mw.mpl.menu.addAction(sideView)
        mw.mpl.menu.addAction(downView)
        
        #第一个子窗口
        #计算X、Y的数组
        x = []
        y = []
        nx = int((xhigh-xlow)/xdistance)+1
        ny = int((yhigh-ylow)/ydistance)+1
        point_count = nx*ny
        for i in range(0, nx):
            x.append(xlow+i*xdistance)
        for i in range(0, ny):
            y.append(ylow+i*ydistance)
        
        #int lx, int ly, int point_count, int prism_count, double x_min, double dx, double x_max,
        #double y_min, double dy, double y_max, double z_obs, double* x, double* y, double* mx, double* my, double* mz, double* p
        mx = [0 for x in range(0,2*model_Number)]
        my = [0 for x in range(0,2*model_Number)]
        mz = [0 for x in range(0,2*model_Number)]
        for i in range(0, len(self.data)):
            if self.data[i][0] == "Cube":
                flag = 1
                xlim = self.data[i][1].split(',')
                if len(xlim)==1:
                    xlim = self.data[i][1].split('，')
                ylim = self.data[i][2].split(',')
                if len(ylim)==1:
                    ylim = self.data[i][2].split('，')
                zlim = self.data[i][3].split(',')
                if len(zlim)==1:
                    zlim = self.data[i][3].split('，')
                mx[i] = float(xlim[0])
                mx[i + model_Number] = float(xlim[1])
                my[i] = float(ylim[0])
                my[i + model_Number] = float(ylim[1])
                mz[i] = float(zlim[0])
                mz[i + model_Number] = float(zlim[1])
        
        NX = c_int(nx)
        NY = c_int(ny)
        POINT_COUNT = c_int(point_count)
        MODEL_NUMBER = c_int(model_Number)
        XLOW = c_double(xlow)
        XDISTANCE = c_double(xdistance)
        XHIGH = c_double(xhigh)
        YLOW = c_double(ylow)
        YDISTANCE = c_double(ydistance)
        YHIGH = c_double(yhigh)
        OBSERVATION_HEIGHT = c_double(Observation_height)
        X = POINTER(c_double)((c_double*len(x))(*x))
        Y = POINTER(c_double)((c_double*len(y))(*y))
        MX = POINTER(c_double)((c_double*len(mx))(*mx))
        MY = POINTER(c_double)((c_double*len(my))(*my))
        MZ = POINTER(c_double)((c_double*len(mz))(*mz))
        DENSITYDATA = POINTER(c_double)((c_double*len(densityData))(*densityData))
        ll = cdll.LoadLibrary   
        Objdll = ll("./Forwarding_DLL.dll") 
        func = Objdll.Forwarding
        func.argtypes = (c_int, c_int,c_int,c_int, c_double,c_double,c_double,c_double,c_double, c_double,  c_double, \
        POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)) #设置函数参数类型
        func.restype  = POINTER(c_double) #设置返回值类型为 double*
        
        data_result = []
        data_result = Objdll.Forwarding(NX, NY, POINT_COUNT, MODEL_NUMBER, XLOW, XDISTANCE, XHIGH, YLOW, YDISTANCE,\
        YHIGH, OBSERVATION_HEIGHT, X, Y, MX, MY, MZ, DENSITYDATA)
        
        F_Data = []
        for i in range(0, len(y)):
            for j in range(0, len(x)):
                temp = []
                for k in range(0, 7):
                    temp.append(float(data_result[k*point_count + j + i * len(x)]))
                temp.append(x[j])
                temp.append(y[i])
                F_Data.append(temp)
                
        headTitle=['0','V', 'X', 'Y']
        if flag == 1:
            headTitle=['0', 'Vxx', 'Vxy', 'Vxz', 'Vyy', 'Vyz', 'Vzz', 'Vz', 'X', 'Y']
        tableWidget = TableWidget(self.father, F_Data, headTitle, 0, 0)
        #传递正演数据
        tableWidget.forwardingInformation = tableWidget.forwardingInformation + "X-Range:"+str(xlow)+"m-"+str(xhigh)+"m  dx"+str(xdistance)+"m\n"
        tableWidget.forwardingInformation = tableWidget.forwardingInformation + "Y-Range:"+str(ylow)+"m-"+str(yhigh)+"m  dy"+str(ydistance)+"m\n"
        tableWidget.forwardingInformation = tableWidget.forwardingInformation + "Observation height:"+str(Observation_height)+"m\n"
        tableWidget.forwardingInformation = tableWidget.forwardingInformation + self.information
        
        #当前Tab页索引
        position = self.father.tab.currentIndex()
        #在self.father的tree加入root
        root = self.father.tree.topLevelItem(position-1)
        # s 记录根节点的名字
        s = root.text(0)
        title = 'Data'
        num = 0
        while title in self.father.tree_record[s]:
            num+=1
            title = 'Data' + str(num)
        frontView.triggered.connect(lambda:self.dialog(1, title))
        sideView.triggered.connect(lambda:self.dialog(2, title))
        downView.triggered.connect(lambda:self.dialog(3, title))
        sub = QMdiSubWindow()
        sub.setWindowIcon(QIcon(".\\image\\logo.png"))
        sub.setWidget(tableWidget)
        sub.setWindowTitle(title)
        sub.resize(750, 750)
        self.father.tab.widget(position).addSubWindow(sub)
        self.father.tab.widget(position).setActiveSubWindow(sub)
        sub.show()
        #设置树上root为选中状态
        selectedList = self.father.tree.selectedItems()
        for i in range(0, len(selectedList)):
            selectedList[i].setSelected(0)
        #记录在 tree_record 中
        self.father.tree_record[s][title]={}
        self.father.tree_record[s][title]={'Number_of_Model':str(self.lineEdit.text()), \
        'Model_Title':str(mwTitle), 'ColorBar_Title':str(mwColorBarTitle),'Observation_height':str(self.le3.text()), \
        'xlow':str(self.xle1.text()), 'xhigh':str(self.xle2.text()), 'xdistance':str(self.xle3.text()), \
        'ylow':str(self.yle1.text()), 'yhigh':str(self.yle2.text()), 'ydistance':str(self.xle3.text()), \
        'ForwardingModel':mw, 'ForwardingModelFlag':0, 'type':'ForwardingData', 'densityMax':self.densityMax, \
        'densityMin':self.densityMin}
        for i in range(0, int(self.lineEdit.text())):
            name_temp = 'Number_'+str(i+1)
            self.father.tree_record[s][title][name_temp] ={}
            for j in range(0, len(self.data[i])):
                self.father.tree_record[s][title][name_temp][str(j)] = str(self.data[i][j])
        #设置继承root的子目录
        child1 = QTreeWidgetItem(root)
        child1.setText(0, title)
        child1.setSelected(1)
        root.setExpanded(1)
        #标注Flag
        return
        
    def ModelData(self):
        for i in range(0, len(self.tablePage)):
            id = self.tablePage[i].cb.currentIndex()
            self.tablePage[i].aa.append(self.tablePage[i].cbItems[id])
            if id==1:
                temp1=self.tablePage[i].le1.text()
                temp2=self.tablePage[i].le2.text()
                temp3=self.tablePage[i].le3.text()
                temp4=self.tablePage[i].le4.text()
                temp5=self.tablePage[i].le5.text()
                temp6=self.tablePage[i].le6.text()
                temp31=temp1+","+temp2
                temp32=temp3+","+temp4
                temp33=temp5+","+temp6
                self.tablePage[i].aa.append(temp31)
                self.tablePage[i].aa.append(temp32)
                self.tablePage[i].aa.append(temp33)
                self.tablePage[i].aa.append(self.tablePage[i].le.text())
                
    def dialog(self, number, index):
        dialog = DialogThreeViews(self, number, index)
        dialog.show()
        
    def front(self, index):
        if len(self.title)==0 or len(self.colorbarTitle)==0:
            return
        if self.flag[0] ==1: 
            QMessageBox.information(self, "Attention", "X-Z Profile already exists")
            return 
        self.flag[0] = 1
        title = self.title[0]
        colorbarTitle = self.colorbarTitle[0]
        tvw = ThreeViewsWidget()
        if title == "": title = "X-Z Profile"
        tvw.mpl.setTitle(title)
        tvw.mpl.setRange(self.densityMin, self.densityMax)
        #计算xy上下限    
        xlow = self.xlow
        xhigh = self.xhigh
        dx = self.dx
        for i in range(0, len(self.data)):
            if self.data[i][0]=="Cube":
                xlim = self.data[i][1].split(',')
                if len(xlim)==1:
                    xlim = self.data[i][1].split('，')
                ylim = self.data[i][2].split(',')
                if len(ylim)==1:
                    ylim = self.data[i][2].split('，')
                zlim = self.data[i][3].split(',')
                if len(zlim)==1:
                    zlim = self.data[i][3].split('，')
                density = float(self.data[i][4])
                tvw.mpl.cubeFront(xlim, ylim, zlim, xlow-dx/2, xhigh+dx/2, 0, self.zmax, density)
        if colorbarTitle == "":
            colorbarTitle="density(g/cm^3)"
        tvw.mpl.setColorbar(colorbarTitle)
        #加子窗口
        sub3 = QMdiSubWindow()
        sub3.setWindowIcon(QIcon(".\\image\\logo.png"))
        sub3.setWidget(tvw)
        sub3.setWindowTitle(title)
        mid=self.father.tab.currentWidget()
        mid.addSubWindow(sub3)
        sub3.show()
        #文件树条目
        selectedList = self.father.tree.selectedItems()
        for i in range(0, len(selectedList)):
            selectedList[i].setSelected(0)
        position = self.father.tab.currentIndex()
        root = self.father.tree.topLevelItem(position-1)
        child3 = QTreeWidgetItem(root)
        child3.setText(0, title)
        #更改 tree_record 的值
        child_name = 'view_'+str(self.father.paintCount[position-1]) 
        root_name = root.text(0)
        self.father.tree_record[root_name][child_name] ={'title':str(title),'type':'Forwarding_Paintint_XZ', \
        'color_Bar_Title':str(colorbarTitle),'index':index}
        self.father.paintCount[position-1] = self.father.paintCount[position-1] +1
        child3.setSelected(1)
        root.setExpanded(1)
        
        
    def side(self, index):
        if len(self.title)==0 or len(self.colorbarTitle)==0:
            return
        if self.flag[1] ==1: 
            QMessageBox.information(self, "Attention", "Y-Z Profile already exists")
            return 
        self.flag[1] = 1
        title = self.title[0]
        colorbarTitle = self.colorbarTitle[0]
        tvw = ThreeViewsWidget()
        if title == "":
            title = "Y-Z Profile"
        tvw.mpl.setTitle(title)
        tvw.mpl.setRange(self.densityMin, self.densityMax)
        #计算xy上下限 
        ylow = self.ylow
        yhigh = self.yhigh
        dy = self.dy
        for i in range(0, len(self.data)):
            if self.data[i][0]=="Cube":
                xlim = self.data[i][1].split(',')
                if len(xlim)==1:
                    xlim = self.data[i][1].split('，')
                ylim = self.data[i][2].split(',')
                if len(ylim)==1:
                    ylim = self.data[i][2].split('，')
                zlim = self.data[i][3].split(',')
                if len(zlim)==1:
                    zlim = self.data[i][3].split('，')
                density = float(self.data[i][4])
                tvw.mpl.cubeSide(xlim, ylim, zlim, ylow-dy/2, yhigh+dy/2, 0, self.zmax, density)
        if colorbarTitle == "":
            colorbarTitle = "density(g/cm^3)"
        tvw.mpl.setColorbar(colorbarTitle)
        #加子窗口
        sub3 = QMdiSubWindow()
        sub3.setWindowIcon(QIcon(".\\image\\logo.png"))
        sub3.setWidget(tvw)
        sub3.setWindowTitle(title)
        mid=self.father.tab.currentWidget()
        mid.addSubWindow(sub3)
        sub3.show()
        #文件树条目
        selectedList = self.father.tree.selectedItems()
        for i in range(0, len(selectedList)):
            selectedList[i].setSelected(0)
        position = self.father.tab.currentIndex()
        root = self.father.tree.topLevelItem(position-1)
        child3 = QTreeWidgetItem(root)
        #更改 tree_record 的值
        child_name = 'view_'+str(self.father.paintCount[position-1]) 
        root_name = root.text(0)
        self.father.tree_record[root_name][child_name] ={'title':title,'type':'Forwarding_Paintint_YZ', \
        'color_Bar_Title':str(colorbarTitle), 'index':index}
        self.father.paintCount[position-1] = self.father.paintCount[position-1] +1
        child3.setText(0, title)
        child3.setSelected(1)
        root.setExpanded(1)
        
    def down(self, index):
        if len(self.title)==0 or len(self.colorbarTitle)==0:
            return
        if self.flag[2] ==1: 
            QMessageBox.information(self, "Attention", "X-Y Profile already exists")
            return 
        self.flag[2] = 1
        title = self.title[0]
        colorbarTitle = self.colorbarTitle[0]
        tvw = ThreeViewsWidget()
        if title == "":
            title ="X-Y Profile"
        tvw.mpl.setTitle(title)
        tvw.mpl.setRange(self.densityMin, self.densityMax)
        #计算xy上下限    
        xlow = self.xlow
        xhigh = self.xhigh
        dx = self.dx
        ylow = self.ylow
        yhigh = self.yhigh
        dy = self.dy
        for i in range(0, len(self.data)):
            if self.data[i][0]=="Cube":
                xlim = self.data[i][1].split(',')
                if len(xlim)==1:
                    xlim = self.data[i][1].split('，')
                ylim = self.data[i][2].split(',')
                if len(ylim)==1:
                    ylim = self.data[i][2].split('，')
                zlim = self.data[i][3].split(',')
                if len(zlim)==1:
                    zlim = self.data[i][3].split('，')
                density = float(self.data[i][4])
                tvw.mpl.cubeDown(xlim, ylim, zlim, xlow-dx/2, xhigh+dx/2, ylow-dy/2, yhigh+dy/2, density)
        if colorbarTitle == "":
            colorbarTitle ="density(g/cm^3)"
        tvw.mpl.setColorbar(colorbarTitle)
        #加子窗口
        sub3 = QMdiSubWindow()
        sub3.setWindowIcon(QIcon(".\\image\\logo.png"))
        sub3.setWidget(tvw)
        sub3.setWindowTitle(title)
        mid=self.father.tab.currentWidget()
        mid.addSubWindow(sub3)
        sub3.show()
        #文件树条目
        selectedList = self.father.tree.selectedItems()
        for i in range(0, len(selectedList)):
            selectedList[i].setSelected(0)
        position = self.father.tab.currentIndex()
        root = self.father.tree.topLevelItem(position-1)
        child3 = QTreeWidgetItem(root)
        child3.setText(0, title)
        #更改 tree_record 的值
        child_name = 'view_'+str(self.father.paintCount[position-1]) 
        root_name = root.text(0)
        self.father.tree_record[root_name][child_name] ={'title':title,'type':'Forwarding_Paintint_XY', \
        'color_Bar_Title':str(colorbarTitle),'index':index}
        self.father.paintCount[position-1] = self.father.paintCount[position-1] +1
        child3.setSelected(1)
        root.setExpanded(1)
    

        
        
