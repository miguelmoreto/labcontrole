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
from PyQt5.Qt import Qt
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
import logging as lg
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
        # Setting locale to display numbers in the QtextEdits:
        self.locale = QtCore.QLocale.system()
        self.locale.setNumberOptions(self.locale.OmitGroupSeparator | self.locale.RejectGroupSeparator)
        lg.info('Locale used: {s}'.format(s=self.locale.name()))
        self.doubleValidator = QtGui.QDoubleValidator()
        self.doubleValidator.setLocale(self.locale)  # Using system locale for number notation.
        self.doubleValidator.setNotation(self.doubleValidator.StandardNotation)
        self.doubleValidator.setDecimals(4)
        self.lineEditRvalueInit.setValidator(self.doubleValidator)
        self.lineEditWvalueInit.setValidator(self.doubleValidator)
        self.lineEditRvalueFinal.setValidator(self.doubleValidator)
        self.lineEditWvalueFinal.setValidator(self.doubleValidator)
        self.lineEditK.setValidator(self.doubleValidator)
        self.lineEditKlgr.setValidator(self.doubleValidator)
        self.lineEditFmin.setValidator(self.doubleValidator)
        self.lineEditFmax.setValidator(self.doubleValidator)
        self.lineEditFminNyq.setValidator(self.doubleValidator)
        self.lineEditFmaxNyq.setValidator(self.doubleValidator)        

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
        lg.basicConfig(level=lg.DEBUG)
        # Initializing system
        self.sys = MySystem.MySystem()

                
        self.init = 1

        ######################## LabControl 3 stuff:
        self.sysDict = {}   # A dictionary that contains the LC3systems objects and the corresponding data.
        self.sysCurrentName = ''
        self.sysCounter = -1
        self.addSystem(0)
        self.treeWidgetSimul.setColumnWidth(0, 60)

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
        self.tabWidget.currentChanged.connect(self.onTabChange)
        # ComboBoxes:
        self.comboBoxSys.currentIndexChanged.connect(self.onChangeSystem)
        self.comboBoxRinit.currentIndexChanged.connect(self.onChangeRinitInputType)
        self.comboBoxRfinal.currentIndexChanged.connect(self.onChangeRfinalInputType)
        self.comboBoxWinit.currentIndexChanged.connect(self.onChangeWinitInputType)
        self.comboBoxWfinal.currentIndexChanged.connect(self.onChangeWfinalInputType)
        # Lists:
        self.listSystem.itemClicked.connect(self.onSysItemClicked)
        self.treeWidgetSimul.itemClicked.connect(self.onTreeSimulClicked)
        # Spinboxes:
        self.doubleSpinBoxKmax.valueChanged.connect(self.onKmaxChange)
        self.doubleSpinBoxKmin.valueChanged.connect(self.onKminChange)
        self.doubleSpinBoxTmax.valueChanged.connect(self.onTmaxChange)
        self.doubleSpinBoxRtime.valueChanged.connect(self.onRtimeChange)
        self.doubleSpinBoxRnoise.valueChanged.connect(self.onRnoiseChange)
        self.doubleSpinBoxWtime.valueChanged.connect(self.onWtimeChange)
        self.doubleSpinBoxWnoise.valueChanged.connect(self.onWnoiseChange)
        self.doubleSpinBodeRes.valueChanged.connect(self.onBodeResChange)
        self.doubleSpinNyqRes.valueChanged.connect(self.onNyquistResChange)
        self.doubleSpinBoxResT.valueChanged.connect(self.onSimluResChange)
        self.doubleSpinBoxLGRpontos.valueChanged.connect(self.onResLGRchange)
        self.doubleSpinBoxTk.valueChanged.connect(self.onTkChange)
        self.spinBoxPtTk.valueChanged.connect(self.onPointsTkChange)
        # LineEdits:
        self.lineEditRvalueInit.textEdited.connect(self.onRvalueInitChange)
        self.lineEditWvalueInit.textEdited.connect(self.onWvalueInitChange)
        self.lineEditRvalueFinal.textEdited.connect(self.onRvalueFinalChange)
        self.lineEditWvalueFinal.textEdited.connect(self.onWvalueFinalChange)
        self.lineEditK.textEdited.connect(self.onKChange)
        self.lineEditKlgr.textEdited.connect(self.onKChange)
        self.lineEditFmin.textEdited.connect(self.onBodeFminChange)
        self.lineEditFmax.textEdited.connect(self.onBodeFmaxChange)
        self.lineEditFminNyq.textEdited.connect(self.onNyquistFminChange)
        self.lineEditFmaxNyq.textEdited.connect(self.onNyquistFmaxChange)

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
        # Buttons:
        self.btnSimul.clicked.connect(self.onBtnSimul)
        self.btnPlotLGR.clicked.connect(self.onBtnLGR)
        self.btnLGRclear.clicked.connect(self.onBtnLGRclear)
        self.btnPlotBode.clicked.connect(self.onBtnPlotBode)
        self.btnBodeClear.clicked.connect(self.onBtnBodeClear)
        self.btnPlotNyquist.clicked.connect(self.onBtnNyquist)
        self.btnClearNyquist.clicked.connect(self.onBtnNyquistClear)
        self.btnSysAdd.clicked.connect(self.onBtnSysAdd)
        self.btnSysRemove.clicked.connect(self.onBtnSysRemove)
        self.btnSysClear.clicked.connect(self.onBtnSysClear)
        self.btnSimulAdd.clicked.connect(self.onBtnSimulAdd)
        self.btnSimulRemove.clicked.connect(self.onBtnSimulRemove)
        self.btnSimulClear.clicked.connect(self.onBtnSimulClear)
        self.btnSimulClearAxis.clicked.connect(self.onBtnSimulClearAxis)
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
    def onChangeRinitInputType(self, index):
        """
        Read the input types from the UI and store them
        in the current system.
        """
        if (index > 4):
            QtWidgets.QMessageBox.critical(self,_translate("MainWindow", "Atenção!", None),_translate("MainWindow", "Tipo de entrada ainda não implementado.", None))
            self.comboBoxRinit.setCurrentIndex(0)
            return
        print('ok')
        self.sysDict[self.sysCurrentName].Rt_initType = index
    
    def onChangeWinitInputType(self, index):
        if (index > 4):
            QtWidgets.QMessageBox.critical(self,_translate("MainWindow", "Atenção!", None),_translate("MainWindow", "Tipo de entrada ainda não implementado.", None))
            self.comboBoxWinit.setCurrentIndex(0)
            return        
        self.sysDict[self.sysCurrentName].Wt_initType = index

    def onChangeRfinalInputType(self, index):
        if (index > 4):
            QtWidgets.QMessageBox.critical(self,_translate("MainWindow", "Atenção!", None),_translate("MainWindow", "Tipo de entrada ainda não implementado.", None))
            self.comboBoxRfinal.setCurrentIndex(0)
            return
        self.sysDict[self.sysCurrentName].Rt_finalType = index

    def onChangeWfinalInputType(self, index):
        if (index > 4):
            QtWidgets.QMessageBox.critical(self,_translate("MainWindow", "Atenção!", None),_translate("MainWindow", "Tipo de entrada ainda não implementado.", None))
            self.comboBoxWfinal.setCurrentIndex(0)
            return
        self.sysDict[self.sysCurrentName].Wt_finalType = index



    def onSysItemClicked(self,item):
        """
        User clicked in the list of stored system data.
        """
        lg.info('Current system is now {s}'.format(s=item.text()))
        self.sysCurrentName = item.text() # Gets the name of the selected system.
        self.updateUIfromSystem(self.sysCurrentName)
    
    def addSystem(self,systype):
        self.sysCounter = self.sysCounter + 1
        sys = LC3systems.LTIsystem(self.sysCounter,systype)
        self.sysDict[sys.Name] = sys
        self.sysCurrentName = sys.Name
        self.listSystem.addItem(sys.Name)
        self.listSystem.setCurrentRow(self.listSystem.count() - 1)    
        self.updateUIfromSystem(self.sysCurrentName)
    
    def onBtnSysAdd(self):
        self.addSystem(self.comboBoxSys.currentIndex())  # System type from the comboBox
        #self.sysCurrentIndex = self.listSystem.currentRow()
        lg.info('Current system is now {s}'.format(s=self.sysCurrentName))

    def onBtnSysRemove(self):
        itens = self.listSystem.selectedItems()
        if (self.listSystem.count() <= 1):
            QtWidgets.QMessageBox.information(self,_translate("MainWindow", "Atenção!", None), _translate("MainWindow", "Ao menos um sistema deve ser mantido na lista. Remoção não efetuada.", None))
            return
        if not itens:
            QtWidgets.QMessageBox.information(self,_translate("MainWindow", "Atenção!", None), _translate("MainWindow", "Nenhum sistema selecionado para remoção.", None))
            return

        row = self.listSystem.currentRow()
        del(self.sysDict[itens[0].text()]) # Removes from the dictionary the system with the name of the selected item in the list.
        self.listSystem.takeItem(row)

        self.sysCurrentName = self.listSystem.currentItem().text()
        lg.info('Current system is now {s}'.format(s=self.sysCurrentName))

    def onBtnSysClear(self):
        self.listSystem.clear()
        self.sysDict = {}
        self.sysCounter = -1
        self.addSystem(0)
    
    def updateUIfromSystem(self,sysname):
        """
        Updates the User Interface from the parameters stored in the LC3systems object.
        """
        self.lineEditGnum.setText(self.sysDict[sysname].GnumStr)
        self.lineEditGden.setText(self.sysDict[sysname].GdenStr)
        self.lineEditCnum.setText(self.sysDict[sysname].CnumStr)
        self.lineEditCden.setText(self.sysDict[sysname].CdenStr)
        self.lineEditHnum.setText(self.sysDict[sysname].HnumStr)
        self.lineEditHden.setText(self.sysDict[sysname].HdenStr)

        systype = self.sysDict[sysname].Type
        # Comboboxes:
        # Blocking events, otherwise this will trigger the System
        #   type ComboBox CurrentIndexChange event:
        self.comboBoxSys.blockSignals(True) 
        self.comboBoxSys.setCurrentIndex(systype)
        self.comboBoxSys.blockSignals(False)
        self.comboBoxRinit.setCurrentIndex(self.sysDict[sysname].Rt_initType)
        self.comboBoxRfinal.setCurrentIndex(self.sysDict[sysname].Rt_finalType)
        self.comboBoxWinit.setCurrentIndex(self.sysDict[sysname].Wt_initType)
        self.comboBoxWfinal.setCurrentIndex(self.sysDict[sysname].Wt_finalType)

        # Spinboxes update:
        # The spinboxes setValue calls will also trigger the corresponding event handlers:
        self.doubleSpinBoxKmax.setValue(self.sysDict[sysname].Kmax)
        self.doubleSpinBoxKmin.setValue(self.sysDict[sysname].Kmin)
        self.doubleSpinBoxLGRpontos.setValue(self.sysDict[sysname].Kpoints)
        self.doubleSpinBoxResT.setValue(self.sysDict[sysname].Delta_t)
        self.doubleSpinBoxTmax.setValue(self.sysDict[sysname].Tmax)
        self.doubleSpinBoxRtime.setValue(self.sysDict[sysname].InstRt)
        self.doubleSpinBoxWtime.setValue(self.sysDict[sysname].InstWt)
        self.doubleSpinBoxRnoise.setValue(self.sysDict[sysname].NoiseRt)
        self.doubleSpinBoxWnoise.setValue(self.sysDict[sysname].NoiseWt)

        #LineEdits:
        self.lineEditRvalueInit.setText(self.locale.toString(self.sysDict[sysname].Rt_initValue))
        self.lineEditWvalueInit.setText(self.locale.toString(self.sysDict[sysname].Wt_initValue))
        self.lineEditRvalueFinal.setText(self.locale.toString(self.sysDict[sysname].Rt_finalValue))
        self.lineEditWvalueFinal.setText(self.locale.toString(self.sysDict[sysname].Wt_finalValue))
        self.lineEditK.setText(self.locale.toString(self.sysDict[sysname].K))
        self.lineEditKlgr.setText(self.locale.toString(self.sysDict[sysname].K))
        self.onKChange(self.locale.toString(self.sysDict[sysname].K))
        self.lineEditFmin.setText(self.locale.toString(self.sysDict[sysname].Fmin))
        self.lineEditFmax.setText(self.locale.toString(self.sysDict[sysname].Fmax))
        self.lineEditFminNyq.setText(self.locale.toString(self.sysDict[sysname].FminNyq))
        self.lineEditFmaxNyq.setText(self.locale.toString(self.sysDict[sysname].FmaxNyq))        

        # System type specific changes in the UI:
        self.groupBoxC.setChecked(self.sysDict[sysname].Cenable)
        self.groupBoxG.setChecked(self.sysDict[sysname].Genable)
        self.groupBoxH.setChecked(self.sysDict[sysname].Henable)
        if (systype < 3): # LTI system
            if (systype == 0): # LTI system 1 (without C(s))
                self.groupBoxC.setEnabled(False)
            else: # LTI system 2 or 3 (with C(s))
                self.groupBoxC.setEnabled(True)
            self.lineEditGden.show()
            self.labelGden.show()
            self.groupBoxG.setTitle(_translate("MainWindow", "Planta G(s)", None))
            self.labelGnum.setText(_translate("MainWindow", "Num:", None))                
            self.groupBoxH.setEnabled(True)
            self.labelTk.setEnabled(False)
            self.doubleSpinBoxTk.setEnabled(False)
            self.labelPtTk.setEnabled(False)
            self.spinBoxPtTk.setEnabled(False)
            self.doubleSpinBoxResT.setEnabled(True)
            self.btnPlotBode.setEnabled(True)
            self.btnPlotLGR.setEnabled(True)
            self.btnPlotNyquist.setEnabled(True)
            self.groupBoxC.setTitle(_translate("MainWindow", "Controlador C(s)", None)) 
        elif (systype == 3): # Discrete time controler system.
            self.labelGden.show()
            self.lineEditGden.show()
            self.groupBoxG.setTitle(_translate("MainWindow", "Planta G(s)", None))
            self.labelGnum.setText(_translate("MainWindow", "Num:", None))                
            self.labelTk.setEnabled(True)
            self.doubleSpinBoxTk.setEnabled(True)
            self.labelPtTk.setEnabled(True)
            self.spinBoxPtTk.setEnabled(True)
            self.groupBoxC.setEnabled(True)
            self.groupBoxH.setEnabled(False)
            self.doubleSpinBoxResT.setEnabled(False)
            self.btnPlotBode.setEnabled(False)
            self.btnPlotLGR.setEnabled(False)
            self.btnPlotNyquist.setEnabled(False)            
            self.groupBoxC.setTitle(_translate("MainWindow", "Controlador C(z)", None))
        elif (systype == 4):
            self.groupBoxC.setEnabled(True)
            self.groupBoxH.setEnabled(False)
            self.lineEditGden.hide()
            # Disable buttons:
            self.btnPlotBode.setEnabled(False)
            self.btnPlotLGR.setEnabled(False)
            self.btnPlotNyquist.setEnabled(False)
            self.labelGden.hide()
            self.lineEditGnum.setText(self.sysDict[sysname].NLsysInputString)
            #self.onGnumChange(self.sys.sysInputString)
            self.groupBoxG.setTitle(_translate("MainWindow", "EDO não linear", None))
            self.labelGnum.setText(_translate("MainWindow", "f(Y,U)=", None))
            self.groupBoxG.updateGeometry()   
        else:
            QtWidgets.QMessageBox.information(self,_translate("MainWindow", "Aviso!", None), _translate("MainWindow", "Sistema ainda não implementado!", None))
            #self.comboBoxSys.setCurrentIndex(self.currentComboIndex)
            return
        self.updateSystemPNG()                 

    def feedbackOpen(self):
        """Open Feedback """ 

        # Change System Diagram accordingly:        
        self.sysDict[self.sysCurrentName].Loop = 'open'
        self.sysDict[self.sysCurrentName].updateSystem()
        self.updateSystemPNG()
        self.statusBar().showMessage(_translate("MainWindow", "Malha aberta.", None))
    
    def feedbackClose(self):
        """Close Feedback """

        # Change System Diagram accordingly:        
        self.sysDict[self.sysCurrentName].Loop = 'closed'
        self.sysDict[self.sysCurrentName].updateSystem()
        # Change PNG accordingly:        
        self.updateSystemPNG()
        self.statusBar().showMessage(_translate("MainWindow", "Malha fechada.", None))

    def onChangeSystem(self,sysindex):
        """
        When user change system topology using the combo box.
        Change the system type in the current LC3system object and
        update the UI.
        """
        self.sysDict[self.sysCurrentName].changeSystemType(sysindex)
        self.updateUIfromSystem(self.sysCurrentName)
        self.sysDict[self.sysCurrentName].updateSystem()
        self.statusBar().showMessage(_translate("MainWindow", "Sistema alterado.", None))  

    def onSliderMove(self,value):
        """Slider change event. 
        This event is called also when setSliderPosition is called during 
        Kmax and Kmin changes. Changes in Kmax and Kmin only alters position
        of the slider and not the gain. This is why there is this test.
        """
        Kmax = self.sysDict[self.sysCurrentName].Kmax
        Kmin = self.sysDict[self.sysCurrentName].Kmin
        Kpoints = self.sysDict[self.sysCurrentName].Kpoints

        gain = float(value)*float((Kmax)-(Kmin))/float(Kpoints) + Kmin        
        self.sysDict[self.sysCurrentName].K = gain
        # Update spinboxes
        self.lineEditK.setText(self.locale.toString(gain))
        self.lineEditKlgr.setText(self.locale.toString(gain))
        # Update system transfer matrix:
        self.sysDict[self.sysCurrentName].updateSystem()
        # Draw Closed Loop Poles:
        self.DrawCloseLoopPoles(gain)
        
    def onKmaxChange(self,value):
        #self.KmaxminChangeFlag = True # To signal onSliderMove that it is a Kmax change
        self.sysDict[self.sysCurrentName].Kmax = value
        self.updateSliderPosition()
    
    def onKminChange(self,value):
        #self.KmaxminChangeFlag = True # To signal onSliderMove that it is a Kmin change
        self.sysDict[self.sysCurrentName].Kmin = value
        self.updateSliderPosition() # update slider position, this call also the event slider move.
    
    def onKChange(self,val):
        #print('Val is {s} of type {t}'.format(s=val,t=type(val)))
        value,_ = self.locale.toDouble(val)
        # Save K value in the system object:
        self.sysDict[self.sysCurrentName].K = value
        # Update system transfer matrix:
        self.sysDict[self.sysCurrentName].updateSystem()
        
        # Update spinboxes
        self.lineEditK.setText(val)
        self.lineEditKlgr.setText(val)
        
        # Draw Closed Loop Poles:
        self.DrawCloseLoopPoles(value)
        # Update slider position.
        self.updateSliderPosition()
    
    def onTreeSimulClicked(self,item,column):
        """
        When the user clicks in a item from the time simulation treewidget list.
        """
        parent = item.parent()
        if not parent: # I'am interested in only child itens.
            lg.debug('Clicked in parent: sys {s} simul {sm}'.format(s=item.text(0),sm=item.text(1)))
            sysname = item.text(0)
            self.sysDict[sysname].setAtiveTimeSimul(item.text(1))
            return
        sysname = parent.text(0)
        #line_index = 0  # Index used to find, using label, an specific plotted line to remove.
        simulname = parent.text(1)
        signal = item.text(1)
        lg.debug('Clicked on child from: sys {s} simul {sm}'.format(s=item.text(0),sm=item.text(1)))
        self.sysDict[sysname].setAtiveTimeSimul(simulname)
        if (column == 1): # The second column has the checkboxes
            label = '{id}:{s}:{sg}'.format(id=sysname,s=simulname,sg=signal)
            if (item.checkState(column) == Qt.Unchecked): # Plot the selected signal.
                lg.debug('Item {s} enabled to plot.'.format(s=label))
                self.mplSimul.axes.plot(self.sysDict[sysname].TimeSimData[simulname]['data']['time'],self.sysDict[sysname].TimeSimData[simulname]['data'][signal],label=label)
                item.setCheckState(1,Qt.Checked)
            elif (item.checkState(column) == Qt.Checked): # Remove the selected signal from the plot.
                lg.debug('Item {s} disabled to plot.'.format(s=label))
                self.removeExistingPlot(self.mplSimul.axes,label)
                item.setCheckState(1,Qt.Unchecked)
            else:
                lg.debug('Item check state not changed.')
                return
            self.mplSimul.axes.autoscale()
            # Getting the actual plot limits:
            ylim = self.mplSimul.axes.get_ylim()
            # Set a new y limit, adding 1/10 of the total:
            #self.mplSimul.axes.set_ylim(top=(ylim[1]+(ylim[1]-ylim[0])/10))
            self.mplSimul.axes.set_xlim(xmin = 0)        
            self.mplSimul.axes.legend(loc='upper right')
            self.mplSimul.draw()
        else:
            lg.info('Not clicked in the checkbox.')

    def onBtnSimulAdd(self):
        """
        Button event handler to add a simulation in the list.
        """
        self.treeWidgetSimul.clearSelection()
        self.sysDict[self.sysCurrentName].addSimul()    # Adding a TimeSimul data to LC3systems object.
        simulname  = self.sysDict[self.sysCurrentName].CurrentSimulName
        lg.debug('Adding a simulation on System {s} with simulname {n}'.format(s=self.sysCurrentName,n=simulname))
        currentItem = QtWidgets.QTreeWidgetItem(self.treeWidgetSimul)
        currentItem.setText(0, self.sysCurrentName)
        currentItem.setText(1, simulname)
        # Setting a simulation tooltip:
        currentItem.setToolTip(0,'System: {i}, type: {t}'.format(i=self.sysDict[self.sysCurrentName].Name,t=self.sysDict[self.sysCurrentName].TypeStr))
        currentItem.setToolTip(1,'K={k}'.format(k=self.sysDict[self.sysCurrentName].K))
        currentItem.setSelected(True)
        return currentItem

    def onBtnSimulRemove(self):
        """
        Button event handler.
        Removes a simulation from the list:
            - remove the treewidget item
            - remove the correct data form the LC3systems object
            - remove the selected plotted lines from the graph
            - select the previos simul and activates it.
        """
        selectItemList = self.treeWidgetSimul.selectedItems()
        if not selectItemList:
            QtWidgets.QMessageBox.information(self,_translate("MainWindow", "Atenção!", None), _translate("MainWindow", "Nenhuma simulação para ser removida.", None))
            return
        else:
            currentItem = selectItemList[0]
        
        # If no index is readed from column 0, then the selected item is a child item.
        # Thus the parent is used:
        if not currentItem.text(0):
            currentItem = currentItem.parent()
            lg.debug('Removing parent simul item {s} from system {sys}'.format(s=currentItem.text(1),sys=currentItem.text(0)))
            
        sysname = currentItem.text(0) # The sys index of the simul to remove (column 0)
        simnameremove = currentItem.text(1) # The simulation name to remove

        lg.debug(simnameremove)
        lg.debug(sysname)
        lg.debug(self.sysDict[sysname].TimeSimData['Name'])
        lg.debug('Removing simul item {s} from system {sys}'.format(s=simnameremove,sys=sysname))

        if (currentItem.childCount() > 0): # Check if it is an empty (not simulated) list item.
            # Remove plotted lines:
            lg.debug('Item to remove: {s}'.format(s=simnameremove))
            for signal in self.sysDict[sysname].TimeSimData[simnameremove]['data'].keys():
                label = '{id}:{s}:{sg}'.format(id=sysname,s=simnameremove,sg=signal)
                #print(label)
                self.removeExistingPlot(self.mplSimul.axes,label)
                    # Redraw the graphic area:
            self.mplSimul.axes.legend(loc='upper right')
            self.mplSimul.draw()
        
        # Remove simulation data from the LC3systems object:
        self.sysDict[sysname].removeSimul(simnameremove)
        
        root = self.treeWidgetSimul.invisibleRootItem()
        index = root.indexOfChild(currentItem)
        # Select the item above to the one that will be removed (if exists: index > 0):
        if (index > 0):
            newitem = root.child(index - 1)
            #print('Item above: {s}'.format(s=itemabove.text(1)))
            # Setting the active simuldata in the object as the previous one in the list:
            newsysname = newitem.text(0) # Get the itemabove system name.
            lg.debug('The up active simul data will be {i} from system {s}'.format(i=newitem.text(1),s=newsysname))
            self.sysDict[newsysname].setAtiveTimeSimul(newitem.text(1))
        else: # There is only one item (the one to be removed) or it is the first of the list (index=0)
            if (root.childCount() > 1) and index == 0: # There is an item below to the one to be removed.
                newitem = root.child(index + 1)
                newsysname = newitem.text(0) # Get the item below system name.
                lg.debug('The down active simul data will be {i} from system {s}'.format(i=newitem.text(1),s=newsysname))
                self.sysDict[newsysname].setAtiveTimeSimul(newitem.text(1))

        # Removing the item from list:
        root.removeChild(currentItem)
        # Selecting the item above (or below):
        if index:
            # If not index, there is nothing else to select in the treelist
            # Clear list selection:
            self.treeWidgetSimul.clearSelection()
            self.treeWidgetSimul.setCurrentItem(newitem)
        
    def onBtnSimulClearAxis(self):
        # Clear plot area:
        self.mplSimul.axes.cla()
        self.mplSimul.axes.set_xlim(0, self.sysDict[self.sysCurrentName].Tmax)
        self.mplSimul.axes.set_ylim(0, 1)
        self.mplSimul.axes.set_ylabel(_translate("MainWindow", "Valor", None))
        self.mplSimul.axes.set_xlabel(_translate("MainWindow", "Tempo [s]", None))
        self.mplSimul.axes.set_title(_translate("MainWindow", "Simulação no tempo", None))        
        self.mplSimul.axes.grid()
        self.mplSimul.draw()
        
    
    def onBtnSimulClear(self):
        """
        Button event handler.
        Erase all the simulation data:
            - Erase the treewidget list
            - Erase the all the simulation data in the LC3Systems objects.
            - Clear the graphic area.
        """
        # Remove all the itens in the treewidget:
        root = self.treeWidgetSimul.invisibleRootItem()
        root.takeChildren()

        for key in self.sysDict:
            self.sysDict[key].clearTimeSimulData()

        # Clear plot area:
        self.mplSimul.axes.cla()
        self.mplSimul.axes.set_xlim(0, self.sysDict[self.sysCurrentName].Tmax)
        self.mplSimul.axes.set_ylim(0, 1)
        self.mplSimul.axes.set_ylabel(_translate("MainWindow", "Valor", None))
        self.mplSimul.axes.set_xlabel(_translate("MainWindow", "Tempo [s]", None))
        self.mplSimul.axes.set_title(_translate("MainWindow", "Simulação no tempo", None))        
        self.mplSimul.axes.grid()
        self.mplSimul.draw()

    def onBtnSimul(self):
        """
        The main simulation button handler.
        """
        
        # Is the system definition has errors, show the error and finish:
        if self._has_expressions_errors():
            return

        addnewflag = 0
        selectItemList = self.treeWidgetSimul.selectedItems()
        # Check if a simulation data already exists in the treeWidgetSimul
        if not selectItemList:
           # Creating new simulation data:
            currentItem = self.onBtnSimulAdd()
        else:
            currentItem = selectItemList[0]
        
        if not currentItem.childCount():  # Check if the simulation item in the list is empty.
            if not currentItem.parent():  # Check if the selected item is not a child item.
                addnewflag = 1
            else:
                currentItem = currentItem.parent() # The selected item was a child item. Using the parent item.

        sysname = currentItem.text(0)
        simulname = self.sysDict[sysname].CurrentSimulName # Get the simulname
        lg.info('Performing Simulation Name: {s} in System {i}'.format(s=simulname,i=sysname))

        self.statusBar().showMessage(_translate("MainWindow", "Simulando, aguarde...", None))
        # Perform a time domain simulation:
        
        #self.sysDict[sysname].TimeSimulationTesting()
        self.sysDict[sysname].TimeSimulation()

        if (addnewflag): # It is a new simul in the list. Add child itens to it:
            for signal in self.sysDict[sysname].TimeSimData[simulname]['data']:
                if signal != 'time':
                    item = QtWidgets.QTreeWidgetItem(currentItem)   # Creat the child itens in the tree.
                    item.setText(1,signal)
                    item.setFlags(item.flags() & ~(Qt.ItemIsUserCheckable)) # Checkbox handling is done in the clicked event handler.
                    if signal in ['y(t)','r(t)']:   # y(t) and r(t) are checked by default.
                        label = '{id}:{s}:{sg}'.format(id=sysname,s=simulname,sg=signal)
                        self.mplSimul.axes.plot(self.sysDict[sysname].TimeSimData[simulname]['data']['time'],self.sysDict[sysname].TimeSimData[simulname]['data'][signal],label=label)
                        item.setCheckState(1, Qt.Checked)
                    else:
                        item.setCheckState(1, Qt.Unchecked)                
                    #print(signal)

        # Update the graph, according to the itens selected in the list:
        for i in range(currentItem.childCount()):
            item = currentItem.child(i)
            signal = item.text(1)
            label = '{id}:{s}:{sg}'.format(id=sysname,s=simulname,sg=signal)
            if (item.checkState(1) == Qt.Checked): # Only update the checked itens.
                # Remove the existing ploted line:
                self.removeExistingPlot(self.mplSimul.axes,label)
                # Plot the new data
                self.mplSimul.axes.plot(self.sysDict[sysname].TimeSimData[simulname]['data']['time'],self.sysDict[sysname].TimeSimData[simulname]['data'][signal],label=label)
                #print(label)

        self.treeWidgetSimul.expandAll()

        self.statusBar().showMessage(_translate("MainWindow", "Simulação concluída.", None))
        # Format the plotting area:
        self.mplSimul.axes.autoscale()     
        self.mplSimul.axes.grid(True)

        # Getting the actual plot limits:
        #ylim = self.mplSimul.axes.get_ylim()
        # Set a new y limit, adding 1/10 of the total:
        #self.mplSimul.axes.set_ylim(top=(ylim[1]+(ylim[1]-ylim[0])/10))
        self.mplSimul.axes.set_xlim(xmin = 0)        
        self.mplSimul.axes.legend(loc='upper right')
        self.mplSimul.axes.set_ylabel(_translate("MainWindow", "Valor", None))
        self.mplSimul.axes.set_xlabel(_translate("MainWindow", "Tempo [s]", None))
        self.mplSimul.axes.set_title(_translate("MainWindow", "Simulação no tempo", None))        
        self.mplSimul.draw()

    
    def removeExistingPlot(self,ax,label):
        """
        Remove an existem plot line from the graph, based on the label.
        """
        line_index = 0  # Index used to find, using label, an specific plotted line to remove.
        for line in ax.get_lines():
            if (line.get_label() == label):
                #print(line_index)
                line.remove()
            line_index = line_index + 1

    
    def onSimluResChange(self,value):
        """
        DoubleSpinBox event handler.
        Changed simulation resolution
        """
        if (value > 0):
            self.sysDict[self.sysCurrentName].Delta_t = self.doubleSpinBoxResT.value()
            # Update discrete time points per dT.
            self.spinBoxPtTk.blockSignals(True)#  valueChanged.disconnect(self.onPointsTkChange)
            self.sysDict[self.sysCurrentName].Npts_dT = self.sysDict[self.sysCurrentName].dT/self.sysDict[self.sysCurrentName].Delta_t
            self.spinBoxPtTk.setValue(int(self.sysDict[self.sysCurrentName].Npts_dT))
            self.spinBoxPtTk.blockSignals(False)#valueChanged.connect(self.onPointsTkChange)
            
    def onPointsTkChange(self, value):
        """
        DoubleSpinBox event handler.
        Changed number of points per dT in discrete time simulation.
        """
        if (value > 0):
            self.sysDict[self.sysCurrentName].Npts_dT = value
            self.doubleSpinBoxResT.blockSignals(True) #valueChanged.disconnect(self.onSimluResChange)
            # Change simulation resolution system and UI:
            self.sysDict[self.sysCurrentName].Delta_t = self.sysDict[self.sysCurrentName].dT/value
            #self.sys.N = self.sys.Tmax/self.sys.delta_t
            self.doubleSpinBoxResT.setValue(self.sysDict[self.sysCurrentName].Delta_t)
            self.doubleSpinBoxResT.blockSignals(False) #valueChanged.connect(self.onSimluResChange)
            
    def onTkChange(self, value):
        """
        Changed the number of the sample period (dT)
        """
        if (value > 0):
            self.sysDict[self.sysCurrentName].dT = value
            self.sysDict[self.sysCurrentName].NdT = int(self.sysDict[self.sysCurrentName].Tmax/value)
            # Change simulation resolution:
            self.doubleSpinBoxResT.blockSignals(True) #valueChanged.disconnect(self.onSimluResChange)
            # Change simulation resolution system and UI:
            self.sysDict[self.sysCurrentName].Delta_t = value/self.sysDict[self.sysCurrentName].Npts_dT
            #self.sys.N = self.sys.Tmax/self.sys.delta_t
            self.doubleSpinBoxResT.setValue(self.sysDict[self.sysCurrentName].Delta_t)
            self.doubleSpinBoxResT.blockSignals(False) #valueChanged.connect(self.onSimluResChange)     
        
    def onBtnLGR(self):
        """
        Plot LGR graphic.
        """
        if self._has_expressions_errors():
            return

        self.statusBar().showMessage(_translate("MainWindow", "Plotando LGR...", None))
        
        # Plot LGR:
        self.sysDict[self.sysCurrentName].RootLocus()
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
        self.sysDict[self.sysCurrentName].Kpontos = self.doubleSpinBoxLGRpontos.value()
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
        self.sysDict[self.sysCurrentName].FminNyq,_ = self.locale.toDouble(value)

    def onNyquistFmaxChange(self, value):
        """
        Nyquist Fmax edited handler
        """
        self.sysDict[self.sysCurrentName].FmaxNyq,_ = self.locale.toDouble(value)
    
    def onNyquistResChange(self, value):
        """
        Nyquist Resolution edited handler
        """
        self.sysDict[self.sysCurrentName].FpointsNyq = value
   
    
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
        self.sysDict[self.sysCurrentName].Fmin,_ = self.locale.toDouble(value)


    def onBodeFmaxChange(self,value):
        """
        Bode Fmax edited handler
        """
        self.sysDict[self.sysCurrentName].Fmax,_ = self.locale.toDouble(value)

    def onBodeResChange(self,value):
        """
        Bode Resolution edited handler
        """
        self.sysDict[self.sysCurrentName].Fpoints = value

    def onTmaxChange(self,value):
        """
        Tmax edited handler
        """
        self.sysDict[self.sysCurrentName].Tmax = value
        # Update total number of samples:
        #self.sys.N = self.sys.Tmax/self.sys.delta_t
        # Update spinboxes maximum values:
        self.doubleSpinBoxRtime.setMaximum(value)
        self.doubleSpinBoxWtime.setMaximum(value)
        # Update the number of discrete sample periods:
        # TO DO: this kind of stuff shoulg go to LC3systems object:
        self.sysDict[self.sysCurrentName].NdT = int(self.sysDict[self.sysCurrentName].Tmax/self.sysDict[self.sysCurrentName].dT)

    def onRtimeChange(self,value):
        """
        r(t) input time edited handler
        """
        self.sysDict[self.sysCurrentName].InstRt = value
        
    def onRnoiseChange(self,value):
        """
        r(t) noise edited
        """
        self.sysDict[self.sysCurrentName].NoiseRt = value
    
    def onWtimeChange(self,value):
        """
        r(t) input time edited handler
        """
        self.sysDict[self.sysCurrentName].InstWt = value

    def onWnoiseChange(self,value):
        """
        w(t) noise edited
        """
        self.sysDict[self.sysCurrentName].NoiseWt = value
    
    def onRvalueInitChange(self, value):
        """
        Event handler of the line edit. Update the system property.
        """
        self.sysDict[self.sysCurrentName].Rt_initValue,_ = self.locale.toDouble(value)

    def onWvalueInitChange(self, value):
        """
        Event handler of the line edit. Update the system property.
        """
        self.sysDict[self.sysCurrentName].Wt_initValue,_ = self.locale.toDouble(value)


    def onRvalueFinalChange(self,value):
        """
        Event handler of the line edit. Update the system property.
        """
        self.sysDict[self.sysCurrentName].Rt_finalValue,_ = self.locale.toDouble(value)
        # if not value:
        #     self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: rgb(255, 170, 170) }")
        #     return
        # else:
        #     self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: rgb(95, 211, 141) }")
        # valid_value = self.checkTFinput(value, expr_var='t')
        # if valid_value == 0:
        #     self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: rgb(255, 170, 170) }")
        #     self._set_expression_error('r(t)', True, '[{}] is not a valid expression'.format(value))
        #     return
        # self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: rgb(95, 211, 141) }")
        # value = value.replace(',','.')        
        
        # #if (int(value) == 2):
        # #    self.lineEditRvalue.setStyleSheet("QLineEdit { background-color: yellow }")
        # self._set_expression_error('r(t)', False)
        # self.sys.Rt = str(value)
 

    def onWvalueFinalChange(self,value):
        """
        Event handler of the line edit. Update the system property.
        """
        self.sysDict[self.sysCurrentName].Wt_finalValue,_ = self.locale.toDouble(value)
        # if not value:
        #     self.lineEditWvalue.setStyleSheet("QLineEdit { background-color: rgb(255, 170, 170) }")
        #     return
        # else:
        #     self.lineEditWvalue.setStyleSheet("QLineEdit { background-color: rgb(95, 211, 141) }")
        
        # valid_value = self.checkTFinput(value, expr_var='t')
        # if valid_value == 0:
        #     self.lineEditWvalue.setStyleSheet("QLineEdit { background-color: rgb(255, 170, 170) }")
        #     self._set_expression_error('w(t)', True, '[{}] is not a valid expression'.format(value))
        #     return
        # self.lineEditWvalue.setStyleSheet("QLineEdit { background-color: rgb(95, 211, 141) }")
        # value = value.replace(',','.')   
        
        # self._set_expression_error('w(t)', False)
        # self.sys.Wt = str(value)

    def onGroupBoxCcheck(self,flag):
        
        if (flag == False):
            self.statusBar().showMessage(_translate("MainWindow", "C(s) desativada.", None))
        else:
            self.statusBar().showMessage(_translate("MainWindow", "C(s) ativada.", None))
        
        self.sysDict[self.sysCurrentName].Cenable = flag
        self._set_expression_active('C[Num](s)', flag)
        self._set_expression_active('C[Den](s)', flag)

    def onGroupBoxGcheck(self,flag):
        
        if (flag == False):
            self.statusBar().showMessage(_translate("MainWindow", "G(s) desativada.", None))
        else:
            self.statusBar().showMessage(_translate("MainWindow", "G(s) ativada.", None))
        self.sysDict[self.sysCurrentName].Genable = flag
        self._set_expression_active('G[Num](s)', flag)
        self._set_expression_active('G[Den](s)', flag)

    def onGroupBoxHcheck(self,flag):
        
        if (flag == False):
            self.statusBar().showMessage(_translate("MainWindow", "H(s) desativada.", None))
        else:
            self.statusBar().showMessage(_translate("MainWindow", "H(s) ativada.", None))
        self.sysDict[self.sysCurrentName].Henable = flag
        self._set_expression_active('H[Num](s)', flag)
        self._set_expression_active('H[Den](s)', flag)

    # def onGroupBoxWcheck(self,flag):
        
    #     if (flag == False):
    #         self.statusBar().showMessage(_translate("MainWindow", "Perturbação desativada.", None))
    #         self.sys.Wt = '0'
    #         self.sys.InstWt = 0
    #         self.sys.ruidoWt = 0
    #         self.checkBoxPert.setDisabled(True)
    #     else:
    #         self.statusBar().showMessage(_translate("MainWindow", "Perturbação ativada.", None))
    #         self.sys.Wt = str(self.lineEditWvalue.text())
    #         self.sys.InstWt = self.doubleSpinBoxWtime.value()
    #         self.sys.ruidoWt = self.doubleSpinBoxWnoise.value()
    #         self.checkBoxPert.setDisabled(False)
    #     self._set_expression_active('w(t)', flag)

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
            print(Gnum)
            
            if (Gnum == 0):
                # Change color ro red:
                self.lineEditGnum.setStyleSheet("QLineEdit { background-color:  rgb(255, 170, 170) }")
                self._set_expression_error('G[Num](s)', True, '[{}] is not a valid expression'.format(value))
            else:
                # Change color to green:
                self.lineEditGnum.setStyleSheet("QLineEdit { background-color:  rgb(95, 211, 141) }")
                self._set_expression_error('G[Num](s)', False)
                self.sys.GnumStr = str(value)
                ####### LabControl 3: 
                self.sysDict[self.sysCurrentName].Gnum = Gnum
                self.sysDict[self.sysCurrentName].GnumStr = str(value)
                self.sysDict[self.sysCurrentName].updateSystem()
                ####################################
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
            ####### LabControl 3: 
            self.sysDict[self.sysCurrentName].Gden = Gden
            self.sysDict[self.sysCurrentName].GdenStr = str(value)
            self.sysDict[self.sysCurrentName].updateSystem()
            ####################################            
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
            ####### LabControl 3: 
            self.sysDict[self.sysCurrentName].Cnum = Cnum
            self.sysDict[self.sysCurrentName].CnumStr = str(value)
            self.sysDict[self.sysCurrentName].updateSystem()
            ####################################            
    
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
            ####### LabControl 3: 
            self.sysDict[self.sysCurrentName].Cden = Cden
            self.sysDict[self.sysCurrentName].CdenStr = str(value)
            self.sysDict[self.sysCurrentName].updateSystem()
            ####################################                
      
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
            ####### LabControl 3: 
            self.sysDict[self.sysCurrentName].Hnum = Hnum
            self.sysDict[self.sysCurrentName].HnumStr = str(value)
            self.sysDict[self.sysCurrentName].updateSystem()
            ####################################             
    
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
            ####### LabControl 3: 
            self.sysDict[self.sysCurrentName].Hden = Hden
            self.sysDict[self.sysCurrentName].HdenStr = str(value)
            self.sysDict[self.sysCurrentName].updateSystem()
            ####################################             
    
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
        Kmax = self.sysDict[self.sysCurrentName].Kmax
        Kmin = self.sysDict[self.sysCurrentName].Kmin
        Kpoints = self.sysDict[self.sysCurrentName].Kpoints
        K = self.sysDict[self.sysCurrentName].K

        position = (float(Kpoints) * (K - Kmin))/(abs(Kmax)+abs(Kmin))
        # Disconnect events to not enter in a event loop:
        self.verticalSliderK.blockSignals(True)#valueChanged.disconnect(self.onSliderMove)
        self.verticalSliderK.setSliderPosition(int(position))
        self.verticalSliderK.blockSignals(False)#valueChanged.connect(self.onSliderMove)
    
    def updateSystemPNG(self):
        png_file_name = ''  
        systype = self.sysDict[self.sysCurrentName].Type
        loop = self.sysDict[self.sysCurrentName].Loop
        
        if (systype == 0): # LTI system 1 (without C(s))
            if loop == 'closed':
                png_file_name = 'diagram1Closed.png'
            else:
                png_file_name = 'diagram1Opened.png'
        elif (systype == 1): # LTI system 2 (with C(s))
            if loop == 'closed':
                png_file_name = 'diagram2Closed.png'
            else:
                png_file_name = 'diagram2Opened.png'
        elif (systype == 2): # LTI system 3 (with C(s) and G(s) after W(s))
            if loop == 'closed':
                png_file_name = 'diagram3Closed.png'
            else:
                png_file_name = 'diagram3Opened.png'
        elif (systype == 3):
            if loop == 'closed':
                png_file_name = 'diagram4Closed.png'
            else:
                png_file_name = 'diagram4Opened.png'
        elif (systype == 4):
            if loop == 'closed':
                png_file_name = 'diagram5Closed.png'
            else:
                png_file_name = 'diagram5Opened.png'
        else:
            self.statusBar().showMessage(_translate("MainWindow", "Sistema ainda não implementado.", None))
            return

        self.label.setPixmap(QtGui.QPixmap(png_file_name))

    
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
        expSys.K = float(self.lineEditK.text())
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
            self.lineEditK.setText(str(expSys.K))
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
            self.lineEditK.setText(str(expSys.K))
            
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
        self.lineEditK.setText(str(1.00))
        #self.doubleSpinBoxK.setValue(1)
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
    app.setStyle('Fusion')
    locale = QtCore.QLocale.system().name()
    # If not portuguese, instal english translator:
    if (locale != 'pt_BR' and locale != 'pt_PT'):
        translator = QtCore.QTranslator()
        translator.load("LabControl3_en.qm")
        app.installTranslator(translator)
    win = LabControl3()
    win.show()
    app.exec_()
    
