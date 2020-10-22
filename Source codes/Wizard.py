from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import xlrd
from TableWidget import TableWidget

class Wizard(QWizard):
    def __init__(self, parent):
        super(Wizard, self).__init__(parent)
        self.setWindowTitle("File-Choosing Wizard")
        self.setWindowIcon(QIcon(".\\image\\logo.png"))
        self.setGeometry(600, 250, 350, 350)
        self.father = parent
        self.linenumber = 0
        #第一页
        firstPage = QWizardPage()
        firstPage.setSubTitle("welcome")
        firstPage.setPixmap(QWizard.WatermarkPixmap, QPixmap(".\\image\\image.jpg"))
        label = QLabel()
        label.setText("This wizard will guide you to select\n and preview the documents. \n \nTips: If you need inversion function, \nplease change the column names to Vxx, Vxy,\n Vxz, Vyy, Vyz, Vzz on the last page. \n If you are ready, please click Next.")
        label.setAlignment(Qt.AlignCenter)
        layout1 = QVBoxLayout()
        layout1.addWidget(label)
        firstPage.setLayout(layout1)
        #第二页
        secondPage = QWizardPage()
        secondPage.setSubTitle("Choose File")
        self.lineEdit = QLineEdit()
        self.button = QPushButton("Choose File", secondPage)
        layout = QHBoxLayout()
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        layout3 = QVBoxLayout()
        layout3.addStretch(5)
        layout3.addLayout(layout)
        layout3.addStretch(5)
        layout3.setAlignment(layout, Qt.AlignCenter)
        secondPage.setLayout(layout3)
        #第三页
        thirdPage  = QWizardPage()
        thirdPage.setSubTitle("preview & choose")
        #self.tw = QTableWidget()
        self.te=QTextEdit()
        self.text1=QLabel("Data Start Line:")
        self.le1=QLineEdit()
        
        layout21=QHBoxLayout()
        layout21.addStretch(1)
        layout21.addWidget(self.text1, 1)
        layout21.addWidget(self.le1, 1)
        layout21.addStretch(1)
        
        layout2 = QVBoxLayout()
        layout2.addWidget(self.te, 3)
        layout2.addLayout(layout21, 1)
        thirdPage.setLayout(layout2)
        #第四页
        forthPage = QWizardPage()
        forthPage.setSubTitle("Fill in the Coordinate Name")
        tip=QLabel(self)
        tip.setText("Double-click the header(s) to name the column(s)！")
        tip.setAlignment(Qt.AlignCenter)
        self.tableWidget=QTableWidget()
        layout4=QVBoxLayout()
        layout4.addWidget(tip, 1)
        layout4.addWidget(self.tableWidget, 9)
        forthPage.setLayout(layout4)
        
        #数据传递变量
        self.startrow=0#文件起始行
        self.headTitle=["ZERO"]#表格表头
        self.uplimit=0#起始行数据上限
        
        self.setWizardStyle(QWizard.ModernStyle)
        self.setPage(1, firstPage)
        self.setPage(2, secondPage)
        self.setPage(3, thirdPage)
        self.setPage(4, forthPage)
        self.setStartId(1)
        self.setWindowFlags(self.windowFlags()&~Qt.WindowContextHelpButtonHint)#设置没有帮助按钮
        #信号槽
        self.button.clicked.connect(self.chooseFile)
        self.currentIdChanged.connect(self.on_currentIdChanged)
        self.finished.connect(self.on_finished)
    def isFloot(self, s):
        try:
            s = float(s) #此处更改想判断的类型
        except TypeError:
            return False
        except ValueError:
            return False
        else:
            return True
            
    
    def chooseFile(self):
        name = QFileDialog.getOpenFileName(self, 'Open File', './', '*.txt *.xls')
        self.lineEdit.setText(str(name[0]))
    def validateCurrentPage(self):
        fileName = self.lineEdit.text()
        id = self.currentId()
        if id==2 :
            if fileName=="":
                QMessageBox.information(self, "Attention", "Please Choose File")
                return 0
            with open(fileName, 'r') as fw:
                lines = fw.readlines()
                h = len(lines)
                for i in range(0,  h):
                    line = lines[i].rstrip().split(',')
                    if self.isFloot(line[0])==1:
                        self.le1.setText(str(i+1))
                        break
        if id==3:
            if self.le1.text()=="":
                QMessageBox.information(self, "Attention", "Please Fill in Data Start Line")
                return 0
            else:
                try:
                    temp=int(self.le1.text())
                except ValueError:
                    QMessageBox.information(self, "Attention", "Data Start Line isn't a integer")
                    return 0
                if temp<1 or temp>self.uplimit:
                    return 0
        if id==4:
            headTemp=[]
            for i in range(1, self.tableWidget.columnCount()):
                headTemp.append(self.tableWidget.item(0, i).text())
            flagX = 0
            flagY = 0
            for i in range(0, len(headTemp)):
                if headTemp[i]=='X' or headTemp[i]=='x':
                    flagX = 1
                if headTemp[i]=='Y' or headTemp[i]=='y':
                    flagY = 1
            if flagX == 0 or flagY == 0:
                QMessageBox.information(self, "Attention", "No X, Y Axes Selected.")
                return 0
        return 1

    def on_currentIdChanged(self):
        fileName = self.lineEdit.text()
        id = self.currentId()
        suffixList = fileName.split('.')
        suffix = suffixList[-1]
        if id==3 and fileName!="":
            if suffix!='xls' and suffix!='xlsx':
                filename = open(fileName)
                line1s = filename.readlines()
                self.uplimit=len(line1s)
                aa=""
                count=1
                for line in line1s:
                    aa=aa+str(count)+"  "+line+"\n"
                    count+=1
                td=QTextDocument(aa)
                self.te.setDocument(td)
            if suffix=='xls' or suffix=='xlsx':
                data = xlrd.open_workbook(fileName)
                table = data.sheets()[0]
                self.uplimit=table.nrows
                aa="" 
                for i in range(0, table.nrows):
                    aa=aa+str(i+1)+"  "
                    for j in range(0, table.ncols):
                        aa=aa+str(table.cell(i, j).value)+"\t"
                    aa=aa+"\n"
                td=QTextDocument(aa)
                self.te.setDocument(td)
        if id==4 and self.le1.text()!="":
            #第四页
            fileName = self.lineEdit.text()
            data=[]
            if suffix!='xls' and suffix!='xlsx':
                filename = open(fileName)
                line1s = filename.readlines()
                for line in line1s[int(self.le1.text())-1:]:
                    if line.rstrip() == '':
                        continue
                    temp= line.rstrip().split(',')
                    for i in range(0, len(temp)):
                        if temp[i]=="":
                            QMessageBox.information(self, "Attention", "File Exceptions.Back to the Previous Page.")
                            self.back()
                            self.back()
                            return
                    data.append(temp)
            if suffix=='xls' or suffix=='xlsx':
                file = xlrd.open_workbook(fileName)
                table = file.sheets()[0] 
                for i in range(int(self.le1.text())-1, table.nrows):
                    datatemp = []
                    for j in range(0, table.ncols):
                        if str(table.cell(i, j).value)=="":
                            QMessageBox.information(self, "Attention", "File Exceptions. Back to the Previous Page.")
                            self.back()
                            self.back()
                            return
                        datatemp.append(str(table.cell(i, j).value))
                    data.append(datatemp)
            tempcount = len(data[0])
            for i in range(1,  len(data)):
                if tempcount != len(data[i]):
                    QMessageBox.information(self, "Attention", "File Exceptions. Back to the Previous Page.")
                    self.back()
                    self.back()
                    return
            self.tableWidget.setColumnCount( len(data[0])+1)#设置列数
            self.tableWidget.setRowCount(len(data)+1)#设置行数
            self.tableWidget.horizontalHeader().setVisible(0)
            self.tableWidget.verticalHeader().setVisible(0)
            self.linenumber = len(data[0])+1
            #设置表头
            temp_header = []
            flag = 0
            with open(fileName, 'r') as f:
                for i in range(0, int(self.le1.text())-1):
                    t = f.readline().rstrip('\n')
                    temp_header = t.rstrip().split(',')
                    #满足文件头的要求
                    if len(temp_header) == len(data[0]):
                        flag = 1
                        for i in range(1,  len(data[0])+1):
                            self.tableWidget.setItem(0, i, QTableWidgetItem(temp_header[i-1]))
            if flag ==0:
                header = ['Vxx', 'Vxy', 'Vxz', 'Vyy', 'Vyz', 'Vzz', 'x', 'y']
                if(len(data[0])+1>8):
                    for i in range(0, len(data[0])-7):
                        header.append('V'+str(i))
                for i in range(1,  len(data[0])+1):
                    self.tableWidget.setItem(0, i, QTableWidgetItem(header[i-1]))
                self.tableWidget.setItem(0, len(data[0])-1,  QTableWidgetItem('x'))
                self.tableWidget.setItem(0, len(data[0]),  QTableWidgetItem('y'))
            for i in range(1,  len(data)+1):
                self.tableWidget.setItem(i,0, QTableWidgetItem(str(i)))
                for j in range(1,  len(data[0])+1):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(data[i-1][j-1]))
            
            
    def on_finished(self):
        #获取文件名
        fileName = self.lineEdit.text()
        #获取表格表头
        for i in range(1, self.tableWidget.columnCount()):
            self.headTitle.append(self.tableWidget.item(0, i).text())
        #获取当前页面
        id = self.currentId()
        if id==4 and fileName!="":
            #当前Tab页索引
            position = self.father.tab.currentIndex()
            #在self.father的tree加入root
            root = self.father.tree.topLevelItem(position-1)
            #起始行数值
            self.startrow=int(self.le1.text())
            #设置树上root为选中状态
            selectedList = self.father.tree.selectedItems()
            for i in range(0, len(selectedList)):
                selectedList[i].setSelected(0)
            #  tree_record 
            title = 'File Data'
            s = 0
            while title in self.father.tree_record[root.text(0)]:
                s+=1
                title = 'File Data' + str(s)
            self.father.tree_record[root.text(0)][title]={'type':'FileData'}
            #设置继承root的子目录
            child = QTreeWidgetItem(root)
            child.setText(0, title)
            root.setExpanded(1)
            child.setSelected(1)
            #子窗口
            #读取文件数据
            data=[]
            suffixList = fileName.split('.')
            suffix = suffixList[-1]
            if suffix!='xls' and suffix!='xlsx':
                filename = open(fileName)
                line1s = filename.readlines()
                for line in line1s[self.startrow-1:]:
                    if line.rstrip() == '':
                        continue
                    temp= line.rstrip().split(',')
                    data.append(temp)
            if suffix=='xls' or suffix=='xlsx':
                data = xlrd.open_workbook(fileName)
                table = data.sheets()[0] 
                for i in range(self.startrow-1, table.nrows):
                    datatemp = []
                    for j in range(0, table.ncols):
                        datatemp.append(str(table.cell(i, j).value))
                    data.append(datatemp)
            self.tableWidget = TableWidget(self.father, data, self.headTitle, 0, 0)
            sub = QMdiSubWindow()
            sub.setWindowIcon(QIcon(".\\image\\logo.png"))
            sub.setWidget(self.tableWidget)
            sub.setWindowTitle(title)
            sub.resize(750, 750)
            self.father.tab.widget(position).addSubWindow(sub)
            sub.show()
            self.father.tab.widget(position).setActiveSubWindow(sub)
            
    
