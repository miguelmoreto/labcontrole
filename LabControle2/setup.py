# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 22:46:15 2014

@author: Moreto
"""

from distutils.core import setup
import py2exe
import matplotlib
 
setup(windows=['LabControle2.py'],
      options={"py2exe": {"includes": ["sip", "PyQt4.QtGui", "PyQt4.QtCore"], 'excludes': ['_wxagg', '_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg', '_fltkagg', '_gtk', '_gtkcairo','Tkinter']}},
      data_files=matplotlib.get_py2exe_datafiles())