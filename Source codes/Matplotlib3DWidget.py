import matplotlib
import numpy as np
matplotlib.use("Qt5Agg")#声明使用QT5
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D #axes3d
import matplotlib.pyplot as plt
from matplotlib.pyplot import *

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        # 配置中文显示
        #plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['font.family'] = ['Times New Roman']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号        
        plt.rcParams['savefig.dpi'] = 300 #图片像素
        #plt.rcParams['savefig.metadata'] = 'Creator'  #图片像素
        #plt.rcParams['figure.dpi'] = 150 #分辨率
        
        self.fig = Figure()  # 新建一个figure
        #self.ax =self.fig.add_subplot(111,projection='3d')
        self.ax = Axes3D(self.fig)
        #self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def D3Paint(self, fileName, x, y, z, xunit, yunit, zunit, colorbarTitle):
        self.ax.set_title(fileName)
        lengthX = len(x)
        lengthZ = len(z)
        times = lengthZ//lengthX
        ellipses = []
        for num in range(0,times):
            ellipses.append(z[lengthX*num:lengthX*(num+1)])
        xx = np.linspace(min(x),max(x),lengthX)     #根据数据特点分为100等份
        yy = np.linspace(min(y),max(y),lengthX)
        X,Y = np.meshgrid(xx,yy)      #将x，y坐标格网化
        #Z = pd.DataFrame(z.reshape(lengthX,lengthX))     #将插值数据转化为矩阵形式
        xunitnew = 'x/'+xunit
        yunitnew = 'y/'+yunit
        zunitnew = 'v/'+zunit
        self.ax.set_xlabel(xunitnew)
        self.ax.set_ylabel(yunitnew)
        self.ax.set_zlabel(zunitnew)
        #ax.set_zlim3d(-40,40)
        #plt.xticks(rotation= 50)  # 改变三维坐标轴的方向
        #plt.yticks(rotation= -50)
        
        #self.ax.contourf(X,Y,ellipses,cmap=cm.jet, linewidth=0.1)#1
        ellipses = np.array(ellipses)
        surf = self.ax.plot_surface(X, Y, ellipses, rstride=1, cstride=1,cmap=cm.jet)
        # 添加映射到图像中的颜色条
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
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
