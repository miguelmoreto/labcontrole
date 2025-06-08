#!/bin/bash
pyinstaller --noconfirm \
    --clean --onedir \
    --contents-directory "." \
    --name=LabControle3 \
    --add-data="MainWindow.ui:." \
    --add-data="HelpWindow.ui:." \
    --add-data="matplotlibwidget.py:." \
    --add-data="./help/*:./help" \
    --add-data="./images/*:./images" \
    --add-data="./images/mpl_toolbar/*:./images/mpl_toolbar"
    --exclude-module=sqlalchemy \
    --hidden-import=numpy.core.multiarray \
    LabControl3.py
#cp libstdc++.so.6 dist/LabControl3/