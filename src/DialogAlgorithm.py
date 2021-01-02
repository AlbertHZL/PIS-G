from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ctypes import *
import threading
from DialogInformation import DialogInformation

class DialogAlgorithm(QDialog):
    sinOut = pyqtSignal(int)
    def __init__(self, parent=None):
        super(DialogAlgorithm, self).__init__(parent)
        self.father = parent
        
        label1 = QLabel("the number of divided layers:")
        label2 = QLabel("maximum number of iterations:")
        label3 = QLabel("                       z_obs:")
        label4 = QLabel("m                         dz:")
        label4_ = QLabel("m     ")
        
        label5 = QLabel("                        zmax:")
        label6 = QLabel("                       m_min:")
        label7 = QLabel("g/cm^3                 m_max:")
        label8= QLabel("g/cm^3               epsilon:")
        label8_ = QLabel("      ")
        
        label9 = QLabel("                         miu:")
        label10 = QLabel("                       sigma:")
        label11 = QLabel("              Max_GPU_Number:")
        label12 = QLabel("             nThreadPerBlock:")
        label12_ = QLabel("      ")
        
        label13 = QLabel("                          wn:")
        label14 = QLabel("                             ")
        label14_le = QLabel(" ")
        label15 = QLabel("                             ")
        label15_le = QLabel(" ")
        label16 = QLabel("                             ")
        label16_le = QLabel(" ")
        label16_ = QLabel("      ")
        
        count = self.checkCuda()
        if count < 1 :
            QMessageBox.information(self, "ATTENTION", "No available GPUs were detected")
            self.close()
            
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.le3 = QLineEdit()
        self.le4 = QLineEdit()
        self.le5 = QLineEdit()
        self.le6 = QLineEdit()
        self.le7 = QLineEdit()
        self.le8 = QLineEdit()
        self.le9 = QLineEdit()
        self.le10 = QLineEdit()
        self.le11 = QLineEdit()
        self.le12 = QLineEdit()
        self.le13 = QLineEdit()
        
        layout1 = QHBoxLayout()
        layout1.addWidget(label1, 3)
        layout1.addWidget(self.le1, 1)
        layout1.addWidget(label2, 2)
        layout1.addWidget(self.le2, 1)
        layout1.addWidget(label3, 2)
        layout1.addWidget(self.le3, 1)
        layout1.addWidget(label4, 2)
        layout1.addWidget(self.le4, 1)
        layout1.addWidget(label4_, 1)
        layout1.addStretch(1)
        
        layout2 = QHBoxLayout()
        layout2.addWidget(label5, 3)
        layout2.addWidget(self.le5, 1)
        layout2.addWidget(label6, 2)
        layout2.addWidget(self.le6, 1)
        layout2.addWidget(label7, 2)
        layout2.addWidget(self.le7, 1)
        layout2.addWidget(label8, 2)
        layout2.addWidget(self.le8, 1)
        layout2.addWidget(label8_, 1)
        layout2.addStretch(1)
        
        layout3 = QHBoxLayout()
        layout3.addWidget(label9, 3)
        layout3.addWidget(self.le9, 1)
        layout3.addWidget(label10, 2)
        layout3.addWidget(self.le10, 1)
        layout3.addWidget(label11, 2)
        layout3.addWidget(self.le11, 1)
        layout3.addWidget(label12, 2)
        layout3.addWidget(self.le12, 1)
        layout3.addWidget(label12_, 1)
        layout3.addStretch(1)
        
        layout4 = QHBoxLayout()
        layout4.addWidget(label13, 3)
        layout4.addWidget(self.le13, 1)
        layout4.addWidget(label14, 2)
        layout4.addWidget(label14_le, 1)
        layout4.addWidget(label15, 2)
        layout4.addWidget(label15_le, 1)
        layout4.addWidget(label16, 2)
        layout4.addWidget(label16_le, 1)
        layout4.addWidget(label16_, 1)
        layout4.addStretch(1)

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addLayout(layout1, 1)
        layout.addStretch(2)
        layout.addLayout(layout2, 1)
        layout.addStretch(2)
        layout.addLayout(layout3, 1)
        layout.addStretch(2)
        layout.addLayout(layout4, 1)
        layout.addStretch(2)
        
        layoutBottom = QHBoxLayout()
        layoutBottom.addStretch(1)
        ok = QPushButton("OK", self)
        cancel = QPushButton("Cancel", self)
        layoutBottom.addWidget(ok, 1)
        layoutBottom.addStretch(2)
        layoutBottom.addWidget(cancel, 1)
        layoutBottom.addStretch(1)
        layout.addLayout(layoutBottom)
        self.setLayout(layout)
        self.setWindowTitle("Input Inversion Parameters")
        self.setWindowIcon(QIcon(".\\image\\logo.png"))
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        cancel.clicked.connect(self.on_cancel_clicked)
        ok.clicked.connect(self.on_ok_clicked)
        self.sinOut.connect(self.on_finish)
    
    def checkCuda(self):
        ll = cdll.LoadLibrary
        Objdll = ll("./grav_rfi_ompcuda.dll")
        count = Objdll.CheckCount()
        return count
    
    def on_finish(self, flag):
        self.father.status.showMessage(" ", 0)
        self.info.close()
        if flag ==1:
            QMessageBox.information(self, "Congratulation", "Inversion Success")
            self.close()
        elif flag ==2:
            QMessageBox.information(self, "ATTENTION", "Please Input Necessary Data")
            self.show()
        elif flag ==3:
            QMessageBox.information(self, "ATTENTION", "Calculation failed. Please check the parameters \n or try to calculate again. ")
            self.show()
        else:
            QMessageBox.information(self, "Error", "Please check the data page")
            self.show()
            
    def on_cancel_clicked(self):
        self.close()
        return
    
    def on_ok_clicked(self):
        t_Calculation = threading.Thread(target=self.Calculation, args = ())
        t_Calculation.start()
        self.info = DialogInformation(self)
        self.info.show()
        self.hide()
        
    def Calculation(self):
        tableWidget = self.father.tableWidget
        tableWidget.flag[0] = 1
        
        try:
            tableWidget.lz = int(self.le1.text())
            tableWidget.kmax = int(self.le2.text())
            tableWidget.z_obs = float(self.le3.text())
            tableWidget.dz = float(self.le4.text())
            tableWidget.zmax = float(self.le5.text())
            tableWidget.m_min = float(self.le6.text())
            tableWidget.m_max = float(self.le7.text())
            tableWidget.epsilon = float(self.le8.text())
            tableWidget.miu = float(self.le9.text())
            tableWidget.sigma = float(self.le10.text())
            tableWidget.Max_GPU_Number = int(self.le11.text())
            tableWidget.nThreadPerBlock = int(self.le12.text())
            tableWidget.wn = float(self.le13.text())
            
        except ValueError:
            self.sinOut.emit(2)
            tableWidget.flag[0] = 0
            return 
        
        self.father.status.showMessage("Computing...", 0)
        
        vzzPosition = 0
        xxPosition = tableWidget.xcol
        yyPosition = tableWidget.ycol
        for i in range(1, tableWidget.lieCount+1):
            if tableWidget.item(0, i).text()=="Vzz":
                vzzPosition = i

        tableWidget.x.clear()
        tableWidget.y.clear()
        for i in range(0, len(tableWidget.data)):
            tableWidget.x.append(float(tableWidget.data[i][xxPosition-1]))
            tableWidget.y.append(float(tableWidget.data[i][yyPosition-1]))
            
        for i in range(0, len(tableWidget.data)):
            try:
                tableWidget.Vzz.append(float(tableWidget.data[i][vzzPosition-1]))
            except ValueError:
                tableWidget.flag[0] = 0
                self.sinOut.emit(4)
                return

        ll = cdll.LoadLibrary   
        Objdll = ll("./grav_rfi_ompcuda.dll") 
        func = Objdll.foo
        
        func.argtypes = (c_int, c_int,c_int,c_int,c_int,c_int, c_int, c_int, \
        c_double,c_double,c_double,c_double,c_double, c_double,  c_double,c_double, c_double , \
        POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double))
        func.restype  = POINTER(c_double)
        
        lx = 1
        ly = 1
        for i in range(1 , len(tableWidget.data)-1):
            if tableWidget.x[i] != tableWidget.x[0]:
                lx = lx+1
            else:
                break;
        for i in range(1 , len(tableWidget.data)-1):
            if tableWidget.y[i] == tableWidget.y[0]:
                ly = ly+1
            else:
                break;
       
        xmin = float(tableWidget.x[0])
        xmax = float(tableWidget.x[0])
        ymin = float(tableWidget.y[0])
        ymax = float(tableWidget.y[0])
        for i in range(1 , len(tableWidget.data)-1):
            if  xmin > tableWidget.x[i]:
                xmin = tableWidget.x[i]
            if xmax < tableWidget.x[i]:
                xmax = tableWidget.x[i]
            if  ymin > tableWidget.y[i]:
                ymin = tableWidget.y[i]
            if ymax < tableWidget.y[i]:
                ymax = tableWidget.y[i]
        tableWidget.dx = (xmax - xmin)/(float(lx)-1)
        tableWidget.dy = (ymax - ymin)/(float(ly)-1)
        tableWidget.nz = tableWidget.lz
        tableWidget.nx = lx
        tableWidget.ny = ly
        tableWidget.point_count = tableWidget.nx * tableWidget.ny
        tableWidget.model_count = tableWidget.nx * tableWidget.ny *tableWidget.nz
        
        zc= []
        thick = []
        for i in range(0,  tableWidget.lz):
            thick.append(tableWidget.dz) 
            t = (i + 0.5) * tableWidget.dz
            zc.append(t) 
            
        mmxx = [0 for x in range(tableWidget.model_count * 2)]
        mmyy = [0 for x in range(tableWidget.model_count * 2)]
        mmzz = [0 for x in range(tableWidget.model_count * 2)]

        for fp in range(0,  tableWidget.point_count):
            for fq in range(0,  tableWidget.lz):
                mmxx[fp+tableWidget.point_count * fq] = tableWidget.x[fp] -  0.5 * tableWidget.dx
                mmxx[fp+tableWidget.point_count * fq + tableWidget.model_count] = tableWidget.x[fp] +  0.5 * tableWidget.dx
                mmyy[fp+tableWidget.point_count * fq] = tableWidget.y[fp] -  0.5 * tableWidget.dy
                mmyy[fp+tableWidget.point_count * fq + tableWidget.model_count] = tableWidget.y[fp] +  0.5 * tableWidget.dy
                mmzz[fp+tableWidget.point_count * fq] = zc[fq] -  0.5 * thick[fq]
                mmzz[fp+tableWidget.point_count * fq + tableWidget.model_count] = zc[fq] +  0.5 * thick[fq]
        tableWidget.mx=mmxx
        tableWidget.my=mmyy
        tableWidget.mz=mmzz
        
        tableWidget.zc = zc
        tableWidget.thick = thick
        
        Point_count = c_int(tableWidget.point_count)
        Prism_count = c_int(tableWidget.model_count)
        Lx = c_int(lx)
        Ly = c_int(ly)
        Lz = c_int(tableWidget.lz)
        Kmax = c_int(tableWidget.kmax)
        Z_obs = c_double(tableWidget.z_obs)
        Dz = c_double(tableWidget.dz)
        Zmax = c_double(tableWidget.zmax)
        M_min = c_double(tableWidget.m_min)
        M_max = c_double(tableWidget.m_max)
        Epsilon = c_double(tableWidget.epsilon)
        Miu = c_double(tableWidget.miu)
        Sigma = c_double(tableWidget.sigma)
        Zc = POINTER(c_double)((c_double*len(zc))(*zc))
        Thick = POINTER(c_double)((c_double*len(thick))(*thick))
        Vzz = POINTER(c_double)((c_double*len(tableWidget.Vzz))(*tableWidget.Vzz))
        X = POINTER(c_double)((c_double*len(tableWidget.x))(*tableWidget.x))
        Y = POINTER(c_double)((c_double*len(tableWidget.y))(*tableWidget.y))
        MMax_GPU_Number = c_int(tableWidget.Max_GPU_Number)
        NThreadPerBlock = c_int(tableWidget.nThreadPerBlock)
        Wn = c_double(tableWidget.wn)
        result = []
        try:
            result = Objdll.foo(Point_count,  Prism_count,  Lx,  Ly,  Lz,  Kmax, MMax_GPU_Number, NThreadPerBlock,  Z_obs, Dz, Zmax, M_min, M_max,\
            Epsilon, Miu, Sigma,Wn, Zc,  Thick,  Vzz, X, Y)
        except(ValueError, MemoryError):
            tableWidget.inversionFlag = 1
            self.sinOut.emit(3)
            tableWidget.flag[0] = 0
            return 
        temp_result = []
        for i in range(0, tableWidget.model_count):
            temp_result.append(float(result[i]))
        tableWidget.m_result.clear()
        
        count = 0
        for i in range(0, tableWidget.nz):
            tempy = []
            for j in range(0, tableWidget.ny):
                tempx = []
                for k in range(0, tableWidget.nx):
                    tempx.append(temp_result[count])
                    count+=1
                tempy.append(tempx)
            tableWidget.m_result.append(tempy)
        tableWidget.inversionFlag = 1
        self.sinOut.emit(1)
        tableWidget.flag[0] = 0
        return       
