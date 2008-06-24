#Boa:Frame:FramePrincipal
# by Moreto
import wx
import SisContinuo

def create(parent):
    return FramePrincipal(parent)

[wxID_FRAMEPRINCIPAL, wxID_FRAMEPRINCIPALBTNSISCONT, 
 wxID_FRAMEPRINCIPALBUTTON2, wxID_FRAMEPRINCIPALBUTTON3, 
 wxID_FRAMEPRINCIPALPANEL1, wxID_FRAMEPRINCIPALSAIR, 
 wxID_FRAMEPRINCIPALSTATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(7)]

class FramePrincipal(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAMEPRINCIPAL, name='FramePrincipal',
              parent=prnt, pos=wx.Point(459, 247), size=wx.Size(250, 250),
              style=wx.DEFAULT_FRAME_STYLE, title='LabControle - Principal')
        self.SetClientSize(wx.Size(242, 222))

        self.panel1 = wx.Panel(id=wxID_FRAMEPRINCIPALPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(242, 222),
              style=wx.TAB_TRAVERSAL)

        self.BtnSisCont = wx.Button(id=wxID_FRAMEPRINCIPALBTNSISCONT,
              label='Sistema Continuo', name='BtnSisCont', parent=self.panel1,
              pos=wx.Point(72, 16), size=wx.Size(100, 30), style=0)
        self.BtnSisCont.Bind(wx.EVT_BUTTON, self.OnBtnSisContButton,
              id=wxID_FRAMEPRINCIPALBTNSISCONT)

        self.button2 = wx.Button(id=wxID_FRAMEPRINCIPALBUTTON2, label='button2',
              name='button2', parent=self.panel1, pos=wx.Point(72, 56),
              size=wx.Size(100, 30), style=0)

        self.button3 = wx.Button(id=wxID_FRAMEPRINCIPALBUTTON3, label='button3',
              name='button3', parent=self.panel1, pos=wx.Point(72, 96),
              size=wx.Size(100, 30), style=0)

        self.Sair = wx.Button(id=wxID_FRAMEPRINCIPALSAIR, label='Sair',
              name='Sair', parent=self.panel1, pos=wx.Point(72, 136),
              size=wx.Size(100, 30), style=0)
        self.Sair.Bind(wx.EVT_BUTTON, self.OnBtnSairButton,
              id=wxID_FRAMEPRINCIPALSAIR)

        self.staticText1 = wx.StaticText(id=wxID_FRAMEPRINCIPALSTATICTEXT1,
              label='Desenvolvido por Miguel Moreto', name='staticText1',
              parent=self.panel1, pos=wx.Point(48, 184), size=wx.Size(153, 13),
              style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnBtnSisContButton(self, event):
        siscont = SisContinuo.create(self)
        siscont.Show()

    def OnBtnSairButton(self, event):
        self.Close()



if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()

    app.MainLoop()
