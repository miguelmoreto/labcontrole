# -*- coding: iso-8859-1 -*-
#Boa:Dialog:Dialog1


__version__ ='$Rev: 35 $'
__date__ = '$LastChangedDate: 2008-09-04 00:29:33 -0300 (qui, 04 set 2008) $'

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

# $Author: miguelmoreto $
#
#
# Dialog de entrada de dados para as funções de transferência do sistema realimentado
# É exibido quando o usuário clica no bloco da função de transferencia no diagrama de blocos da interface gráfica.
#

import wx
from utils import *
from inspect import *

# define _ or add _ to builtins in your app file
_ = wx.GetTranslation

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
              pos=wx.Point(553, 323), size=wx.Size(256, 235),
              style=wx.DEFAULT_DIALOG_STYLE, title='Par\xe2metros da FT')
        self.SetClientSize(wx.Size(248, 207))

        self.textNum = wx.StaticText(id=wxID_DIALOG1TEXTNUM,
              label=_('Numerador:'), name='textNum', parent=self,
              pos=wx.Point(32, 100), size=wx.Size(57, 13), style=0)

        self.textCtrlNum = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRLNUM,
              name='textCtrlNum', parent=self, pos=wx.Point(96, 96),
              size=wx.Size(116, 21), style=0, value='[2,10]')
        self.textCtrlNum.SetToolTipString(_('Utilize v\xedrgula para separar os elementos do vetor.'))

        self.textDen = wx.StaticText(id=wxID_DIALOG1TEXTDEN,
              label=_('Denominador:'), name='textDen', parent=self,
              pos=wx.Point(21, 136), size=wx.Size(67, 13), style=0)

        self.textCtrlDen = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRLDEN,
              name='textCtrlDen', parent=self, pos=wx.Point(96, 132),
              size=wx.Size(116, 21), style=0, value='[1, 2, 10]')
        self.textCtrlDen.SetToolTipString(_('Utilize v\xedrgula para separar os elementos do vetor.'))

        self.btnOk = wx.Button(id=wxID_DIALOG1BTNOK, label='Ok', name='btnOk',
              parent=self, pos=wx.Point(16, 168), size=wx.Size(80, 30),
              style=0)
        self.btnOk.SetToolTipString('')
        self.btnOk.Bind(wx.EVT_BUTTON, self.OnBtnOkButton, id=wxID_DIALOG1BTNOK)

        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label=_('Cancelar'),
              name='btnCancel', parent=self, pos=wx.Point(152, 168),
              size=wx.Size(80, 30), style=0)
        self.btnCancel.SetToolTipString('')

        self.textHelp = wx.StaticText(id=wxID_DIALOG1TEXTHELP,
              label=_('Preencha os campos abaixo com os coeficientes\ndos polin\xf4mios em fun\xe7\xe3o da vari\xe1vel s que\ndescrevem o numerador e denominador da fun-\n\xe7\xe3o de transfer\xeancia.\nExemplo:\ns^2+2s+10 => [1, 2, 10]'),
              name='textHelp', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(229, 78), style=0)
        self.textHelp.SetToolTipString('')

    def __init__(self, parent):
        self._init_ctrls(parent)
                

    def OnBtnOkButton(self, event):
        """
        Evento do botão OK. Lê os valores dos campos de entrada.
        """
        self.textonum = self.textCtrlNum.GetLineText(0)
        if self.textonum.startswith('[') :
                self.Num = eval(self.textonum)
        else :
                equacao = parseexpr(self.textonum)                
                self.Num = equacao.c.tolist()
                
        self.textoden = self.textCtrlDen.GetLineText(0)
        if self.textoden.startswith('[') :
                self.Den = eval(self.textoden)
        else :
                equacao = parseexpr(self.textoden)
                self.Den = equacao.c.tolist()
        
        self.EndModal(wx.ID_OK)

    def AtualizaCampos(self,Num,Den):
		
        self.textCtrlNum.SetValue(str(Num))
        self.textCtrlDen.SetValue(str(Den))


