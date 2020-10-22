import matplotlib
matplotlib.use("Qt5Agg")#声明使用QT5
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
#from matplotlib.font_manager import FontProperties

class MyMplPara(FigureCanvas):
    def __init__(self, parent=None):
        # 配置中文显示
        plt.rcParams['font.family'] = ['Times New Roman']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号        
        plt.rcParams['savefig.dpi'] = 300 #图片像素
        #plt.rcParams['figure.dpi'] = 150 #分辨率
        
        self.fig = Figure()  # 新建一个figure
        self.axes = self.fig.add_subplot(111, aspect='equal')
        
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
    def setTitle(self, title):
        self.axes.set_title(title)

    def xy_section(self, x1, x2, y1, y2, z, dx, dy, dz, deep, colorbarTitle):
        xx = np.linspace(x1, x2, int((x2-x1)/dx+1))     #根据数据特点分为20等份
        yy = np.linspace(y1, y2, int((y2-y1)/dy+1))
        X,Y = np.meshgrid(xx,yy)#将x，y坐标格网化
        
        CS = self.axes.contourf(X,Y,z,10, cmap=cm.jet)
        cbar = self.fig.colorbar(CS, shrink=1, aspect=10,)
        if colorbarTitle == "":
            cbar.ax.set_ylabel("density(g/cm^3)")
        else:
            cbar.ax.set_ylabel(colorbarTitle)
        self.axes.tick_params(labelsize=9)
        #labels = self.axes.get_xticklabels() + self.axes.get_yticklabels()
        #[label.set_fontname('Times New Roman') for label in labels]
        self.axes.set_xlabel('x/m')
        self.axes.set_ylabel('y/m')
        
    def xz_section(self, x1,x2, z1, z2, value, dx, dy, dz, deep, colorbarTitle):
        xx = np.linspace(x1, x2, int((x2-x1)/dx+1))     #根据数据特点分为20等份
        zz = np.linspace(z1, z2, int((z2-z1)/dz+1))
        X,Z = np.meshgrid(xx,zz)      #将x，y坐标格网化
    
        CS = self.axes.contourf(X,Z,value,10, cmap=cm.jet)
        cbar = self.fig.colorbar(CS, shrink=1, aspect=10,)
        if colorbarTitle == "":
            cbar.ax.set_ylabel("density(g/cm^3)")
        else:
            cbar.ax.set_ylabel(colorbarTitle)
        self.axes.tick_params(labelsize=9)
        #labels = self.axes.get_xticklabels() + self.axes.get_yticklabels()
        #[label.set_fontname('Times New Roman') for label in labels]
        self.axes.set_xlabel('x/m')
        self.axes.set_ylabel('z/m')
        #self.axes.set_title('Y = '+ deep +'m 时的XZ剖面图')
        self.axes.invert_yaxis()
        
    def yz_section(self, y1,y2, z1, z2, value, dx, dy, dz, deep, colorbarTitle):
        yy = np.linspace(y1, y2, int((y2-y1)/dy+1))     #根据数据特点分为20等份
        zz = np.linspace(z1, z2, int((z2-z1)/dz+1))
        Y,Z = np.meshgrid(yy,zz)      #将x，y坐标格网化
        CS = self.axes.contourf(Y,Z,value,10, cmap=cm.jet)
        cbar = self.fig.colorbar(CS, shrink=1, aspect=10,)
        if colorbarTitle == "":
            cbar.ax.set_ylabel("density(g/cm^3)")
        else:
            cbar.ax.set_ylabel(colorbarTitle)
        self.axes.tick_params(labelsize=9)
        #labels = self.axes.get_xticklabels() + self.axes.get_yticklabels()
        #[label.set_fontname('Times New Roman') for label in labels]
        self.axes.set_xlabel('y/m')
        self.axes.set_ylabel('z/m')
        #self.axes.set_title('X = '+ deep +'m 时的YZ剖面图')
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
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
