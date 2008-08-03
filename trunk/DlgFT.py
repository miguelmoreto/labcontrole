# -*- coding: iso-8859-1 -*-
#Boa:Dialog:Dialog1

import wx

def create(parent):
    return Dialog1(parent)

[wxID_DIALOG1, wxID_DIALOG1BTNCANCEL, wxID_DIALOG1BTNOK, 
 wxID_DIALOG1TEXTCTRLDEN, wxID_DIALOG1TEXTCTRLNUM, wxID_DIALOG1TEXTDEN, 
 wxID_DIALOG1TEXTHELP, wxID_DIALOG1TEXTNUM, 
] = [wx.NewId() for _init_ctrls in range(8)]

class Dialog1(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              pos=wx.Point(670, 446), size=wx.Size(256, 235),
              style=wx.DEFAULT_DIALOG_STYLE, title='Par\xe2metros da FT')
        self.SetClientSize(wx.Size(248, 207))

        self.btnOk = wx.Button(id=wxID_DIALOG1BTNOK, label='Ok', name='btnOk',
              parent=self, pos=wx.Point(16, 168), size=wx.Size(80, 30),
              style=0)
        self.btnOk.Bind(wx.EVT_BUTTON, self.OnBtnOkButton, id=wxID_DIALOG1BTNOK)

        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label='Cancelar',
              name='btnCancel', parent=self, pos=wx.Point(152, 168),
              size=wx.Size(80, 30), style=0)

        self.textCtrlDen = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRLDEN,
              name='textCtrlDen', parent=self, pos=wx.Point(96, 132),
              size=wx.Size(116, 21), style=0, value='[1, 2, 10]')

        self.textCtrlNum = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRLNUM,
              name='textCtrlNum', parent=self, pos=wx.Point(96, 96),
              size=wx.Size(116, 21), style=0, value='[2,10]')

        self.textNum = wx.StaticText(id=wxID_DIALOG1TEXTNUM, label='Numerador:',
              name='textNum', parent=self, pos=wx.Point(32, 100),
              size=wx.Size(56, 13), style=0)

        self.textHelp = wx.StaticText(id=wxID_DIALOG1TEXTHELP,
              label='Preencha os campos abaixo com os coeficientes\ndos polin\xf4mios em fun\xe7\xe3o da vari\xe1vel s que\ndescrevem o numerador e denominador da fun-\n\xe7\xe3o de transfer\xeancia.\nExemplo:\ns^2+2s+10 => [1, 2, 10]',
              name='textHelp', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(229, 78), style=0)

        self.textDen = wx.StaticText(id=wxID_DIALOG1TEXTDEN,
              label='Denominador:', name='textDen', parent=self,
              pos=wx.Point(21, 136), size=wx.Size(67, 13), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
                

    def OnBtnOkButton(self, event):
        """
        Evento do botão OK. Lê os valores dos campos de entrada.
        """
        self.Num = eval(self.textCtrlNum.GetLineText(0))
        
        self.Den = eval(self.textCtrlDen.GetLineText(0))
        
        self.EndModal(wx.ID_OK)

    def AtualizaCampos(self,Num,Den):
    
        self.textCtrlNum.SetValue(str(Num))
        self.textCtrlDen.SetValue(str(Den))


