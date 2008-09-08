# -*- coding: iso-8859-1 -*-
#Boa:Frame:Frame

__version__ ='$Rev$'
__date__ = '$LastChangedDate$'

##    Este arquivo é parte do programa LabControle
##
##    LabControle é um software livre; você pode redistribui-lo e/ou 
##    modifica-lo dentro dos termos da Licença Pública Geral GNU como 
##    publicada pela Fundação do Software Livre (FSF); na versão 3 da 
##    Licença.
##
##    Este programa é distribuido na esperança que possa ser  util, 
##    mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a 
##    qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral
##    GNU para maiores detalhes.
##
##    Você deve ter recebido uma cópia da Licença Pública Geral GNU
##    junto com este programa, se não, escreva para a Fundação do Software
##    Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# $Author$
#
#

import wx
from wx.lib.anchors import LayoutAnchors
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
#from matplotlib import rc
#rc('text', usetex=True)
from matplotlib.figure import Figure
from matplotlib.axes import Subplot

from matplotlib.widgets import Button
from matplotlib.patches import Rectangle, FancyArrow,Ellipse

import numpy

from Sistema import *
import DlgFT
import DlgEntrada
import DlgAbout


# define _ or add _ to builtins in your app file
_ = wx.GetTranslation

#from matplotlib.backends.backend_wx import *#NavigationToolbar2Wx

def create(parent):
    return Frame(parent)

[wxID_FRAME, wxID_FRAMEBODEFMAX, wxID_FRAMEBODEFMIN, wxID_FRAMEBODEPONTOS, 
 wxID_FRAMEBTNBODE, wxID_FRAMEBTNLGR, wxID_FRAMEBTNLGRSIM, wxID_FRAMEBUTTON1, 
 wxID_FRAMECONTINUAR, wxID_FRAMEFMAXTXT, wxID_FRAMEFMINTXT, wxID_FRAMEGANHO, 
 wxID_FRAMEGRAFVARLIST, wxID_FRAMEIMBD, wxID_FRAMEKMAX, wxID_FRAMELIMPAR, 
 wxID_FRAMENOTEBOOK, wxID_FRAMEPANEL1, wxID_FRAMEPANEL2, wxID_FRAMEPANEL3, 
 wxID_FRAMEPANEL4, wxID_FRAMEPANEL5, wxID_FRAMEPANEL6, wxID_FRAMEPANELBODE, 
 wxID_FRAMEPANELLGR, wxID_FRAMEPONTOSBODETXT, wxID_FRAMEREBD, wxID_FRAMERIBD, 
 wxID_FRAMESIMULAR, wxID_FRAMESLIDER1, wxID_FRAMESPLITTERWINDOW1, 
 wxID_FRAMESPLITTERWINDOW2, wxID_FRAMESPLITTERWINDOW3, wxID_FRAMESTACOES, 
 wxID_FRAMESTATUSBAR1, wxID_FRAMESTTMAX, wxID_FRAMETMAX, wxID_FRAMETXTBODE, 
 wxID_FRAMETXTIMBD, wxID_FRAMETXTK, wxID_FRAMETXTKMAX, wxID_FRAMETXTOPCOES, 
 wxID_FRAMETXTREDB, wxID_FRAMETXTRIDB, 
] = [wx.NewId() for _init_ctrls in range(44)]

[wxID_FRAMEMENUOPCOESCONFIGMENUITEM1, wxID_FRAMEMENUOPCOESITEMS1, 
] = [wx.NewId() for _init_coll_MenuOpcoes_Items in range(2)]

[wxID_FRAMEARQUIVOMENUITEMSALVAR] = [wx.NewId() for _init_coll_Arquivo_Items in range(1)]

[wxID_FRAMEMENUAJUDAMENUAJUDAITEMSOBRE] = [wx.NewId() for _init_coll_MenuAjuda_Items in range(1)]

