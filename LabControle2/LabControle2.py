# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 15:24:20 2014

@author: User
"""

from PyQt4 import QtCore,QtGui, QtSvg

from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

import MainWindow
import Sistema
import utils
import numpy

           

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

MESSAGE = "<p><b>Sobre o LabControle2</b></p>" \
            "<p>O LabControle é um software desenvolvido " \
            "para ser utilizado em atividades de laboratório de " \
            "disciplinas de Sistemas de Controle.</p>" \
            "<p>O LabControle2 foi desenvolvido por Miguel Moreto" \
            "professor do Departamento de Engenharia Elétrica da UFSC"\
            "para uso nos laboratórios da disciplina EEL7063 - Sistemas "\
            "de Controle.</p>" \
            "<p>O LabControle2 foi desenvolvido em linguagem Python "\
            "e seu código é livre, podendo ser acessado no site:</p>"\
            "<p><b>http://sites.google.com/site/controlelab/</b></p>"

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
        # Adding toolbar spacer:
        empty = QtGui.QWidget()
        empty.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        self.toolBar.insertWidget(self.actionClose,empty)
        
        # Set diagram the current tab:
        self.tabWidget.setCurrentIndex(0)
        
        
        self.image = QtGui.QImage()        
        self.graphicsView.setScene(QtGui.QGraphicsScene(self))
        self.graphicsView.setViewport(QtGui.QWidget())
        
        # Load initial SVG file
        svg_file = QtCore.QFile('diagram1Opened.svg')
        if not svg_file.exists():
            QtGui.QMessageBox.critical(self, "Open SVG File",
                    "Could not open file '%s'." % 'diagram1Opened.svg')

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
        
        #self.backgroundItem = QtGui.QGraphicsRectItem(self.svgItem.boundingRect())
        #self.backgroundItem.setBrush(QtCore.Qt.gray)
        #self.backgroundItem.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        #self.backgroundItem.setVisible(True)
        #self.backgroundItem.setZValue(-1)

        self.scene.addItem(self.svgItem)
        
        
        # Initial definitions:
        self.checkBoxPert.setDisabled(True) # Perturbation is disabled by default
        self.checkBoxControle.setDisabled(True) # Control signal is disabled by default

        # Adding toolbars
        self.mpltoolbarSimul = NavigationToolbar(self.mplSimul, self)
        self.mpltoolbarLGR = NavigationToolbar(self.mplLGR, self)
        self.mpltoolbarBode = NavigationToolbar(self.mplBode, self)
        self.mpltoolbarNyquist = NavigationToolbar(self.mplNyquist, self)
        self.VBoxLayoutSimul.addWidget(self.mpltoolbarSimul)
        self.VBoxLayoutLGR.addWidget(self.mpltoolbarLGR)
        self.VBoxLayoutBode.addWidget(self.mpltoolbarBode)
        self.VBoxLayoutNyquist.addWidget(self.mpltoolbarNyquist)
        
        # MATPLOTLIB API AXES CONFIG
        self.mplSimul.figure.set_facecolor('0.90')
        self.mplSimul.figure.set_tight_layout(True)
        self.mplLGR.figure.set_facecolor('0.90')
        self.mplLGR.figure.set_tight_layout(True)
        self.mplBode.figure.set_facecolor('0.90')
        self.mplBode.figure.set_tight_layout(True)

        
        #self.mplSimul.axes.plot(x,y)
        self.mplSimul.axes.set_xlabel(_translate("MainWindow", "Tempo [s]", None))
        self.mplSimul.axes.set_ylabel(_translate("MainWindow", "Valor", None))
        self.mplSimul.axes.set_title(_translate("MainWindow", "Simulação no tempo", None))
        self.mplSimul.axes.set_xlim(0, self.doubleSpinBoxTmax.value())
        self.mplSimul.axes.set_ylim(0, 1)
        self.mplSimul.axes.grid(True)
        #self.mplSimul.axes.autoscale(True)
        self.mplSimul.draw()
        
        self.mplBode.figure.clf()
        self.mplNyquist.figure.clf()
        
        # Initializing system
        self.sys = Sistema.SistemaContinuo()
        # Updating values from GUI:
        self.sys.Fmin = self.doubleSpinFmin.value()
        self.sys.Fmax = self.doubleSpinFmax.value()
        self.sys.Fpontos = self.doubleSpinBodeRes.value()
                
        self.init = 1
                
        # Connecting events:
        QtCore.QObject.connect(self.radioBtnOpen, QtCore.SIGNAL("clicked()"), self.feedbackOpen)
        QtCore.QObject.connect(self.radioBtnClose, QtCore.SIGNAL("clicked()"), self.feedbackClose)
        QtCore.QObject.connect(self.verticalSliderK, QtCore.SIGNAL("valueChanged(int)"), self.onSliderMove)
        QtCore.QObject.connect(self.comboBoxSys, QtCore.SIGNAL("currentIndexChanged(int)"), self.onChangeSystem)
        # Spinboxes:
        QtCore.QObject.connect(self.doubleSpinBoxKmax, QtCore.SIGNAL("valueChanged(double)"), self.onKmaxChange)
        QtCore.QObject.connect(self.doubleSpinBoxKmin, QtCore.SIGNAL("valueChanged(double)"), self.onKminChange)
        QtCore.QObject.connect(self.doubleSpinBoxKlgr, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        QtCore.QObject.connect(self.doubleSpinBoxK, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        QtCore.QObject.connect(self.doubleSpinBoxTmax, QtCore.SIGNAL("valueChanged(double)"), self.onTmaxChange)
        QtCore.QObject.connect(self.doubleSpinBoxRtime, QtCore.SIGNAL("valueChanged(double)"), self.onRtimeChange)
        QtCore.QObject.connect(self.doubleSpinBoxRnoise, QtCore.SIGNAL("valueChanged(double)"), self.onRnoiseChange)
        QtCore.QObject.connect(self.doubleSpinBoxWtime, QtCore.SIGNAL("valueChanged(double)"), self.onWtimeChange)
        QtCore.QObject.connect(self.doubleSpinBoxWnoise, QtCore.SIGNAL("valueChanged(double)"), self.onWnoiseChange)
        QtCore.QObject.connect(self.doubleSpinFmin, QtCore.SIGNAL("valueChanged(double)"), self.onBodeFminChange)
        QtCore.QObject.connect(self.doubleSpinFmax, QtCore.SIGNAL("valueChanged(double)"), self.onBodeFmaxChange)
        QtCore.QObject.connect(self.doubleSpinBodeRes, QtCore.SIGNAL("valueChanged(double)"), self.onBodeResChange)
        QtCore.QObject.connect(self.doubleSpinFminNyq, QtCore.SIGNAL("valueChanged(double)"), self.onNyquistFminChange)
        QtCore.QObject.connect(self.doubleSpinFmaxNyq, QtCore.SIGNAL("valueChanged(double)"), self.onNyquistFmaxChange)        
        QtCore.QObject.connect(self.doubleSpinNyqRes, QtCore.SIGNAL("valueChanged(double)"), self.onNyquistResChange)
        QtCore.QObject.connect(self.doubleSpinBoxResT, QtCore.SIGNAL("valueChanged(double)"), self.onSimluResChange)
        QtCore.QObject.connect(self.doubleSpinBoxLGRpontos, QtCore.SIGNAL("valueChanged(double)"), self.onResLGRchange)
        # LineEdits:
        QtCore.QObject.connect(self.lineEditRvalue, QtCore.SIGNAL("textEdited(QString)"), self.onRvalueChange)
        QtCore.QObject.connect(self.lineEditWvalue, QtCore.SIGNAL("textEdited(QString)"), self.onWvalueChange)
        QtCore.QObject.connect(self.lineEditGnum, QtCore.SIGNAL("textEdited(QString)"), self.onGnumChange)
        QtCore.QObject.connect(self.lineEditGden, QtCore.SIGNAL("textEdited(QString)"), self.onGdenChange)
        QtCore.QObject.connect(self.lineEditCnum, QtCore.SIGNAL("textEdited(QString)"), self.onCnumChange)
        QtCore.QObject.connect(self.lineEditCden, QtCore.SIGNAL("textEdited(QString)"), self.onCdenChange)
        QtCore.QObject.connect(self.lineEditHnum, QtCore.SIGNAL("textEdited(QString)"), self.onHnumChange)
        QtCore.QObject.connect(self.lineEditHden, QtCore.SIGNAL("textEdited(QString)"), self.onHdenChange)
        # Group Boxes:
        QtCore.QObject.connect(self.groupBoxC, QtCore.SIGNAL("toggled(bool)"), self.onGroupBoxCcheck)
        QtCore.QObject.connect(self.groupBoxG, QtCore.SIGNAL("toggled(bool)"), self.onGroupBoxGcheck)
        QtCore.QObject.connect(self.groupBoxH, QtCore.SIGNAL("toggled(bool)"), self.onGroupBoxHcheck)
        QtCore.QObject.connect(self.groupBoxWt, QtCore.SIGNAL("toggled(bool)"), self.onGroupBoxWcheck)
        # Buttons:
        QtCore.QObject.connect(self.btnSimul, QtCore.SIGNAL("clicked()"), self.onBtnSimul)
        QtCore.QObject.connect(self.btnContinuar, QtCore.SIGNAL("clicked()"), self.onBtnContinue)
        QtCore.QObject.connect(self.btnLimparSimul, QtCore.SIGNAL("clicked()"), self.onBtnClearSimul)
        QtCore.QObject.connect(self.btnPlotLGR, QtCore.SIGNAL("clicked()"), self.onBtnLGR)
        QtCore.QObject.connect(self.btnLGRclear, QtCore.SIGNAL("clicked()"), self.onBtnLGRclear)
        QtCore.QObject.connect(self.btnPlotBode, QtCore.SIGNAL("clicked()"), self.onBtnPlotBode)
        QtCore.QObject.connect(self.btnBodeClear, QtCore.SIGNAL("clicked()"), self.onBtnBodeClear)
        QtCore.QObject.connect(self.btnPlotNyquist, QtCore.SIGNAL("clicked()"), self.onBtnNyquist)
        QtCore.QObject.connect(self.btnClearNyquist, QtCore.SIGNAL("clicked()"), self.onBtnNyquistClear)
        # Actions
        QtCore.QObject.connect(self.actionHelp, QtCore.SIGNAL("triggered()"), self.onAboutAction)
        
        self.statusBar().showMessage(_translate("MainWindow", "Pronto.", None))        
        
               
    def feedbackOpen(self):
        """Open Feedback """ 

        self.sys.Malha = 'Aberta'
        
        # Change SVG accordingly:        
        self.updateSystemSVG()
        
        self.statusBar().showMessage(_translate("MainWindow", "Malha aberta.", None))
    
    def feedbackClose(self):
        """Close Feedback """

        self.sys.Malha = 'Fechada'
        
        # Change SVG accordingly:        
        self.updateSystemSVG()        
        
        self.statusBar().showMessage(_translate("MainWindow", "Malha fechada.", None))

    def onChangeSystem(self,sysindex):
        """
        Whem user change system topology using the combo box.
        Update block diagram and anable/disable input groupboxes.
        """
       
        if (sysindex == 0): # LTI system 1 (without C(s))
            self.groupBoxC.setEnabled(False)
            self.sys.Type = 0
            # Disable C(s):
            self.sys.Cnum = [1]
            self.sys.Cden = [1]
            self.sys.Atualiza()            
            
        elif (sysindex == 1): # LTI system 2 (with C(s))
            self.sys.Type = 1
            self.groupBoxC.setEnabled(True)
            # Update system if C(s) group box is checked or not.
            self.onGroupBoxCcheck(self.groupBoxC.isChecked())
        else:
            self.statusBar().showMessage(_translate("MainWindow", "Sistema ainda não implementado.", None))
            return
        
        self.updateSystemSVG()
        self.statusBar().showMessage(_translate("MainWindow", "Sistema alterado.", None)) 

    
    def onSliderMove(self,value):
        """Slider change event. 
        This event is called also when setSliderPosition is called during 
        Kmax and Kmin changes. Changes in Kmax and Kmin only alters position
        of the slider and not the gain. This is why there is this test.
        """

        gain = float(value)*float((self.sys.Kmax)-(self.sys.Kmin))/float(self.sys.Kpontos) + self.sys.Kmin        
        self.sys.K = gain
        # Disconnect events to not enter in a event loop:
        QtCore.QObject.disconnect(self.doubleSpinBoxKlgr, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        QtCore.QObject.disconnect(self.doubleSpinBoxK, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        # Update spinboxes
        self.doubleSpinBoxKlgr.setValue(gain)
        self.doubleSpinBoxK.setValue(gain)
        # Draw Closed Loop Poles:
        self.DrawCloseLoopPoles(gain)
        # Reconect events:
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
        # Draw Closed Loop Poles:
        self.DrawCloseLoopPoles(value)
        # Reconect events:
        QtCore.QObject.connect(self.doubleSpinBoxKlgr, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)
        QtCore.QObject.connect(self.doubleSpinBoxK, QtCore.SIGNAL("valueChanged(double)"), self.onKChange)        
        # Update slider position.
        self.updateSliderPosition()

    def onBtnSimul(self):
        
        Tmax = self.sys.Tmax
        self.sys.X0r = 0
        self.sys.X0w = 0
        
        stringR = self.sys.Rt
        stringW = self.sys.Wt
        
        delta_t = 0.01
        
        self.statusBar().showMessage(_translate("MainWindow", "Simulando, aguarde...", None))
        # Create the input vectors r(t) and w(t):
        t,r,w = self.sys.CriaEntrada(stringR, stringW, 0, Tmax, delta_t, 
                            self.sys.InstRt, self.sys.InstWt)
        
        # Perform a time domain simulation:
        y = self.sys.Simulacao(t, r, w)        
        
        self.statusBar().showMessage(_translate("MainWindow", "Simulação concluída.", None))
        self.mplSimul.axes.autoscale(True)        
        
        #self.mplSimul.figure.clf()
        self.mplSimul.axes.cla()
        self.mplSimul.axes.hold(True)
        #ax = self.mplSimul.figure.add_subplot(111)
        legend = []
        flag = 0

        if (self.checkBoxEntrada.isChecked()):
            self.mplSimul.axes.plot(t,r,'b')
            legend.append(_translate("MainWindow", "Entrada: u(t)", None))
            flag = 1
        if (self.checkBoxSaida.isChecked()):
            self.mplSimul.axes.plot(t,y,'r')
            legend.append(_translate("MainWindow", "Saída: y(t)", None))
            flag = 1
        if (self.checkBoxErro.isChecked()):
            self.mplSimul.axes.plot(t,r-y,'g')
            legend.append(_translate("MainWindow", "Erro: e(t)", None))
            flag = 1
        if (self.checkBoxPert.isChecked()):
            self.mplSimul.axes.plot(t,w,'m')
            legend.append(_translate("MainWindow", "Perturbação: w(t)", None))
            flag = 1
        
        if (flag == 0):
            self.statusBar().showMessage(_translate("MainWindow", "Nenhum sinal selecionado!", None))
            return
        
        self.mplSimul.axes.grid()
        
        ylim = self.mplSimul.axes.get_ylim()
        
        # Set a new y limit, adding 1/10 of the total.
        self.mplSimul.axes.set_ylim(ymax=(ylim[1]+(ylim[1]-ylim[0])/10))
        
        # Add legend:
        self.mplSimul.axes.legend(legend, loc=0)
        self.mplSimul.axes.set_ylabel(_translate("MainWindow", "Valor", None))
        self.mplSimul.axes.set_xlabel(_translate("MainWindow", "Tempo [s]", None))
        self.mplSimul.axes.set_title(_translate("MainWindow", "Simulação no tempo", None))
        
        # Enable continue button:
        self.btnContinuar.setEnabled(True)
        
        
        self.mplSimul.draw()
        
    def onBtnContinue(self):
        """
        Continue simulation button
        """        
        Tmax = self.sys.Tmax
        
        Tinic = self.sys.tfinal
        stringR = self.sys.Rt
        stringW = self.sys.Wt
        #delta_t = 0.01
        
        # Create time and input vector:
        t,r,w = self.sys.CriaEntrada(stringR, stringW, Tinic , Tmax, self.doubleSpinBoxResT.value(), 
                            self.sys.InstRt, self.sys.InstWt,self.sys.Rfinal,
                            self.sys.Wfinal)
        
        self.statusBar().showMessage(_translate("MainWindow", "Simulando, aguarde...", None))
        
        # Simulate the system:
        y = self.sys.Simulacao(t, r, w)
        
        self.statusBar().showMessage(_translate("MainWindow", "Simulação concluída.", None))
        
        self.mplSimul.axes.autoscale(True)        
        
        legend = []
        
        flag = 0

        if (self.checkBoxEntrada.isChecked()):
            self.mplSimul.axes.plot(t,r,'b')
            legend.append(_translate("MainWindow", "Entrada: u(t)", None))
            flag = 1
        if (self.checkBoxSaida.isChecked()):
            self.mplSimul.axes.plot(t,y,'r')
            legend.append(_translate("MainWindow", "Saída: y(t)", None))
            flag = 1
        if (self.checkBoxErro.isChecked()):
            self.mplSimul.axes.plot(t,r-y,'g')
            legend.append(_translate("MainWindow", "Erro: e(t)", None))
            flag = 1
        if (self.checkBoxPert.isChecked()):
            self.mplSimul.axes.plot(t,w,'m')
            legend.append(_translate("MainWindow", "Perturbação: w(t)", None))
            flag = 1
        
        if (flag == 0):
            self.statusBar().showMessage(_translate("MainWindow", "Nenhum sinal selecionado!", None))
            return        
        
        self.mplSimul.axes.grid(True)
        ylim = self.mplSimul.axes.get_ylim()
        # Set a new y limit, adding 1/10 of the total.
        self.mplSimul.axes.set_ylim(ymax=(ylim[1]+(ylim[1]-ylim[0])/10))
        # Add legend:
        self.mplSimul.axes.legend(legend, loc=0)
        
        # Draw the graphic:
        self.mplSimul.draw()

    
    def onBtnClearSimul(self):
        """
        Clear simulation graphic button
        """
        # Clear figure:
        #self.mplSimul.figure.clf()
        self.mplSimul.axes.cla()
        self.mplSimul.axes.set_xlim(0, self.sys.Tmax)
        self.mplSimul.axes.set_ylim(0, 1)
        self.mplSimul.axes.set_ylabel(_translate("MainWindow", "Valor", None))
        self.mplSimul.axes.set_xlabel(_translate("MainWindow", "Tempo [s]", None))
        self.mplSimul.axes.set_title(_translate("MainWindow", "Simulação no tempo", None))        
        self.mplSimul.axes.grid()
        self.mplSimul.draw()
        # Disable continue button:
        self.btnContinuar.setEnabled(False)
        
        # Reset initial conditions:
        self.sys.X0r = None
        self.sys.X0w = None
    
    def onSimluResChange(self,value):
        """
        Changed simulation resolution handler
        """
        self.sys.delta_t = self.doubleSpinBoxResT.value()
        
    def onBtnLGR(self):
        """
        Plot LGR graphic.
        """
        self.statusBar().showMessage(_translate("MainWindow", "Plotando LGR...", None))
        self.sys.LGR(self.mplLGR.figure)
        
        self.statusBar().showMessage(_translate("MainWindow", "Concluído.", None))
        
        self.axesLGR = self.mplLGR.figure.gca()
        self.axesLGR.grid(True)
        self.axesLGR.set_xlabel(_translate("MainWindow", "Eixo real", None))
        self.axesLGR.set_ylabel(_translate("MainWindow", "Eixo imaginário", None))
        self.axesLGR.set_title(_translate("MainWindow", "Lugar Geométrico das raízes de C(s)*G(s)*H(s)", None))

        # Tenta apagar a instância dos pólos em malha fechada na figura. Se já
        # existirem, apaga, senão não faz nada.
        try:
            del self.polosLGR
        except AttributeError:
            pass        
        
        # Draw closed loop poles with current gain:
        self.DrawCloseLoopPoles(self.sys.K)
        
        # Forbidden regions:
        # GUI parameters:
        Ribd = abs(self.doubleSpinBoxRibd.value())
        Rebd = abs(self.doubleSpinBoxRebd.value())
        Imbd = abs(self.doubleSpinBoxImbd.value())
        
        xlimites = self.axesLGR.get_xlim()
        ylimites = self.axesLGR.get_ylim()

        if Rebd > 0:
            if Rebd < 0.5:
                inic = Rebd + 0.5
            else:
                inic = 0
            y = [ylimites[0],ylimites[1],ylimites[1],ylimites[0]]
            x = [-Rebd,-Rebd,inic,inic]
            self.axesLGR.fill(x,y,facecolor=(1,0.6,0.5),linewidth=0)            
        
        if Ribd > 0:
            # R = Ribd * I
            y = [0,ylimites[1],ylimites[1],0,ylimites[0],ylimites[0]]
            x = [0,-Ribd*ylimites[1],0,0,0,Ribd*ylimites[0]]
            self.axesLGR.fill(x,y,facecolor=(1,0.6,0.5),linewidth=0)            
        
        if Imbd > 0:
            x = [xlimites[0],xlimites[1],xlimites[1],xlimites[0]]
            y = [-Imbd,-Imbd,Imbd,Imbd]
            self.axesLGR.fill(x,y,facecolor=(1,0.6,0.5),linewidth=0)        
        
        self.mplLGR.draw()

    def onBtnLGRclear(self):
        # Clear figure:

        self.axesLGR.cla()
        #self.mplSimul.axes.set_xlim(0, self.sys.Tmax)
        #self.mplSimul.axes.set_ylim(0, 1)
        #self.mplSimul.axes.set_ylabel(_translate("MainWindow", "Valor", None))
        #self.mplSimul.axes.set_xlabel(_translate("MainWindow", "Tempo [s]", None))
        #self.mplSimul.axes.set_title(_translate("MainWindow", "Simulação no tempo", None))        
        #self.mplSimul.axes.grid()
        self.mplLGR.draw()
    
    def onResLGRchange(self,value):
        """
        Chagen LGR number of points gain.
        """
        self.sys.Kpontos = self.doubleSpinBoxLGRpontos.value()
        
    def DrawCloseLoopPoles(self,gain):
            
        # Calcula raízes do polinômio 1+k*TF(s):
        raizes = self.sys.RaizesRL(gain)
        txt = ''
        for r in raizes:
            if numpy.isreal(r):
                temp = "%.3f, " %(r)
            else:
                temp = "%.3f+j%.3f, " %(r.real,r.imag)
            txt = txt + temp
        
        txt = _translate("MainWindow", "Pólos em MF: ", None) + txt
        self.statusBar().showMessage(txt)
        
        # Plotando pólos do sist. realimentado:
        
        try: # Se nenhum LGR foi traçado, não faz mais nada.
            self.polosLGR[0].set_xdata(numpy.real(raizes))
            self.polosLGR[0].set_ydata(numpy.imag(raizes))
        except AttributeError:
            try: # Se nenhum polo foi desenhado, desenha então:
                self.polosLGR = self.axesLGR.plot(numpy.real(raizes), numpy.imag(raizes),
                                'xb',ms=7,mew=3)
            except AttributeError:

                return
            else:
                self.mplLGR.draw()
        else:
            self.mplLGR.draw()

        finally:
            pass
        
        return        
    
    def onBtnNyquist(self):
        """
        Plot nyquist diagram Button handler
        """
        self.statusBar().showMessage(_translate("MainWindow", "Traçando Nyquist...", None))
        
        
        
        self.sys.Nyquist(self.mplNyquist.figure,completo=self.checkBoxNyqNegFreq.isChecked(),comcirculo=self.checkBoxNyqCirc.isChecked())
        
        [ax] = self.mplNyquist.figure.get_axes()
        # Setting labels and title:
        ax.set_xlabel('$Re[KC(j\omega)G(j\omega)H(j\omega)]$')
        ax.set_ylabel('$Im[KC(j\omega)G(j\omega)H(j\omega)]$')
        ax.set_title('Diagrama de Nyquist')
        
        self.mplNyquist.draw()
        
        self.statusBar().showMessage(_translate("MainWindow", "Concluído.", None))

    
    def onBtnNyquistClear(self):
        """
        Clear figure of the Nyquist diagram. Button handler.
        """
        self.mplNyquist.figure.clf()
        self.mplNyquist.draw()
        pass
    
    def onNyquistFminChange(self, value):
        """
        Nyquist Fmin edited handler
        """
        self.sys.NyqFmin = self.doubleSpinFminNyq.value()

    def onNyquistFmaxChange(self, value):
        """
        Nyquist Fmax edited handler
        """
        self.sys.NyqFmax = self.doubleSpinFmaxNyq.value()
    
    def onNyquistResChange(self, value):
        """
        Nyquist Resolution edited handler
        """
        self.sys.NyqFpontos = self.doubleSpinNyqRes.value()
   
    
    def onBtnPlotBode(self):
        
        self.statusBar().showMessage(_translate("MainWindow", "Traçando Bode...", None))
        # Plotting Bode:
        
        self.sys.Bode(self.mplBode.figure)
        [ax1,ax2] = self.mplBode.figure.get_axes()
        # Ajusting labels e title:
        
        ax1.set_ylabel(_translate("MainWindow", "Magnitude [dB]", None))
        ax2.set_ylabel(_translate("MainWindow", "Fase [graus]", None))
        ax2.set_xlabel(_translate("MainWindow", "Frequência [Hz]", None))
        ax1.set_title(_translate("MainWindow", "Diagrama de Bode de K*C(s)*G(s)", None))
        
        self.mplBode.draw()
        
        self.statusBar().showMessage(_translate("MainWindow", "Concluído.", None))
    
    def onBtnBodeClear(self):
        # Clear Bode figure:

        self.mplBode.figure.clf()
        #self.mplSimul.axes.set_xlim(0, self.sys.Tmax)
        #self.mplSimul.axes.set_ylim(0, 1)
        #self.mplSimul.axes.set_ylabel(_translate("MainWindow", "Valor", None))
        #self.mplSimul.axes.set_xlabel(_translate("MainWindow", "Tempo [s]", None))
        #self.mplSimul.axes.set_title(_translate("MainWindow", "Simulação no tempo", None))        
        #self.mplSimul.axes.grid()
        self.mplBode.draw() 


    def onBodeFminChange(self,value):
        """
        Bode Fmin edited handler
        """
        self.sys.Fmin = self.doubleSpinFmin.value()


    def onBodeFmaxChange(self,value):
        """
        Bode Fmax edited handler
        """
        self.sys.Fmax = self.doubleSpinFmax.value()

    def onBodeResChange(self,value):
        """
        Bode Resolution edited handler
        """
        self.sys.Fpontos = self.doubleSpinBodeRes.value()

   
    def onTmaxChange(self,value):
        """
        Tmax edited handler
        """
        self.sys.Tmax = value

    def onRtimeChange(self,value):
        """
        r(t) input time edited handler
        """
        self.sys.InstRt = value
        
    def onRnoiseChange(self,value):
        """
        r(t) noise edited
        """
        self.sys.ruidoRt = value

    def onWtimeChange(self,value):
        """
        r(t) input time edited handler
        """
        self.sys.InstWt = value

    def onWnoiseChange(self,value):
        """
        w(t) noise edited
        """
        self.sys.ruidoWt = value
    
    def onRvalueChange(self,value):
        """
        r(t) string input edited handler
        """
        if not value:
            self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: rgb(255, 170, 170) }")
            return
        else:
            self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: rgb(95, 211, 141) }")
        
        value.replace(',','.')        
        
        #if (int(value) == 2):
        #    self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: yellow }")
        self.sys.Rt = str(value)
 

    def onWvalueChange(self,value):
        """
        r(t) string input edited handler
        """
        self.sys.Wt = str(value)

    def onGroupBoxCcheck(self,flag):
        
        if (flag == False):
            self.statusBar().showMessage(_translate("MainWindow", "C(s) desativada.", None))
            self.sys.Cnum = [1]
            self.sys.Cden = [1]
            self.sys.Atualiza()
        else:
            self.onCnumChange(self.lineEditCnum.text())
            self.onCdenChange(self.lineEditCden.text())
            self.statusBar().showMessage(_translate("MainWindow", "C(s) ativada.", None))
    
    def onGroupBoxGcheck(self,flag):
        
        if (flag == False):
            self.statusBar().showMessage(_translate("MainWindow", "G(s) desativada.", None))
            self.sys.Gnum = [1]
            self.sys.Gden = [1]
            self.sys.Atualiza()
        else:
            self.onGnumChange(self.lineEditGnum.text())
            self.onGdenChange(self.lineEditGden.text())
            self.statusBar().showMessage(_translate("MainWindow", "G(s) ativada.", None))
            
    def onGroupBoxHcheck(self,flag):
        
        if (flag == False):
            self.statusBar().showMessage(_translate("MainWindow", "H(s) desativada.", None))
            self.sys.Hnum = [1]
            self.sys.Hden = [1]
            self.sys.Atualiza()
        else:
            self.onHnumChange(self.lineEditHnum.text())
            self.onHdenChange(self.lineEditHden.text())
            self.statusBar().showMessage(_translate("MainWindow", "H(s) ativada.", None))

    def onGroupBoxWcheck(self,flag):
        
        if (flag == False):
            self.statusBar().showMessage(_translate("MainWindow", "Perturbação desativada.", None))
            self.sys.Wt = '0'
            self.sys.InstWt = 0
            self.checkBoxPert.setDisabled(True)
        else:
            self.statusBar().showMessage(_translate("MainWindow", "Perturbação ativada.", None))
            self.sys.Wt = str(self.lineEditWvalue.text())
            self.sys.InstWt = self.doubleSpinBoxWtime.value()
            self.checkBoxPert.setDisabled(False)

            

    def onGnumChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditGnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            return
            
        Gnum = self.checkTFinput(value)
        
        if (Gnum == 0):
            self.lineEditGnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
        else:
            self.lineEditGnum.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
            self.sys.GnumStr = str(value)
            self.sys.Gnum = Gnum
            self.sys.Atualiza()
    
    def onGdenChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditGden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            return
            
        Gden = self.checkTFinput(value)
        
        if (Gden == 0):
            self.lineEditGden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
        else:
            self.lineEditGden.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
            self.sys.GdenStr = str(value)
            self.sys.Gden = Gden
            self.sys.Atualiza()

    def onCnumChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditCnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            return
            
        Cnum = self.checkTFinput(value)
        
        if (Cnum == 0):
            self.lineEditCnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
        else:
            self.lineEditCnum.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
            self.sys.CnumStr = str(value)
            self.sys.Cnum = Cnum
            self.sys.Atualiza()
    
    def onCdenChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditCden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            return
            
        Cden = self.checkTFinput(value)
        
        if (Cden == 0):
            self.lineEditCden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
        else:
            self.lineEditCden.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
            self.sys.CdenStr = str(value)
            self.sys.Cden = Cden
            self.sys.Atualiza()  
      
    def onHnumChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditHnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            return
            
        Hnum = self.checkTFinput(value)
        
        if (Hnum == 0):
            self.lineEditHnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
        else:
            self.lineEditHnum.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
            self.sys.HnumStr = str(value)
            self.sys.Hnum = Hnum
            self.sys.Atualiza()
    
    def onHdenChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditHden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            return
            
        Hden = self.checkTFinput(value)
        
        if (Hden == 0):
            self.lineEditHden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
        else:
            self.lineEditHden.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
            self.sys.HdenStr = str(value)
            self.sys.Hden = Hden
            self.sys.Atualiza()
    
    def checkTFinput(self, value):
        """
        Check if input string is correct.
        
        Return 0 if it has an error.
        Otherwise, returns a list with polynomial coefficients
        """
        value.replace(',','.')
        
        retorno = None
        
        if value.startsWith('['):
            try:
                retorno = eval(str(value))
            except:
                retorno = 0
        else:
            try:
                equacao = utils.parseexpr(str(value))
                retorno = equacao.c.tolist()
                #self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: green }")
            except:
                #self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: red }")
                retorno = 0
        if retorno == 0:
            self.statusBar().showMessage(_translate("MainWindow", "Expressão inválida.", None))
        else:
            self.statusBar().showMessage(_translate("MainWindow", "Expressão válida.", None))
        
        return retorno

    
    def updateSliderPosition(self):
        position = (float(self.sys.Kpontos) * (self.sys.K - self.sys.Kmin))/(abs(self.sys.Kmax)+abs(self.sys.Kmin))
        # Disconnect events to not enter in a event loop:
        QtCore.QObject.disconnect(self.verticalSliderK, QtCore.SIGNAL("valueChanged(int)"), self.onSliderMove)
        self.verticalSliderK.setSliderPosition(int(position))
        QtCore.QObject.connect(self.verticalSliderK, QtCore.SIGNAL("valueChanged(int)"), self.onSliderMove)
    
    def updateSystemSVG(self):
        svg_file_name = ''        
        
        if (self.sys.Type == 0): # LTI system 1 (without C(s))
            if self.sys.Malha == 'Fechada':
                svg_file_name = 'diagram1Closed.svg'
            else:
                svg_file_name = 'diagram1Opened.svg'
        elif (self.sys.Type == 1): # LTI system 2 (with C(s))
            if self.sys.Malha == 'Fechada':
                svg_file_name = 'diagram2Closed.svg'
            else:
                svg_file_name = 'diagram2Opened.svg'
        else:
            self.statusBar().showMessage(_translate("MainWindow", "Sistema ainda não implementado.", None))
            return

        # Load svg file.
        svg_file = QtCore.QFile(svg_file_name)
        if not svg_file.exists():
            QtGui.QMessageBox.critical(self, "Open SVG File",
                                       "Could not open file '%s'." % svg_file_name)
            self.outlineAction.setEnabled(False)
            self.backgroundAction.setEnabled(False)
            return
        # Update svg image:
        self.scene.clear()
        #self.graphicsView.resetTransform()
        self.svgItem = QtSvg.QGraphicsSvgItem(svg_file.fileName())
        #self.svgItem.setFlags(QtGui.QGraphicsItem.ItemClipsToShape)
        #self.svgItem.setCacheMode(QtGui.QGraphicsItem.NoCache)
        self.scene.addItem(self.svgItem)
    
    def onAboutAction(self):
        QtGui.QMessageBox.about(self,"Sobre o LabControle2", MESSAGE)
        
        
       

        
if __name__ == '__main__':
    app = QtGui.QApplication([])
    #translator = QtCore.QTranslator()
    #translator.load("LabControle2_en.qm")
    #app.installTranslator(translator)
    
    win = LabControle2()
    win.show()
    app.exec_()