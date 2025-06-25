## Released the first beta version of LabControl 3!

Check the Releases section: https://github.com/miguelmoreto/labcontrole/releases

### New Features of LabControl 3

* The user can handle multiple system definitions. A list of systems has been added in the program interface.
* The user can plot multiple time domain and frequency domain simulations. Iterative lists in the interface makes it possible to select which signals to plot.
* The plotting of the Nyquist diagram has been improved.
* In the time domain response, the control action signal is now available to be plotted.
* Use of the Controls module to handle transfer functions and solve systems (for continuous linear systems).
* Complete re-structuring of the internal data structure.
* Improvement of the user interface.
* New way of configuring the inputs for time domain simulation

## Description
The LabControl is a simulation software for linear control systems. It is designed to be used as an auxiliary tool for teaching classical control system theory.

LabControl as its own website in Brazilian Portuguese that can be acessed in http://sites.google.com/site/controlelab/

You can find more information in english using the LabControle Wiki.

Some Screenshots are available https://sites.google.com/site/controlelab/screenshots.

LabControl runs on Windows (tested only in Windows 10 64bits), and Linux. In order to run from source, it is recommended [Anaconda](https://www.anaconda.com/).


## Running from source on Linux

It is recommended to run LabControl3 using the [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) enviroment.
In order to run from the python source code, you will need to install de dependencies.
1. Create a dedicated conda enviroment (optional):
`conda create --name labcontrole python nomkl --no-default-packages` 

1. Switch to that envirioment:
`conda activate labcontrole`

1. Install dependencies:
	1. `conda install numpy scipy`
	2. `conda install pyqt`
	3. `conda install matplotlib`
	3. `conda install -c conda-forge control slycot`

1. Download the source code using git. Run in a command line:
`git clone https://github.com/miguelmoreto/labcontrole.git`

2. Enter in the created folder:
`cd labcontrole`

1. Run the script:
Run `python LabControl3.py`

#### Observations: 
The python [slycot](https://github.com/python-control/Slycot) is needed for LabControl3. If you manage to install it outside Anaconda enviroment, then you will be able to run LabControl3 without Anaconda.

## Running from source on Windows

The steps are simular to those for Linux instructions above, using the Anaconda Prompt:
1. Create a dedicated conda enviroment (optional):
`conda create --name labcontrole python --no-default-packages` 

1. Switch to that envirioment:
`conda activate labcontrole`

1. Install dependencies:
	1. `conda install conda-forge::blas=*=openblas` (not necessary for linux)
	1. `conda install numpy scipy`
	2. `conda install pyqt` (install pyQt version 6)
	3. `conda install matplotlib`
	3. `conda install -c conda-forge control slycot`

1. Download the source code using git. Run in a command line:
`git clone https://github.com/miguelmoreto/labcontrole.git`

2. Enter in the created folder:
`cd labcontrole`

1. Run the script:
Run `python LabControl3.py`

## About

The LabControle 3 is a major update from LabControle 2. Labcontrole 2 was written originaly in Python 2.7 language. Later it was ported to python 3 and graphical library updated to PyQt6. 

It depends on the folowing python packges:
* Matplotlib
* Scipy
* Numpy
* PyQt6
* Controls (with slycot)

## Developers

Labcontrol 3 was created and is maintained by professor Miguel Moreto at Federal University of Santa Catarina, Florianópolis, SC, Brazil.

Acknowledgments:
* prof. Eduardo Batista, Florianópolis, SC, Brazil.
* Anderson Livramento, Florianópolis, SC, Brazil.
