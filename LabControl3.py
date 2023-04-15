#!/usr/bin/ python3
# -*- coding: utf-8 -*-
#==============================================================================
# This file is part of LabControl 3.
# 
# LabControl 3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
# 
# LabControl 3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with LabControl 3.  If not, see <http://www.gnu.org/licenses/>.
#==============================================================================
#==============================================================================
# Este arquivo é parte do programa LabControl 3
# 
# LabControl 3 é um software livre; você pode redistribui-lo e/ou 
# modifica-lo dentro dos termos da Licença Pública Geral GNU como 
# publicada pela Fundação do Software Livre (FSF); na versão 3 da 
# Licença.
# Este programa é distribuido na esperança que possa ser  util, 
# mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a 
# qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral
# GNU para maiores detalhes.
# 
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, escreva para a Fundação do Software
# Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#==============================================================================
#
# Developed by Miguel Moreto
# Florianopolis, Brazil, 2023
import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5 import (
    QtCore,
    QtGui,
    QtWidgets
)
from PyQt5.uic import loadUi
import images_rc

from matplotlib.backends.backend_qt5agg  import NavigationToolbar2QT as NavigationToolbar

import MySystem
import utils
import numpy
import subprocess
import pickle
#import encript
import base64
import LC3systems

from labnavigationtoolbar import CustomNavigationToolbar
           
try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

MESSAGE = _translate("MainWindow", "<p><b>Sobre o LabControl 3</b></p>" \
            "<p>O LabControl é um software desenvolvido " \
            "para ser utilizado em atividades de laboratório de " \
            "disciplinas de Sistemas de Controle.</p>" \
            "<p>O LabControl 3 foi desenvolvido por Miguel Moreto, " \
            "professor do Departamento de Engenharia Elétrica da UFSC "\
            "para uso nos laboratórios da disciplina EEL7063 - Sistemas "\
            "de Controle.</p>" \
            "<p>O LabControl 3 é uma atualização do LabControle 3 e foi "\
            "<p>O foi desenvolvido em linguagem Python 3. "\
            "Seu código é livre, podendo ser acessado no site:</p>"\
            "<p><b><a href=\"https://github.com/miguelmoreto/labcontrole\">https://github.com/miguelmoreto/labcontrole</a></b></p>"\
            "<p>Contribua enviando sugestões e relatórios de bugs (issues)!</p>"\
			"<p>Contribuidores:</p>"\
			"<p>Anderson Livramento</p>"\
            "<p>Florianópolis, SC, 2020</p>", None)

