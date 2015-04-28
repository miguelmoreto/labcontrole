# -*- coding: utf-8 -*-
#==============================================================================
# This file is part of LabControle 2.
# 
# LabControle 2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
# 
# LabControle 2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with LabControle 2.  If not, see <http://www.gnu.org/licenses/>.
#==============================================================================
#==============================================================================
# Este arquivo é parte do programa LabControle 2
# 
# LabControle 2 é um software livre; você pode redistribui-lo e/ou 
# modifica-lo dentro dos termos da Licença Pública Geral GNU como 
# publicada pela Fundação do Software Livre (FSF); na versão 3 da 
# Licença.
# Este programa é distribuido na esperança que possa ser  util, 
# mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a 
# qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral
# GNU para maiores detalhes.
# 
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, escreva para a Fundação do Software
# Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#==============================================================================
#
# Developed by Miguel Moreto
# Florianopolis, Brazil, 2015
     
from distutils.core import setup
import py2exe
import matplotlib
import os
import zmq
import sys
#

os.environ["PATH"] = os.environ["PATH"] + os.path.pathsep + os.path.split(zmq.__file__)[0]
python_dir = sys.exec_prefix

Mydata_files = matplotlib.get_py2exe_datafiles()

#
#for files in os.listdir('./images'):
#    f1 = './images/' + files
#    if os.path.isfile(f1): # skip directories
#        f2 = 'images', [f1]
#        Mydata_files.append(f2)

Mydata_files.append(('', ['./diagram1Closed.svg']))
Mydata_files.append(('', ['./diagram1Opened.svg']))
Mydata_files.append(('', ['./diagram2Closed.svg']))
Mydata_files.append(('', ['./diagram2Opened.svg']))
Mydata_files.append(('', ['./diagram3Closed.svg']))
Mydata_files.append(('', ['./diagram3Opened.svg']))
Mydata_files.append(('', ['./diagram4Closed.svg']))
Mydata_files.append(('', ['./diagram4Opened.svg']))
Mydata_files.append(('', ['./diagram5Closed.svg']))
Mydata_files.append(('', ['./diagram5Opened.svg']))
Mydata_files.append(('', ['./LabControle2_en.qm']))
#Mydata_files.append(('imageformats', [python_dir + r'\Lib\site-packages\PyQt4\plugins\imageformats\qico4.dll']))

#,"icon_resources": [(1, "./images/labcontrole.ico")]
setup(windows=[{"script": "LabControle2.py"}],
      options={"py2exe": {"includes": ["sip", "PyQt4.QtGui", "PyQt4.QtCore",
                                       "zmq.utils", "zmq.utils.jsonapi", 
                                       "zmq.utils.strtypes",
                                       "scipy.sparse.csgraph._validation",
                                       "scipy.special._ufuncs_cxx"],
                                       'excludes': ['_gtkagg', '_wxagg','_tkagg',"numpy.core._dotblas",
                                       "pywin", "pywin.debugger", "pywin.debugger.dbgcon", 
                                       "pywin.dialogs", "pywin.dialogs.list",
                                       "Tkconstants","Tkinter","tcl"]}},
      data_files=Mydata_files)