# PySSPFM Documentation

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/logoPySSPFM_white.PNG> <br>
</p>

## Introduction

<p align="center" width="100%">
    <img align="center" width=80%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20worflow.PNG> <br>
    <em>PySSPFM workflow</em>
</p>

<p align="justify" width="100%">
Following the SSPFM measurement, one or more SSPFM files are generated. A measurement form should be completed by the user (template for: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20Bruker.csv">standard SSPFM</a>, <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20ZI%20DFRT.csv">SSPFM-DFRT</a>). 
The PySSPFM application then proceeds with two stages of measurement processing:
In the first data analysis step, amplitude and phase measurements are extracted and calibrated ufor each segment and nanoloops are created.
The second step creates the piezoresponse hysteresis loop, and extracts piezoelectric and ferroelectric properties using an algorithm based on the lmfit library. Various artifact decorrelation protocols improve measurement accuracy.
Then, SSPFM mapping can be performed.
A toolbox is provided including machine learning algorithms (K-Means), phase separation, mapping cross-correlation, SPM file conversion, and viewers for result analysis.
</p>

## GUI

<p align="justify" width="100%"> 
The graphical user interface <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/gui">codes</a> have been crafted using the <a href="https://docs.python.org/fr/3/library/tkinter.html">Tkinter</a> library. The <a href="https://pypi.org/project/Pillow">PIL library</a> is employed to open and display the application's logo and icon on the graphical interfaces.
</p>

### Main window

<p align="center" width="100%">
    <img align="center" width="15%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20main%20GUI.PNG> <br>
</p>

<p align="justify" width="100%">
The graphical user interface of the main window constitutes the menu of the PySSPFM application. It can be launched directly from the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/main.py">interface code</a> or from the PySSPFM.exe file. It encompasses an array of buttons, each corresponding to an executable script. A secondary window is subsequently opened for the selected script. The interface can be closed either using the <img src="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Exit%20Button.PNG" width="60"> button in the bottom or the <img src="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Close%20Button.PNG" width="20"> button in the upper right corner.
</p>

### Secondary window

<p align="justify" width="100%">
The graphical user interface of the secondary window is specific to each of the respective executable Python scripts, constituting their dedicated menu. It can be initiated directly from the code of the respective interface or from the main menu. 
</p>

<p align="center" width="100%">
    <img align="center" width="20%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/File%20Management%20Section.PNG> <br>
</p>

<p align="justify" width="100%">
In most instances, they encompass a primary file management section to select the input and output file paths, with a 'Browse' or 'Select' button to interactively choose the path in the file explorer. In the majority of cases, once the input path is selected, the other paths are automatically populated based on the default path management. However, all the paths can be modified.
</p>

<p align="center" width="100%">
    <img align="center" width="20%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/User%20Parameters%20Section.PNG> <br>
</p>

<p align="justify" width="100%">
Following this, sections are allocated to parameters relevant to the processing step. Depending on the variable type, the parameter can be entered in a field, via a check button, a gauge, etc. 
</p>

<p align="center" width="100%">
    <img align="center" width="20%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Tooltip.png> <br>
</p>

<p align="justify" width="100%">
Users are guided through tooltips when hovering the mouse over the button. The parameter name, a brief and overall description, along with its possible values and activation conditions, are provided.
</p>

<p align="center" width="100%">
    <img align="center" width="20%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Plot%20and%20save%20section.PNG> <br>
</p>

<p align="justify" width="100%">
Lastly, in most cases, a final section allows the user to choose whether to display the processing results in the console (verbose), show the figures on the screen (show plots), or save them. 
</p>

<p align="center" width="100%">
    <img align="center" width="20%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Start%20and%20Exit%20section.PNG> <br>
</p>

<p align="justify" width="100%">
The processing can be executed with the 'Start' button, and the interface also features an 'Exit' button
</p>

## File management

<p align="center" width="100%">
    <img align="center" width=80%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20File%20Management.PNG> <br>
    <em>PySSPFM file management</em>
</p>

### Input files

#### Datacube files

<p align="justify" width="100%">
The input processed datacube files can be in the form of spreadsheets (columns of value lists for each measurement) with extensions 'txt', 'csv', or 'xlsx', or directly in the format of a Bruker SSPFM file with an 'spm' extension. SSPFM files from other manufacturers are not supported. It is advisable to extract the measurements from them and place them into a spreadsheet. The header dimensions, the column separator in the spreadsheet files to be extracted, and the measurements to be extracted are customizable. A converter from spm files to spreadsheets is also available.
</p>

#### Measurement sheet

<p align="justify" width="100%">
Prior to conducting the SSPFM measurement, the user must complete a measurement form. Templates are available for both the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20Bruker.csv">standard SSPFM</a> and <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20ZI%20DFRT.csv">SSPFM-DFRT</a>) modes. This measurement form serves to guide the user in carrying out the SSPFM measurements and to maintain a record of critical measurement parameters. It also automatically generates certain measurement information based on the provided parameters, such as total measurement time, tip-induced pressure, lock-in amplifier settings, quality factor, and resonance settling time. Furthermore, completing the form is a mandatory prerequisite for the subsequent measurement processing. The parameters to be employed for measurement processing include grid dimensions, calibration coefficients, sign of piezoelectric coeffcient, sinusoidal voltage magnitude, voltage application direction, and SSPFM polarization signal parameters.
</p>

### Output files

#### First step of data analysis

#### Second step of data analysis

#### Toolbox

## First step of data analysis

### Input file

### Parameters

### Segment

### Calibration

### Nanoloop

### File management

## Second step of data analysis

### Input file

### Parameters

### Hysteresis

### Artifact decoupling

### File management

## SSPFM mapping

## Toolbox

### Viewers

### Hysteresis clustering (K-Means)

### Mean loop

### 2D cross correlation

### Pixel extremum

### SPM converter

## Overall settings

