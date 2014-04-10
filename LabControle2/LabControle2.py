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
        
        
        # Initial definitions:
        #self.Kpoints = 200 # Number of the K values to plot root locus        
        self.KmaxminChangeFlag = False
        self.SliderMoved = False
        
        
        x=[0,10,100]
        y=[3,4,5]


        # Adding toolbars
        self.mpltoolbarSimul = NavigationToolbar(self.mplSimul, self)
        self.mpltoolbarLGR = NavigationToolbar(self.mplLGR, self)
        self.VBoxLayoutSimul.addWidget(self.mpltoolbarSimul)
        self.VBoxLayoutLGR.addWidget(self.mpltoolbarLGR)
        
        # MATPLOTLIB API AXES CONFIG
        self.mplSimul.figure.set_facecolor('0.90')
        self.mplSimul.figure.set_tight_layout(True)
        self.mplLGR.figure.set_facecolor('0.90')
        self.mplLGR.figure.set_tight_layout(True)

        
        self.mplSimul.axes.plot(x,y)
        self.mplSimul.axes.set_xlabel(_translate("MainWindow", "Tempo [s]", None))
        self.mplSimul.axes.set_ylabel(_translate("MainWindow", "Valor", None))
        self.mplSimul.axes.set_title(_translate("MainWindow", "Simulação no tempo", None))
        self.mplSimul.axes.set_xlim(0, self.doubleSpinBoxTmax.value())
        self.mplSimul.axes.set_ylim(0, 1)
        self.mplSimul.axes.grid(True)
        self.mplSimul.axes.autoscale(True)
        self.mplSimul.draw()
        
        # Initializing system
        self.sys = Sistema.SistemaContinuo()
        
        
        self.init = 1
        
        
        # Connecting events:
        QtCore.QObject.connect(self.radioBtnOpen, QtCore.SIGNAL("clicked()"), self.feedbackOpen)
        QtCore.QObject.connect(self.radioBtnClose, QtCore.SIGNAL("clicked()"), self.feedbackClose)
        QtCore.QObject.connect(self.verticalSliderK, QtCore.SIGNAL("valueChanged(int)"), self.onSliderMove)
        # Spinboxes:
        QtCore.QObject.connect(self.doubleSpinBoxKmax, QtCore.SIGNAL("valueChanged(double)"), self.onKmaxChange)
        QtCore.QObject.connect(self.doubleSpinBoxKmin, QtCore.SIGNAL("valueChanged(double)"), self.onKminChange)
        QtCore.QObject.connect(self.doubleSpinBoxKlgr, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        QtCore.QObject.connect(self.doubleSpinBoxK, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        # Buttons:
        QtCore.QObject.connect(self.btnSimul, QtCore.SIGNAL("clicked()"), self.onBtnSimul)
        
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
    
    def onSliderMove(self,value):
        """Slider change event. 
        This event is called also when setSliderPosition is called during 
        Kmax and Kmin changes. Changes in Kmax and Kmin only alters position
        of the slider and not the gain. This is why there is this test.
        """

        gain = float(value)*float(abs(self.sys.Kmax)-abs(self.sys.Kmin))/float(self.sys.Kpontos) + self.sys.Kmin        
        self.sys.K = gain
        # Disconnect events to not enter in a event loop:
        QtCore.QObject.disconnect(self.doubleSpinBoxKlgr, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        QtCore.QObject.disconnect(self.doubleSpinBoxK, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        # Update spinboxes
        self.doubleSpinBoxKlgr.setValue(gain)
        self.doubleSpinBoxK.setValue(gain)
        QtCore.QObject.connect(self.doubleSpinBoxKlgr, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        QtCore.QObject.connect(self.doubleSpinBoxK, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)      
        
    def onKmaxChange(self,value):
        #self.KmaxminChangeFlag = True # To signal onSliderMove that it is a Kmax change
        self.sys.Kmax = value
        self.updateSliderPosition()
    
    def onKminChange(self,value):
        #self.KmaxminChangeFlag = True # To signal onSliderMove that it is a Kmin change
        self.sys.Kmin = value
        self.updateSliderPosition() # update slider position, this call also the event slider move.
    
    def onKChange(self,value):
        # Save K value in the LTI system.
        self.sys.K = value
        # Disconnect events to not enter in a event loop:
        QtCore.QObject.disconnect(self.doubleSpinBoxKlgr, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        QtCore.QObject.disconnect(self.doubleSpinBoxK, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        # Update spinboxes
        self.doubleSpinBoxKlgr.setValue(value)
        self.doubleSpinBoxK.setValue(value)
        QtCore.QObject.connect(self.doubleSpinBoxKlgr, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        QtCore.QObject.connect(self.doubleSpinBoxK, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)        
        # Update slider position.
        self.updateSliderPosition()

    def onBtnSimul(self):
        
        Tmax = self.doubleSpinBoxTmax.value()
        self.sys.X0r = None
        self.sys.X0w = None
        
        stringR = self.sys.Rt
        stringW = self.sys.Wt
        
        delta_t = 0.01
        
        self.statusBar().showMessage(_translate("MainWindow", "Iniciando simulação...", None))
        # Create the input vectors r(t) and w(t):
        t,r,w = self.sys.CriaEntrada(stringR, stringW, 0, Tmax, delta_t, 
                            self.sys.InstRt, self.sys.InstWt)
        
        # Perform a time domain simulation:
        y = self.sys.Simulacao(t, r, w)        
        
        self.statusBar().showMessage(_translate("MainWindow", "Simulação concluída.", None))
        
        self.mplSimul.figure.clf()
        ax = self.mplSimul.figure.add_subplot(111)
        legend = []
        flag = 0
        
        
        if (self.checkBoxEntrada.isChecked()):
            ax.plot(t,r,'b')
            legend.append(_translate("MainWindow", "Entrada: u(t)", None))
            flag = 1
        if (self.checkBoxSaida.isChecked()):
            ax.plot(t,y,'r')
            legend.append(_translate("MainWindow", "Saída: y(t)", None))
            flag = 1
        
        
        self.mplSimul.draw()
        print Tmax
        pass
    
    def updateSliderPosition(self):
        position = (float(self.sys.Kpontos) * (self.sys.K - self.sys.Kmin))/(abs(self.sys.Kmax)+abs(self.sys.Kmin))
        # Disconnect events to not enter in a event loop:
        QtCore.QObject.disconnect(self.verticalSliderK, QtCore.SIGNAL("valueChanged(int)"), self.onSliderMove)
        self.verticalSliderK.setSliderPosition(int(position))
        QtCore.QObject.connect(self.verticalSliderK, QtCore.SIGNAL("valueChanged(int)"), self.onSliderMove)
        
if __name__ == '__main__':
    app = QtGui.QApplication([])
    #translator = QtCore.QTranslator()
    #translator.load("LabControle2_en.qm")
    #app.installTranslator(translator)
    
    win = LabControle2()
    win.show()
    app.exec_()