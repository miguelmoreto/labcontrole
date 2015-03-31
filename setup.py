# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 22:46:15 2014

@author: Moreto
"""
     
from distutils.core import setup
import py2exe
import matplotlib
import os
import zmq
#

os.environ["PATH"] = os.environ["PATH"] + os.path.pathsep + os.path.split(zmq.__file__)[0]

Mydata_files = matplotlib.get_py2exe_datafiles()

#Mydata_files.append([('images', ['./images/about.png']),('images', ['./images/calc.png']),
#                ('images', ['./images/close.png']),('images', ['./images/config.png']),
#                ('images', ['./images/fileopen.png']),('images', ['./images/filesave.png']),
#                ('images', ['./images/help.png']),('images', ['./images/icon1.png'])])
#Mydata_files.append(('images', ['./images/about.png']))

for files in os.listdir('./images'):
    f1 = './images/' + files
    if os.path.isfile(f1): # skip directories
        f2 = 'images', [f1]
        Mydata_files.append(f2)

Mydata_files.append(('', ['./diagram1Closed.svg']))
Mydata_files.append(('', ['./diagram1Opened.svg']))
Mydata_files.append(('', ['./diagram2Closed.svg']))
Mydata_files.append(('', ['./diagram2Opened.svg']))
Mydata_files.append(('', ['./diagram3Closed.svg']))
Mydata_files.append(('', ['./diagram3Opened.svg']))

#numpy.core._dotblas
#
 
setup(windows=[{"script": "LabControle2.py","icon_resources": [(1, "./images/labcontrole.ico")]}],
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