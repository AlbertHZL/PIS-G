import matplotlib
import numpy as np
matplotlib.use("Qt5Agg")#声明使用QT5
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.pyplot import *

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        # 配置中文显示
        plt.rcParams['font.family'] = ['Times New Roman'] 
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.rcParams['savefig.dpi'] = 300 #图片像素
        #plt.rcParams['figure.dpi'] = 150 #分辨率
        #plt.rcParams['figure.figsize'] = (2.0, 1.0) # 设置figure_size尺寸
        
        self.fig = Figure()  # 新建一个figure--绘图对象
        self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改

        #self.axes.hold(True)  # 每次绘图的时候不保留上一次绘图的结果
        
        #self.setAlignment(Qt.AlignCenter)
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def section(self, number, fileName, x, y, xunit, vunit, flag):
        temp=''
        for i in range(0, len(fileName)):
            temp=temp+fileName[i]+" "
        temp+=" Profile"
        temp = "Line "+str(number)+"  "+temp
        self.fig.suptitle(temp)
        sLenth = len(y)
        tLenth = len(x)
        lines = sLenth//tLenth
        for i in range(0, lines):
            zz=y[i*tLenth:(i+1)*tLenth]
            if flag==1:
                self.axes.plot(x, zz, label=fileName[i], marker="o", markersize=3)#, labels=fileName[i]
            else:
                self.axes.plot(x, zz, label=fileName[i])
        self.axes.legend(loc='upper right')
        
        #plt.title(temp)
        xunitnew = 'x/'+xunit
        yunitnew = 'y/'+vunit
        self.axes.set_ylabel(yunitnew)
        self.axes.set_xlabel(xunitnew)
        self.axes.grid(True)
        
    def gridPaint(self, fileName, x, y, z, xunit, yunit, colorbarTitle, flag1, flag2):
        self.fig.suptitle(fileName)
        X, Y = np.meshgrid(x, y)
        lengthX = len(x)
        lengthZ = len(z)
        times = lengthZ//lengthX
        ellipses = [z[0:lengthX]]
        for num in range(1,times):
            ellipses += [z[lengthX*num:lengthX*(num+1)]]
        levels=MaxNLocator(nbins=15).tick_values(min(z), max(z))
        surf = self.axes.contourf(X, Y, ellipses, levels=levels, cmap=cm.jet)#levels=levels, cmap=cm.jet, linewidth=0.1
        self.fig.colorbar(surf, shrink=1, aspect=10, label=colorbarTitle)
        xunitnew = 'x/'+xunit
        yunitnew = 'y/'+yunit
        self.axes.set_ylabel(yunitnew)
        self.axes.set_xlabel(xunitnew)
        if flag1==1:
            if flag2==1:
                C = self.axes.contour(X, Y, ellipses, 10)
                self.axes.clabel(C, inline=True, fmt='%1.1f', colors='k', fontsize=10)
            else:
                self.axes.contour(X, Y, ellipses, 10)
        
    def saveFig(self, fileName):
        self.fig.savefig(fileName)
     
class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
