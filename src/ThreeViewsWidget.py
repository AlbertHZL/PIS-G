import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import matplotlib.patches as patches
import matplotlib as mpl

class MyMpl(FigureCanvas):
    def __init__(self, parent=None):
        
        plt.rcParams['font.family'] = ['Times New Roman']
        plt.rcParams['axes.unicode_minus'] = False   
        plt.rcParams['savefig.dpi'] = 300
        
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111, aspect='equal')
        
        self.vmin = 0.0
        self.vmax = 0.0
        self.d = 0.0
        self.colorList = ['darkblue','blue','royalblue','cornflowerblue','steelblue', 'deepskyblue',\
        'skyblue','lightblue','lightcyan','greenyellow','yellowgreen','yellow','gold','goldenrod',\
        'orange','darkorange','orangered','red','firebrick','maroon']
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
    def setTitle(self, title):
        self.axes.set_title(title)
    
    def setRange(self, vmin, vmax):
        self.vmin = vmin
        self.vmax = vmax
        self.d = (vmax - vmin)/(len(self.colorList)-1)
        
    def setColorbar(self, colorbarTitle):
        norm = mpl.colors.Normalize(vmin=self.vmin, vmax=self.vmax)
        cmap = plt.cm.RdYlBu_r
        cax = self.fig.add_axes([0.85, 0.1, 0.02, 0.785])
        cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, spacing='proportional')
        cb.set_label(colorbarTitle)
        
    def cubeFront(self, xlim, ylim, zlim, xdown, xup, zdown, zup, density):
        
        x=float(xlim[0])
        z=float(zlim[0])
        xdis = float(xlim[1])-x
        zdis = float(zlim[1])-z
       
        if self.d == 0:
            colorIndex = 1
        else:
            colorIndex = int((density - self.vmin)/self.d)
        self.axes.add_patch(patches.Rectangle((x, z), xdis, zdis, color = self.colorList[colorIndex]))
        self.axes.set_xlabel('x/m')
        self.axes.set_ylabel('z/m')
        self.axes.axis([xdown, xup, zup, zdown])
        
    def cubeSide(self, xlim, ylim, zlim, ydown, yup, zdown, zup, density):
        y=float(ylim[0])
        z=float(zlim[0])
        ydis = float(ylim[1])-y
        zdis = float(zlim[1])-z
        
        if self.d == 0:
            colorIndex = 1
        else:
            colorIndex = int((density - self.vmin)/self.d)
        self.axes.add_patch(patches.Rectangle((y, z), ydis, zdis, color = self.colorList[colorIndex]))
        self.axes.set_xlabel('y/m')
        self.axes.set_ylabel('z/m')
        self.axes.axis([ydown, yup, zup, zdown])
        
    def cubeDown(self, xlim, ylim, zlim, xdown, xup, ydown, yup, density):
        x=float(xlim[0])
        y=float(ylim[0])
        xdis = float(xlim[1])-x
        ydis = float(ylim[1])-y
        
        if self.d == 0:
            colorIndex = 1
        else:
            colorIndex = int((density - self.vmin)/self.d)
        self.axes.add_patch(patches.Rectangle((x, y), xdis, ydis, color = self.colorList[colorIndex]))
        self.axes.set_xlabel('x/m')
        self.axes.set_ylabel('y/m')
        self.axes.axis([xdown, xup, ydown, yup])
        
    def saveFig(self, fileName):
        self.fig.savefig(fileName)
     
class ThreeViewsWidget(QWidget):
    def __init__(self, parent=None):
        super(ThreeViewsWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMpl(self)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
