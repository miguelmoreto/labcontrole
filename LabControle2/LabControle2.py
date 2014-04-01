# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 15:24:20 2014

@author: User
"""

from PyQt4 import QtCore,QtGui

from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

import MainWindow


class LabControle2(QtGui.QMainWindow,MainWindow.Ui_MainWindow):
    """
    hwl is inherited from both QtGui.QDialog and hw.Ui_Dialog
    """
    def __init__(self,parent=None):
        super(LabControle2,self).__init__(parent)
        self.setupUi(self)
        self.statusBar().showMessage('Pronto')
        
        # Adding toolbars
        self.mpltoolbarSimul = NavigationToolbar(self.mplSimul, self)
        self.VBoxLayoutSimul.addWidget(self.mpltoolbarSimul)
        
        
        x=[0,10,100]
        y=[3,4,5]

        self.mplDiagrama.axes.set_xscale('log') # Nothing Happens 
        self.mplDiagrama.axes.set_title('GRAPH') # Nothing Happens
        
        self.mplDiagrama.axes.plot(x,y)
        
        self.mplDiagrama.draw()
        
if __name__ == '__main__':
    app = QtGui.QApplication([])
    #translator = QtCore.QTranslator()
    #translator.load("LabControle2_en.qm")
    #app.installTranslator(translator)
    
    win = LabControle2()
    win.show()
    app.exec_()