class LabControl3(QtWidgets.QMainWindow):#,MainWindow.Ui_MainWindow):
    """
    hwl is inherited from both QtGui.QDialog and hw.Ui_Dialog
    """
    def __init__(self,parent=None):
        self.init = 0
        super(LabControl3,self).__init__(parent)
        loadUi('MainWindow.ui', self)
        
        self.currentComboIndex = 0
        
        # Adding toolbar spacer and a Hidden system label:
        empty = QtWidgets.QWidget()
        self.labelHide = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.labelHide.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelHide.setFont(font)
        self.labelHide.setText('')
        self.labelHide.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        empty.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Preferred)
        self.toolBar.insertWidget(self.actionClose,empty)
        self.toolBar.insertWidget(self.actionClose,self.labelHide)
        self.label.setPixmap(QtGui.QPixmap( "diagram1Opened.png"))
        
        # Set diagram the current tab:
        self.tabWidget.setCurrentIndex(0)
        
        
        self.image = QtGui.QImage()        
        
        # Initial definitions:
        self.checkBoxPert.setDisabled(True) # Perturbation is disabled by default
        self.checkBoxControle.setDisabled(True) # Control signal is disabled by default

        # Adding toolbars
        self.mpltoolbarSimul = NavigationToolbar(self.mplSimul, self)
        #self.mpltoolbarSimul = CustomNavigationToolbar(self.mplSimul, self)
        self.mpltoolbarLGR = NavigationToolbar(self.mplLGR, self)
        self.mpltoolbarBode = NavigationToolbar(self.mplBode, self)
        #self.mpltoolbarBode = CustomNavigationToolbar(self.mplBode, self)
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
        self.sys = MySystem.MySystem()
        # Updating values from GUI:
        self.sys.Fmin = self.doubleSpinFmin.value()
        self.sys.Fmax = self.doubleSpinFmax.value()
        self.sys.Fpontos = self.doubleSpinBodeRes.value()
                
        self.init = 1

        ######################## LabControl 3 stuff:
        self.sysList = []   # A list that contains the LC3systems objects and the corresponding data.
        self.sysCurrentIndex = 0
        self.addSystem(1)

        ########################

        # Error messages
        self.expressions_errors = {
            'r(t)': {
                'error': False,
                'active': True,
                'message': ''
            },
            'w(t)': {
                'error': False,
                'active': True,
                'message': ''
            },
            'G[Num](s)': {
                'error': False,
                'active': True,
                'message': ''
            },
            'G[Den](s)': {
                'error': False,
                'active': True,
                'message': ''
            },
            'H[Num](s)': {
                'error': False,
                'active': True,
                'message': ''
            },
            'H[Den](s)': {
                'error': False,
                'active': True,
                'message': ''
            },
            'C[Num](s)': {
                'error': False,
                'active': True,
                'message': ''
            },
            'C[Den](s)': {
                'error': False,
                'active': True,
                'message': ''
            },
            'f(y,u)': {
                'error': False,
                'active': True,
                'message': ''
            },
        }
                
        # Connecting events:
        self.radioBtnOpen.clicked.connect(self.feedbackOpen)
        self.radioBtnClose.clicked.connect(self.feedbackClose)
        self.verticalSliderK.valueChanged.connect(self.onSliderMove)
        self.comboBoxSys.currentIndexChanged.connect(self.onChangeSystem)
        self.tabWidget.currentChanged.connect(self.onTabChange)
        # Lists:
        self.listSystem.itemClicked.connect(self.onSysItemClicked)
        # Spinboxes:
        self.doubleSpinBoxKmax.valueChanged.connect(self.onKmaxChange)
        self.doubleSpinBoxKmin.valueChanged.connect(self.onKminChange)
        self.doubleSpinBoxKlgr.valueChanged.connect(self.onKChange)
        self.doubleSpinBoxK.valueChanged.connect(self.onKChange)
        self.doubleSpinBoxTmax.valueChanged.connect(self.onTmaxChange)
        self.doubleSpinBoxRtime.valueChanged.connect(self.onRtimeChange)
        self.doubleSpinBoxRnoise.valueChanged.connect(self.onRnoiseChange)
        self.doubleSpinBoxWtime.valueChanged.connect(self.onWtimeChange)
        self.doubleSpinBoxWnoise.valueChanged.connect(self.onWnoiseChange)
        self.doubleSpinFmin.valueChanged.connect(self.onBodeFminChange)
        self.doubleSpinFmax.valueChanged.connect(self.onBodeFmaxChange)
        self.doubleSpinBodeRes.valueChanged.connect(self.onBodeResChange)
        self.doubleSpinFminNyq.valueChanged.connect(self.onNyquistFminChange)
        self.doubleSpinFmaxNyq.valueChanged.connect(self.onNyquistFmaxChange)
        self.doubleSpinNyqRes.valueChanged.connect(self.onNyquistResChange)
        self.doubleSpinBoxResT.valueChanged.connect(self.onSimluResChange)
        self.doubleSpinBoxLGRpontos.valueChanged.connect(self.onResLGRchange)
        self.doubleSpinBoxDeltaR.valueChanged.connect(self.onRvarChange)
        self.doubleSpinBoxDeltaRtime.valueChanged.connect(self.onRvarInstChange)
        self.doubleSpinBoxTk.valueChanged.connect(self.onTkChange)
        self.spinBoxPtTk.valueChanged.connect(self.onPointsTkChange)
        # LineEdits:
        self.lineEditRvalue.textEdited.connect(self.onRvalueChange)
        self.lineEditWvalue.textEdited.connect(self.onWvalueChange)
        self.lineEditGnum.textEdited.connect(self.onGnumChange)
        self.lineEditGden.textEdited.connect(self.onGdenChange)
        self.lineEditCnum.textEdited.connect(self.onCnumChange)
        self.lineEditCden.textEdited.connect(self.onCdenChange)
        self.lineEditHnum.textEdited.connect(self.onHnumChange)
        self.lineEditHden.textEdited.connect(self.onHdenChange)
        # Group Boxes:
        self.groupBoxC.toggled.connect(self.onGroupBoxCcheck)
        self.groupBoxG.toggled.connect(self.onGroupBoxGcheck)
        self.groupBoxH.toggled.connect(self.onGroupBoxHcheck)
        self.groupBoxWt.toggled.connect(self.onGroupBoxWcheck)
        # Buttons:
        self.btnSimul.clicked.connect(self.onBtnSimul)
        self.btnContinuar.clicked.connect(self.onBtnContinue)
        self.btnLimparSimul.clicked.connect(self.onBtnClearSimul)
        self.btnPlotLGR.clicked.connect(self.onBtnLGR)
        self.btnLGRclear.clicked.connect(self.onBtnLGRclear)
        self.btnPlotBode.clicked.connect(self.onBtnPlotBode)
        self.btnBodeClear.clicked.connect(self.onBtnBodeClear)
        self.btnPlotNyquist.clicked.connect(self.onBtnNyquist)
        self.btnClearNyquist.clicked.connect(self.onBtnNyquistClear)
        self.btnSysAdd.clicked.connect(self.onBtnSysAdd)
        self.btnSysRemove.clicked.connect(self.onBtnSysRemove)
        self.btnSysClear.clicked.connect(self.onBtnSysClear)
        # Actions
        self.actionHelp.triggered.connect(self.onAboutAction)
        self.actionCalc.triggered.connect(self.onCalcAction)
        self.actionSalvar_sistema.triggered.connect(self.onSaveAction)
        self.actionCarregar_sistema.triggered.connect(self.onLoadAction)
        self.actionReset.triggered.connect(self.onResetAction)
        
        self.statusBar().showMessage(_translate("MainWindow", "Pronto.", None))        
        
    def _has_expressions_errors(self):
        result = False
        if any([(self.expressions_errors[e].get('error') and self.expressions_errors[e].get('active'))
                for e in self.expressions_errors]):
            result = True
            # Get error messages
            msgs = []
            for e in self.expressions_errors:
                if self.expressions_errors[e].get('error') and self.expressions_errors[e].get('active'):
                    msgs.append('<i>{}</i> for <b>{}</b>'.format(
                        self.expressions_errors[e].get('message'),
                        e
                    ))
            QtWidgets.QMessageBox.critical(self, 'Oops!', '<br />'.join(msgs))
        return result
    
    def _set_expression_error(self, expr, error, message=''):
        self.expressions_errors[expr]['error'] = error
        self.expressions_errors[expr]['message'] = message

    def _set_expression_active(self, expr, active):
        self.expressions_errors[expr]['active'] = active
    
    ########### LabControl 3 stuff:
    def onSysItemClicked(self,item):
        """
        User clicked in the list of stored system data.
        """
        print(item.text())
        self.sysCurrentIndex = self.listSystem.currentRow()
        print('Sys index: {i}'.format(i=self.sysCurrentIndex))
    
    def addSystem(self,systype):
        index = len(self.sysList)
        sys = LC3systems.LTIsystem(index,systype)
        self.sysList.append(sys)
        self.listSystem.addItem(sys.Name)
        self.listSystem.setCurrentRow(index)
    
    def onBtnSysAdd(self):
        self.addSystem(self.currentComboIndex + 1)
        self.sysCurrentIndex = self.listSystem.currentRow()

    def onBtnSysRemove(self):
        if (self.sysCurrentIndex == 0):
            QtWidgets.QMessageBox.information(self,_translate("MainWindow", "Atenção!", None), _translate("MainWindow", "Ao menos um sistema deve ser mantido na lista. Remoção não efetuada.", None))
            return
        self.listSystem.takeItem(self.sysCurrentIndex)
        self.sysCurrentIndex = self.listSystem.currentRow()

    def onBtnSysClear(self):
        ## To do
        pass
    #################################   
    
    def feedbackOpen(self):
        """Open Feedback """ 

        self.sys.Malha = 'Aberta'
        
        # Change SVG accordingly:        
        self.updateSystemPNG()
        
        self.statusBar().showMessage(_translate("MainWindow", "Malha aberta.", None))
    
    def feedbackClose(self):
        """Close Feedback """

        self.sys.Malha = 'Fechada'
        
        # Change SVG accordingly:        
        self.updateSystemPNG()
        
        self.statusBar().showMessage(_translate("MainWindow", "Malha fechada.", None))

    def onChangeSystem(self,sysindex):
        """
        Whem user change system topology using the combo box.
        Update block diagram and anable/disable input groupboxes.
        """
        
        # Check prvious system type and disable unecessary itens:
        if (self.sys.Type == 4 and sysindex != 4):
            self.lineEditGden.show()
            self.labelGden.show()
            self.groupBoxH.setEnabled(True)
            self.groupBoxG.setTitle(_translate("MainWindow", "Planta G(s)", None))
            self.labelGnum.setText(_translate("MainWindow", "Num:", None))
            # Restoring saved G(s)
            self.sys.Type = sysindex
            self.lineEditGnum.setText(self.sys.GnumStr)
            self.onGnumChange(self.sys.GnumStr)
            # Re-enable buttons:
            self.btnPlotBode.setEnabled(True)
            self.btnPlotLGR.setEnabled(True)
            self.btnPlotNyquist.setEnabled(True)

        elif (self.sys.Type == 3 and sysindex != 3):
            self.labelTk.setEnabled(False)
            self.doubleSpinBoxTk.setEnabled(False)
            self.labelPtTk.setEnabled(False)
            self.spinBoxPtTk.setEnabled(False)
            self.doubleSpinBoxResT.setEnabled(True)
            self.checkBoxControle.setEnabled(False)
            self.groupBoxH.setEnabled(True)
            self.groupBoxC.setTitle(_translate("MainWindow", "Controlador C(s)", None))
            # Re-enable buttons:
            self.btnPlotBode.setEnabled(True)
            self.btnPlotLGR.setEnabled(True)
            self.btnPlotNyquist.setEnabled(True)
            
        # Check current system choice and enable necessary itens:
        self._set_expression_active('f(y,u)', sysindex == 4)
        self._set_expression_active('G[Num](s)', sysindex != 4)
        self._set_expression_active('G[Den](s)', sysindex != 4)
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
        elif (sysindex == 2): # LTI system 3 (with G(s) after W(s))
            self.sys.Type = 2
            # in this case, G(s) goes to G2(s) in Sistema class while G(s)=1/1
            self.sys.G2num = self.sys.Gnum
            self.sys.G2den = self.sys.Gden
            self.sys.Gnum = [1]
            self.sys.Gden = [1]
            self.sys.Atualiza()
            self.groupBoxC.setEnabled(True)
            self.onGroupBoxCcheck(self.groupBoxC.isChecked())
            self.onGroupBoxGcheck(self.groupBoxG.isChecked())
            # Update system if C(s) group box is checked or not.
