# -*- coding: iso-8859-1 -*-
#Boa:Frame:Frame

import wx
from wx.lib.anchors import LayoutAnchors
import matplotlib
matplotlib.use('WX')
from matplotlib.backends.backend_wx import NavigationToolbar2Wx, FigureCanvasWx,\
     FigureManager

from matplotlib.figure import Figure
from matplotlib.axes import Subplot
import matplotlib.numerix as numpy

#from matplotlib.backends.backend_wx import *#NavigationToolbar2Wx

def create(parent):
    return Frame(parent)

[wxID_FRAME, wxID_FRAMECONTINUAR, wxID_FRAMEGRAFVARLIST, wxID_FRAMELIMPAR, 
 wxID_FRAMENOTEBOOK, wxID_FRAMEPANEL1, wxID_FRAMEPANEL2, wxID_FRAMEPANEL3, 
 wxID_FRAMEPANEL4, wxID_FRAMEPANEL5, wxID_FRAMEPANELBODE, wxID_FRAMEPANELLGR, 
 wxID_FRAMESIMULAR, wxID_FRAMESPLITTERWINDOW1, wxID_FRAMESPLITTERWINDOW2, 
 wxID_FRAMESPLITTERWINDOW3, wxID_FRAMESTACOES, wxID_FRAMESTATUSBAR1, 
 wxID_FRAMESTTMAX, wxID_FRAMETMAX, wxID_FRAMETXTOPCOES, 
] = [wx.NewId() for _init_ctrls in range(21)]

[wxID_FRAMEARQUIVOMENUITEMSALVAR] = [wx.NewId() for _init_coll_Arquivo_Items in range(1)]

[wxID_FRAMEMENUOPCOESCONFIGMENUITEM1] = [wx.NewId() for _init_coll_MenuOpcoes_Items in range(1)]

[wxID_FRAMEMENUAJUDAMENUAJUDAITEMSOBRE] = [wx.NewId() for _init_coll_MenuAjuda_Items in range(1)]

