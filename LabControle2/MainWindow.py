# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Tue Apr 01 17:39:27 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(600, 600))
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabDiagrama = QtGui.QWidget()
        self.tabDiagrama.setObjectName(_fromUtf8("tabDiagrama"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.tabDiagrama)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mplDiagrama = MatplotlibWidget(self.tabDiagrama)
        self.mplDiagrama.setEnabled(True)
        self.mplDiagrama.setObjectName(_fromUtf8("mplDiagrama"))
        self.horizontalLayout.addWidget(self.mplDiagrama)
        self.tabWidget.addTab(self.tabDiagrama, _fromUtf8(""))
        self.tabSimul = QtGui.QWidget()
        self.tabSimul.setObjectName(_fromUtf8("tabSimul"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tabSimul)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frameSimul = QtGui.QFrame(self.tabSimul)
        self.frameSimul.setMinimumSize(QtCore.QSize(120, 0))
        self.frameSimul.setMaximumSize(QtCore.QSize(150, 16777215))
        self.frameSimul.setAutoFillBackground(False)
        self.frameSimul.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameSimul.setFrameShadow(QtGui.QFrame.Raised)
        self.frameSimul.setLineWidth(1)
        self.frameSimul.setObjectName(_fromUtf8("frameSimul"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frameSimul)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.labelSimulTit = QtGui.QLabel(self.frameSimul)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelSimulTit.setFont(font)
        self.labelSimulTit.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSimulTit.setObjectName(_fromUtf8("labelSimulTit"))
        self.verticalLayout_2.addWidget(self.labelSimulTit)
        self.labelTmax = QtGui.QLabel(self.frameSimul)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelTmax.setFont(font)
        self.labelTmax.setText(_fromUtf8("Tmax [s]:"))
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.verticalLayout_2.addWidget(self.labelTmax)
        self.lineEditTmax = QtGui.QLineEdit(self.frameSimul)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEditTmax.setFont(font)
        self.lineEditTmax.setInputMask(_fromUtf8(""))
        self.lineEditTmax.setText(_fromUtf8("10"))
        self.lineEditTmax.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditTmax.setPlaceholderText(_fromUtf8(""))
        self.lineEditTmax.setObjectName(_fromUtf8("lineEditTmax"))
        self.verticalLayout_2.addWidget(self.lineEditTmax)
        spacerItem = QtGui.QSpacerItem(20, 60, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.labelMostrar = QtGui.QLabel(self.frameSimul)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelMostrar.setFont(font)
        self.labelMostrar.setObjectName(_fromUtf8("labelMostrar"))
        self.verticalLayout_2.addWidget(self.labelMostrar)
        self.checkBoxSaida = QtGui.QCheckBox(self.frameSimul)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.checkBoxSaida.setFont(font)
        self.checkBoxSaida.setChecked(True)
        self.checkBoxSaida.setObjectName(_fromUtf8("checkBoxSaida"))
        self.verticalLayout_2.addWidget(self.checkBoxSaida)
        self.checkBoxEntrada = QtGui.QCheckBox(self.frameSimul)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBoxEntrada.setFont(font)
        self.checkBoxEntrada.setChecked(True)
        self.checkBoxEntrada.setObjectName(_fromUtf8("checkBoxEntrada"))
        self.verticalLayout_2.addWidget(self.checkBoxEntrada)
        self.checkBoxErro = QtGui.QCheckBox(self.frameSimul)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBoxErro.setFont(font)
        self.checkBoxErro.setObjectName(_fromUtf8("checkBoxErro"))
        self.verticalLayout_2.addWidget(self.checkBoxErro)
        self.checkBoxPert = QtGui.QCheckBox(self.frameSimul)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBoxPert.setFont(font)
        self.checkBoxPert.setObjectName(_fromUtf8("checkBoxPert"))
        self.verticalLayout_2.addWidget(self.checkBoxPert)
        spacerItem1 = QtGui.QSpacerItem(20, 61, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.btnPlot = QtGui.QPushButton(self.frameSimul)
        self.btnPlot.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnPlot.setFont(font)
        self.btnPlot.setObjectName(_fromUtf8("btnPlot"))
        self.verticalLayout_2.addWidget(self.btnPlot)
        self.btnContinuar = QtGui.QPushButton(self.frameSimul)
        self.btnContinuar.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnContinuar.setFont(font)
        self.btnContinuar.setObjectName(_fromUtf8("btnContinuar"))
        self.verticalLayout_2.addWidget(self.btnContinuar)
        self.btnLimparSimul = QtGui.QPushButton(self.frameSimul)
        self.btnLimparSimul.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnLimparSimul.setFont(font)
        self.btnLimparSimul.setObjectName(_fromUtf8("btnLimparSimul"))
        self.verticalLayout_2.addWidget(self.btnLimparSimul)
        self.horizontalLayout_2.addWidget(self.frameSimul)
        self.VBoxLayoutSimul = QtGui.QVBoxLayout()
        self.VBoxLayoutSimul.setObjectName(_fromUtf8("VBoxLayoutSimul"))
        self.mplSimul = MatplotlibWidget(self.tabSimul)
        self.mplSimul.setObjectName(_fromUtf8("mplSimul"))
        self.VBoxLayoutSimul.addWidget(self.mplSimul)
        self.horizontalLayout_2.addLayout(self.VBoxLayoutSimul)
        self.tabWidget.addTab(self.tabSimul, _fromUtf8(""))
        self.tabLGR = QtGui.QWidget()
        self.tabLGR.setObjectName(_fromUtf8("tabLGR"))
        self.tabWidget.addTab(self.tabLGR, _fromUtf8(""))
        self.tabBode = QtGui.QWidget()
        self.tabBode.setObjectName(_fromUtf8("tabBode"))
        self.tabWidget.addTab(self.tabBode, _fromUtf8(""))
        self.tabNiquist = QtGui.QWidget()
        self.tabNiquist.setObjectName(_fromUtf8("tabNiquist"))
        self.tabWidget.addTab(self.tabNiquist, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuArquivo = QtGui.QMenu(self.menubar)
        self.menuArquivo.setObjectName(_fromUtf8("menuArquivo"))
        self.menuOp_es = QtGui.QMenu(self.menubar)
        self.menuOp_es.setObjectName(_fromUtf8("menuOp_es"))
        self.menuIdioma_Language = QtGui.QMenu(self.menubar)
        self.menuIdioma_Language.setObjectName(_fromUtf8("menuIdioma_Language"))
        self.menuAjuda = QtGui.QMenu(self.menubar)
        self.menuAjuda.setObjectName(_fromUtf8("menuAjuda"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSalvar_sistema = QtGui.QAction(MainWindow)
        self.actionSalvar_sistema.setObjectName(_fromUtf8("actionSalvar_sistema"))
        self.actionCarregar_sistema = QtGui.QAction(MainWindow)
        self.actionCarregar_sistema.setObjectName(_fromUtf8("actionCarregar_sistema"))
        self.actionResolu_o_da_simula_o = QtGui.QAction(MainWindow)
        self.actionResolu_o_da_simula_o.setObjectName(_fromUtf8("actionResolu_o_da_simula_o"))
        self.actionN_mero_de_pontos_LGR = QtGui.QAction(MainWindow)
        self.actionN_mero_de_pontos_LGR.setObjectName(_fromUtf8("actionN_mero_de_pontos_LGR"))
        self.actionSobre_o_LabControle = QtGui.QAction(MainWindow)
        self.actionSobre_o_LabControle.setObjectName(_fromUtf8("actionSobre_o_LabControle"))
        self.menuArquivo.addAction(self.actionSalvar_sistema)
        self.menuArquivo.addAction(self.actionCarregar_sistema)
        self.menuOp_es.addAction(self.actionResolu_o_da_simula_o)
        self.menuOp_es.addAction(self.actionN_mero_de_pontos_LGR)
        self.menuAjuda.addAction(self.actionSobre_o_LabControle)
        self.menubar.addAction(self.menuArquivo.menuAction())
        self.menubar.addAction(self.menuOp_es.menuAction())
        self.menubar.addAction(self.menuIdioma_Language.menuAction())
        self.menubar.addAction(self.menuAjuda.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "LabControle 2.0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDiagrama), _translate("MainWindow", "Diagrama", None))
        self.labelSimulTit.setText(_translate("MainWindow", "Configuração", None))
        self.lineEditTmax.setToolTip(_translate("MainWindow", "Tempo máximo de simulação", None))
        self.labelMostrar.setText(_translate("MainWindow", "Mostrar:", None))
        self.checkBoxSaida.setText(_translate("MainWindow", "Saída: y(t)", None))
        self.checkBoxEntrada.setText(_translate("MainWindow", "Entrada: u(t)", None))
        self.checkBoxErro.setText(_translate("MainWindow", "Erro: e(t)", None))
        self.checkBoxPert.setText(_translate("MainWindow", "Perturbação: w(t)", None))
        self.btnPlot.setText(_translate("MainWindow", "Plot", None))
        self.btnContinuar.setText(_translate("MainWindow", "Continuar", None))
        self.btnLimparSimul.setText(_translate("MainWindow", "Limpar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSimul), _translate("MainWindow", "Simulação", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLGR), _translate("MainWindow", "Lugar das Raízes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBode), _translate("MainWindow", "Diagrama de Bode", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNiquist), _translate("MainWindow", "Diagrama de Nyquist", None))
        self.menuArquivo.setTitle(_translate("MainWindow", "Arquivo", None))
        self.menuOp_es.setTitle(_translate("MainWindow", "Opções", None))
        self.menuIdioma_Language.setTitle(_translate("MainWindow", "Idioma/Language", None))
        self.menuAjuda.setTitle(_translate("MainWindow", "Ajuda", None))
        self.actionSalvar_sistema.setText(_translate("MainWindow", "Salvar sistema", None))
        self.actionCarregar_sistema.setText(_translate("MainWindow", "Carregar sistema", None))
        self.actionResolu_o_da_simula_o.setText(_translate("MainWindow", "Resolução da simulação", None))
        self.actionResolu_o_da_simula_o.setToolTip(_translate("MainWindow", "Alterar a resolução da simulação", None))
        self.actionN_mero_de_pontos_LGR.setText(_translate("MainWindow", "Número de pontos LGR", None))
        self.actionN_mero_de_pontos_LGR.setToolTip(_translate("MainWindow", "Alterar o número de pontos do Lugar Geométrico das Raízes", None))
        self.actionSobre_o_LabControle.setText(_translate("MainWindow", "Sobre o LabControle", None))

from matplotlibwidget import MatplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
