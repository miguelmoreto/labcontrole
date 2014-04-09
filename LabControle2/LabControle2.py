# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 15:24:20 2014

@author: User
"""

from PyQt4 import QtCore,QtGui, QtSvg

from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

import MainWindow
import Sistema


try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class LabControle2(QtGui.QMainWindow,MainWindow.Ui_MainWindow):
    """
    hwl is inherited from both QtGui.QDialog and hw.Ui_Dialog
    """
    def __init__(self,parent=None):
        self.init = 0
        super(LabControle2,self).__init__(parent)
        
        # Init variables:
        self.SVGRect = QtCore.QRectF()
        self.GraphSize = QtCore.QSize()
        
        self.setupUi(self)
        #self.statusBar().showMessage('Pronto')
        self.tabWidget.setCurrentIndex(0)
        
        # Adding toolbars
        self.mpltoolbarSimul = NavigationToolbar(self.mplSimul, self)
        self.VBoxLayoutSimul.addWidget(self.mpltoolbarSimul)
        
        self.image = QtGui.QImage()        
        
        self.graphicsView.setScene(QtGui.QGraphicsScene(self))
        
        self.graphicsView.setViewport(QtGui.QWidget())
        
        svg_file = QtCore.QFile('diagramOpened.svg')
        if not svg_file.exists():
            QtGui.QMessageBox.critical(self, "Open SVG File",
                    "Could not open file '%s'." % 'diagramOpened.svg')

            self.outlineAction.setEnabled(False)
            self.backgroundAction.setEnabled(False)
            return        
        
        self.scene = self.graphicsView.scene()
        self.scene.clear()
        self.graphicsView.resetTransform()
        
        self.svgItem = QtSvg.QGraphicsSvgItem(svg_file.fileName())        
        self.svgItem.setFlags(QtGui.QGraphicsItem.ItemClipsToShape)
        self.svgItem.setCacheMode(QtGui.QGraphicsItem.NoCache)
        #self.svgItem.setZValue(0)
        
        self.backgroundItem = QtGui.QGraphicsRectItem(self.svgItem.boundingRect())
        self.backgroundItem.setBrush(QtCore.Qt.gray)
        self.backgroundItem.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.backgroundItem.setVisible(True)
        self.backgroundItem.setZValue(-1)

        #self.scene.addItem(self.backgroundItem)
        self.scene.addItem(self.svgItem)
        
        x=[0,10,100]
        y=[3,4,5]


        self.mplSimul.axes.set_xscale('log') # Nothing Happens 
        self.mplSimul.axes.set_title('GRAPH') # Nothing Happens
        
        self.mplSimul.axes.plot(x,y)
        
        self.mplSimul.draw()
        
        # Initializing system
        self.sys = Sistema.SistemaContinuo()
        
        
        self.init = 1
        
        self.groupBoxC.setStyleSheet("QGroupBox { border:2px solid rgb(175, 198, 233);border-radius: 3px;} QGroupBox::title {background-color: transparent;}")
        #self.groupBoxC.setStyleSheet("QGroupBox::title {background-color: transparent;padding:2 13px;}")        
        
        # Connecting events:
        QtCore.QObject.connect(self.radioBtnOpen, QtCore.SIGNAL("clicked()"), self.feedbackOpen)
        QtCore.QObject.connect(self.radioBtnClose, QtCore.SIGNAL("clicked()"), self.feedbackClose)
        
        self.statusBar().showMessage(_translate("MainWindow", "Pronto.", None))        
        
               
    def feedbackOpen(self):
        """Open Feedback """ 
        svg_file = QtCore.QFile('diagramOpened.svg')
        if not svg_file.exists():
            QtGui.QMessageBox.critical(self, "Open SVG File",
                                       "Could not open file '%s'." % 'diagramOpened.svg')
            self.outlineAction.setEnabled(False)
            self.backgroundAction.setEnabled(False)
            return   
        self.sys.Malha = 'Aberta'
        
        # Update svg image with open loop.
        self.scene.clear()
        self.svgItem = QtSvg.QGraphicsSvgItem(svg_file.fileName())
        self.scene.addItem(self.svgItem)
        self.statusBar().showMessage(_translate("MainWindow", "Malha aberta.", None))
        
    def feedbackClose(self):
        """Close Feedback """    
        svg_file = QtCore.QFile('diagramClosed.svg')
        if not svg_file.exists():
            QtGui.QMessageBox.critical(self, "Open SVG File",
                                       "Could not open file '%s'." % 'diagramClosed.svg')
            self.outlineAction.setEnabled(False)
            self.backgroundAction.setEnabled(False)
            return   

        self.sys.Malha = 'Fechada'
        
        # Update svg image with closed loop.
        self.scene.clear()
        self.svgItem = QtSvg.QGraphicsSvgItem(svg_file.fileName())
        self.scene.addItem(self.svgItem)
        
        self.statusBar().showMessage(_translate("MainWindow", "Malha fechada.", None))        
        
if __name__ == '__main__':
    app = QtGui.QApplication([])
    #translator = QtCore.QTranslator()
    #translator.load("LabControle2_en.qm")
    #app.installTranslator(translator)
    
    win = LabControle2()
    win.show()
    app.exec_()