from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from mpl_toolkits.mplot3d import Axes3D#, axes3d
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
import matplotlib as mpl

class MyModelWidget(FigureCanvas):
    def __init__(self, parent=None):
        # 配置中文显示
        plt.rcParams['font.family'] = ['Times New Roman']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号        
        plt.rcParams['savefig.dpi'] = 300 #图片像素
        #plt.rcParams['figure.dpi'] = 150 #分辨率
        
        self.fig = Figure()  # 新建一个figure
        self.ax = Axes3D(self.fig)
        #self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.menu = QMenu()#右键菜单
        
        self.vmin = 0.0
        self.vmax = 0.0
        self.d = 0.0
        self.colorList = ['#00008B', '#0000FF' ,'#4169E1', '#6495ED','#87CEEB',  '#87CEFA', '#B0E0E6',\
        '#AFEEEE', '#E1FFFF','#FFFACD','#F5DEB3','#F0E68C', '#F4A460','#FF7F50', '#FF6347',\
        '#D2691E',  '#FF4500', '#FF0000','#A52A2A' ,'#800000']

        
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    
    def setRange(self, vmin, vmax):
        self.vmin = vmin
        self.vmax = vmax
        self.d = (vmax - vmin)/(len(self.colorList)-1)
        
    def setColorbar(self, colorBarTitle):
        #添加colorbar
        norm = mpl.colors.Normalize(vmin=self.vmin, vmax=self.vmax)
        cmap = plt.cm.RdYlBu_r
        cax = self.fig.add_axes([0.01, 0.1, 0.02, 0.85])
        cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, spacing='proportional')
        cb.set_label(colorBarTitle)
        
    def setTitle(self, title):
        self.ax.set_title(title)#, verticalalignment = 'top', fontproperties=self.font_song
        
    def paintCube(self, xlim, ylim, zlim,density, xdown, xup, ydown, yup, zup, xx, yy):
        # 正文体顶点和面
        verts = [(float(xlim[0]), float(ylim[0]), float(zlim[0])), (float(xlim[0]), float(ylim[1]), float(zlim[0])), (float(xlim[1]), float(ylim[1]), float(zlim[0])), (float(xlim[1]), float(ylim[0]), float(zlim[0])), (float(xlim[0]), float(ylim[0]), float(zlim[1])), (float(xlim[0]), float(ylim[1]), float(zlim[1])), (float(xlim[1]), float(ylim[1]), float(zlim[1])), (float(xlim[1]), float(ylim[0]), float(zlim[1]))]
        faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [0, 3, 7, 4]]
        poly3d = [[verts[vert_id] for vert_id in face] for face in faces]  # 获得每个面的顶点
        # 绘制顶点
        x, y, z = zip(*verts)      #将顶点元组解压为x,y,z
        #计算颜色
        if self.d == 0:
            colorIndex = 1
        else:
            colorIndex = int((density - self.vmin)/self.d)
        # 绘制多边形面
        self.ax.add_collection3d(Poly3DCollection(poly3d, facecolors=self.colorList[colorIndex], linewidths=1, alpha=0.5))     #画面
        self.ax.add_collection3d(Line3DCollection(poly3d, colors='k', linewidths=0.5, linestyles=':'))  #连线
        if(xx == 1000):
            self.ax.set_xlabel('X/km')         #设置坐标轴的属性
        else:
            self.ax.set_xlabel('X/m')         #设置坐标轴的属性
        self.ax.set_xlim3d(xdown, xup)
        if(xx == 1000):
            self.ax.set_ylabel('Y/km')         #设置坐标轴的属性
        else:
            self.ax.set_ylabel('Y/m')         #设置坐标轴的属性
        #self.ax.set_ylabel('Y/m')
        self.ax.set_ylim3d(ydown, yup)
        self.ax.set_zlabel('Z/m')
        self.ax.set_zlim3d(0, zup)
        self.ax.invert_zaxis()
    
    def saveFig(self, fileName):
        self.fig.savefig(fileName)
        
    #右键事件
    def contextMenuEvent(self, event):
        #得到窗口坐标
        #point = event.pos()
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
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
        
