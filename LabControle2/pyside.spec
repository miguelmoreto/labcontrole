import os
a = Analysis(
    [os.path.join(HOMEPATH,'support\\_mountzlib.py')
        , os.path.join(HOMEPATH,'support\\useUnicode.py')
        , os.path.normpath(os.path.join('D:\\Moreto\\Programas\\LabControle2', 'LabControle2.py'))
        , os.path.normpath(os.path.join('D:\\Moreto\\Programas\\LabControle2', 'MainWindow.py'))
        , os.path.normpath(os.path.join('D:\\Moreto\\Programas\\LabControle2', 'Sistema.py'))
        # add the files you want PyInstaller to analyse the "import" statements
        # to detect the libraries to include
    ],
     pathex=['C:\\WinPython-64bit-2.7.6.3\\python-2.7.6.amd64\\Scripts']
)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\build_output', 'LabControle2.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=os.path.join('dist', 'dist_output'))