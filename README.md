## English Description
The LabControl is a simulation software for linear control systems. It is designed to be used as an auxiliary tool for teaching classical control system theory.

LabControl as its own website in Brazilian Portuguese that can be acessed in http://sites.google.com/site/controlelab/

You can find more information in english using the LabControle Wiki.

Some Screenshots are available https://sites.google.com/site/controlelab/screenshots.

LabControl runs on Windows 7, Windows 8 (32 or 64bits, both from sorce or binaries) and on Linux (from the source code only).

## Descrição em Português
O LabControle é um simulador de sistemas de controle lineares para ser utilizado como apoio em disciplinas teóricas e práticas de sistemas de controle.

Para maiores informações sobre o projeto, acesse o site do LabControle: http://sites.google.com/site/controlelab/

O LabControle roda em Windows 7, Windows 8 (32 ou 64bits, tando do código fonte como de binários) além de rodar em Linux (pelo código fonte apenas).

## New Features of LabControl 3 

* The user can handle and compare multiple systems parameters. A system list was added to the main UI.
* The user can plot in the same graphic multiple time domain simulations, from different parameters and different systems.
* The control action signal is available to plot.
* Using python Controls module to handle transfer functions and solving the system.
* System data structure completed restrutured.

## Executar no Linux

Siga os passos abaixo:

1. Baixe o código fonte usando git. Execute a seguinte linha de comando:

`git clone https://github.com/miguelmoreto/labcontrole.git`
1. Entre na pasta criada:

`cd labcontrole`
1. Execute o script:

`./run.sh`

## Downloads

### LabControl3

Not available yet.

### LabControle 2:

Se Releases section: https://github.com/miguelmoreto/labcontrole/releases

## About

The LabControl 3 is a major update from LabControle 2. Labcontrole 2 was written originaly in Python 2.7 language. Later it was ported to python 3 and graphical library updated to PyQt5. 

It depends on the folowing python packges:
* Matplotlib
* Scipy
* Numpy
* Pyqt5
* Controls

## Developers

Labcontrol 3 was created and is maintained by professor Miguel Moreto from Federal University of Santa Catarina, Florianópolis, SC, Brazil.

Contributors:
* Anderson Livramento, Florianópolis, SC, Brazil.
