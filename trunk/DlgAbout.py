# -*- coding: iso-8859-1 -*-
#Boa:Dialog:AboutDlg

__version__ ='$Rev: 31 $'
__date__ = '$LastChangedDate: 2008-09-03 12:31:48 -0300 (qua, 03 set 2008) $'

##    Este arquivo � parte do programa LabControle
##
##    LabControle � um software livre; voc� pode redistribui-lo e/ou 
##    modifica-lo dentro dos termos da Licen�a P�blica Geral GNU como 
##    publicada pela Funda��o do Software Livre (FSF); na vers�o 3 da 
##    Licen�a.
##
##    Este programa � distribuido na esperan�a que possa ser  util, 
##    mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUA��O a 
##    qualquer MERCADO ou APLICA��O EM PARTICULAR. Veja a Licen�a P�blica Geral
##    GNU para maiores detalhes.
##
##    Voc� deve ter recebido uma c�pia da Licen�a P�blica Geral GNU
##    junto com este programa, se n�o, escreva para a Funda��o do Software
##    Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# $Author: miguelmoreto $
#
#

import wx

def create(parent):
    return AboutDlg(parent)

[wxID_ABOUTDLG, wxID_ABOUTDLGBTNOK, wxID_ABOUTDLGDESCTXT, 
 wxID_ABOUTDLGSTATICBITMAP1, wxID_ABOUTDLGSTATICBITMAP2, 
 wxID_ABOUTDLGSTATICBITMAP3, wxID_ABOUTDLGVERSAOTXT, 
] = [wx.NewId() for _init_ctrls in range(7)]

class AboutDlg(wx.Dialog):
    def _init_coll_SizerLogos_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticBitmap1, 0, border=4,
              flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER)
        parent.AddWindow(self.staticBitmap2, 0, border=4,
              flag=wx.EXPAND | wx.ALIGN_CENTER | wx.ALL)

    def _init_coll_flexGridSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticBitmap3, 0, border=4,
              flag=wx.EXPAND | wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.VersaoTxt, 0, border=4,
              flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER)
        parent.AddWindow(self.DescTxt, 1, border=4,
              flag=wx.EXPAND | wx.ALIGN_CENTER | wx.ALL)
        parent.AddSizer(self.SizerLogos, 0, border=4,
              flag=wx.EXPAND | wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.BtnOk, 0, border=4, flag=wx.ALIGN_CENTER | wx.ALL)

    def _init_coll_SizerLogos_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(0)
        parent.AddGrowableCol(0)
        parent.AddGrowableCol(1)

    def _init_coll_flexGridSizer1_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(0)
        parent.AddGrowableRow(2)
        parent.AddGrowableRow(3)
        parent.AddGrowableCol(0)

    def _init_sizers(self):
        # generated method, don't edit
        self.flexGridSizer1 = wx.FlexGridSizer(cols=1, hgap=0, rows=5, vgap=0)

        self.SizerLogos = wx.FlexGridSizer(cols=2, hgap=0, rows=1, vgap=0)

        self._init_coll_flexGridSizer1_Items(self.flexGridSizer1)
        self._init_coll_flexGridSizer1_Growables(self.flexGridSizer1)
        self._init_coll_SizerLogos_Items(self.SizerLogos)
        self._init_coll_SizerLogos_Growables(self.SizerLogos)

        self.SetSizer(self.flexGridSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_ABOUTDLG, name='AboutDlg', parent=prnt,
              pos=wx.Point(564, 209), size=wx.Size(364, 393),
              style=wx.DEFAULT_DIALOG_STYLE, title='Sobre o LabControle')
        self.SetClientSize(wx.Size(356, 365))

        self.BtnOk = wx.Button(id=wx.ID_OK, label='OK', name='BtnOk',
              parent=self, pos=wx.Point(136, 329), size=wx.Size(84, 30),
              style=0)

        self.VersaoTxt = wx.StaticText(id=wxID_ABOUTDLGVERSAOTXT,
              label='Vers\xe3o: 1.0 r31', name='VersaoTxt', parent=self,
              pos=wx.Point(4, 73), size=wx.Size(348, 19),
              style=wx.ALIGN_CENTRE)
        self.VersaoTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Arial'))
        self.VersaoTxt.SetHelpText('')

        self.DescTxt = wx.StaticText(id=wxID_ABOUTDLGDESCTXT, label='Descricao',
              name='DescTxt', parent=self, pos=wx.Point(4, 100),
              size=wx.Size(348, 150), style=0)
        self.DescTxt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'MS Shell Dlg 2'))

        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.Bitmap(u'./gplv3.png',
              wx.BITMAP_TYPE_PNG), id=wxID_ABOUTDLGSTATICBITMAP1,
              name='staticBitmap1', parent=self, pos=wx.Point(8, 262),
              size=wx.Size(152, 55), style=0)
        self.staticBitmap1.SetMinSize(wx.Size(152, 54))

        self.staticBitmap2 = wx.StaticBitmap(bitmap=wx.Bitmap(u'./python.png',
              wx.BITMAP_TYPE_PNG), id=wxID_ABOUTDLGSTATICBITMAP2,
              name='staticBitmap2', parent=self, pos=wx.Point(168, 262),
              size=wx.Size(180, 55), style=0)
        self.staticBitmap2.SetMinSize(wx.Size(180, 61))

        self.staticBitmap3 = wx.StaticBitmap(bitmap=wx.Bitmap(u'D:/Moreto/Programs/LabControle/logoLabControle.png',
              wx.BITMAP_TYPE_PNG), id=wxID_ABOUTDLGSTATICBITMAP3,
              name='staticBitmap3', parent=self, pos=wx.Point(4, 4),
              size=wx.Size(348, 61), style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        descricao = """        O LabControle � um programa simulador de sistemas de controle lineares e invariantes no tempo. Foi desenvolvido por Miguel Moreto na Universidade Federal de Santa Catarina.
        Este software � distribu�do sob a GNU General Public License vers�o 3.
        Acesse o site <http://www.gnu.org/licenses/> para obter o texto completo da licen�a."""
        
        self.DescTxt.SetLabel(descricao)
        self.Layout()
