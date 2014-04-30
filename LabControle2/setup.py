from distutils.core import setup
import matplotlib
import numpy
import scipy
import py2exe

excludes = ['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg', '_fltkagg', '_gtk', '_gtkcairo', '_wxagg', 'Tkinter']
includes = ["sip", "PyQt4.QtGui", "numpy", "scipy.signal", "scipy.special", "scipy.linalg", 'scipy.special._ufuncs_cxx', 'scipy.sparse.csgraph._validation']

setup(
	windows=['LabControle2.py'],
	options={"py2exe": {"includes": includes}},
	data_files=matplotlib.get_py2exe_datafiles()
	)