#==============================================================================
        elif (sysindex == 3): # Discrete time controller
            self.sys.Type = 3
            self.labelTk.setEnabled(True)
            self.doubleSpinBoxTk.setEnabled(True)
            self.labelPtTk.setEnabled(True)
            self.spinBoxPtTk.setEnabled(True)
            self.groupBoxC.setEnabled(True)
            self.groupBoxH.setEnabled(False)
            self.onGroupBoxCcheck(self.groupBoxC.isChecked())
            self.checkBoxControle.setEnabled(True)
            self.doubleSpinBoxResT.setEnabled(False)
            self.btnPlotBode.setEnabled(False)
            self.btnPlotLGR.setEnabled(False)
            self.btnPlotNyquist.setEnabled(False)            
            self.groupBoxC.setTitle(_translate("MainWindow", "Controlador C(z)", None))
#==============================================================================
        elif (sysindex == 4): # Non-linear system
            self.sys.Type = 4
            self.groupBoxC.setEnabled(True)
            self.groupBoxH.setEnabled(False)
            self.onGroupBoxCcheck(self.groupBoxC.isChecked())
            self.lineEditGden.hide()
            # Disable buttons:
            self.btnPlotBode.setEnabled(False)
            self.btnPlotLGR.setEnabled(False)
            self.btnPlotNyquist.setEnabled(False)
            self.labelGden.hide()
            # Saving previous Gnum string:
            self.sys.GnumStr = str(self.lineEditGnum.text())
            self.lineEditGnum.setText(self.sys.sysInputString)
            self.onGnumChange(self.sys.sysInputString)
            self.groupBoxG.setTitle(_translate("MainWindow", "EDO não linear", None))
            self.labelGnum.setText(_translate("MainWindow", "f(y,u)=", None))
            self.lineEditGnum.setText(self.sys.sysInputString)
            # self.onGnumChange(self.sys.sysInputString)
            self.groupBoxG.updateGeometry()
        else:
            QtWidgets.QMessageBox.information(self,_translate("MainWindow", "Aviso!", None), _translate("MainWindow", "Sistema ainda não implementado!", None))
            self.comboBoxSys.setCurrentIndex(self.currentComboIndex)
            return
        
        self.updateSystemPNG()
        self.statusBar().showMessage(_translate("MainWindow", "Sistema alterado.", None))
        self.currentComboIndex = sysindex

    
    def onSliderMove(self,value):
        """Slider change event. 
        This event is called also when setSliderPosition is called during 
        Kmax and Kmin changes. Changes in Kmax and Kmin only alters position
        of the slider and not the gain. This is why there is this test.
        """

        gain = float(value)*float((self.sys.Kmax)-(self.sys.Kmin))/float(self.sys.Kpontos) + self.sys.Kmin        
        self.sys.K = gain
        # Disconnect events to not enter in a event loop:
        self.doubleSpinBoxKlgr.valueChanged.disconnect(self.onKChange)
        self.doubleSpinBoxK.valueChanged.disconnect(self.onKChange)
        # Update spinboxes
        self.doubleSpinBoxKlgr.setValue(gain)
        self.doubleSpinBoxK.setValue(gain)
        # Draw Closed Loop Poles:
        self.DrawCloseLoopPoles(gain)
        # Reconect events:
        self.doubleSpinBoxKlgr.valueChanged.connect(self.onKChange)
        self.doubleSpinBoxK.valueChanged.connect(self.onKChange)
        
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
        self.doubleSpinBoxKlgr.valueChanged.disconnect(self.onKChange)
        self.doubleSpinBoxK.valueChanged.disconnect(self.onKChange)
        # Update spinboxes
        self.doubleSpinBoxKlgr.setValue(value)
        self.doubleSpinBoxK.setValue(value)
        # Draw Closed Loop Poles:
        self.DrawCloseLoopPoles(value)
        # Reconect events:
        self.doubleSpinBoxKlgr.valueChanged.connect(self.onKChange)
        self.doubleSpinBoxK.valueChanged.connect(self.onKChange)
        # Update slider position.
        self.updateSliderPosition()

    def onBtnSimul(self):
        
        if self._has_expressions_errors():
            return

        self.sys.X0r = None
        self.sys.X0w = None
        
        self.statusBar().showMessage(_translate("MainWindow", "Simulando, aguarde...", None))
        # Create the input vectors r(t) and w(t):
        t,r,w = self.sys.CriaEntrada(0, self.doubleSpinBoxResT.value())
        self.sys.N = len(t)
        
        # Perform a time domain simulation:
        if (self.sys.Type < 3):
            y = self.sys.Simulacao(t, r, w)
        elif (self.sys.Type == 4):
            if (self.sys.NLsysParseString(self.sys.sysInputString) == 0):
                self.statusBar().showMessage(_translate("MainWindow", "Erro na função f(y,u)!", None))
                return
            self.sys.NLsysReset()
            #print self.sys.sysString
            y = self.sys.NLsysSimulate(r)
        elif (self.sys.Type == 3):
            t_plot, t_plot_k, u_plot, y_plot, e_plot, e_plot_step = self.sys.DiscreteSimulate(r)
            
            #print "Discrete simul Not ready yet"
            #return
        
        self.statusBar().showMessage(_translate("MainWindow", "Simulação concluída.", None))
        self.mplSimul.axes.autoscale(True)        
        
        # Clear matplotlib toolbar history:
        #self.mpltoolbarSimul._views.clear()
        #self.mpltoolbarSimul._positions.clear()
        #self.mpltoolbarSimul._update_view()        

        # Setting curve navigation (but not for discrete time simulatioin or if output is disable)
        #self.mpltoolbarSimul.clear_curve_point()
        #if self.sys.Type != 3 and self.checkBoxSaida.isChecked():
        #    self.mpltoolbarSimul.init_curve_point([(self.mplSimul.axes, t, y)])
        
        #self.mplSimul.figure.clf()
        self.mplSimul.axes.cla()
        try:
            self.mplSimul.axes.hold(True)
        except AttributeError:
            #print("Ignoring matplotlib hold statement.")
            pass
        
        #ax = self.mplSimul.figure.add_subplot(111)
        legend = []
        flag = 0

        if (self.checkBoxEntrada.isChecked()):
            self.mplSimul.axes.plot(t,r,'b')
            self.mplSimul.axes.plot([0, 0],[0,r[0]], label="_nolegend_", color='b')
            legend.append(_translate("MainWindow", "Entrada: u(t)", None))
            flag = 1
        if (self.checkBoxSaida.isChecked()):
            if (self.sys.Type == 3):
                self.mplSimul.axes.plot(t_plot, y_plot, color='r', linewidth=1)
            else:
                self.mplSimul.axes.plot(t,y,'r')
            legend.append(_translate("MainWindow", "Saída: y(t)", None))
            flag = 1
        if (self.checkBoxErro.isChecked()):
            if (self.sys.Type == 3):
                self.mplSimul.axes.plot(t_plot, e_plot, 'y',)
                self.mplSimul.axes.plot(t_plot_k, e_plot_step, 'yo',)
            else:
                self.mplSimul.axes.plot(t,r-y,'g')
            legend.append(_translate("MainWindow", "Erro: e(t)", None))
            flag = 1
        if (self.checkBoxPert.isChecked()):
            self.mplSimul.axes.plot(t,w,'m')
            legend.append(_translate("MainWindow", "Perturbação: w(t)", None))
            flag = 1
        
        if (self.checkBoxControle.isChecked()):
            if (self.sys.Type == 3):
                self.mplSimul.axes.step(t_plot_k,u_plot, color='m',where='post')
        
        
        if (flag == 0):
            self.statusBar().showMessage(_translate("MainWindow", "Nenhum sinal selecionado!", None))
            return
        
        self.mplSimul.axes.grid()
        
        ylim = self.mplSimul.axes.get_ylim()
        
        # Set a new y limit, adding 1/10 of the total.
        self.mplSimul.axes.set_ylim(top=(ylim[1]+(ylim[1]-ylim[0])/10))
        self.mplSimul.axes.set_xlim([0,t[-1]])
        
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
        
        Tinic = self.sys.tfinal
        
        lastRvalue = self.sys.Rfinal
        # Create time and input vector:
        t,r,w = self.sys.CriaEntrada(Tinic, self.doubleSpinBoxResT.value(), 
                            self.sys.Rfinal, self.sys.Wfinal)
        self.sys.N = len(t)
        #r[0] = self.
        self.statusBar().showMessage(_translate("MainWindow", "Simulando, aguarde...", None))

        # Perform a time domain simulation:
        if (self.sys.Type < 3):
            y = self.sys.Simulacao(t, r, w)
        elif (self.sys.Type == 4):
            if (self.sys.NLsysParseString(self.sys.sysInputString) == 0):
                self.statusBar().showMessage(_translate("MainWindow", "Erro na função f(y,u)!", None))
                return
            #self.sys.NLsysReset()
            #print self.sys.sysString
            y = self.sys.NLsysSimulate(r)
        elif (self.sys.Type == 3):
            print("Discrete simul Not ready yet")
            return
        
        self.statusBar().showMessage(_translate("MainWindow", "Simulação concluída.", None))
        
        self.mplSimul.axes.autoscale(True)        
        
        legend = []
        
        flag = 0

        if (self.checkBoxEntrada.isChecked()):
            self.mplSimul.axes.plot(t,r,'b')
            # Draw line
            self.mplSimul.axes.plot([Tinic, Tinic],[lastRvalue,r[0]], label="_nolegend_", color='b')
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
        self.mplSimul.axes.set_ylim(top=(ylim[1]+(ylim[1]-ylim[0])/10))
        self.mplSimul.axes.set_xlim([0,t[-1]])
        # Add legend:
        self.mplSimul.axes.legend(legend, loc=0)
        
        # Draw the graphic:
        self.mplSimul.draw()

    
    def onBtnClearSimul(self):
        """
        Clear simulation graphic button
        """
        # Clear figure:
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
        
        # Reset non-linear system:
        self.sys.NLsysReset()
    
    def onSimluResChange(self,value):
        """
        Changed simulation resolution handler
        """
        if (value > 0):
            self.sys.delta_t = self.doubleSpinBoxResT.value()
            # Update total number of samples:
            self.sys.N = self.sys.Tmax/self.sys.delta_t
            # Update discrete time points per dT.
            self.spinBoxPtTk.valueChanged.disconnect(self.onPointsTkChange)
            self.sys.Npts_dT = self.sys.dT/self.sys.delta_t
            self.spinBoxPtTk.setValue(int(self.sys.Npts_dT))
            self.spinBoxPtTk.valueChanged.connect(self.onPointsTkChange)
            #
            
    def onPointsTkChange(self, value):
        """
        Changed number of points per dT in discrete time simul.
        """
        if (value > 0):
            self.sys.Npts_dT = value
            self.doubleSpinBoxResT.valueChanged.disconnect(self.onSimluResChange)
            # Change simulation resolution system and UI:
            self.sys.delta_t = self.sys.dT/value
            self.sys.N = self.sys.Tmax/self.sys.delta_t
            self.doubleSpinBoxResT.setValue(self.sys.delta_t)
            self.doubleSpinBoxResT.valueChanged.connect(self.onSimluResChange)
            
    def onTkChange(self, value):
        """
        Changed the number of the sample period (dT)
        """
        if (value > 0):
            self.sys.dT = value
            self.sys.NdT = int(self.sys.Tmax/value)
            # Change simulation resolution:
            self.doubleSpinBoxResT.valueChanged.disconnect(self.onSimluResChange)
            # Change simulation resolution system and UI:
            self.sys.delta_t = value/self.sys.Npts_dT
            self.sys.N = self.sys.Tmax/self.sys.delta_t
            self.doubleSpinBoxResT.setValue(self.sys.delta_t)
            self.doubleSpinBoxResT.valueChanged.connect(self.onSimluResChange)     
        
    def onBtnLGR(self):
        """
        Plot LGR graphic.
        """
        if self._has_expressions_errors():
            return

        self.statusBar().showMessage(_translate("MainWindow", "Plotando LGR...", None))
        
        # Plot LGR:
        self.sys.LGR(self.mplLGR.figure)
        
        self.statusBar().showMessage(_translate("MainWindow", "Concluído.", None))
        
        self.axesLGR = self.mplLGR.figure.gca()
        self.axesLGR.grid(True)
        self.axesLGR.set_xlabel(_translate("MainWindow", "Eixo real", None))
        self.axesLGR.set_ylabel(_translate("MainWindow", "Eixo imaginário", None))
        self.axesLGR.set_title(_translate("MainWindow", "Lugar Geométrico das raízes de C(s)*G(s)*H(s)", None))

        # Attempt to erase the closed loop poles instance in the figure
        #  if they exist, erase, else does nothing.
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
        
        if (abs(xlimites[0]-xlimites[1])<0.1):
            self.axesLGR.set_xlim((xlimites[0]-1,xlimites[1]+1))
            xlimites = self.axesLGR.get_xlim()

        if (abs(ylimites[0]-ylimites[1])<0.1):
            self.axesLGR.set_ylim((ylimites[0]-1,ylimites[1]+1))
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
        """
        Clear figure of the Root Locus diagram. Button handler.
        """        
        # Clear figure:
        self.mplLGR.figure.clf()
        self.mplLGR.draw()
    
    def onResLGRchange(self,value):
        """
        Chage the number of LGR gain points (resolution).
        """
        self.sys.Kpontos = self.doubleSpinBoxLGRpontos.value()
        # Update slider position.
        self.updateSliderPosition()
        
    def DrawCloseLoopPoles(self,gain):
            
        # Calcula raízes do polinômio 1+k*TF(s):
        raizes = self.sys.RaizesRL(gain)
        txt = ''
        for r in raizes:
            if (txt == ''):
                txt = self.createRootString(r)
            else:
                txt = txt + '; ' + self.createRootString(r)
        
        if not self.sys.Hide:
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
        if self._has_expressions_errors():
            return

        self.statusBar().showMessage(_translate("MainWindow", "Traçando Nyquist...", None))
        
        ax = self.sys.Nyquist(self.mplNyquist.figure,completo=self.checkBoxNyqNegFreq.isChecked(),comcirculo=self.checkBoxNyqCirc.isChecked())
        
        #[ax] = self.mplNyquist.figure.get_axes()
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

        if self._has_expressions_errors():
            return

        self.statusBar().showMessage(_translate("MainWindow", "Traçando Bode...", None))
        
        # Plotting Bode:
        dB, phase, f, ax1, ax2 = self.sys.Bode(self.mplBode.figure)

        # Custom Navigation
        #self.mpltoolbarBode.init_curve_point([(ax1, f, dB), (ax2, f, phase)])
        #self.mpltoolbarBode.siblings = [ax1, ax2]
        #self.mpltoolbarBode.error = 0.1

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
        # Update total number of samples:
        self.sys.N = self.sys.Tmax/self.sys.delta_t
        # Update spinboxes maximum values:
        self.doubleSpinBoxRtime.setMaximum(value)
        self.doubleSpinBoxWtime.setMaximum(value)
        self.doubleSpinBoxDeltaRtime.setMaximum(value)
        # Update the number of discrete sample periods:
        self.sys.NdT = int(self.sys.Tmax/self.sys.dT)

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
    
    def onRvarChange(self, value):
        """
        r(t) input variation value changed
        """
        self.sys.RtVar = value

    def onRvarInstChange(self, value):
        """
        r(t) input variation time value changed
        """
        self.sys.RtVarInstant = value

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
        # if not value:
        #     self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: rgb(255, 170, 170) }")
        #     return
        # else:
        #     self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: rgb(95, 211, 141) }")
        valid_value = self.checkTFinput(value, expr_var='t')
        if valid_value == 0:
            self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: rgb(255, 170, 170) }")
            self._set_expression_error('r(t)', True, '[{}] is not a valid expression'.format(value))
            return
        self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: rgb(95, 211, 141) }")
        value = value.replace(',','.')        
        
        #if (int(value) == 2):
        #    self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: yellow }")
        self._set_expression_error('r(t)', False)
        self.sys.Rt = str(value)
 

    def onWvalueChange(self,value):
        """
        w(t) string input edited handler
        """

        # if not value:
        #     self.lineEditWvalue.setStyleSheet("QLineEdit { background-color: rgb(255, 170, 170) }")
        #     return
        # else:
        #     self.lineEditWvalue.setStyleSheet("QLineEdit { background-color: rgb(95, 211, 141) }")
        
        valid_value = self.checkTFinput(value, expr_var='t')
        if valid_value == 0:
            self.lineEditWvalue.setStyleSheet("QLineEdit { background-color: rgb(255, 170, 170) }")
            self._set_expression_error('w(t)', True, '[{}] is not a valid expression'.format(value))
            return
        self.lineEditWvalue.setStyleSheet("QLineEdit { background-color: rgb(95, 211, 141) }")
        value = value.replace(',','.')   
        
        self._set_expression_error('w(t)', False)
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
        self._set_expression_active('C[Num](s)', flag)
        self._set_expression_active('C[Den](s)', flag)

    def onGroupBoxGcheck(self,flag):
        
        if (flag == False):
            self.statusBar().showMessage(_translate("MainWindow", "G(s) desativada.", None))
            self.sys.Gnum = [1]
            self.sys.Gden = [1]
            self.sys.G2num = [1]
            self.sys.G2den = [1]
            self.sys.Atualiza()
        else:
            self.onGnumChange(self.lineEditGnum.text())
            self.onGdenChange(self.lineEditGden.text())
            self.statusBar().showMessage(_translate("MainWindow", "G(s) ativada.", None))
        self._set_expression_active('G[Num](s)', flag)
        self._set_expression_active('G[Den](s)', flag)

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
        self._set_expression_active('H[Num](s)', flag)
        self._set_expression_active('H[Den](s)', flag)

    def onGroupBoxWcheck(self,flag):
        
        if (flag == False):
            self.statusBar().showMessage(_translate("MainWindow", "Perturbação desativada.", None))
            self.sys.Wt = '0'
            self.sys.InstWt = 0
            self.sys.ruidoWt = 0
            self.checkBoxPert.setDisabled(True)
        else:
            self.statusBar().showMessage(_translate("MainWindow", "Perturbação ativada.", None))
            self.sys.Wt = str(self.lineEditWvalue.text())
            self.sys.InstWt = self.doubleSpinBoxWtime.value()
            self.sys.ruidoWt = self.doubleSpinBoxWnoise.value()
            self.checkBoxPert.setDisabled(False)
        self._set_expression_active('w(t)', flag)

    def onGnumChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditGnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            return
        
        # If is a linear or discrete system, uses G(s):
        if (self.sys.Type < 4):
            Gnum = self.checkTFinput(value)
            
            if (Gnum == 0):
                # Change color ro red:
                self.lineEditGnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
                self._set_expression_error('G[Num](s)', True, '[{}] is not a valid expression'.format(value))
            else:
                # Change color to green:
                self.lineEditGnum.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
                self._set_expression_error('G[Num](s)', False)
                self.sys.GnumStr = str(value)
                if self.sys.Type == 2:
                    self.sys.G2num = Gnum
                else:
                    self.sys.Gnum = Gnum
                self.sys.Atualiza()
        elif (self.sys.Type == 4):
            # Parse and check NL system input string:
            sysstr = self.sys.NLsysParseString(str(value))
            
            if (sysstr):
                # Change color to green:
                self.statusBar().showMessage(_translate("MainWindow", "Expressão válida!", None))
                self.lineEditGnum.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
                self._set_expression_error('f(y,u)', False)
            else:
                # Wrong input, change color ro red:
                self.statusBar().showMessage(_translate("MainWindow", "Expressão inválida!", None))
                self.lineEditGnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
                self._set_expression_error('f(y,u)', True, '[{}] is not a valid expression'.format(value))
                
    
    def onGdenChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditGden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            self._set_expression_error('G[Den](s)', True, '[{}] is not a valid expression'.format(value))
            return
            
        Gden = self.checkTFinput(value)
        
        if (Gden == 0):
            self.lineEditGden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            self._set_expression_error('G[Den](s)', True, '[{}] is not a valid expression'.format(value))
        else:
            self.lineEditGden.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
            self._set_expression_error('G[Den](s)', False)
            self.sys.GdenStr = str(value)
            if self.sys.Type == 2:
                self.sys.G2den = Gden
            else:
                self.sys.Gden = Gden
            self.sys.Atualiza()

    def onCnumChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditCnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            self._set_expression_error('C[Num](s)', True, '[{}] is not a valid expression'.format(value))
            return
            
        Cnum = self.checkTFinput(value)
        
        if (Cnum == 0):
            self.lineEditCnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            self._set_expression_error('C[Num](s)', True, '[{}] is not a valid expression'.format(value))
        else:
            self.lineEditCnum.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
            self._set_expression_error('C[Num](s)', False)
            self.sys.CnumStr = str(value)
            self.sys.Cnum = Cnum
            self.sys.Atualiza()
    
    def onCdenChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditCden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            self._set_expression_error('C[Den](s)', True, '[{}] is not a valid expression'.format(value))
            return
            
        Cden = self.checkTFinput(value)
        
        if (Cden == 0):
            self.lineEditCden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            self._set_expression_error('C[Den](s)', True, '[{}] is not a valid expression'.format(value))
        else:
            self.lineEditCden.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
            self._set_expression_error('C[Den](s)', False)
            self.sys.CdenStr = str(value)
            self.sys.Cden = Cden
            self.sys.Atualiza()  
      
    def onHnumChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditHnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            self._set_expression_error('H[Num](s)', True, '[{}] is not a valid expression'.format(value))
            return
            
        Hnum = self.checkTFinput(value)
        
        if (Hnum == 0):
            self.lineEditHnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            self._set_expression_error('H[Num](s)', True, '[{}] is not a valid expression'.format(value))
        else:
            self.lineEditHnum.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
            self._set_expression_error('H[Num](s)', False)
            self.sys.HnumStr = str(value)
            self.sys.Hnum = Hnum
            self.sys.Atualiza()
    
    def onHdenChange(self,value):
        """
        When user enters a character.
        """
        if not value:
            self.lineEditHden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            self._set_expression_error('H[Den](s)', True, '[{}] is not a valid expression'.format(value))
            return
            
        Hden = self.checkTFinput(value)
        
        if (Hden == 0):
            self.lineEditHden.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
            self._set_expression_error('H[Den](s)', True, '[{}] is not a valid expression'.format(value))
        else:
            self.lineEditHden.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
            self._set_expression_error('H[Den](s)', False)
            self.sys.HdenStr = str(value)
            self.sys.Hden = Hden
            self.sys.Atualiza()
    
    def checkTFinput(self, value, expr_var='s'):
        """
        Check if input string is correct.
        
        Return 0 if it has an error.
        Otherwise, returns a list with polynomial coefficients
        """
        value = value.replace(' ','') # remove spaces
        value = value.replace(',','.') # change , to .
        value = value.replace(')(',')*(') # insert * between parentesis
        value = value.replace('z','s') # change , to .        
        
        retorno = None
        
        if len(value) == 0:
            return 0
        
        if value[0] == '[':
            try:
                retorno = eval(str(value))
            except:
                retorno = 0
        else:
            try:
                equacao = utils.parseexpr(str(value), expr_var=expr_var)
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
        self.verticalSliderK.valueChanged.disconnect(self.onSliderMove)
        self.verticalSliderK.setSliderPosition(int(position))
        self.verticalSliderK.valueChanged.connect(self.onSliderMove)
    
    def updateSystemPNG(self):
        svg_file_name = ''        
        
        if (self.sys.Type == 0): # LTI system 1 (without C(s))
            if self.sys.Malha == 'Fechada':
                svg_file_name = 'diagram1Closed.png'
            else:
                svg_file_name = 'diagram1Opened.png'
        elif (self.sys.Type == 1): # LTI system 2 (with C(s))
            if self.sys.Malha == 'Fechada':
                svg_file_name = 'diagram2Closed.png'
            else:
                svg_file_name = 'diagram2Opened.png'
        elif (self.sys.Type == 2): # LTI system 3 (with C(s) and G(s) after W(s))
            if self.sys.Malha == 'Fechada':
                svg_file_name = 'diagram3Closed.png'
            else:
                svg_file_name = 'diagram3Opened.png'
        elif (self.sys.Type == 3):
            if self.sys.Malha == 'Fechada':
                svg_file_name = 'diagram4Closed.png'
            else:
                svg_file_name = 'diagram4Opened.png'
        elif (self.sys.Type == 4):
            if self.sys.Malha == 'Fechada':
                svg_file_name = 'diagram5Closed.png'
            else:
                svg_file_name = 'diagram5Opened.png'
        else:
            self.statusBar().showMessage(_translate("MainWindow", "Sistema ainda não implementado.", None))
            return

        self.label.setPixmap(QtGui.QPixmap(svg_file_name))

    
    def onAboutAction(self):
        QtWidgets.QMessageBox.about(self,_translate("MainWindow", "Sobre o LabControle2", None), MESSAGE)
        
    
    def onCalcAction(self):
        try:
            p=subprocess.Popen('calc.exe')
        except OSError:
            QtWidgets.QMessageBox.critical(self,_translate("MainWindow", "Erro!", None),_translate("MainWindow", "Executável da calculadora não encontrado (calc.exe).", None))
            
    
    def onSaveAction(self):
        """
        Save system data in an external file with encrypted data.
        
        If the extension of the file is dat, system data is stored with hide flag = False
        If the extension is tst the hide flag is True.
        """
        fileName = str()
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                _translate("MainWindow", "Salvar sistema", None),
                                "sisXX.LCN",_translate("MainWindow", "Arquivos LabControle Normal (*.LCN);;Arquivos LabControle Oculto (*.LCO)", None),options=options)

        hide = False
        

        if fileName.endswith("LCN"):
            hide = False
            #pickle.dump(expSys, open(fileName, "wb" ),pickle.HIGHEST_PROTOCOL)
            
        elif fileName.endswith("LCO"):
            hide = True
        else:
            self.statusBar().showMessage(_translate("MainWindow", "Tipo de arquivo não reconhecido.", None))
            return
        
        expSys = ExportSystem()
        expSys.Gnum = self.lineEditGnum.text()
        expSys.Gden = self.lineEditGden.text()
        expSys.Cnum = self.lineEditCnum.text()
        expSys.Cden = self.lineEditCden.text()
        expSys.Hnum = self.lineEditHnum.text()
        expSys.Hden = self.lineEditHden.text()
        expSys.K = self.doubleSpinBoxK.value()
        expSys.Type = self.sys.Type
        expSys.Malha = self.sys.Malha
        expSys.Hide = hide
        # Store groupbox checked status:
        expSys.Genabled = self.groupBoxG.isChecked()
        expSys.Cenabled = self.groupBoxC.isChecked()
        expSys.Henabled = self.groupBoxH.isChecked()
        
        # Pickle object into a string:
        temp = pickle.dumps(expSys,1)
        # Encode string:
        temp1 = base64.b64encode(temp)
        # Write encoded string to disk:
        f = open(fileName,"wb")
        f.write(temp1)
        f.close()
        
        self.statusBar().showMessage(_translate("MainWindow", "Sistema salvo.", None))
        
    def onLoadAction(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                _translate("MainWindow", "Abrir arquivo de sistema", None),
                'sys',
                _translate("MainWindow", "Arquivos LabControle (*.LCN *.LCO)", None))
        
        if not fileName:
            return
        
        expSys = ExportSystem()
        
        # Read encoded string from file:
        f = open(fileName, 'rb')
        temp1 = f.read()
        f.close()
        # Decode string:
        temp = base64.b64decode(temp1)
        # Unpickle object from string:
        expSys = pickle.loads(temp)
        
        self.sys.Hide = expSys.Hide        
        
        if expSys.Hide == False:
            self.labelHide.setText('')
            # Update feedback switch
            if expSys.Malha == 'Aberta':
                self.radioBtnOpen.setChecked(True)
            else:
                self.radioBtnClose.setChecked(True)            
            # Update system type and SVG:
            self.sys.Type = expSys.Type
            self.sys.Malha = expSys.Malha        
            self.comboBoxSys.setCurrentIndex(expSys.Type)
            self.onChangeSystem(expSys.Type)
            # Update groupboxes checkboxes:
            self.groupBoxG.setChecked(expSys.Genabled)
            self.groupBoxC.setChecked(expSys.Cenabled)
            self.groupBoxH.setChecked(expSys.Henabled)
            # Update UI and call the callbacks to update system.
            self.lineEditGnum.setText(expSys.Gnum)
            self.onGnumChange(expSys.Gnum)
            self.lineEditGden.setText(expSys.Gden)
            self.onGdenChange(expSys.Gden)
            self.lineEditCnum.setText(expSys.Cnum)
            self.onCnumChange(expSys.Cnum)
            self.lineEditCden.setText(expSys.Cden)
            self.onCdenChange(expSys.Cden)
            self.lineEditHnum.setText(expSys.Hnum)
            self.onHnumChange(expSys.Hnum)
            self.lineEditHden.setText(expSys.Hden)
            self.onHdenChange(expSys.Hden)
            
            # Update gain
            self.doubleSpinBoxK.setValue(expSys.K)
            # Enable or re-enable group boxes:
            self.groupBoxG.setEnabled(True)
            self.groupBoxC.setEnabled(True)
            self.groupBoxH.setEnabled(True)
            # Re-enable Root Locus button:
            self.btnPlotLGR.setEnabled(True)
            self.comboBoxSys.setEnabled(True)
        elif expSys.Hide == True:
            self.labelHide.setText(_translate("MainWindow", "Modo Oculto", None))
            # Update feedback switch
            if expSys.Malha == 'Aberta':
                self.radioBtnOpen.setChecked(True)
            else:
                self.radioBtnClose.setChecked(True)                 
            # Update system type and SVG:                        
            self.sys.Type = expSys.Type
            self.sys.Malha = expSys.Malha
            self.comboBoxSys.setCurrentIndex(expSys.Type)
            self.onChangeSystem(expSys.Type)
            # Update groupboxes checkboxes:
            self.groupBoxG.setChecked(expSys.Genabled)
            self.groupBoxC.setChecked(expSys.Cenabled)
            self.groupBoxH.setChecked(expSys.Henabled)            

            # Call the callbacks to update system.
            self.onGnumChange(expSys.Gnum)
            self.onGdenChange(expSys.Gden)
            self.onCnumChange(expSys.Cnum)
            self.onCdenChange(expSys.Cden)
            self.onHnumChange(expSys.Hnum)
            self.onHdenChange(expSys.Hden)
            
            # Update gain
            self.doubleSpinBoxK.setValue(expSys.K)
            
            #self.onChangeSystem(expSys.Type)
       

            # Update UI:
            self.lineEditGnum.setText('*****')
            self.lineEditGden.setText('*****')
            self.lineEditCnum.setText('*****')
            self.lineEditCden.setText('*****')
            self.lineEditHnum.setText('*****')
            self.lineEditHden.setText('*****')
            # Disable groupboxes:
            self.groupBoxG.setEnabled(False) #setHidden
            self.groupBoxC.setEnabled(False)
            self.groupBoxH.setEnabled(False)
            # Disable Root Locus button:
            self.btnPlotLGR.setEnabled(False)

            # Disable change system combo box:
            self.comboBoxSys.setEnabled(False)
        
    def onResetAction(self):
        self.labelHide.setText('')
        self.radioBtnOpen.setChecked(True)        
        self.sys.Type = 0
        self.sys.Malha = 'Aberta'
        self.comboBoxSys.setCurrentIndex(0)
        self.onChangeSystem(0)
        self.groupBoxG.setEnabled(True)
        self.groupBoxC.setEnabled(True)
        self.groupBoxH.setEnabled(True)
        self.groupBoxC.setChecked(False)
        self.lineEditGnum.setText(str('2*s+10'))
        self.onGnumChange(str('2*s+10'))
        self.lineEditGden.setText(str('1*s^2+2*s+10'))
        self.onGdenChange(str('1*s^2+2*s+10'))
        self.lineEditCnum.setText(str('1'))
        self.onCnumChange(str('1'))
        self.lineEditCden.setText(str('1'))
        self.onCdenChange(str('1'))
        self.lineEditHnum.setText(str('1'))
        self.onHnumChange(str('1'))
        self.lineEditHden.setText(str('1'))
        self.onHdenChange(str('1'))
        self.doubleSpinBoxK.setValue(1)
        self.btnPlotLGR.setEnabled(True)
        self.comboBoxSys.setEnabled(True)

    def onTabChange(self, index):
        # Clearing the lists:
        self.listWidgetCLpoles.clear()
        self.listWidgetOLpoles.clear()
        self.listWidgetOLzeros.clear()
        self.listWidgetRLpoints.clear()
        
        if (self.sys.Hide == True or self.sys.Type > 2):
            txt = _translate("MainWindow", "Desabilitado", None)
            item = QtWidgets.QListWidgetItem()
            item.setText(txt)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.listWidgetCLpoles.addItem(item)
            item = QtWidgets.QListWidgetItem()
            item.setText(txt)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.listWidgetOLpoles.addItem(item)
            item = QtWidgets.QListWidgetItem()
            item.setText(txt)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.listWidgetOLzeros.addItem(item)
            item = QtWidgets.QListWidgetItem()
            item.setText(txt)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.listWidgetRLpoints.addItem(item)
            return
            
        # Check if SysInfo tab:
        if (index == 5):
            # Closed loop poles:
            rootsCL = self.sys.RaizesRL(self.sys.K)
            for root in rootsCL:
                item = QtWidgets.QListWidgetItem()
                item.setText(self.createRootString(root))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.listWidgetCLpoles.addItem(item)
            
            rootsOL = self.sys.RaizesOL()
            for root in rootsOL:
                item = QtWidgets.QListWidgetItem()
                item.setText(self.createRootString(root))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.listWidgetOLpoles.addItem(item)
                
            zerosOL = self.sys.ZerosOL()
            for zero in zerosOL:
                item = QtWidgets.QListWidgetItem()
                item.setText(self.createRootString(zero))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.listWidgetOLzeros.addItem(item)
            
            pontos, ganhos = self.sys.PontosSeparacao()
            i = 0
            for ponto in pontos:
                item = QtWidgets.QListWidgetItem()
                item.setText(self.createRootString(ponto) + " com Kc =  %0.3f" %(ganhos[i]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.listWidgetRLpoints.addItem(item)
                i = i + 1
                
    # Given a numpy number (complex or not) return a formatted string.
    def createRootString(self, root):
        root_str = ''
        r_real = numpy.real(root)
        r_imag = numpy.imag(root)
        
        if (r_imag == 0):
            root_str = str(numpy.around(r_real, decimals=3))
        else:
            if (r_imag > 0):
                root_str = str(numpy.around(r_real, decimals=3)) + ' + j'+ str(numpy.around(r_imag, decimals=3))
            else:
                root_str = str(numpy.around(r_real, decimals=3)) + ' - j'+ str(numpy.around(abs(r_imag), decimals=3))
        
        return root_str
    
        
        


class ExportSystem:
    
    Gnum = str()
    Gden = str()
    Cnum = str()
    Cden = str()
    Hnum = str()
    Hden = str()
    Genabled = True
    Cenabled = False
    Henabled = False
    K = 1.0
    Type = 0
    Malha = 'Aberta'
    Hide = False

        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    locale = QtCore.QLocale.system().name()
    # If not portuguese, instal english translator:
    if (locale != 'pt_BR' and locale != 'pt_PT'):
        translator = QtCore.QTranslator()
        translator.load("LabControl3_en.qm")
        app.installTranslator(translator)
    
    win = LabControl3()
    win.show()
    app.exec_()
