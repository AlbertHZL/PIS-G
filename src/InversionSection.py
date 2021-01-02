import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.pyplot import *

class MyMplPara(FigureCanvas):
    def __init__(self, parent=None):
        
        plt.rcParams['font.family'] = ['Times New Roman']
        plt.rcParams['axes.unicode_minus'] = False       
        plt.rcParams['savefig.dpi'] = 300
        
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111, aspect='equal')
        
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
    def setTitle(self, title):
        self.axes.set_title(title)

    def xy_section(self, x1, x2, y1, y2, z, dx, dy, dz, deep, colorbarTitle):
        xx = np.linspace(x1, x2, int((x2-x1)/dx+1))
        yy = np.linspace(y1, y2, int((y2-y1)/dy+1))
        X,Y = np.meshgrid(xx,yy)
        
        CS = self.axes.contourf(X,Y,z,10, cmap=cm.jet)
        cbar = self.fig.colorbar(CS, shrink=1, aspect=10,)
        if colorbarTitle == "":
            cbar.ax.set_ylabel("density(g/cm^3)")
        else:
            cbar.ax.set_ylabel(colorbarTitle)
        self.axes.tick_params(labelsize=9)
        self.axes.set_xlabel('x/m')
        self.axes.set_ylabel('y/m')
        
    def xz_section(self, x1,x2, z1, z2, value, dx, dy, dz, deep, colorbarTitle):
        xx = np.linspace(x1, x2, int((x2-x1)/dx+1))
        zz = np.linspace(z1, z2, int((z2-z1)/dz+1))
        X,Z = np.meshgrid(xx,zz) 
    
        CS = self.axes.contourf(X,Z,value,10, cmap=cm.jet)
        cbar = self.fig.colorbar(CS, shrink=1, aspect=10,)
        if colorbarTitle == "":
            cbar.ax.set_ylabel("density(g/cm^3)")
        else:
            cbar.ax.set_ylabel(colorbarTitle)
        self.axes.tick_params(labelsize=9)
        self.axes.set_xlabel('x/m')
        self.axes.set_ylabel('z/m')
        self.axes.invert_yaxis()
        
    def yz_section(self, y1,y2, z1, z2, value, dx, dy, dz, deep, colorbarTitle):
        yy = np.linspace(y1, y2, int((y2-y1)/dy+1)) 
        zz = np.linspace(z1, z2, int((z2-z1)/dz+1))
        Y,Z = np.meshgrid(yy,zz)
        CS = self.axes.contourf(Y,Z,value,10, cmap=cm.jet)
        cbar = self.fig.colorbar(CS, shrink=1, aspect=10,)
        if colorbarTitle == "":
            cbar.ax.set_ylabel("density(g/cm^3)")
        else:
            cbar.ax.set_ylabel(colorbarTitle)
        self.axes.tick_params(labelsize=9)
        self.axes.set_xlabel('y/m')
        self.axes.set_ylabel('z/m')
        self.axes.invert_yaxis()
        
    def saveFig(self, fileName):
        self.fig.savefig(fileName)
     
class InversionSection(QWidget):
    def __init__(self, parent=None):
        super(InversionSection, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplPara(self)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
