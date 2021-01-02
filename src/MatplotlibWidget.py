import matplotlib
import numpy as np
matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.pyplot import *

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        
        plt.rcParams['font.family'] = ['Times New Roman'] 
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['savefig.dpi'] = 300
        
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
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
                self.axes.plot(x, zz, label=fileName[i], marker="o", markersize=3)
            else:
                self.axes.plot(x, zz, label=fileName[i])
        self.axes.legend(loc='upper right')
        
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
        surf = self.axes.contourf(X, Y, ellipses, levels=levels, cmap=cm.jet)
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
        self.mpl_ntb = NavigationToolbar(self.mpl, self)
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
