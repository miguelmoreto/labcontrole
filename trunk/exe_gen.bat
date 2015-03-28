echo Generating binary dist version...
c:\WinPython-64bit-2.7.6.3\python-2.7.6.amd64\Scripts\pyinstaller.exe -w -D LabControle2.py --hidden-import=scipy.special._ufuncs_cxx
echo Copying hacked manifest file...
copy /Y Microsoft.VC90.MFC.manifest .\dist\LabControle2\Microsoft.VC90.MFC.manifest
echo Manifest updated.
echo Copying figures..
copy .\*.svg .\dist\LabControle2\
mkdir .\dist\LabControle2\images
copy .\images\*.* .\dist\LabControle2\images\