# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 15:24:20 2014

@author: User
"""

from PyQt4 import QtCore,QtGui, QtSvg

from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

import MainWindow


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
        self.statusBar().showMessage('Pronto')
        
        # Adding toolbars
        self.mpltoolbarSimul = NavigationToolbar(self.mplSimul, self)
        self.VBoxLayoutSimul.addWidget(self.mpltoolbarSimul)
        
        self.image = QtGui.QImage()        
        
        self.graphicsView.setScene(QtGui.QGraphicsScene(self))
        
        self.graphicsView.setViewport(QtGui.QWidget())
        
        svg_file = QtCore.QFile('cubic.svg')
        if not svg_file.exists():
            QtGui.QMessageBox.critical(self, "Open SVG File",
                    "Could not open file '%s'." % 'cubic.svg')

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

        self.scene.addItem(self.backgroundItem)
        self.scene.addItem(self.svgItem)
        
        self.SVGRect = self.svgItem.boundingRect()
        self.GraphSize = self.graphicsView.size()
        print 'SVG rect'
        print self.SVGRect.width(), self.SVGRect.height()
        print 'Graphsize'
        print self.GraphSize.width(), self.GraphSize.height()
        #print self.graphicsView.viewport().size()
        #print self.scene.width()
        self.graphicsView.scale(self.GraphSize.width()/self.SVGRect.width(), self.GraphSize.height()/self.SVGRect.height())
        
        self.oldW = self.graphicsView.viewport().size().width()#self.GraphSize.width();
        self.oldH = self.graphicsView.viewport().size().height()#self.GraphSize.height();
        print self.oldW, self.oldH
        #self.scene.update (10, 10, 300, 300)
        #print s.width ()
        
        x=[0,10,100]
        y=[3,4,5]

        self.mplDiagrama.axes.set_xscale('log') # Nothing Happens 
        self.mplDiagrama.axes.set_title('GRAPH') # Nothing Happens
        
        self.mplDiagrama.axes.plot(x,y)
        
        self.mplDiagrama.draw()
        
        
        QtCore.QObject.connect(self, QtCore.SIGNAL("resize()"), self.onResize)
        
        self.init = 1
        
    def resizeEvent(self, evt=None):
        self.emit(QtCore.SIGNAL("resize()"))
        
    def onResize(self):
        self.SVGRect = self.svgItem.boundingRect()
        self.GraphSize = self.graphicsView.size()
        print 'SVG rect'
        print self.SVGRect.width(), self.SVGRect.height()
        print 'Graphsize'
        print self.GraphSize.width(), self.GraphSize.height()
        #print self.image.s
        #print self.scene.width()
        #print self.graphicsView.size()
        sx = self.oldW/float(self.graphicsView.viewport().size().width())
        sy = self.oldH/float(self.graphicsView.viewport().size().height())
        ##print sx, sy
        ##self.graphicsView.scale(sx, sy)
        #print self.graphicsView.viewport().size()
        self.oldW = self.graphicsView.viewport().size().width()
        self.oldH = self.graphicsView.viewport().size().height()
        ##print self.oldW, self.oldH
        
        
if __name__ == '__main__':
    app = QtGui.QApplication([])
    #translator = QtCore.QTranslator()
    #translator.load("LabControle2_en.qm")
    #app.installTranslator(translator)
    
    win = LabControle2()
    win.show()
    app.exec_()