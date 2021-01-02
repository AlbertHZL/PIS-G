import matplotlib
import numpy as np
matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.pyplot import *

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        
        plt.rcParams['font.family'] = ['Times New Roman']
        plt.rcParams['axes.unicode_minus'] = False    
        plt.rcParams['savefig.dpi'] = 300
       
        self.fig = Figure() 
        self.ax = Axes3D(self.fig)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def D3Paint(self, fileName, x, y, z, xunit, yunit, zunit, colorbarTitle):
        self.ax.set_title(fileName)
        lengthX = len(x)
        lengthZ = len(z)
        times = lengthZ//lengthX
        ellipses = []
        for num in range(0,times):
            ellipses.append(z[lengthX*num:lengthX*(num+1)])
        xx = np.linspace(min(x),max(x),lengthX)
        yy = np.linspace(min(y),max(y),lengthX)
        X,Y = np.meshgrid(xx,yy)
        xunitnew = 'x/'+xunit
        yunitnew = 'y/'+yunit
        zunitnew = 'v/'+zunit
        self.ax.set_xlabel(xunitnew)
        self.ax.set_ylabel(yunitnew)
        self.ax.set_zlabel(zunitnew)
        
        ellipses = np.array(ellipses)
        surf = self.ax.plot_surface(X, Y, ellipses, rstride=1, cstride=1,cmap=cm.jet)
        cbar = self.fig.colorbar(surf, extend='neither', spacing='proportional',
                        orientation='vertical', shrink=0.85, format="%.0f")
        cbar.set_label(colorbarTitle, size=10)
        
    def saveFig(self, fileName):
        self.fig.savefig(fileName)
     
class Matplotlib3DWidget(QWidget):
    def __init__(self, parent=None):
        super(Matplotlib3DWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
