# -*- coding: iso-8859-1 -*-

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
# Script para gerar um executável usando o py2exe.
#
# Baseado no exemplo fornecido juntamente com o py2exe.
#**********************************************************************
# In this case, the py2exe command is subclassed to create an installation
# script for InnoSetup, which can be compiled with the InnoSetup compiler
# to a single file windows installer.
#
# By default, the installer will be created as dist_dir\Output\setup.exe.
# Used successfully in Python2.5 with matplotlib 0.91.2 and PyQt4 (and Qt 4.3.3) 
#
# To run type in the command prompt:
#
# python setup.py py2exe
#
# Developed by Miguel Moreto besed on the extending exemple from the
# py2exe samples folder.
from distutils.core import setup
from distutils.dir_util import remove_tree
import py2exe
import sys
import os

# We need to import the glob module to search for all Matplotlib files.
import glob

# ###############################################################
# The manifest will be inserted as resource into test_wx.exe.  This
# gives the controls the Windows XP appearance (if run on XP ;-)
#
# Another option would be to store if in a file named
# test_wx.exe.manifest, and probably copy it with the data_files
# option.
#
manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

RT_MANIFEST = 24

# Mudando critério de inclusão de dlls do sistema, conforme o site do py2exe.
origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ("msvcp71.dll", "gdiplus.dll"):
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL


# ###############################################################
# Output folder (where the executables will be):
out_dir = r'..\..\ProgramsEXE\LabControle'

# Current folder:
current_dir = os.getcwd()


# ###############################################################
# arguments for the setup() call

pyOscilo = dict(
    script = "SisContinuo.py",
	icon_resources = [(0, r".\py1.ico")],
	version = "1.0.0",
	company_name = "UFSC - LABSPOT",
	copyright = "Miguel Moreto",
	name = "LabControle",
	description = "Simulador educacional de sistemas de controle LIT.",
    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="test_wx"))],
    dest_base = r"LabControle")

zipfile = r"lib\shardlib"


# We need to exclude matplotlib backends not being used by this executable.  You may find
# that you need different excludes to create a working executable with your chosen backend.
# We also need to include include various numerix libraries that the other functions call.

options = {
    'py2exe': { "dist_dir": out_dir,
                "includes" : ["matplotlib.backends",  "matplotlib.backends.backend_wxagg",
                               "matplotlib.figure","pylab", "numpy", "matplotlib.numerix.fft", "matplotlib.numerix.ma",
                               "matplotlib.numerix.linear_algebra", "matplotlib.numerix.random_array",
                               "scipy.io.numpyio","IPython.Extensions.path"],
                'excludes': ['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg',
                             '_fltkagg', '_gtk', '_gtkcairo', 'PyQt4','Tkinter'],
                'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                 'libgobject-2.0-0.dll','QtCore4.dll','QtGui4.dll']
              }
       }
 

