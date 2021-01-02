from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from InversionSection import InversionSection

class DialogInversionSection(QDialog):
    def __init__(self, parent, controlNumber, tableWidget, flag, index):
        super(DialogInversionSection, self).__init__(parent)
        self.father = parent
        
        label1 = QLabel("Z = ")
        label2 = QLabel("Y = ")
        label3 = QLabel("X = ")
        labelUnit1 = QLabel("m")
        labelUnit2 = QLabel("m")
        labelUnit3 = QLabel("m")
        label4 = QLabel("Painting Title:")
        self.title = QLineEdit()
        label5 = QLabel("ColorBar Title:")
        self.colorbarTitle = QLineEdit()
        
        self.cb1 = QComboBox()
        self.cbItems1 = []
        for i in range(0, len(tableWidget.zc)):
            self.cbItems1.append(str(tableWidget.zc[i]))
        self.cb1.addItems(self.cbItems1)
        
        self.cb2 = QComboBox()
        self.cbItems2 = []
        for i in range(0, len(tableWidget.y), tableWidget.nx):
            self.cbItems2.append(str(tableWidget.y[i]))
        self.cb2.addItems(self.cbItems2)
        
        self.cb3 = QComboBox()
        self.cbItems3 = []
        for i in range(0, tableWidget.nx):
            self.cbItems3.append(str(tableWidget.x[i]))
        self.cb3.addItems(self.cbItems3)
        
        ok = QPushButton("OK", self)
        cancel = QPushButton("Cancel", self)
        layoutBottom = QHBoxLayout()
        layoutBottom.addStretch(1)
        layoutBottom.addWidget(ok, 1)
        layoutBottom.addStretch(2)
        layoutBottom.addWidget(cancel, 1)
        layoutBottom.addStretch(1)
        
        layout1 = QHBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(label1, 2)
        layout1.addWidget(self.cb1, 1)
        layout1.addWidget(labelUnit1)
        layout1.addStretch(1)
        
        layout2 = QHBoxLayout()
        layout2.addStretch(1)
        layout2.addWidget(label2, 2)
        layout2.addWidget(self.cb2, 1)
        layout2.addWidget(labelUnit2)
        layout2.addStretch(1)
        
        layout3 = QHBoxLayout()
        layout3.addStretch(1)
        layout3.addWidget(label3, 2)
        layout3.addWidget(self.cb3, 1)
        layout3.addWidget(labelUnit3)
        layout3.addStretch(1)
        
        layout4 = QHBoxLayout()
        layout4.addStretch(1)
        layout4.addWidget(label4, 1)
        layout4.addWidget(self.title, 1)
        layout4.addStretch(1)
        
        layout5 = QHBoxLayout()
        layout5.addStretch(1)
        layout5.addWidget(label5, 1)
        layout5.addWidget(self.colorbarTitle, 1)
        layout5.addStretch(1)
        
        layout = QVBoxLayout()
        if controlNumber == 1:
            layout.addLayout(layout1)
        elif controlNumber == 2:
            layout.addLayout(layout2)
        elif controlNumber == 3:
            layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(layoutBottom)
        
        self.setLayout(layout)
        self.setWindowTitle("Choose Data")
        
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        ok.clicked.connect(lambda:self.on_ok_clicked(controlNumber, tableWidget, flag, index))
        cancel.clicked.connect(self.on_cancel_clicked)
        
    def on_cancel_clicked(self):
        self.close()
        return
        
    def on_ok_clicked(self, controlNumber, tableWidget, flag, index):
        inversionTitle = self.title.text()
        inversionColorbarTitle = self.colorbarTitle.text()
        self.father.flag = 1
        position = self.father.tab.currentIndex()
        root = self.father.tree.topLevelItem(position-1)
        root_name = root.text(0)
        if inversionTitle!="":
            for key, value in self.father.tree_record[root_name].items():
                if 'title' not in self.father.tree_record[root_name][key]:continue
                if inversionTitle == self.father.tree_record[root_name][key]['title']:
                    QMessageBox.information(self, "ATTENTION", "Painting Title already exists")
                    return
        
        m_result = []
        type = "Inversion_Paint_parallel_"
        if flag == 0:
            m_result = tableWidget.m_result
            dz = tableWidget.dz
        if controlNumber == 1:
            id = self.cb1.currentIndex()
            z = m_result[id]
            x1 = tableWidget.x[0]
            x2 = tableWidget.x[-1]
            y1 = tableWidget.y[0]
            y2 = tableWidget.y[-1]
            dx = tableWidget.dx
            dy = tableWidget.dy
            depth = self.cbItems1[id]
            inversionSection = InversionSection()
            if inversionTitle == "":
                inversionTitle = "Z = "+str(depth)+"m X-Y Profile"
            
            order = 1
            flag = 0
            name_temp = inversionTitle
            while flag == 0:
                flag = 1
                for key, value in self.father.tree_record[root_name].items():
                    if 'title' not in self.father.tree_record[root_name][key]:
                        flag = 2
                        continue
                    if name_temp == self.father.tree_record[root_name][key]['title']:
                        flag = 0
                        break
                if flag ==2:    continue
                if flag == 1:    inversionTitle = name_temp
                name_temp = inversionTitle + '_' +str(order)
                order = order + 1    
            inversionSection.mpl.setTitle(inversionTitle)
            inversionSection.mpl.xy_section(x1, x2, y1, y2, z, dx, dy, dz, depth, inversionColorbarTitle)
            
            sub = QMdiSubWindow()
            sub.setWindowIcon(QIcon(".\\image\\logo.png"))
            sub.setWidget(inversionSection)
            sub.setWindowTitle(inversionTitle)
            mid=self.father.tab.currentWidget()
            mid.addSubWindow(sub)
            sub.show()
            
            selectedList = self.father.tree.selectedItems()
            for i in range(0, len(selectedList)):
                selectedList[i].setSelected(0)
            child3 = QTreeWidgetItem(root)
            child3.setText(0, inversionTitle)
            child3.setSelected(1)
            root.setExpanded(1)
            #tree_record
            child_name = 'view_'+str(self.father.paintCount[position-1]) 
            
            self.father.tree_record[root_name][child_name] ={'title':inversionTitle,'type':type+'XY', \
            'color_Bar_Title':str(inversionColorbarTitle), 'id':str(id),  'depth':str(depth), 'index':index}
            self.father.paintCount[position-1] = self.father.paintCount[position-1] +1
        if controlNumber == 2:
            id = self.cb2.currentIndex()
            y = []
            for i in range(0, tableWidget.nz):
                temp = []
                for j in range(0, tableWidget.nx):
                    temp.append(m_result[i][id][j])
                y.append(temp)
            x1 = tableWidget.x[0]
            x2 = tableWidget.x[-1]
            z1 = tableWidget.zc[0]
            z2 = tableWidget.zc[-1]
            dx = tableWidget.dx
            dy = tableWidget.dy
            depth = self.cbItems2[id]
            inversionSection = InversionSection()
            if inversionTitle == "":
                inversionTitle = "Y = "+str(depth)+"m X-Z Profile"
            
            order = 1
            flag = 0
            name_temp = inversionTitle
            while flag == 0:
                flag = 1
                for key, value in self.father.tree_record[root_name].items():
                    if 'title' not in self.father.tree_record[root_name][key]:
                        flag = 2
                        continue
                    if name_temp == self.father.tree_record[root_name][key]['title']:
                        flag = 0
                        break
                if flag ==2:    continue
                if flag == 1:    inversionTitle = name_temp
                name_temp = inversionTitle + '_' +str(order)
                order = order + 1    
                
            inversionSection.mpl.setTitle(inversionTitle)
            inversionSection.mpl.xz_section(x1, x2, z1, z2, y, dx, dy, dz, depth, inversionColorbarTitle)
            
            sub = QMdiSubWindow()
            sub.setWindowIcon(QIcon(".\\image\\logo.png"))
            sub.setWidget(inversionSection)
            sub.setWindowTitle(inversionTitle)
            mid=self.father.tab.currentWidget()
            mid.addSubWindow(sub)
            sub.show()
            
            selectedList = self.father.tree.selectedItems()
            for i in range(0, len(selectedList)):
                selectedList[i].setSelected(0)
            child3 = QTreeWidgetItem(root)
            child3.setText(0, inversionTitle)
            child3.setSelected(1)
            root.setExpanded(1)
            #tree_record
            child_name = 'view_'+str(self.father.paintCount[position-1]) 
            self.father.tree_record[root_name][child_name] ={'title':inversionTitle,'type':type+'XZ', \
            'color_Bar_Title':str(inversionColorbarTitle), 'id':str(id), 'depth':str(depth), 'index':index}
            self.father.paintCount[position-1] = self.father.paintCount[position-1] +1
        if controlNumber == 3:
            id = self.cb3.currentIndex()
            x = []
            for i in range(0, tableWidget.nz):
                temp = []
                for j in range(0, tableWidget.ny):
                    temp.append(m_result[i][j][id])
                x.append(temp)
            z1 = tableWidget.zc[0]
            z2 = tableWidget.zc[-1]
            y1 = tableWidget.y[0]
            y2 = tableWidget.y[-1]
            dx = tableWidget.dx
            dy = tableWidget.dy
            depth = self.cbItems3[id]
            inversionSection = InversionSection()
            if inversionTitle == "":
                inversionTitle = "X = "+str(depth)+"m Y-Z Profile"
            
            order = 1
            flag = 0
            name_temp = inversionTitle
            while flag == 0:
                flag = 1
                for key, value in self.father.tree_record[root_name].items():
                    if 'title' not in self.father.tree_record[root_name][key]:
                        flag = 2
                        continue
                    if name_temp == self.father.tree_record[root_name][key]['title']:
                        flag = 0
                        break
                if flag ==2:    continue
                if flag == 1:    inversionTitle = name_temp
                name_temp = inversionTitle + '_' +str(order)
                order = order + 1    
            inversionSection.mpl.setTitle(inversionTitle)
            inversionSection.mpl.yz_section(y1, y2, z1, z2, x, dx, dy, dz, depth, inversionColorbarTitle)
            
            sub = QMdiSubWindow()
            sub.setWindowIcon(QIcon(".\\image\\logo.png"))
            sub.setWidget(inversionSection)
            sub.setWindowTitle(inversionTitle)
            mid=self.father.tab.currentWidget()
            mid.addSubWindow(sub)
            sub.show()
            
            selectedList = self.father.tree.selectedItems()
            for i in range(0, len(selectedList)):
                selectedList[i].setSelected(0)
            child3 = QTreeWidgetItem(root)
            child3.setText(0, inversionTitle)
            child3.setSelected(1)
            root.setExpanded(1)
            #tree_record
            child_name = 'view_'+str(self.father.paintCount[position-1]) 
            self.father.tree_record[root_name][child_name] ={'title':inversionTitle,'type':type+'YZ', \
            'color_Bar_Title':str(inversionColorbarTitle), 'id':str(id), 'depth':str(depth), 'index':index}
            self.father.paintCount[position-1] = self.father.paintCount[position-1] +1
        self.close()
        return              
