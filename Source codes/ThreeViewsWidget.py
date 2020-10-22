import matplotlib
matplotlib.use("Qt5Agg")#声明使用QT5
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
# from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import matplotlib.patches as patches
# from matplotlib.font_manager import FontProperties
import matplotlib as mpl

class MyMpl(FigureCanvas):
    def __init__(self, parent=None):
        # 配置中文显示
        plt.rcParams['font.family'] = ['Times New Roman']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号        
        plt.rcParams['savefig.dpi'] = 300 #图片像素
        
        self.fig = Figure()  # 新建一个figure
        self.axes = self.fig.add_subplot(111, aspect='equal')  # 建立一个子图，如果要建立复合图，可以在这里修改
        #self.setAlignment(Qt.AlignCenter)
        
        self.vmin = 0.0
        self.vmax = 0.0
        self.d = 0.0
        self.colorList = ['darkblue','blue','royalblue','cornflowerblue','steelblue', 'deepskyblue',\
        'skyblue','lightblue','lightcyan','greenyellow','yellowgreen','yellow','gold','goldenrod',\
        'orange','darkorange','orangered','red','firebrick','maroon']
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
    def setTitle(self, title):
        self.axes.set_title(title)
    
    def setRange(self, vmin, vmax):
        self.vmin = vmin
        self.vmax = vmax
        self.d = (vmax - vmin)/(len(self.colorList)-1)
        
    def setColorbar(self, colorbarTitle):
        #添加colorbar
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
        #self.axes.invert_yaxis()
        #计算颜色
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
        #计算颜色
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
        #计算颜色
        if self.d == 0:
            colorIndex = 1
        else:
            colorIndex = int((density - self.vmin)/self.d)
        self.axes.add_patch(patches.Rectangle((x, y), xdis, ydis, color = self.colorList[colorIndex]))
        self.axes.set_xlabel('x/m')
        self.axes.set_ylabel('y/m')
        self.axes.axis([xdown, xup, ydown, yup])
        #self.fig.tight_layout()#紧凑
    
    def saveFig(self, fileName):
        self.fig.savefig(fileName)
     
class ThreeViewsWidget(QWidget):
    def __init__(self, parent=None):
        super(ThreeViewsWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMpl(self)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
