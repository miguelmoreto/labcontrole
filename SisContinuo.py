#Boa:Frame:Frame

import wx
from wx.lib.anchors import LayoutAnchors

def create(parent):
    return Frame(parent)

[wxID_FRAME, wxID_FRAMENOTEBOOK1, wxID_FRAMEPANEL1, wxID_FRAMEPANEL2, 
 wxID_FRAMESPLITTERWINDOW1, wxID_FRAMEWINDOW1, 
] = [wx.NewId() for _init_ctrls in range(6)]

class Frame(wx.Frame):
    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel1, select=False,
              text='Diagrama')
        parent.AddPage(imageId=-1, page=self.splitterWindow1, select=True,
              text='Gr\xe1ficos')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME, name='Frame', parent=prnt,
              pos=wx.Point(423, 227), size=wx.Size(725, 455),
              style=wx.DEFAULT_FRAME_STYLE,
              title='LabControle - Sistema continuo')
        self.SetClientSize(wx.Size(717, 427))

        self.notebook1 = wx.Notebook(id=wxID_FRAMENOTEBOOK1, name='notebook1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(717, 427), style=0)

        self.panel1 = wx.Panel(id=wxID_FRAMEPANEL1, name='panel1',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(709, 401),
              style=wx.TAB_TRAVERSAL)

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_FRAMESPLITTERWINDOW1,
              name='splitterWindow1', parent=self.notebook1, pos=wx.Point(0, 0),
              size=wx.Size(709, 401), style=wx.DOUBLE_BORDER)
        self.splitterWindow1.SetMinimumPaneSize(100)
        self.splitterWindow1.SetSashSize(5)
        self.splitterWindow1.SetBorderSize(2)

        self.window1 = wx.Window(id=wxID_FRAMEWINDOW1, name='window1',
              parent=self.splitterWindow1, pos=wx.Point(105, 0),
              size=wx.Size(604, 401), style=0)
        self.window1.SetBackgroundColour(wx.Colour(255, 255, 157))

        self.panel2 = wx.Panel(id=wxID_FRAMEPANEL2, name='panel2',
              parent=self.splitterWindow1, pos=wx.Point(0, 0), size=wx.Size(100,
              401), style=wx.TAB_TRAVERSAL)
        self.panel2.SetBackgroundColour(wx.Colour(179, 255, 179))
        self.splitterWindow1.SplitVertically(self.panel2, self.window1, 100)

        self._init_coll_notebook1_Pages(self.notebook1)

    def __init__(self, parent):
        self._init_ctrls(parent)
