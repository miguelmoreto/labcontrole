# -*- coding: iso-8859-1 -*-
#Boa:Dialog:Dialog1

import wx

def create(parent):
    return Dialog1(parent)

[wxID_DIALOG1, wxID_DIALOG1BTNCANCEL, wxID_DIALOG1BTNOK, 
 wxID_DIALOG1TEXTCTRLINST, wxID_DIALOG1TEXTCTRLVAL, wxID_DIALOG1TEXTDEN, 
 wxID_DIALOG1TEXTHELP, wxID_DIALOG1TEXTNUM, 
] = [wx.NewId() for _init_ctrls in range(8)]

class Dialog1(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              pos=wx.Point(670, 413), size=wx.Size(256, 268),
              style=wx.DEFAULT_DIALOG_STYLE, title='Par\xe2metros da Entrada')
        self.SetClientSize(wx.Size(248, 240))

        self.btnOk = wx.Button(id=wxID_DIALOG1BTNOK, label='Ok', name='btnOk',
              parent=self, pos=wx.Point(16, 192), size=wx.Size(80, 30),
              style=0)
        self.btnOk.Bind(wx.EVT_BUTTON, self.OnBtnOkButton, id=wxID_DIALOG1BTNOK)

        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label='Cancelar',
              name='btnCancel', parent=self, pos=wx.Point(152, 192),
              size=wx.Size(80, 30), style=0)

        self.textCtrlInst = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRLINST,
              name='textCtrlInst', parent=self, pos=wx.Point(96, 156),
              size=wx.Size(116, 21), style=0, value='0')

        self.textCtrlVal = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRLVAL,
              name='textCtrlVal', parent=self, pos=wx.Point(96, 120),
              size=wx.Size(116, 21), style=0, value='1')

        self.textNum = wx.StaticText(id=wxID_DIALOG1TEXTNUM, label='Valor:',
              name='textNum', parent=self, pos=wx.Point(56, 124),
              size=wx.Size(29, 13), style=0)

        self.textHelp = wx.StaticText(id=wxID_DIALOG1TEXTHELP,
              label='Preencha os campos abaixo com os par\xe2metros\nda entrada:\nValor: valor do degrau ou fun\xe7\xe3o no tempo (t);\nInstante: instante de tempo que a entrada \xe9\n               aplicada.\nExemplo:\nDeg. unit\xe1rio em 2seg.:  Val. = 1 e Inst. = 2\nRampa em 0seg.: Val. = t e Inst. = 0',
              name='textHelp', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(227, 104), style=0)

        self.textDen = wx.StaticText(id=wxID_DIALOG1TEXTDEN, label='Instante:',
              name='textDen', parent=self, pos=wx.Point(40, 160),
              size=wx.Size(45, 13), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
                

    def OnBtnOkButton(self, event):
        """
        Evento do botão OK. Lê os valores dos campos de entrada.
        """
        self.Valor = self.textCtrlVal.GetLineText(0)
        
        self.Instante = eval(self.textCtrlInst.GetLineText(0))
        
        self.EndModal(wx.ID_OK)

    def AtualizaCampos(self,Val,Inst):
    
        self.textCtrlVal.SetValue(Val)
        self.textCtrlInst.SetValue(str(Inst))


