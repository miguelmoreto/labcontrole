#!/bin/bash
pyinstaller --noconfirm \
    --clean --onedir \
    --add-data="MainWindow.ui:." \
    --add-data="HelpWindow.ui:." \
    --add-data="matplotlibwidget.py:." \
    --exclude-module=sqlalchemy \
    --hidden-import=PyQt5.sip \
    LabControl3.py
cp libstdc++.so.6 dist/LabControl3/