class Frame(wx.Frame):
    def _init_coll_flexGridSizer9_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.txtK, 0, border=4,
              flag=wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        parent.AddWindow(self.Ganho, 0, border=4,
              flag=wx.ALIGN_TOP | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)

    def _init_coll_flexGridSizer4_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.txtKmax, 1, border=4,
              flag=wx.ALIGN_CENTER | wx.ALIGN_RIGHT | wx.ALL)
        parent.AddWindow(self.Kmax, 1, border=4, flag=wx.ALL | wx.ALIGN_CENTER)

    def _init_coll_flexGridSizerBode_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.txtBode, 0, border=4,
              flag=wx.EXPAND | wx.ALIGN_CENTER | wx.ALL)
        parent.AddSizer(self.flexGridSizerBode1, 0, border=4,
              flag=wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.panel6, 0, border=4, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.btnBode, 0, border=4,
              flag=wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.button1, 0, border=4,
              flag=wx.ALIGN_CENTER | wx.ALL)

    def _init_coll_flexGridSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.stTmax, 1, border=4,
              flag=wx.ALL | wx.ALIGN_CENTER)
        parent.AddWindow(self.Tmax, 1, border=4, flag=wx.ALL | wx.ALIGN_CENTER)

    def _init_coll_flexGridSizerBode1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.FminTxt, 0, border=4,
              flag=wx.EXPAND | wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.BodeFmin, 0, border=4,
              flag=wx.EXPAND | wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.FmaxTxt, 0, border=4,
              flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER)
        parent.AddWindow(self.BodeFmax, 0, border=4,
              flag=wx.EXPAND | wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.PontosBodeTxt, 0, border=4,
              flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER)
        parent.AddWindow(self.BodePontos, 0, border=4,
              flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER)

    def _init_coll_flexGridSizer3_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.flexGridSizer4, 0, border=0,
              flag=wx.ALL | wx.ALIGN_CENTER)
        parent.AddSizer(self.flexGridSizer8, 1, border=0,
              flag=wx.GROW | wx.ALL | wx.ALIGN_CENTER)
        parent.AddSizer(self.flexGridSizer5, 0, border=0,
              flag=wx.ALL | wx.ALIGN_CENTER)
        parent.AddSizer(self.flexGridSizer6, 0, border=0,
              flag=wx.ALIGN_CENTER | wx.ALL)
        parent.AddSizer(self.flexGridSizer7, 0, border=0,
              flag=wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.btnLGR, 0, border=2,
              flag=wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.btnLGRSim, 0, border=2,
              flag=wx.ALL | wx.ALIGN_CENTER)

    def _init_coll_flexGridSizer2_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableCol(1)

    def _init_coll_flexGridSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.txtOpcoes, 0, border=2,
              flag=wx.ALL | wx.ALIGN_CENTER)
        parent.AddSizer(self.flexGridSizer2, 0, border=4,
              flag=wx.ALL | wx.ALIGN_CENTER)
        parent.AddWindow(self.GrafVarList, 1, border=4, flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.stAcoes, 0, border=4,
              flag=wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.Simular, 0, border=4,
              flag=wx.ALL | wx.ALIGN_CENTER)
        parent.AddWindow(self.Continuar, 0, border=4,
              flag=wx.ALL | wx.ALIGN_CENTER)
        parent.AddWindow(self.Limpar, 0, border=4,
              flag=wx.ALL | wx.ALIGN_CENTER)

    def _init_coll_flexGridSizer3_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(1)
        parent.AddGrowableCol(0)

    def _init_coll_flexGridSizer1_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(2)
        parent.AddGrowableCol(0)

    def _init_coll_flexGridSizer6_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.txtRedb, 0, border=4,
              flag=wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.Rebd, 0, border=4, flag=wx.ALL | wx.ALIGN_CENTER)

    def _init_coll_flexGridSizer7_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.txtImbd, 0, border=4,
              flag=wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.Imbd, 0, border=4, flag=wx.ALL | wx.ALIGN_CENTER)

    def _init_coll_flexGridSizer5_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.txtRidb, 1, border=4,
              flag=wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.Ribd, 1, border=4, flag=wx.ALIGN_CENTER | wx.ALL)

    def _init_coll_flexGridSizerBode1_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableCol(0)

    def _init_coll_flexGridSizer8_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(0)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panel1, 0, border=0, flag=wx.EXPAND)

    def _init_coll_flexGridSizer8_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.flexGridSizer9, 0, border=4,
              flag=wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.slider1, 0, border=4,
              flag=wx.EXPAND | wx.ALIGN_CENTER | wx.ALL)

    def _init_coll_flexGridSizerBode_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(2)
        parent.AddGrowableCol(0)

    def _init_coll_BarraMenus_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.Arquivo, title='Arquivo')
        parent.Append(menu=self.MenuOpcoes, title='Op\xe7\xf5es')
        parent.Append(menu=self.MenuAjuda, title='Ajuda')

    def _init_coll_MenuAjuda_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAMEMENUAJUDAMENUAJUDAITEMSOBRE,
              kind=wx.ITEM_NORMAL, text='Sobre o LabControle')
        self.Bind(wx.EVT_MENU, self.OnMenuAbout,
              id=wxID_FRAMEMENUAJUDAMENUAJUDAITEMSOBRE)

    def _init_coll_MenuOpcoes_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAMEMENUOPCOESCONFIGMENUITEM1,
              kind=wx.ITEM_NORMAL, text='Num. pontos LGR')
        parent.Append(help='', id=wxID_FRAMEMENUOPCOESITEMS1,
              kind=wx.ITEM_NORMAL, text='Simula\xe7\xe3o resolu\xe7\xe3o')
        self.Bind(wx.EVT_MENU, self.OnMenuPontosLGR,
              id=wxID_FRAMEMENUOPCOESCONFIGMENUITEM1)
        self.Bind(wx.EVT_MENU, self.OnMenuSimRes, id=wxID_FRAMEMENUOPCOESITEMS1)

    def _init_coll_Arquivo_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAMEARQUIVOMENUITEMSALVAR,
              kind=wx.ITEM_NORMAL, text='Salvar sistema')

    def _init_coll_Notebook_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel1, select=False,
              text='Diagrama')
        parent.AddPage(imageId=-1, page=self.splitterWindow1, select=True,
              text='Simula\xe7\xe3o')
        parent.AddPage(imageId=-1, page=self.splitterWindow2, select=False,
              text='Lugar das ra\xedzes')
        parent.AddPage(imageId=-1, page=self.splitterWindow3, select=False,
              text='Diagrama de bode')

    def _init_coll_statusBar1_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(2)

        parent.SetStatusText(number=0, text='StatusCampo1')
        parent.SetStatusText(number=1, text='StatusCampo2')

        parent.SetStatusWidths([-1, -1])

    def _init_utils(self):
        # generated method, don't edit
        self.BarraMenus = wx.MenuBar()

        self.MenuOpcoes = wx.Menu(title='')

        self.MenuAjuda = wx.Menu(title='')

        self.Arquivo = wx.Menu(title='')

        self._init_coll_BarraMenus_Menus(self.BarraMenus)
        self._init_coll_MenuOpcoes_Items(self.MenuOpcoes)
        self._init_coll_MenuAjuda_Items(self.MenuAjuda)
        self._init_coll_Arquivo_Items(self.Arquivo)

    def _init_sizers(self):
        # generated method, don't edit
        self.flexGridSizer1 = wx.FlexGridSizer(cols=1, hgap=0, rows=0, vgap=0)

        self.flexGridSizer2 = wx.FlexGridSizer(cols=2, hgap=0, rows=1, vgap=0)

        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.flexGridSizer3 = wx.FlexGridSizer(cols=1, hgap=0, rows=0, vgap=0)
        self.flexGridSizer3.SetMinSize(wx.Size(134, 505))

        self.flexGridSizer4 = wx.FlexGridSizer(cols=2, hgap=0, rows=1, vgap=0)

        self.flexGridSizer5 = wx.FlexGridSizer(cols=2, hgap=0, rows=1, vgap=0)

        self.flexGridSizer6 = wx.FlexGridSizer(cols=2, hgap=0, rows=1, vgap=0)

        self.flexGridSizer7 = wx.FlexGridSizer(cols=2, hgap=0, rows=1, vgap=0)

        self.flexGridSizer8 = wx.FlexGridSizer(cols=0, hgap=0, rows=1, vgap=0)

        self.flexGridSizer9 = wx.FlexGridSizer(cols=1, hgap=0, rows=2, vgap=0)

        self.flexGridSizerBode = wx.FlexGridSizer(cols=1, hgap=0, rows=5,
              vgap=0)

        self.flexGridSizerBode1 = wx.FlexGridSizer(cols=2, hgap=0, rows=3,
              vgap=0)

        self._init_coll_flexGridSizer1_Items(self.flexGridSizer1)
        self._init_coll_flexGridSizer1_Growables(self.flexGridSizer1)
        self._init_coll_flexGridSizer2_Growables(self.flexGridSizer2)
        self._init_coll_flexGridSizer2_Items(self.flexGridSizer2)
        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_flexGridSizer3_Items(self.flexGridSizer3)
        self._init_coll_flexGridSizer3_Growables(self.flexGridSizer3)
        self._init_coll_flexGridSizer4_Items(self.flexGridSizer4)
        self._init_coll_flexGridSizer5_Items(self.flexGridSizer5)
        self._init_coll_flexGridSizer6_Items(self.flexGridSizer6)
        self._init_coll_flexGridSizer7_Items(self.flexGridSizer7)
        self._init_coll_flexGridSizer8_Items(self.flexGridSizer8)
        self._init_coll_flexGridSizer8_Growables(self.flexGridSizer8)
        self._init_coll_flexGridSizer9_Items(self.flexGridSizer9)
        self._init_coll_flexGridSizerBode_Items(self.flexGridSizerBode)
        self._init_coll_flexGridSizerBode_Growables(self.flexGridSizerBode)
        self._init_coll_flexGridSizerBode1_Items(self.flexGridSizerBode1)
        self._init_coll_flexGridSizerBode1_Growables(self.flexGridSizerBode1)

        self.panel2.SetSizer(self.flexGridSizer1)
        self.Notebook.SetSizer(self.boxSizer1)
        self.panel4.SetSizer(self.flexGridSizerBode)
        self.panel5.SetSizer(self.flexGridSizer3)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME, name='Frame', parent=prnt,
              pos=wx.Point(490, 170), size=wx.Size(648, 551),
              style=wx.DEFAULT_FRAME_STYLE,
              title=_('LabControle v1.1 - Sistema continuo - by Moreto'))
        self._init_utils()
        self.SetClientSize(wx.Size(640, 523))
        self.SetStatusBarPane(1)
        self.SetThemeEnabled(False)
        self.SetMenuBar(self.BarraMenus)
        self.SetMinSize(wx.Size(640, 480))
        self.Enable(True)
        self.Center(wx.BOTH)
        self.SetToolTipString(_('LabControle v1.1 - Sistema continuo - by Moreto'))

        self.Notebook = wx.Notebook(id=wxID_FRAMENOTEBOOK, name='Notebook',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(640, 480), style=0)
        self.Notebook.SetFitToCurrentPage(True)
        self.Notebook.SetAutoLayout(True)
        self.Notebook.SetToolTipString(_('Selecione a opera\xe7\xe3o desejada.'))
        self.Notebook.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_FRAMESPLITTERWINDOW1,
              name='splitterWindow1', parent=self.Notebook, pos=wx.Point(0, 0),
              size=wx.Size(632, 454),
              style=wx.SP_3DBORDER | wx.SP_3D | wx.DOUBLE_BORDER)
        self.splitterWindow1.SetMinimumPaneSize(130)
        self.splitterWindow1.SetSashSize(5)
        self.splitterWindow1.SetBorderSize(2)
        self.splitterWindow1.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.splitterWindow1.SetForegroundColour(wx.Colour(255, 0, 0))

        self.panel2 = wx.Panel(id=wxID_FRAMEPANEL2, name='panel2',
              parent=self.splitterWindow1, pos=wx.Point(0, 0), size=wx.Size(130,
              454), style=wx.TAB_TRAVERSAL)
        self.panel2.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.panel2.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.panel2.SetToolTipString('Painel de configura\xe7\xe3o da simula\xe7\xe3o temporal.')

        self.panel3 = wx.Panel(id=wxID_FRAMEPANEL3, name='panel3',
              parent=self.splitterWindow1, pos=wx.Point(135, 0),
              size=wx.Size(497, 454), style=wx.TAB_TRAVERSAL)
        self.panel3.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.splitterWindow1.SplitVertically(self.panel2, self.panel3, 130)

        self.Simular = wx.Button(id=wxID_FRAMESIMULAR, label=_('Simular'),
              name='Simular', parent=self.panel2, pos=wx.Point(21, 314),
              size=wx.Size(88, 40), style=0)
        self.Simular.SetToolTipString(_('Simular o sistema na configura\xe7\xe3o atual.'))
        self.Simular.Bind(wx.EVT_BUTTON, self.OnSimularButton,
              id=wxID_FRAMESIMULAR)

        self.Limpar = wx.Button(id=wxID_FRAMELIMPAR, label=_('Limpar'),
              name='Limpar', parent=self.panel2, pos=wx.Point(21, 410),
              size=wx.Size(88, 40), style=0)
        self.Limpar.SetToolTipString(_('Limpar a \xe1rea do gr\xe1fico.'))
        self.Limpar.Bind(wx.EVT_BUTTON, self.OnLimparButton,
              id=wxID_FRAMELIMPAR)

        self.GrafVarList = wx.CheckListBox(choices=[ 'Saída: y(t)',
              'Entrada: r(t)', 'Erro: e(t)', 'Perturbação: w(t)',
              'Controle: u(t)'], id=wxID_FRAMEGRAFVARLIST, name='GrafVarList',
              parent=self.panel2, pos=wx.Point(4, 66), size=wx.Size(122, 213),
              style=wx.LB_EXTENDED)
        self.GrafVarList.SetStringSelection('')
        self.GrafVarList.SetToolTipString(_('Selecione os sinais que deseja plotar.'))
        self.GrafVarList.SetMinSize(wx.Size(122, 120))

        self.txtOpcoes = wx.StaticText(id=wxID_FRAMETXTOPCOES,
              label=_('Configura\xe7\xf5es:'), name='txtOpcoes',
              parent=self.panel2, pos=wx.Point(4, 2), size=wx.Size(121, 19),
              style=0)
        self.txtOpcoes.Center(wx.BOTH)
        self.txtOpcoes.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))
        self.txtOpcoes.SetToolTipString(_('Painel de configura\xe7\xe3o da simula\xe7\xe3o temporal.'))

        self.stTmax = wx.StaticText(id=wxID_FRAMESTTMAX, label=_('Tmax:'),
              name='stTmax', parent=self.panel2, pos=wx.Point(6, 32),
              size=wx.Size(54, 21), style=wx.ALIGN_RIGHT)
        self.stTmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))
        self.stTmax.Center(wx.BOTH)
        self.stTmax.SetToolTipString(_('Tempo total da simula\xe7\xe3o.'))

        self.Tmax = wx.TextCtrl(id=wxID_FRAMETMAX, name='Tmax',
              parent=self.panel2, pos=wx.Point(68, 31), size=wx.Size(56, 23),
              style=0, value='10')
        self.Tmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))
        self.Tmax.Center(wx.BOTH)
        self.Tmax.SetToolTipString(_('Ajuste o tempo total da simula\xe7\xe3o.'))

        self.Continuar = wx.Button(id=wxID_FRAMECONTINUAR, label=_('Continuar'),
              name='Continuar', parent=self.panel2, pos=wx.Point(21, 362),
              size=wx.Size(88, 40), style=0)
        self.Continuar.SetToolTipString(_('Continuar a simula\xe7\xe3o de onde parou.'))
        self.Continuar.Enable(False)
        self.Continuar.Bind(wx.EVT_BUTTON, self.OnContinuarButton,
              id=wxID_FRAMECONTINUAR)

        self.stAcoes = wx.StaticText(id=wxID_FRAMESTACOES,
              label=_('A\xe7\xf5es:'), name='stAcoes', parent=self.panel2,
              pos=wx.Point(37, 287), size=wx.Size(55, 19),
              style=wx.ALIGN_CENTRE)
        self.stAcoes.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))
        self.stAcoes.SetToolTipString('')

        self.statusBar1 = wx.StatusBar(id=wxID_FRAMESTATUSBAR1,
              name='statusBar1', parent=self, style=0)
        self.statusBar1.SetStatusText('')
        self.statusBar1.SetToolTipString('statusBar1')
        self.statusBar1.SetLabel('StatusCampo1')
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

        self.splitterWindow2 = wx.SplitterWindow(id=wxID_FRAMESPLITTERWINDOW2,
              name='splitterWindow2', parent=self.Notebook, pos=wx.Point(0, 0),
              size=wx.Size(632, 454), style=wx.SP_3D)
        self.splitterWindow2.SetMinimumPaneSize(130)

        self.panelLGR = wx.Panel(id=wxID_FRAMEPANELLGR, name='panelLGR',
              parent=self.splitterWindow2, pos=wx.Point(134, 0),
              size=wx.Size(498, 454), style=wx.TAB_TRAVERSAL)
        self.panelLGR.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.panelLGR.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.panel5 = wx.Panel(id=wxID_FRAMEPANEL5, name='panel5',
              parent=self.splitterWindow2, pos=wx.Point(0, 0), size=wx.Size(130,
              454), style=wx.TAB_TRAVERSAL)
        self.panel5.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.panel5.SetToolTipString('Painel de configura\xe7\xe3o do LGR.')
        self.splitterWindow2.SplitVertically(self.panel5, self.panelLGR, 130)

        self.splitterWindow3 = wx.SplitterWindow(id=wxID_FRAMESPLITTERWINDOW3,
              name='splitterWindow3', parent=self.Notebook, pos=wx.Point(0, 0),
              size=wx.Size(632, 454), style=wx.SP_3D)
        self.splitterWindow3.SetMinimumPaneSize(130)

        self.panel4 = wx.Panel(id=wxID_FRAMEPANEL4, name='panel4',
              parent=self.splitterWindow3, pos=wx.Point(0, 0), size=wx.Size(130,
              454), style=wx.TAB_TRAVERSAL)
        self.panel4.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.panelBode = wx.Panel(id=wxID_FRAMEPANELBODE, name='panelBode',
              parent=self.splitterWindow3, pos=wx.Point(134, 0),
              size=wx.Size(498, 454), style=wx.TAB_TRAVERSAL)
        self.splitterWindow3.SplitVertically(self.panel4, self.panelBode, 130)

        self.panel1 = wx.Panel(id=wxID_FRAMEPANEL1, name='panel1',
              parent=self.Notebook, pos=wx.Point(0, 0), size=wx.Size(632, 454),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.txtKmax = wx.StaticText(id=wxID_FRAMETXTKMAX, label='Kmax:',
              name='txtKmax', parent=self.panel5, pos=wx.Point(9, 5),
              size=wx.Size(64, 21), style=wx.ALIGN_CENTRE | wx.ALIGN_RIGHT)
        self.txtKmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.txtKmax.SetToolTipString('M\xe1ximo ganho utilizado no tra\xe7ado do LGR')

        self.Kmax = wx.TextCtrl(id=wxID_FRAMEKMAX, name='Kmax',
              parent=self.panel5, pos=wx.Point(81, 4), size=wx.Size(40, 24),
              style=0, value='10')
        self.Kmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.Kmax.SetToolTipString('M\xe1ximo ganho utilizado no tra\xe7ado do LGR')
        self.Kmax.Bind(wx.EVT_TEXT, self.OnKmaxText, id=wxID_FRAMEKMAX)

        self.slider1 = wx.Slider(id=wxID_FRAMESLIDER1, maxValue=10, minValue=0,
              name='slider1', parent=self.panel5, pos=wx.Point(80, 36),
              size=wx.Size(46, 227), style=wx.SL_AUTOTICKS | wx.SL_VERTICAL,
              value=0)
        self.slider1.SetMax(100)
        self.slider1.SetMin(0)
        self.slider1.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.slider1.SetToolTipString('Ajuste do ganho')
        self.slider1.SetMinSize(wx.Size(48, 140))
        self.slider1.Bind(wx.EVT_SCROLL, self.OnSlider1Scroll)

        self.txtK = wx.StaticText(id=wxID_FRAMETXTK, label='Ganho:',
              name='txtK', parent=self.panel5, pos=wx.Point(8, 122),
              size=wx.Size(60, 22), style=0)
        self.txtK.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.txtK.SetToolTipString('Ganho atual do sistema.')

        self.Ganho = wx.TextCtrl(id=wxID_FRAMEGANHO, name='Ganho',
              parent=self.panel5, pos=wx.Point(11, 152), size=wx.Size(53, 24),
              style=wx.TE_CENTER, value='1')
        self.Ganho.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.Ganho.SetToolTipString('Ganho atual do sistema.')
        self.Ganho.Bind(wx.EVT_TEXT, self.OnGanhoText, id=wxID_FRAMEGANHO)

        self.txtRidb = wx.StaticText(id=wxID_FRAMETXTRIDB, label='Ribd:',
              name='txtRidb', parent=self.panel5, pos=wx.Point(13, 272),
              size=wx.Size(55, 22), style=wx.ALIGN_RIGHT)
        self.txtRidb.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))

        self.Ribd = wx.TextCtrl(id=wxID_FRAMERIBD, name='Ribd',
              parent=self.panel5, pos=wx.Point(76, 271), size=wx.Size(40, 25),
              style=0, value='0')
        self.Ribd.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.Ribd.SetHelpText('')

        self.txtRedb = wx.StaticText(id=wxID_FRAMETXTREDB, label='Rebd:',
              name='txtRedb', parent=self.panel5, pos=wx.Point(14, 306),
              size=wx.Size(54, 21), style=wx.ALIGN_RIGHT)
        self.txtRedb.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))

        self.Rebd = wx.TextCtrl(id=wxID_FRAMEREBD, name='Rebd',
              parent=self.panel5, pos=wx.Point(76, 304), size=wx.Size(40, 25),
              style=0, value='0')
        self.Rebd.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))

        self.txtImbd = wx.StaticText(id=wxID_FRAMETXTIMBD, label='Imbd:',
              name='txtImbd', parent=self.panel5, pos=wx.Point(14, 340),
              size=wx.Size(54, 19), style=wx.ALIGN_RIGHT)
        self.txtImbd.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))

        self.Imbd = wx.TextCtrl(id=wxID_FRAMEIMBD, name='Imbd',
              parent=self.panel5, pos=wx.Point(76, 337), size=wx.Size(40, 25),
              style=0, value='0')
        self.Imbd.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))

        self.btnLGR = wx.Button(id=wxID_FRAMEBTNLGR, label='Tra\xe7ar LGR',
              name='btnLGR', parent=self.panel5, pos=wx.Point(21, 368),
              size=wx.Size(88, 40), style=0)
        self.btnLGR.SetToolTipString('Tra\xe7ar o LGR')
        self.btnLGR.Bind(wx.EVT_BUTTON, self.OnBtnLGRButton,
              id=wxID_FRAMEBTNLGR)

        self.btnLGRSim = wx.Button(id=wxID_FRAMEBTNLGRSIM, label='Simular',
              name='btnLGRSim', parent=self.panel5, pos=wx.Point(21, 412),
              size=wx.Size(88, 40), style=0)
        self.btnLGRSim.SetToolTipString('Simular o sistema com o ganho atual')
        self.btnLGRSim.Bind(wx.EVT_BUTTON, self.OnSimularButton,
              id=wxID_FRAMEBTNLGRSIM)

        self.txtBode = wx.StaticText(id=wxID_FRAMETXTBODE, label='Bode',
              name='txtBode', parent=self.panel4, pos=wx.Point(4, 4),
              size=wx.Size(122, 28), style=wx.ALIGN_CENTRE)
        self.txtBode.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))

        self.FminTxt = wx.StaticText(id=wxID_FRAMEFMINTXT, label='Fmin:',
              name='FminTxt', parent=self.panel4, pos=wx.Point(5, 44),
              size=wx.Size(64, 25), style=wx.ALIGN_RIGHT)
        self.FminTxt.SetAutoLayout(True)
        self.FminTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.FminTxt.SetToolTipString('Freq. minima para o tra\xe7ado do diagrama de bode.')

        self.BodeFmin = wx.TextCtrl(id=wxID_FRAMEBODEFMIN, name='BodeFmin',
              parent=self.panel4, pos=wx.Point(77, 44), size=wx.Size(48, 25),
              style=0, value='0.01')
        self.BodeFmin.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.BodeFmin.SetToolTipString('Entre com a freq. minima para o tra\xe7ado do diagrama de bode.')

        self.FmaxTxt = wx.StaticText(id=wxID_FRAMEFMAXTXT, label='Fmax:',
              name='FmaxTxt', parent=self.panel4, pos=wx.Point(5, 77),
              size=wx.Size(64, 25), style=wx.ALIGN_RIGHT)
        self.FmaxTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.FmaxTxt.SetToolTipString('Freq. m\xe1xima para o tra\xe7ado do diagrama de bode.')

        self.BodeFmax = wx.TextCtrl(id=wxID_FRAMEBODEFMAX, name='BodeFmax',
              parent=self.panel4, pos=wx.Point(77, 77), size=wx.Size(48, 25),
              style=0, value='100')
        self.BodeFmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.BodeFmax.SetToolTipString('Entre com a freq. m\xe1xima para o tra\xe7ado do diagrama de bode.')

        self.PontosBodeTxt = wx.StaticText(id=wxID_FRAMEPONTOSBODETXT,
              label='Pontos:', name='PontosBodeTxt', parent=self.panel4,
              pos=wx.Point(5, 110), size=wx.Size(64, 25), style=wx.ALIGN_RIGHT)
        self.PontosBodeTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'MS Shell Dlg 2'))
        self.PontosBodeTxt.SetToolTipString('N\xfamero de pontos do gr\xe1fico do diagrama de bode.')

        self.BodePontos = wx.TextCtrl(id=wxID_FRAMEBODEPONTOS,
              name='BodePontos', parent=self.panel4, pos=wx.Point(77, 110),
              size=wx.Size(48, 25), style=0, value='3000')
        self.BodePontos.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.BodePontos.SetToolTipString('Entre com o n\xfamero de pontos do gr\xe1fico do diagrama de bode.')

        self.btnBode = wx.Button(id=wxID_FRAMEBTNBODE, label='Tra\xe7ar Bode',
              name='btnBode', parent=self.panel4, pos=wx.Point(21, 362),
              size=wx.Size(88, 40), style=0)
        self.btnBode.Bind(wx.EVT_BUTTON, self.OnBtnBodeButton,
              id=wxID_FRAMEBTNBODE)

        self.button1 = wx.Button(id=wxID_FRAMEBUTTON1, label='button1',
              name='button1', parent=self.panel4, pos=wx.Point(21, 410),
              size=wx.Size(88, 40), style=0)

        self.panel6 = wx.Panel(id=wxID_FRAMEPANEL6, name='panel6',
              parent=self.panel4, pos=wx.Point(4, 147), size=wx.Size(122, 207),
              style=wx.TAB_TRAVERSAL)
        self.panel6.SetMinSize(wx.Size(122, 40))

        self._init_coll_Notebook_Pages(self.Notebook)

        self._init_sizers()

    def __init__(self, parent):
        

        self._init_ctrls(parent)
        
        # A partir de agora não é código automático do BOA constructor.

        # =============== FLOAT CANVAS ===================
        # Criando FloatCanvas onde é desenhado o diagrama de blocos:
        self.DBFigura, self.DBCanvas = self.DesenhaDiagramaBlocos(self.panel1)

        # =============== FIGURAS DO MATPLOTLIB ==========
        # Criando figuras para plotar os resultados das simulações.
        self.fig1 = self.CriaPainelGrafico(self.panel3)
        self.fig2 = self.CriaPainelGrafico(self.panelLGR)
        self.fig3 = self.CriaPainelGrafico(self.panelBode)

        # Atualiza os sizers:
        self.panel2.Layout()
        self.panel4.Layout()
        self.panel5.Layout()
        self.Layout()

        self.GrafVarList.Check(0,True)
        self.GrafVarList.Check(1,True)
        
        # Limpando barra de status:
        self.statusBar1.SetStatusText(number=0, text='')
        self.statusBar1.SetStatusText(number=1, text='')
        
        # Cria instância do sistema realimentado:
        self.sis = SistemaContinuo()
        
        # Ajusta o slider:
        self.SliderMax = 200
        self.slider1.SetMax(self.SliderMax)
        self.flag = False
        posicao = self.sis.K * (float(self.SliderMax) / self.sis.Kmax)
        self.slider1.SetValue(int(posicao))
        self.slider1.SetTickFreq(self.SliderMax/20) # O número de ticks vai ser 20
 

    def CriaPainelGrafico(self,parent):
        """ Rotina de criação de um painel gráfico para plotar dados.
            Como argumento da função, é passado um objeto do tipo wx.Panel
            onde será criado o FigureCanvas do Matplotlib.
            O Canvas é criado com um sizer e com a toolbar2Wx do Matplotlib.
            
            A função retorna o handler para a figura criada.
        """
        
        
        # Criando figura e toolbar do Matplotlib:
        tamanho = parent.GetSizeTuple()

        figura = Figure()
        canvas = FigureCanvas(parent,-1, figura)
        toolbar = NavigationToolbar2Wx(canvas)
        toolbar.Realize()

        # Colocando Canvas e toolbar no sizer:
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(canvas, 1, wx.GROW)
        sizer.Add(toolbar, 0, wx.ALL|wx.GROW)
        parent.SetSizer(sizer)
        parent.Fit()
        parent.Refresh()
        
        #print sizer.GetSize(), sizer.GetPosition(), tamanho
        
        return figura
    
    def DesenhaDiagramaBlocos(self,parent):

        # Criando o Canvas grafico do Matplotlib:
        tamanho = parent.GetSizeTuple()

        figura = Figure()
        canvas = FigureCanvas(parent,-1, figura)
        # Colocando Canvas e toolbar no sizer:
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(canvas, 1, wx.EXPAND)
        parent.SetSizer(sizer)
        parent.Fit()
        parent.Refresh()
        
        
        parent.SetSize(tamanho)
        
        canvas.draw()
        
        axes1 = figura.add_axes([0.01, 0.01, 0.98, 0.98])
        
        
        # Botões:
        axR = figura.add_axes([0.02, 0.45, 0.08, 0.1])
        axC = figura.add_axes([0.44, 0.45, 0.12, 0.1])
        axG = figura.add_axes([0.8, 0.45, 0.12, 0.1])
        axW = figura.add_axes([0.677-0.05, 0.75, 0.1, 0.1])
        axH = figura.add_axes([0.5, 0.205, 0.12, 0.1])
        axK = figura.add_axes([0.27, 0.45, 0.08, 0.1])
        
        self.axM = figura.add_axes([0.75, 0.228, 0.05*0.619, 0.05])
        btnR = Button(axR, 'Ref')
        btnC = Button(axC, 'C(s)')
        btnG = Button(axG, 'G(s)')
        btnW = Button(axW, 'W(s)')
        btnH = Button(axH, 'H(s)')
        btnK = Button(axK, 'K')
        self.btnM = Button(self.axM, '')
        
        # Eventos dos botões:
        btnR.on_clicked(self.OnBtnR)
        btnC.on_clicked(self.OnBtnC)
        btnG.on_clicked(self.OnBtnG)
        btnW.on_clicked(self.OnBtnW)
        btnH.on_clicked(self.OnBtnH)
        btnK.on_clicked(self.OnBtnK)
        self.btnM.on_clicked(self.OnBtnM)
        
        
        # Setas e linhas:
        axes1.add_patch(FancyArrow(0.93,0.5,0.04,0,0.001,
                            head_width=0.02,head_length=0.02,fc='k'))
        axes1.add_patch(FancyArrow(0.05-0.01,0.5,0.085,0,0.001,
                            head_width=0.02,head_length=0.02,fc='k'))
        axes1.add_patch(FancyArrow(0.16,0.5,0.085,0,0.001,
                            head_width=0.02,head_length=0.02,fc='k'))
        axes1.add_patch(FancyArrow(0.36-0.02,0.5,0.08,0,0.001,
                            head_width=0.02,head_length=0.02,fc='k'))
        axes1.add_patch(FancyArrow(0.56,0.5,0.08-0.005,0,0.001,
                            head_width=0.02,head_length=0.02,fc='k'))
        axes1.add_patch(FancyArrow(0.705,0.5,0.08,0,0.001,
                            head_width=0.02,head_length=0.02,fc='k'))
        axes1.add_patch(FancyArrow(0.68,0.76,0,-0.195,0.001,
                            head_width=0.015,head_length=0.022,fc='k'))
        axes1.add_patch(FancyArrow(0.17,0.25,0,0.2-0.012,0.001,
                            head_width=0.015,head_length=0.022,fc='k'))
        axes1.add_patch(FancyArrow(0.17,0.25,0.77,0,0.002,
                            head_width=0,head_length=0,fc='k'))
        axes1.add_patch(FancyArrow(0.94,0.5,0,-0.25,0.002,
                            head_width=0,head_length=0,fc='k'))

        
        # Somadores:
        axes1.add_patch(Ellipse((0.17,0.5),0.08*0.619,0.08,fc='0.85'))
        axes1.add_patch(Ellipse((0.68,0.5),0.08*0.619,0.08,fc='0.85'))

        # Textos:
        axes1.text(0.15,0.49,'+'); axes1.text(0.66,0.49,'+')
        axes1.text(0.167,0.47,'-'); axes1.text(0.676,0.51,'+')
        axes1.text(0.11,0.53,'r(t)'); axes1.text(0.21,0.53,'e(t)')
        axes1.text(0.73,0.53,'u(t)'); axes1.text(0.95,0.53,'y(t)')
        axes1.text(0.69,0.68,'w(t)')

        axes1.set_axis_off()

        canvas.draw()
        
        return figura, canvas

