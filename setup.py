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
#'_tkagg',

os.environ["PATH"] = os.environ["PATH"] + os.path.pathsep + os.path.split(zmq.__file__)[0]

 
setup(windows=['LabControle2.py'], 
      options={"py2exe": {"includes": ["sip", "PyQt4.QtGui", "PyQt4.QtCore",
                                       "zmq.utils", "zmq.utils.jsonapi", 
                                       "zmq.utils.strtypes",
                                       "scipy.sparse.csgraph._validation",
                                       "scipy.special._ufuncs_cxx"],
                                       'excludes': ['_gtkagg', '_wxagg',
                                       "pywin", "pywin.debugger", "pywin.debugger.dbgcon", 
                                       "pywin.dialogs", "pywin.dialogs.list",
                                       "Tkconstants","Tkinter","tcl"]}},
      data_files=matplotlib.get_py2exe_datafiles())