#  
# Save matplotlib-data to mpl-data ( It is located in the matplotlib\mpl-data 
# folder and the compiled programs will look for it in \mpl-data
# note: using matplotlib.get_mpldata_info
data_files = [(r'mpl-data', glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\*.*')),
                    # Because matplotlibrc does not have an extension, glob does not find it (at least I think that's why)
                    # So add it manually here:
                  (r'mpl-data', [r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
                  (r'mpl-data\images',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\images\*.*')),
                  (r'mpl-data\fonts\afm',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\fonts\afm\*.*')),
                  (r'mpl-data\fonts\pdfcorefonts',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\fonts\pdfcorefonts\*.*')),
                  (r'mpl-data\fonts\ttf',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\*.*')),
#                  (r'\.',glob.glob(r'C:\Python25\Lib\site-packages\wx-2.8-msw-ansi\wx\gdiplus.*')),
                  ('.\\',glob.glob(current_dir + '\\*.ico')),
                  ('.\\',glob.glob(current_dir + '\\*.png')),
                  (r'locale\en_US\LC_MESSAGES',[current_dir + r'\locale\en_US\LC_MESSAGES\LabControle.mo'])
                  ]


# ###############################################################
#HKEY_CLASSES_ROOT\Folder\shell\pyOscilo\command
class InnoScript:
    def __init__(self,
                 name,
                 lib_dir,
                 dist_dir,
                 windows_exe_files = [],
                 lib_files = [],
                 version = "1.0"):
        self.lib_dir = lib_dir
        self.dist_dir = dist_dir
        if not self.dist_dir[-1] in "\\/":
            self.dist_dir += "\\"
        self.name = name
        self.version = version
        self.windows_exe_files = [self.chop(p) for p in windows_exe_files]
        self.lib_files = [self.chop(p) for p in lib_files]

    def chop(self, pathname):
        assert pathname.startswith(self.dist_dir)
        return pathname[len(self.dist_dir):]
    
    def create(self, pathname="\\LabControle.iss"):
        self.pathname = self.dist_dir + pathname
        ofi = self.file = open(self.pathname, "w")
        print >> ofi, "; WARNING: This script has been created by py2exe. Changes to this script"
        print >> ofi, "; will be overwritten the next time py2exe is run!"
        print >> ofi, r"[Setup]"
        print >> ofi, r"AppName=%s" % self.name
        print >> ofi, r"AppVerName=%s %s" % (self.name, self.version)
        print >> ofi, r"DefaultDirName={pf}\%s" % self.name
        print >> ofi, r"DefaultGroupName=%s" % self.name
        print >> ofi
        
        print >> ofi, r"[Languages]"
        print >> ofi, "Name: \"ptbr\"; MessagesFile: \"compiler:Languages\\BrazilianPortuguese.isl\""
        print >> ofi

        print >> ofi, r"[Tasks]"
        print >> ofi, r'Name: desktopicon; Description: "Criar ícone no &desktop"; GroupDescription: "Additional icons:"'
        print >> ofi

        
        print >> ofi, r"[Files]"
        for path in self.windows_exe_files + self.lib_files:
            print >> ofi, r'Source: "%s"; DestDir: "{app}\%s"; Flags: ignoreversion' % (path, os.path.dirname(path))
        print >> ofi

        print >> ofi, r"[Icons]"
        for path in self.windows_exe_files:
            print >> ofi, r'Name: "{group}\%s %s"; Filename: "{app}\%s"; WorkingDir: "{app}\"; IconFilename: "{app}\py1.ico"' % (self.name, self.version, path)
            print >> ofi, r'Name: "{commondesktop}\%s %s"; Filename: "{app}\%s";  WorkingDir: "{app}\"; IconFilename: "{app}\py1.ico"; Tasks: desktopicon' % (self.name, self.version, path)
        print >> ofi, 'Name: "{group}\Uninstall %s %s"; Filename: "{uninstallexe}"' % (self.name, self.version)

    def compile(self):
        try:
            import ctypes
        except ImportError:
            try:
                import win32api
            except ImportError:
                import os
                os.startfile(self.pathname)
            else:
                print "Ok, using win32api."
                win32api.ShellExecute(0, "compile",
                                                self.pathname,
                                                None,
                                                None,
                                                0)
        else:
            print "Cool, you have ctypes installed."
            res = ctypes.windll.shell32.ShellExecuteA(0, "compile",
                                                      self.pathname,
                                                      None,
                                                      None,
                                                      0)
            if res < 32:
                raise RuntimeError, "ShellExecute failed, error %d" % res
		


# ###############################################################

from py2exe.build_exe import py2exe

class build_installer(py2exe):
    # This class first builds the exe file(s), then creates a Windows installer.
    # You need InnoSetup for it.
    def run(self):
        # First, let py2exe do it's work.
        py2exe.run(self)

        lib_dir = self.lib_dir
        dist_dir = self.dist_dir
        
		
        # create the Installer, using the files py2exe has created.
        script = InnoScript("LabControle",
                            lib_dir,
                            dist_dir,
                            self.windows_exe_files,
                            self.lib_files)
        print "*** creating the inno setup script***"
        script.create()
        print "*** compiling the inno setup script***"
        script.compile()
        # Note: By default the final setup.exe will be in an Output subdirectory.

# ###############################################################

setup(
    options = options,
    # The lib directory contains everything except the executables and the python dll.
    zipfile = zipfile,
    windows = [pyOscilo],
	data_files=data_files,
    # use out build_installer class as extended py2exe build command
    cmdclass = {"py2exe": build_installer},
    )

# ###############################################################
# Clean up removing the "build" dir.
print 'Cleaning build dir'
remove_tree(current_dir + '\\build')
	
# for console program use 'console = [{"script" : "scriptname.py"}]
#setup(windows=[{"script" : "App.py"}], options=opts,   data_files=data_files)