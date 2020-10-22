from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TreeWidget(QTreeWidget):
    def __init__(self, parent):
        super(TreeWidget, self).__init__(parent)
        self.father = parent
        
        #右键事件
        self.rightKeyMenu = QMenu()
        self.actionSave = QAction("Save", self)
        self.actionDelete = QAction("Delete", self)
        self.actionExpand = QAction("Spread", self)
        self.actionZhe = QAction("Fold", self)
        #正演数据的右键事件
        self.actionPaint = QAction("Painting",  self)
        self.actionForwardingSave = QAction("Save Data", self)
        
        #信号槽
        self.actionSave.triggered.connect(self.on_Save)
        self.actionDelete.triggered.connect(self.on_Delete)
        self.actionExpand.triggered.connect(self.on_Expand)
        self.actionZhe.triggered.connect(self.on_Zhe)
        self.actionPaint.triggered.connect(self.father.paintModel)
        self.actionForwardingSave.triggered.connect(self.father.forwardingSave)
    #保存操作
    def on_Save(self):
        selectedList = self.father.tree.selectedItems()
        if len(selectedList)!=1:
            return
        item = selectedList[0]
        root = item.parent()
        ind = root.indexOfChild(item)
        mw = self.father.tab.currentWidget().subWindowList()[ind].widget()
        print(ind)
        name = QFileDialog.getSaveFileName(self, 'Open File', './', '*.png *.pdf *.jpg')
        mw.mpl.saveFig(name[0])
        self.father.status.showMessage("Picture Saves Successfully", 3000)
        
    #删除操作
    def on_Delete(self):
        selectedList = self.father.tree.selectedItems()
        if len(selectedList)!=1:
            return
        item = selectedList[0]
        root = item.parent()
        ind = root.indexOfChild(item)
        #更改tree_record
        root_name = root.text(0)
        order = 0
        for key,  value in self.father.tree_record[root_name].items():
            if order == ind:
                self.father.tree_record[root_name].pop(key)
                break
            order = order +1
        root.takeChild(ind)
        mdiarea=self.father.tab.currentWidget()
        mdiarea.removeSubWindow(mdiarea.subWindowList()[ind])
        
    #展开操作
    def on_Expand(self):
        selectedList = self.father.tree.selectedItems()
        if len(selectedList)!=1:
            return
        item = selectedList[0]
        item.setExpanded(1)
        
    #折叠操作
    def on_Zhe(self):
        selectedList = self.father.tree.selectedItems()
        if len(selectedList)!=1:
            return
        item = selectedList[0]
        item.setExpanded(0)
        
    #右键事件
    def contextMenuEvent(self, event):
        self.rightKeyMenu.clear()
        #得到窗口坐标
        point = event.pos()
        item = self.itemAt(point)
        if item==None:
            return
        topCount = self.father.tree.topLevelItemCount()
        for i in range(0,  topCount):
            if self.father.tree.topLevelItem(i)==item:
                if item.isExpanded()==0:
                    self.rightKeyMenu.addAction(self.actionExpand)
                else:
                    self.rightKeyMenu.addAction(self.actionZhe)
            if self.father.tree.topLevelItem(i)==item.parent():
                #如果是第一个孩子，则没有右键目录
                #如果是file data，则没有右键目录
                #如果是正演产生的数据，则加上 painting 和 save data
                root = item.parent().text(0)
                child = item.text(0)
                if child not in self.father.tree_record[root]:
                    self.rightKeyMenu.addAction(self.actionSave)
                    self.rightKeyMenu.addAction(self.actionDelete)
                elif self.father.tree_record[root][child]['type'] == 'FileData':
                    return 
                elif self.father.tree_record[root][child]['type'] == 'ForwardingData':
                    self.rightKeyMenu.addAction(self.actionPaint)
                    self.rightKeyMenu.addAction(self.actionForwardingSave)
                elif self.father.tree_record[root][child]['type'] == "ForwardingModelFlag":
                    self.rightKeyMenu.addAction(self.actionSave)
                else:
                    self.rightKeyMenu.addAction(self.actionSave)
                    self.rightKeyMenu.addAction(self.actionDelete)
        #菜单出现的位置为当前鼠标的位置
        self.rightKeyMenu.exec(QCursor.pos())
        event.accept()