# Funções dos eventos dos botões:    
    def OnBtnR(self,event):
        """
        Evento do botão da referência.
        """
        dlg = DlgEntrada.Dialog1(self)
        dlg.SetTitle('Parâmetros da entrada r(t)')
        dlg.AtualizaCampos(self.sis.Rt,self.sis.InstRt)
        
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.sis.Rt = dlg.Valor
            self.sis.InstRt = dlg.Instante
            txt = "r(t) atualizada: " + self.sis.Rt + ' em: ' \
                            + str(self.sis.InstRt) + 'seg.'
            self.statusBar1.SetStatusText(number=0, text=txt)
        else:
            self.statusBar1.SetStatusText(number=0, text='r(t) não atualizada')
        
        dlg.Destroy()

    def OnBtnC(self,event):
        """
        Evento do botão do controlador.
        """
        
        dlg = DlgFT.Dialog1(self)
        dlg.SetTitle('Parâmetros de C(s)')
        dlg.AtualizaCampos(self.sis.Cnum,self.sis.Cden)
        
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.sis.Cnum = dlg.Num
            self.sis.Cden = dlg.Den
            txt = "C(s) atualizado: Num=" + str(self.sis.Cnum) + " e Den=" + str(self.sis.Cden)
            self.statusBar1.SetStatusText(number=0, text=txt)
        else:
            self.statusBar1.SetStatusText(number=0, text='C(s) nao atualizado')
        
        dlg.Destroy()
        
        self.sis.Atualiza()

    def OnBtnG(self,event):
        """
        Evento do botão da planta.
        """
        dlg = DlgFT.Dialog1(self)
        dlg.SetTitle('Parâmetros de G(s)')
        dlg.AtualizaCampos(self.sis.Gnum,self.sis.Gden)
        
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.sis.Gnum = dlg.Num
            self.sis.Gden = dlg.Den
            txt = "G(s) atualizado: Num=" + str(self.sis.Gnum) + " e Den=" + str(self.sis.Gden)
            self.statusBar1.SetStatusText(number=0, text=txt)
        else:
            self.statusBar1.SetStatusText(number=0, text='G(s) nao atualizado')
        
        dlg.Destroy()
        
        self.sis.Atualiza()      

    def OnBtnH(self,event):
        """
        Evento do botão da realimentação.
        """
        dlg = DlgFT.Dialog1(self)
        dlg.SetTitle('Parâmetros de H(s)')
        dlg.AtualizaCampos(self.sis.Hnum,self.sis.Hden)
        
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.sis.Hnum = dlg.Num
            self.sis.Hden = dlg.Den
            txt = "H(s) atualizado: Num=" + str(self.sis.Hnum) + " e Den=" + str(self.sis.Hden)
            self.statusBar1.SetStatusText(number=0, text=txt)
        else:
            self.statusBar1.SetStatusText(number=0, text='H(s) nao atualizado')
        
        dlg.Destroy()
        
        self.sis.Atualiza()

    def OnBtnW(self,event):
        """
        Evento do botão da perturbação.
        Permite que o usuário entre com a função ou valor da entrada w(t).
        """
        
        dlg = DlgEntrada.Dialog1(self)
        dlg.SetTitle('Parâmetros da entrada w(t)')
        dlg.AtualizaCampos(self.sis.Wt,self.sis.InstWt)
        
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.sis.Wt = dlg.Valor
            self.sis.InstWt = dlg.Instante
            txt = "w(t) atualizada: " + self.sis.Wt + ' em: ' \
                    + str(self.sis.InstWt) + 'seg.'
            self.statusBar1.SetStatusText(number=0, text=txt)
        else:
            self.statusBar1.SetStatusText(number=0, text='w(t) não atualizada')
        
        dlg.Destroy()
        
    def OnBtnM(self,event):
        """
        Evento do botão abre/fecha a malha.
        """
        self.axM.clear()
        if self.sis.Malha == 'Fechada':
            self.btnM = Button(self.axM, '')
            self.sis.Malha = 'Aberta'
            
        elif self.sis.Malha == 'Aberta':
            self.btnM = Button(self.axM, "------")
            self.sis.Malha = 'Fechada'

        self.DBCanvas.draw()
    
    def OnBtnK(self,event):
        """
        Evento do botão do ganho K.
        """
        K = self.sis.K
        # Cria dialog:
        dialog = wx.TextEntryDialog(self,"Entre com o valor do ganho.",
                "Ajuste do ganho",str(K),style=wx.OK|wx.CANCEL|wx.CENTRE)
        
        # Mostra dialog:
        if dialog.ShowModal() == wx.ID_OK:
            self.sis.K = float(dialog.GetValue())
        else:
            dialog.Destroy()
            return
        
        
        dialog.Destroy()

        # Atualiza interface do LGR:
        self.Ganho.SetValue(str(self.sis.K))

        
