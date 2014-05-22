echo MainWindow..
python "%WINPYDIR%\Lib\site-packages\PyQt4\uic\pyuic.py" -x MainWindow.ui -o MainWindow.py
echo Dialog..
python "%WINPYDIR%\Lib\site-packages\PyQt4\uic\pyuic.py" -x DialogSysInfo.ui -o DialogSysInfo.py
