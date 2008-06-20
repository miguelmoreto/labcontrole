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
 wxID_FRAMENOTEBOOK1, wxID_FRAMEPANEL1, wxID_FRAMEPANEL2, wxID_FRAMEPANEL3, 
 wxID_FRAMEPLOT, wxID_FRAMESPLITTERWINDOW1, wxID_FRAMESTTMAX, wxID_FRAMETMAX, 
 wxID_FRAMETXTOPCOES, 
] = [wx.NewId() for _init_ctrls in range(13)]

class Frame(wx.Frame):
    def _init_coll_flexGridSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.txtOpcoes, 0, border=2,
              flag=wx.ALL | wx.ALIGN_CENTER)
        parent.AddSizer(self.flexGridSizer2, 0, border=4,
              flag=wx.ALL | wx.ALIGN_CENTER)
        parent.AddWindow(self.GrafVarList, 1, border=4, flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.Plot, 0, border=4, flag=wx.ALL | wx.ALIGN_CENTER)
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

        parent.AddGrowableRow(1)
        parent.AddGrowableCol(0)

    def _init_coll_flexGridSizer2_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableCol(1)

    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel1, select=False,
              text='Diagrama')
        parent.AddPage(imageId=-1, page=self.splitterWindow1, select=True,
              text='Gr\xe1ficos')

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
              pos=wx.Point(467, 276), size=wx.Size(725, 455),
              style=wx.DEFAULT_FRAME_STYLE,
              title='LabControle - Sistema continuo')
        self.SetClientSize(wx.Size(717, 427))

        self.notebook1 = wx.Notebook(id=wxID_FRAMENOTEBOOK1, name='notebook1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(717, 427), style=0)
        self.notebook1.SetFitToCurrentPage(True)

        self.panel1 = wx.Panel(id=wxID_FRAMEPANEL1, name='panel1',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(709, 401),
              style=wx.TAB_TRAVERSAL)

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_FRAMESPLITTERWINDOW1,
              name='splitterWindow1', parent=self.notebook1, pos=wx.Point(0, 0),
              size=wx.Size(709, 401),
              style=wx.SP_3DBORDER | wx.SP_3D | wx.DOUBLE_BORDER)
        self.splitterWindow1.SetMinimumPaneSize(100)
        self.splitterWindow1.SetSashSize(5)
        self.splitterWindow1.SetBorderSize(2)
        self.splitterWindow1.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)

        self.panel2 = wx.Panel(id=wxID_FRAMEPANEL2, name='panel2',
              parent=self.splitterWindow1, pos=wx.Point(0, 0), size=wx.Size(150,
              401), style=wx.TAB_TRAVERSAL)
        self.panel2.SetBackgroundColour(wx.Colour(235, 233, 237))
        self.panel2.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)

        self.panel3 = wx.Panel(id=wxID_FRAMEPANEL3, name='panel3',
              parent=self.splitterWindow1, pos=wx.Point(155, 0),
              size=wx.Size(554, 401), style=wx.TAB_TRAVERSAL)
        self.panel3.SetBackgroundColour(wx.Colour(128, 255, 128))
        self.splitterWindow1.SplitVertically(self.panel2, self.panel3, 150)

        self.Plot = wx.Button(id=wxID_FRAMEPLOT, label='Tra\xe7ar', name='Plot',
              parent=self.panel2, pos=wx.Point(37, 318), size=wx.Size(75, 23),
              style=0)

        self.Limpar = wx.Button(id=wxID_FRAMELIMPAR, label='Limpar',
              name='Limpar', parent=self.panel2, pos=wx.Point(37, 377),
              size=wx.Size(75, 23), style=0)

        self.GrafVarList = wx.CheckListBox(choices=[], id=wxID_FRAMEGRAFVARLIST,
              name='GrafVarList', parent=self.panel2, pos=wx.Point(4, 66),
              size=wx.Size(142, 244), style=0)
        self.GrafVarList.SetStringSelection('')

        self.txtOpcoes = wx.StaticText(id=wxID_FRAMETXTOPCOES,
              label='Configura\xe7\xf5es:', name='txtOpcoes',
              parent=self.panel2, pos=wx.Point(14, 2), size=wx.Size(121, 19),
              style=0)
        self.txtOpcoes.Center(wx.BOTH)
        self.txtOpcoes.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.stTmax = wx.StaticText(id=wxID_FRAMESTTMAX, label='Tmax:',
              name='stTmax', parent=self.panel2, pos=wx.Point(16, 32),
              size=wx.Size(54, 21), style=wx.ALIGN_RIGHT)
        self.stTmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))
        self.stTmax.Center(wx.BOTH)

        self.Tmax = wx.TextCtrl(id=wxID_FRAMETMAX, name='Tmax',
              parent=self.panel2, pos=wx.Point(78, 31), size=wx.Size(56, 23),
              style=0, value='10')
        self.Tmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))
        self.Tmax.Center(wx.BOTH)

        self.Continuar = wx.Button(id=wxID_FRAMECONTINUAR, label='Continuar',
              name='Continuar', parent=self.panel2, pos=wx.Point(37, 349),
              size=wx.Size(75, 23), style=0)

        self._init_coll_notebook1_Pages(self.notebook1)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # A partir de agora não é código automático do BOA constructor.
        # Criando figura para plotar o resultado da simulação.
        self.fig = Figure()
        self.canvas = FigureCanvasWx(self.panel3, -1, self.fig)
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
       
        # Create a figure manager to manage things
        self.figmgr = FigureManager(self.canvas, 1, self)
        # Now put all into a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.toolbar, 0, wx.ALL|wx.GROW)
        sizer.Add(self.canvas, 1, wx.GROW)
        self.panel3.SetSizer(sizer)
        self.panel3.Fit()
        self.panel3.Refresh()

        # Exemplo de plot.
        self.plot_data()
        self.Show()
        
    def plot_data(self):
        # Use ths line if using a toolbar
        a = self.fig.add_subplot(111)
        
        # Or this one if there is no toolbar
        #a = Subplot(self.fig, 111)
        
        t = numpy.arange(0.0,3.0,0.01)
        s = numpy.sin(2*numpy.pi*t)
        c = numpy.cos(2*numpy.pi*t)
        a.plot(t,s)
        a.plot(t,c)
        self.toolbar.update()