##    def onclick(self,event):
##        x = event.xdata
##        y = event.ydata
##        if x != None and y != None:
##            txt = "Posicao (%f, %f)" %(float(x),float(y))
##            self.statusBar1.SetStatusText(number=0, text=txt)
##        else:
##            self.statusBar1.SetStatusText(number=0, text='Fora')

    def OnSimularButton(self, event):
        """
        Botão simular.
        """
        
        Tmax = float(self.Tmax.GetLineText(0))

        self.sis.X0r = None
        self.sis.X0w = None

        stringR = self.sis.Rt
        stringW = self.sis.Wt

        delta_t = 0.01

        # Cria vetor de tempo e de entrada:
        t,r,w = self.sis.CriaEntrada(stringR, stringW, 0, Tmax, delta_t, 
                            self.sis.InstRt, self.sis.InstWt)
        
        self.statusBar1.SetStatusText(number=1,text="Simulando, aguarde...")
        
        # Simula o sistema para a entrada calculada:
        y = self.sis.Simulacao(t, r, w)
        
        self.statusBar1.SetStatusText(number=1,text="Simulação concluída.")
        
        #y,t,u = sis.RespostaDegrau(tempo_degrau=0.5, delta_t=0.01, tmax=Tmax)
        
        # Plotando:
        self.fig1.clf()
        ax = self.fig1.add_subplot(111)
        
        legenda = []

        flag = 0

        # Verificando se a saída está marcada para plotar:
        if self.GrafVarList.IsChecked(0):
            ax.plot(t,y,'r')
            legenda.append(r'Saida: y(t)')
            flag = 1

        # Verificando se a entrada r(t) está marcada para plotar:
        if self.GrafVarList.IsChecked(1):
            ax.plot(t,r,'b')
            legenda.append(r'Entrada: u(t)')
            flag = 1
        # Verificando se o sinal de erro está marcado para plotar:
        if self.GrafVarList.IsChecked(2):
            ax.plot(t,r-y,'g')
            legenda.append(r'Erro: e(t)')
            flag = 1
        # Verificando se a entrada w(t) está marcada para plotar:
        if self.GrafVarList.IsChecked(3):
            ax.plot(t,w,'m')
            legenda.append(r'Perturbacao: w(t)')
            flag = 1
        
        # Se nenhuma saida foi selecionado, não faz nada.
        if flag == 0:
            return
        
        ax.grid()
        
        ylim = ax.get_ylim()
        
        # Seta novo limite máximo do eixo y, somando 1/10 do valor total da escala.
        ax.set_ylim(ymax=(ylim[1]+(ylim[1]-ylim[0])/10))
        
        ax.legend(legenda, loc=0)
        
        ax.set_xlabel('Tempo [s]')
        ax.set_title('Simulacao no tempo')
        
        # Se o tab ativo é outro, troca para o tab da simulação:
        if self.Notebook.GetSelection() != 1:
            self.Notebook.SetSelection(1)
            
        # Atualiza a tela.
        self.fig1.canvas.draw()
        # Habilita botão continuar:
        self.Continuar.Enable()
        
        # Salva dados para o continuar:
        #self.t = t
        #self.r = r
        #self.w = w
        #self.y = y
        
        event.Skip()

    def OnSlider1Scroll(self, event):
        """
        Evento quando a posição do slider é modificada.
        
        Atualiza interface que com a função SetValue dispara o
        evento do wx.TextControl do Ganho e neste outro evento o
        valor do ganho no sistema é atualizado
        """
        
        # Lê slider:
        SliderVal = self.slider1.GetValue()
        # Calcula ganho em função do SliderMax (para dar mais precisão)
        #  já que o wx.Slider só retorna um int:
        Ganho = (self.sis.Kmax / float(self.SliderMax)) * float(self.slider1.GetValue())
        # Atualiza sistema:
        self.sis.K = Ganho
        # Atualiza interface:
        self.flag = True
        self.Ganho.SetValue(str(Ganho))
        self.flag = False
                
        event.Skip()

    def OnKmaxText(self, event):
        """
        Evento quando o texto do Kmax é alterado.
        Altera o valor do Kmax no sistema.
        """
        self.sis.Kmax = float(self.Kmax.GetValue())
        # Escreve mensagem na status bar:
        txt = "Ganho maximo alterado para: %f" %(self.sis.Kmax)
        self.statusBar1.SetStatusText(number=0,text=txt)
        # Atualiza posição do slider:
        posicao = self.sis.K * (float(self.SliderMax) / self.sis.Kmax)
        self.slider1.SetValue(int(posicao))
        
        event.Skip()

    def OnGanhoText(self, event):
        """
        Evento quando o usuário entra com um ganho manualmente.
        """
        
        try: # Testa para ver se o valor digitado é um número.
            Ganho = float(self.Ganho.GetValue())
        except ValueError:
            event.Skip()
            return
        
        # Atualiza sistema:
        self.sis.K = Ganho
        # Escreve mensagem na status bar:
        txt = "Ganho alterado para: %f" %(Ganho)
        self.statusBar1.SetStatusText(number=0,text=txt)

        # Ajusta o slider se o ganho for digitado na interface:
        if self.flag == False:
            posicao = Ganho * (float(self.SliderMax) / self.sis.Kmax)
            self.slider1.SetValue(int(posicao))
        
        self.DesenhaPolosMF(Ganho)
        
        event.Skip()

    def OnBtnLGRButton(self, event):
        """
        Evento do botão de traçado do LGR.
        """
        
        delta_k = float(self.sis.Kmax) / float(self.SliderMax)
        kvect = numpy.arange(0,self.sis.Kmax,delta_k)
        
        txt = "Plotando LGR com %d pontos..." %(len(kvect))
        self.statusBar1.SetStatusText(number=1,text=txt)
        
        self.sis.LGR(kvect,self.fig2)
        
        self.statusBar1.SetStatusText(number=1,text='Finalizado.')
        
        
        # Salva a instância
        self.axesLGR = self.fig2.gca()
        
        self.axesLGR.grid(True)
        self.axesLGR.set_xlabel("Eixo real")
        self.axesLGR.set_ylabel("Eixo imaginario")
        self.axesLGR.set_title("Lugar Geometrico das raizes de C(s)*G(s)")
        
        # Tenta apagar a instância dos pólos em malha fechada na figura. Se já
        # existirem, apaga, senão não faz nada.
        try:
            del self.polosLGR
        except AttributeError:
            pass
        
        # Plota pólos em MF com o ganho inicial do LGR (ganho unitário):
        self.DesenhaPolosMF(self.sis.K)
        
        # # Traçado das regiões proibidas:
        # Parâmetros da interface gráfica:
        Ribd = abs(float(self.Ribd.GetValue()))
        Rebd = abs(float(self.Rebd.GetValue()))
        Imbd = abs(float(self.Imbd.GetValue()))
        
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

        # Atualiza a tela.
        self.fig2.canvas.draw()   
             
        event.Skip()

    def DesenhaPolosMF(self,Ganho):
            
        # Calcula raízes do polinômio 1+k*TF(s):
        raizes = self.sis.RaizesRL(Ganho)
        txt = "Raizes da eq. caracteristica: " + str(raizes)
        self.statusBar1.SetStatusText(number=1,text=txt)
        
        # Plotando pólos do sist. realimentado:
        
        try: # Se nenhum LGR foi traçado, não faz mais nada.
            self.polosLGR[0].set_xdata(real(raizes))
            self.polosLGR[0].set_ydata(imag(raizes))
        except AttributeError:
            try: # Se nenhum polo foi desenhado, desenha então:
                self.polosLGR = self.axesLGR.plot(real(raizes), imag(raizes),
                                'xb',ms=7,mew=3)
            except AttributeError:

                return
            else:
                self.fig2.canvas.draw()
        else:
            self.fig2.canvas.draw()

        finally:
            pass
        
        return

    def OnLimparButton(self, event):
        """
        Evento do botão limpar.
        """
        # Limpando a área do gráfico da simulação:
        self.fig1.clf()
        self.fig1.canvas.draw()
        self.Continuar.Disable()
        
        self.sis.X0r = None
        self.sis.X0w = None
        
        event.Skip()

    def OnContinuarButton(self, event):
        """
        Evento do botão continuar simulação.
        """
        Tmax = float(self.Tmax.GetLineText(0))
        Tinic = self.sis.tfinal
        
        stringR = self.sis.Rt
        stringW = self.sis.Wt

        delta_t = 0.01

        # Cria vetor de tempo e de entrada:
        t,r,w = self.sis.CriaEntrada(stringR, stringW, Tinic , Tmax, delta_t, 
                            self.sis.InstRt, self.sis.InstWt,self.sis.Rfinal,
                            self.sis.Wfinal)
        
        self.statusBar1.SetStatusText(number=1,text="Simulando, aguarde...")
        
        # Simula o sistema para a entrada calculada:
        y = self.sis.Simulacao(t, r, w)
        
        self.statusBar1.SetStatusText(number=1,text="Simulação concluída.")
        
        # Concatenando com os dados da simulação anterior:
        #t = concatenate((self.t,t))
        #r = concatenate((self.r,r))
        #w = concatenate((self.w,w))
        #y = concatenate((self.y,y))
        
        #y,t,u = sis.RespostaDegrau(tempo_degrau=0.5, delta_t=0.01, tmax=Tmax)
        
        # Plotando:
        #self.fig1.clf()
        ax = self.fig1.gca()
        
        legenda = []

        flag = 0

        # Verificando se a saída está marcada para plotar:
        if self.GrafVarList.IsChecked(0):
            ax.plot(t,y,'r')
            legenda.append(r'Saida: y(t)')
            flag = 1

        # Verificando se a entrada r(t) está marcada para plotar:
        if self.GrafVarList.IsChecked(1):
            ax.plot(t,r,'b')
            legenda.append(r'Entrada: u(t)')
            flag = 1
        # Verificando se o sinal de erro está marcado para plotar:
        if self.GrafVarList.IsChecked(2):
            ax.plot(t,r-y,'g')
            legenda.append(r'Erro: e(t)')
            flag = 1
        # Verificando se a entrada w(t) está marcada para plotar:
        if self.GrafVarList.IsChecked(3):
            ax.plot(t,w,'m')
            legenda.append(r'Perturbacao: w(t)')
            flag = 1
        
        # Se nenhuma saida foi selecionado, não faz nada.
        if flag == 0:
            return
        
        ax.grid(True)
        
        ylim = ax.get_ylim()
        
        # Seta novo limite máximo do eixo y, somando 1/10 do valor total da escala.
        ax.set_ylim(ymax=(ylim[1]+(ylim[1]-ylim[0])/10))
        
        ax.legend(legenda, loc=0)
        
        # Se o tab ativo é outro, troca para o tab da simulação:
        if self.Notebook.GetSelection() != 1:
            self.Notebook.SetSelection(1)
            
        # Atualiza a tela.
        self.fig1.canvas.draw()        
        
        event.Skip()

    def OnMenuAbout(self, event):
        """
        Evento do botão "About".
        """
        
        dlg = DlgAbout.AboutDlg(self)
        versao = __version__.strip('$')
        dlg.VersaoTxt.SetLabel("Vers\xe3o: 1.1\nSVN " + versao)
        result = dlg.ShowModal()

        if result == wx.ID_OK:
            self.statusBar1.SetStatusText(number=1,text="Obrigado!")
            
        dlg.Destroy()
        event.Skip()

    def OnMenuPontosLGR(self, event):
        """
        Evento do item do menu configuração para alterar o número de pontos do 
        traçado do LGR.
        """
        # Cria dialog:
        dialog = wx.TextEntryDialog(self,"Entre com o número de pontos\n para o traçado do LGR.",
                "Num. pontos no LGR",str(self.SliderMax),style=wx.OK|wx.CANCEL|wx.CENTRE)
        
        # Mostra dialog:
        if dialog.ShowModal() == wx.ID_OK:
            pontos = int(dialog.GetValue())
        else:
            dialog.Destroy()
            return

        dialog.Destroy()

        # Atualiza o slider:
        self.SliderMax = pontos
        self.slider1.SetMax(self.SliderMax)
        posicao = self.sis.K * (float(self.SliderMax) / self.sis.Kmax)
        self.slider1.SetValue(int(posicao))
        self.slider1.SetTickFreq(self.SliderMax/20) # O número de ticks vai ser 20

        txt = "Num. de pontos: %d" %(self.SliderMax)
        self.statusBar1.SetStatusText(number=0,text=txt)

        event.Skip()

    def OnMenuSimRes(self, event):
        """
        Evento do item do menu configuração para ajustar a resolução (delta t)
        utilizada na simulação no tempo.
        """

        # Cria dialog:
        dialog = wx.TextEntryDialog(self,"Entre com a nova resolução temporal \n para as simulações (em segundos):",
                "Ajuste da resolução",str(self.sis.delta_t),style=wx.OK|wx.CANCEL|wx.CENTRE)
        
        # Mostra dialog:
        if dialog.ShowModal() == wx.ID_OK:
            self.sis.delta_t = float(dialog.GetValue())
        else:
            dialog.Destroy()
            return

        dialog.Destroy()        

        txt = "Resolução: %f seg." %(self.sis.delta_t)
        self.statusBar1.SetStatusText(number=0,text=txt)
        
        event.Skip()

    def OnBtnBodeButton(self, event):
        """
        Evento do botão para traçado do diagrama de Bode.
        """

        # Lendo valores da interface:
        Fmin = float(self.BodeFmin.GetLineText(0))
        Fmax = float(self.BodeFmax.GetLineText(0))
        Pontos = float(self.BodePontos.GetLineText(0))
        
        f=arange(Fmin,Fmax,(Fmax-Fmin)/Pontos)
        
        self.statusBar1.SetStatusText(number=1,text='Tracando bode ...')
        
        self.sis.Bode(f,self.fig3)

        # Atualiza a tela.
        self.fig3.canvas.draw()
        self.statusBar1.SetStatusText(number=1,text='Concluido')
        
        event.Skip()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    
    # choose language
    #locale = wx.Locale(wx.LANGUAGE_ENGLISH_US)
    locale = wx.Locale(wx.LANGUAGE_DEFAULT)
    
    # setup catalog
    wx.Locale.AddCatalogLookupPathPrefix('locale')
    locale.AddCatalog('LabControle')
        
    frame = create(None)
    frame.Show()

    app.MainLoop()
