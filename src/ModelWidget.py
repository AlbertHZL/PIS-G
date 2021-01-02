from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib as mpl

class MyModelWidget(FigureCanvas):
    def __init__(self, parent=None):
        
        plt.rcParams['font.family'] = ['Times New Roman']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['savefig.dpi'] = 300
        
        self.fig = Figure()
        self.ax = Axes3D(self.fig)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.menu = QMenu()
        
        self.vmin = 0.0
        self.vmax = 0.0
        self.d = 0.0
        self.colorList = ['#00008B', '#0000FF' ,'#4169E1', '#6495ED','#87CEEB',  '#87CEFA', '#B0E0E6',\
        '#AFEEEE', '#E1FFFF','#FFFACD','#F5DEB3','#F0E68C', '#F4A460','#FF7F50', '#FF6347',\
        '#D2691E',  '#FF4500', '#FF0000','#A52A2A' ,'#800000']

        
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    
    def setRange(self, vmin, vmax):
        self.vmin = vmin
        self.vmax = vmax
        self.d = (vmax - vmin)/(len(self.colorList)-1)
        
    def setColorbar(self, colorBarTitle):
        norm = mpl.colors.Normalize(vmin=self.vmin, vmax=self.vmax)
        cmap = plt.cm.RdYlBu_r
        cax = self.fig.add_axes([0.01, 0.1, 0.02, 0.85])
        cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, spacing='proportional')
        cb.set_label(colorBarTitle)
        
    def setTitle(self, title):
        self.ax.set_title(title)
        
    def paintCube(self, xlim, ylim, zlim,density, xdown, xup, ydown, yup, zup, xx, yy):
        verts = [(float(xlim[0]), float(ylim[0]), float(zlim[0])), (float(xlim[0]), float(ylim[1]), float(zlim[0])), (float(xlim[1]), float(ylim[1]), float(zlim[0])), (float(xlim[1]), float(ylim[0]), float(zlim[0])), (float(xlim[0]), float(ylim[0]), float(zlim[1])), (float(xlim[0]), float(ylim[1]), float(zlim[1])), (float(xlim[1]), float(ylim[1]), float(zlim[1])), (float(xlim[1]), float(ylim[0]), float(zlim[1]))]
        faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [0, 3, 7, 4]]
        poly3d = [[verts[vert_id] for vert_id in face] for face in faces]
        x, y, z = zip(*verts)
        if self.d == 0:
            colorIndex = 1
        else:
            colorIndex = int((density - self.vmin)/self.d)
        self.ax.add_collection3d(Poly3DCollection(poly3d, facecolors=self.colorList[colorIndex], linewidths=1, alpha=0.5))
        self.ax.add_collection3d(Line3DCollection(poly3d, colors='k', linewidths=0.5, linestyles=':'))
        if(xx == 1000):
            self.ax.set_xlabel('X/km')
        else:
            self.ax.set_xlabel('X/m')
        self.ax.set_xlim3d(xdown, xup)
        if(xx == 1000):
            self.ax.set_ylabel('Y/km')
        else:
            self.ax.set_ylabel('Y/m')
        
        self.ax.set_ylim3d(ydown, yup)
        self.ax.set_zlabel('Z/m')
        self.ax.set_zlim3d(0, zup)
        self.ax.invert_zaxis()
    
    def saveFig(self, fileName):
        self.fig.savefig(fileName)
 
    def contextMenuEvent(self, event):
        self.menu.exec(QCursor.pos())
        event.accept()
        
class ModelWidget(QWidget):
    def __init__(self, parent=None):
        super(ModelWidget, self).__init__(parent)
        self.father = parent
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyModelWidget(self.father)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)     