class Frame(wx.Frame):
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

    def _init_coll_flexGridSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.stTmax, 1, border=4,
              flag=wx.ALL | wx.ALIGN_CENTER)
        parent.AddWindow(self.Tmax, 1, border=4, flag=wx.ALL | wx.ALIGN_CENTER)

    def _init_coll_flexGridSizer1_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(2)
        parent.AddGrowableCol(0)

    def _init_coll_flexGridSizer2_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableCol(1)

    def _init_coll_BarraMenus_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.Arquivo, title='Arquivo')
        parent.Append(menu=self.MenuOpcoes, title='Op\xe7\xf5es')
        parent.Append(menu=self.MenuAjuda, title='Ajuda')

    def _init_coll_MenuAjuda_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAMEMENUAJUDAMENUAJUDAITEMSOBRE,
              kind=wx.ITEM_NORMAL, text='Sobre o LabControle')

    def _init_coll_MenuOpcoes_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAMEMENUOPCOESCONFIGMENUITEM1,
              kind=wx.ITEM_NORMAL, text='Configura\xe7\xe3o')

    def _init_coll_Arquivo_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAMEARQUIVOMENUITEMSALVAR,
              kind=wx.ITEM_NORMAL, text='Salvar sistema')

    def _init_coll_Notebook_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel1, select=False,
              text='Diagrama')
        parent.AddPage(imageId=-1, page=self.splitterWindow1, select=False,
              text='Simula\xe7\xe3o')
        parent.AddPage(imageId=-1, page=self.splitterWindow2, select=False,
              text='Lugar das ra\xedzes')
        parent.AddPage(imageId=-1, page=self.splitterWindow3, select=True,
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

        self._init_coll_flexGridSizer1_Items(self.flexGridSizer1)
        self._init_coll_flexGridSizer1_Growables(self.flexGridSizer1)
        self._init_coll_flexGridSizer2_Growables(self.flexGridSizer2)
        self._init_coll_flexGridSizer2_Items(self.flexGridSizer2)

        self.panel2.SetSizer(self.flexGridSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME, name='Frame', parent=prnt,
              pos=wx.Point(457, 308), size=wx.Size(725, 512),
              style=wx.DEFAULT_FRAME_STYLE,
              title='LabControle - Sistema continuo')
        self._init_utils()
        self.SetClientSize(wx.Size(717, 484))
        self.SetStatusBarPane(1)
        self.SetThemeEnabled(False)
        self.SetMenuBar(self.BarraMenus)

        self.Notebook = wx.Notebook(id=wxID_FRAMENOTEBOOK, name='Notebook',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(717, 441), style=0)
        self.Notebook.SetFitToCurrentPage(True)
        self.Notebook.SetAutoLayout(True)

        self.panel1 = wx.Panel(id=wxID_FRAMEPANEL1, name='panel1',
              parent=self.Notebook, pos=wx.Point(0, 0), size=wx.Size(709, 415),
              style=wx.TAB_TRAVERSAL)

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_FRAMESPLITTERWINDOW1,
              name='splitterWindow1', parent=self.Notebook, pos=wx.Point(0, 0),
              size=wx.Size(709, 415),
              style=wx.SP_3DBORDER | wx.SP_3D | wx.DOUBLE_BORDER)
        self.splitterWindow1.SetMinimumPaneSize(130)
        self.splitterWindow1.SetSashSize(5)
        self.splitterWindow1.SetBorderSize(2)
        self.splitterWindow1.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.splitterWindow1.SetForegroundColour(wx.Colour(255, 0, 0))

        self.panel2 = wx.Panel(id=wxID_FRAMEPANEL2, name='panel2',
              parent=self.splitterWindow1, pos=wx.Point(0, 0), size=wx.Size(130,
              415), style=wx.TAB_TRAVERSAL)
        self.panel2.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.panel2.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)

        self.panel3 = wx.Panel(id=wxID_FRAMEPANEL3, name='panel3',
              parent=self.splitterWindow1, pos=wx.Point(135, 0),
              size=wx.Size(574, 415), style=wx.TAB_TRAVERSAL)
        self.panel3.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.splitterWindow1.SplitVertically(self.panel2, self.panel3, 130)

        self.Simular = wx.Button(id=wxID_FRAMESIMULAR, label='Simular',
              name='Simular', parent=self.panel2, pos=wx.Point(27, 326),
              size=wx.Size(75, 23), style=0)

        self.Limpar = wx.Button(id=wxID_FRAMELIMPAR, label='Limpar',
              name='Limpar', parent=self.panel2, pos=wx.Point(27, 388),
              size=wx.Size(75, 23), style=0)

        self.GrafVarList = wx.CheckListBox(choices=[], id=wxID_FRAMEGRAFVARLIST,
              name='GrafVarList', parent=self.panel2, pos=wx.Point(4, 66),
              size=wx.Size(122, 225), style=0)
        self.GrafVarList.SetStringSelection('')

        self.txtOpcoes = wx.StaticText(id=wxID_FRAMETXTOPCOES,
              label='Configura\xe7\xf5es:', name='txtOpcoes',
              parent=self.panel2, pos=wx.Point(4, 2), size=wx.Size(121, 19),
              style=0)
        self.txtOpcoes.Center(wx.BOTH)
        self.txtOpcoes.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.stTmax = wx.StaticText(id=wxID_FRAMESTTMAX, label='Tmax:',
              name='stTmax', parent=self.panel2, pos=wx.Point(6, 32),
              size=wx.Size(54, 21), style=wx.ALIGN_RIGHT)
        self.stTmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))
        self.stTmax.Center(wx.BOTH)

        self.Tmax = wx.TextCtrl(id=wxID_FRAMETMAX, name='Tmax',
              parent=self.panel2, pos=wx.Point(68, 31), size=wx.Size(56, 23),
              style=0, value='10')
        self.Tmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))
        self.Tmax.Center(wx.BOTH)

        self.Continuar = wx.Button(id=wxID_FRAMECONTINUAR, label='Continuar',
              name='Continuar', parent=self.panel2, pos=wx.Point(27, 357),
              size=wx.Size(75, 23), style=0)

        self.stAcoes = wx.StaticText(id=wxID_FRAMESTACOES, label='A\xe7\xf5es:',
              name='stAcoes', parent=self.panel2, pos=wx.Point(37, 299),
              size=wx.Size(55, 19), style=wx.ALIGN_CENTRE)
        self.stAcoes.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.statusBar1 = wx.StatusBar(id=wxID_FRAMESTATUSBAR1,
              name='statusBar1', parent=self, style=0)
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

        self.splitterWindow2 = wx.SplitterWindow(id=wxID_FRAMESPLITTERWINDOW2,
              name='splitterWindow2', parent=self.Notebook, pos=wx.Point(0, 0),
              size=wx.Size(709, 415), style=wx.SP_3D)
        self.splitterWindow2.SetMinimumPaneSize(130)

        self.panelLGR = wx.Panel(id=wxID_FRAMEPANELLGR, name='panelLGR',
              parent=self.splitterWindow2, pos=wx.Point(134, 0),
              size=wx.Size(575, 415), style=wx.TAB_TRAVERSAL)

        self.panel5 = wx.Panel(id=wxID_FRAMEPANEL5, name='panel5',
              parent=self.splitterWindow2, pos=wx.Point(0, 0), size=wx.Size(130,
              415), style=wx.TAB_TRAVERSAL)
        self.splitterWindow2.SplitVertically(self.panel5, self.panelLGR, 130)

        self.splitterWindow3 = wx.SplitterWindow(id=wxID_FRAMESPLITTERWINDOW3,
              name='splitterWindow3', parent=self.Notebook, pos=wx.Point(0, 0),
              size=wx.Size(709, 415), style=wx.SP_3D)
        self.splitterWindow3.SetMinimumPaneSize(130)

        self.panel4 = wx.Panel(id=wxID_FRAMEPANEL4, name='panel4',
              parent=self.splitterWindow3, pos=wx.Point(0, 0), size=wx.Size(130,
              415), style=wx.TAB_TRAVERSAL)

        self.panelBode = wx.Panel(id=wxID_FRAMEPANELBODE, name='panelBode',
              parent=self.splitterWindow3, pos=wx.Point(134, 0),
              size=wx.Size(575, 415), style=wx.TAB_TRAVERSAL)
        self.splitterWindow3.SplitVertically(self.panel4, self.panelBode, 130)

        self._init_coll_Notebook_Pages(self.Notebook)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # A partir de agora não é código automático do BOA constructor.
        # Criando figura para plotar o resultado da simulação.
        fig1 = self.CriaPainelGrafico(self.panel3)
        fig2 = self.CriaPainelGrafico(self.panelLGR)
        fig3 = self.CriaPainelGrafico(self.panelBode)
        

        # Exemplo de plot.
        self.plot_data(fig1)
        self.plot_data(fig2)
        self.plot_data(fig3)

        a = self.GetSize()
        
        self.SetSize(a)

        # Atualiza os sizers:
        self.panel2.Layout()
        self.Layout()
        #self.panel3.Layout()

        #self.Show()
        
    def plot_data(self,figura):
        
        # Use ths line if using a toolbar
        a = figura.add_subplot(111)
        
        #a.set_axis_bgcolor(color = '0.2')
        # Or this one if there is no toolbar
        #a = Subplot(self.fig, 111)
        
        t = numpy.arange(0.0,3.0,0.01)
        s = numpy.sin(2*numpy.pi*t)
        c = numpy.cos(2*numpy.pi*t)
        a.plot(t,s)
        a.plot(t,c)
        a.grid()
        #toolbar.update()

    def CriaPainelGrafico(self,parent):
        """ Rotina de criação de um painel gráfico para plotar dados.
            Como argumento da função, é passado um objeto do tipo wx.Panel
            onde será criado o FigureCanvas do Matplotlib.
            O Canvas é criado com um sizer e com a toolbar2Wx do Matplotlib.
            
            A função retorna o handler para a figura criada.
        """
        
        # Criando figura e toolbar do Matplotlib:
        tamanho = parent.GetSizeTuple()
        #a = tamanho[0]/96
        #b = tamanho[1]/96
        #figura = Figure((a,b),96)
        figura = Figure()
        canvas = FigureCanvasWx(parent,-1, figura)
        toolbar = NavigationToolbar2Wx(canvas)
        toolbar.Realize()

        # Colocando Canvas e toolbar no sizer:
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(canvas, 1, wx.GROW)
        sizer.Add(toolbar, 0, wx.ALL|wx.GROW)
        parent.SetSizer(sizer)
        parent.Fit()
        parent.Refresh()
        
        #sizer.SetDimension(0,0,709,415)
        
        print sizer.GetSize(), sizer.GetPosition(), tamanho
        
        return figura
##    def OnFrameSize(self, event):
##        a = self.sizer2.GetSize()
##        
##        self.statusBar1.SetFields(['abc',str(a)])
##        


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()

    app.MainLoop()
